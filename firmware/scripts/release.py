import sys
import os
import json
import zipfile
import argparse
from pathlib import Path
from typing import Optional

# Chuyển đến thư mục gốc của dự án
os.chdir(Path(__file__).resolve().parent.parent)

################################################################################
# Các hàm tiện ích chung
################################################################################

def get_board_type_from_compile_commands() -> Optional[str]:
    """Phân tích cú pháp BOARD_TYPE đã biên dịch hiện tại từ build/compile_commands.json"""
    compile_file = Path("build/compile_commands.json")
    if not compile_file.exists():
        return None
    with compile_file.open() as f:
        data = json.load(f)
    for item in data:
        if not item["file"].endswith("main.cc"):
            continue
        cmd = item["command"]
        if "-DBOARD_TYPE=\\\"" in cmd:
            return cmd.split("-DBOARD_TYPE=\\\"")[1].split("\\\"")[0].strip()
    return None


def get_project_version() -> Optional[str]:
    """Đọc set(PROJECT_VER "x.y.z") từ tệp CMakeLists.txt gốc"""
    with Path("CMakeLists.txt").open() as f:
        for line in f:
            if line.startswith("set(PROJECT_VER"):
                return line.split("\"")[1]
    return None


def merge_bin() -> None:
    if os.system("idf.py merge-bin") != 0:
        print("merge-bin không thành công", file=sys.stderr)
        sys.exit(1)


def zip_bin(name: str, version: str) -> None:
    """Nén build/merged-binary.bin thành releases/v{version}_{name}.zip"""
    out_dir = Path("releases")
    out_dir.mkdir(exist_ok=True)
    output_path = out_dir / f"v{version}_{name}.zip"

    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("build/merged-binary.bin", arcname="merged-binary.bin")
    print(f"Nén bin vào {output_path} đã hoàn tất")

################################################################################
# các hàm liên quan đến board / biến thể
################################################################################

_BOARDS_DIR = Path("main/boards")


def _collect_variants(config_filename: str = "config.json") -> list[dict[str, str]]:
    """Duyệt qua tất cả các board trong main/boards, thu thập thông tin biến thể.

    Ví dụ trả về:
        [{{"board": "bread-compact-ml307", "name": "bread-compact-ml307"}}, ...]
    """
    variants: list[dict[str, str]] = []
    for board_path in _BOARDS_DIR.iterdir():
        if not board_path.is_dir():
            continue
        if board_path.name == "common":
            continue
        cfg_path = board_path / config_filename
        if not cfg_path.exists():
            print(f"[CẢNH BÁO] {cfg_path} không tồn tại, bỏ qua", file=sys.stderr)
            continue
        try:
            with cfg_path.open() as f:
                cfg = json.load(f)
            for build in cfg.get("builds", []):
                variants.append({"board": board_path.name, "name": build["name"]})
        except Exception as e:
            print(f"[LỖI] Phân tích {cfg_path} không thành công: {e}", file=sys.stderr)
    return variants


def _parse_board_config_map() -> dict[str, str]:
    """Xây dựng ánh xạ của CONFIG_BOARD_TYPE_xxx và board_type từ main/CMakeLists.txt"""
    cmake_file = Path("main/CMakeLists.txt")
    mapping: dict[str, str] = {}
    lines = cmake_file.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines):
        if "if(CONFIG_BOARD_TYPE_" in line:
            config_name = line.strip().split("if(")[1].split(")")[0]
            if idx + 1 < len(lines):
                next_line = lines[idx + 1].strip()
                if next_line.startswith("set(BOARD_TYPE"):
                    board_type = next_line.split('"')[1]
                    mapping[config_name] = board_type
    return mapping


def _find_board_config(board_type: str) -> Optional[str]:
    """Tìm CONFIG_BOARD_TYPE_xxx tương ứng cho board_type đã cho"""
    for config, b_type in _parse_board_config_map().items():
        if b_type == board_type:
            return config
    return None

################################################################################
# Kiểm tra board_type trong CMakeLists
################################################################################

def _board_type_exists(board_type: str) -> bool:
    cmake_file = Path("main/CMakeLists.txt")
    pattern = f'set(BOARD_TYPE "{board_type}")'
    return pattern in cmake_file.read_text(encoding="utf-8")

################################################################################
# Triển khai biên dịch
################################################################################

def release(board_type: str, config_filename: str = "config.json", *, filter_name: Optional[str] = None) -> None:
    """Biên dịch và đóng gói tất cả/các biến thể được chỉ định của board_type được chỉ định

    Đối số:
        board_type: tên thư mục trong main/boards
        config_filename: tên config.json (mặc định: config.json)
        filter_name: nếu được chỉ định, chỉ biên dịch build["name"] phù hợp
    """
    cfg_path = _BOARDS_DIR / board_type / config_filename
    if not cfg_path.exists():
        print(f"[CẢNH BÁO] {cfg_path} không tồn tại, bỏ qua {board_type}")
        return

    project_version = get_project_version()
    print(f"Phiên bản dự án: {project_version} ({cfg_path})")

    with cfg_path.open() as f:
        cfg = json.load(f)
    target = cfg["target"]

    builds = cfg.get("builds", [])
    if filter_name:
        builds = [b for b in builds if b["name"] == filter_name]
        if not builds:
            print(f"[LỖI] Không tìm thấy biến thể {filter_name} trong {config_filename} của {board_type}", file=sys.stderr)
            sys.exit(1)

    for build in builds:
        name = build["name"]
        if not name.startswith(board_type):
            raise ValueError(f"build.name {name} phải bắt đầu bằng {board_type}")

        output_path = Path("releases") / f"v{project_version}_{name}.zip"
        if output_path.exists():
            print(f"Bỏ qua {name} vì {output_path} đã tồn tại")
            continue

        # Xử lý sdkconfig_append
        board_type_config = _find_board_config(board_type)
        sdkconfig_append = [f"{board_type_config}=y"]
        sdkconfig_append.extend(build.get("sdkconfig_append", []))

        print("-" * 80)
        print(f"tên: {name}")
        print(f"mục tiêu: {target}")
        for item in sdkconfig_append:
            print(f"sdkconfig_append: {item}")

        os.environ.pop("IDF_TARGET", None)

        # Gọi set-target
        if os.system(f"idf.py set-target {target}") != 0:
            print("set-target không thành công", file=sys.stderr)
            sys.exit(1)

        # Nối sdkconfig
        with Path("sdkconfig").open("a") as f:
            f.write("\n")
            f.write("# Nối bởi release.py\n")
            for append in sdkconfig_append:
                f.write(f"{append}\n")
        # Xây dựng với macro BOARD_NAME được định nghĩa thành name
        if os.system(f"idf.py -DBOARD_NAME={name} build") != 0:
            print("xây dựng không thành công")
            sys.exit(1)

        # merge-bin
        merge_bin()

        # Zip
        zip_bin(name, project_version)

################################################################################
# Mục nhập CLI
################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("board", nargs="?", default=None, help="Loại board hoặc all")
    parser.add_argument("-c", "--config", default="config.json", help="Chỉ định tên tệp config, mặc định là config.json")
    parser.add_argument("--list-boards", action="store_true", help="Liệt kê tất cả các board và danh sách biến thể được hỗ trợ")
    parser.add_argument("--json", action="store_true", help="Kết hợp với --list-boards, đầu ra định dạng JSON")
    parser.add_argument("--name", help="Chỉ định tên biến thể, chỉ biên dịch biến thể phù hợp")

    args = parser.parse_args()

    # Chế độ danh sách
    if args.list_boards:
        variants = _collect_variants(config_filename=args.config)
        if args.json:
            print(json.dumps(variants))
        else:
            for v in variants:
                print(f"{v['board']}: {v['name']}")
        sys.exit(0)

    # Chế độ đóng gói firmware thư mục hiện tại
    if args.board is None:
        merge_bin()
        curr_board_type = get_board_type_from_compile_commands()
        if curr_board_type is None:
            print("Không thể phân tích cú pháp board_type từ compile_commands.json", file=sys.stderr)
            sys.exit(1)
        project_ver = get_project_version()
        zip_bin(curr_board_type, project_ver)
        sys.exit(0)

    # Chế độ biên dịch
    board_type_input: str = args.board
    name_filter: str | None = args.name

    # Kiểm tra board_type trong CMakeLists
    if board_type_input != "all" and not _board_type_exists(board_type_input):
        print(f"[LỖI] Không tìm thấy board_type {board_type_input} trong main/CMakeLists.txt", file=sys.stderr)
        sys.exit(1)

    variants_all = _collect_variants(config_filename=args.config)

    # Lọc danh sách board_type
    target_board_types: set[str]
    if board_type_input == "all":
        target_board_types = {v["board"] for v in variants_all}
    else:
        target_board_types = {board_type_input}

    for bt in sorted(target_board_types):
        if not _board_type_exists(bt):
            print(f"[LỖI] Không tìm thấy board_type {bt} trong main/CMakeLists.txt", file=sys.stderr)
            sys.exit(1)
        cfg_path = _BOARDS_DIR / bt / args.config
        if bt == board_type_input and not cfg_path.exists():
            print(f"Board {bt} không có tệp cấu hình {args.config} được định nghĩa, bỏ qua")
            sys.exit(0)
        release(bt, config_filename=args.config, filter_name=name_filter if bt == board_type_input else None)

import sys
import os
import json
import zipfile
import argparse
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

# Chuyển đến thư mục gốc của dự án
os.chdir(Path(__file__).resolve().parent.parent)
_FIRMWARE_ROOT = Path.cwd().resolve()
_REPO_ROOT = _FIRMWARE_ROOT.parent

_ROM_DIR = (_REPO_ROOT / "Rom").resolve()


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


def get_project_name() -> Optional[str]:
    """Đọc tên project(...) từ CMakeLists.txt gốc"""
    with Path("CMakeLists.txt").open() as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("project("):
                return stripped.split("(", 1)[1].split(")", 1)[0].strip()
    return None


def merge_bin() -> None:
    if os.system("idf.py merge-bin") != 0:
        print("merge-bin không thành công", file=sys.stderr)
        sys.exit(1)


def _ensure_idf_tools() -> None:
    """Đảm bảo `idf.py` sẵn sàng trước khi chạy các lệnh ESP-IDF"""
    if shutil.which("idf.py") is None:
        print(
            "[LỖI] Không tìm thấy lệnh idf.py. Vui lòng cài đặt ESP-IDF và thiết lập môi trường trước khi build.",
            file=sys.stderr,
        )
        sys.exit(1)


def zip_bin(name: str, version: str) -> Path:
    """Nén build/merged-binary.bin thành releases/v{version}_{name}.zip"""
    out_dir = Path("releases")
    out_dir.mkdir(exist_ok=True)
    output_path = out_dir / f"v{version}_{name}.zip"

    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("build/merged-binary.bin", arcname="merged-binary.bin")
    print(f"Nén bin vào {output_path} đã hoàn tất")
    return output_path

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


def _chip_family_from_target(target: str) -> str:
    mapping = {
        "esp32": "ESP32",
        "esp32s2": "ESP32-S2",
        "esp32s3": "ESP32-S3",
        "esp32c2": "ESP32-C2",
        "esp32c3": "ESP32-C3",
        "esp32c6": "ESP32-C6",
        "esp32h2": "ESP32-H2",
        "esp32p4": "ESP32-P4",
    }
    return mapping.get(target.lower(), target.upper())


@contextmanager
def _temporary_sdkconfig(board_root: Path, sdkconfig_files: list[str], sdkconfig_append: list[str]):
    """Nối thêm cấu hình vào sdkconfig và khôi phục trạng thái ban đầu sau khi build"""

    sdkconfig_path = Path("sdkconfig")
    original_content: Optional[str] = None
    if sdkconfig_path.exists():
        original_content = sdkconfig_path.read_text(encoding="utf-8")

    initial_size = sdkconfig_path.stat().st_size if sdkconfig_path.exists() else 0

    try:
        with sdkconfig_path.open("a", encoding="utf-8") as f:
            if initial_size > 0 and (original_content is None or not original_content.endswith("\n")):
                f.write("\n")
            f.write("# Nối bởi release.py\n")
            for rel_path in sdkconfig_files:
                file_path = Path(rel_path)
                if not file_path.is_absolute():
                    file_path = board_root / rel_path
                if not file_path.exists():
                    raise FileNotFoundError(f"Không tìm thấy tệp sdkconfig phụ {rel_path}")
                f.write(f"# >>> {rel_path}\n")
                content = file_path.read_text(encoding="utf-8")
                f.write(content)
                if not content.endswith("\n"):
                    f.write("\n")
                f.write(f"# <<< {rel_path}\n")
            for append in sdkconfig_append:
                f.write(f"{append}\n")
        yield
    finally:
        if original_content is None:
            if sdkconfig_path.exists():
                sdkconfig_path.unlink()
        else:
            sdkconfig_path.write_text(original_content, encoding="utf-8")

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

def _default_manifest_parts() -> list[dict[str, int | str]]:
    return [
        {"path": "bootloader.bin", "offset": 0x1000},
        {"path": "partitions.bin", "offset": 0x8000},
        {"path": "app.bin", "offset": 0x10000},
    ]


def _create_manifest(
    rom_root: Path,
    *,
    chip_family: str,
    version: str,
    build: dict,
) -> Path:
    manifest_path = rom_root / "manifest.json"
    parts_cfg = build.get("manifest_parts")
    parts: list[dict[str, int | str]] = []

    if parts_cfg:
        for entry in parts_cfg:
            rel_path = entry["path"]
            rel_path = str(rel_path).replace("\\", "/")
            offset_raw = entry["offset"]
            offset = int(str(offset_raw), 0)
            parts.append({"path": rel_path, "offset": offset})
    else:
        parts = _default_manifest_parts()

    manifest = {
        "name": build.get("manifest_name", build.get("name")),
        "version": version,
        "builds": [
            {
                "chipFamily": chip_family,
                "parts": [
                    {"path": str(item["path"]), "offset": item["offset"]}
                    for item in parts
                ],
            }
        ],
    }

    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest_path


def _prettify_name(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def _write_metadata(
    rom_root: Path,
    *,
    build: dict,
    manifest_path: Path,
    version: str,
) -> dict[str, str]:
    metadata_path = rom_root / "metadata.json"
    try:
        manifest_rel_path = manifest_path.relative_to(_REPO_ROOT)
    except ValueError:
        manifest_rel_path = manifest_path
    manifest_rel = manifest_rel_path.as_posix()
    if not manifest_rel.startswith("./") and not manifest_rel.startswith("../"):
        manifest_rel = f"./{manifest_rel}"
    metadata = {
        "id": build["name"],
        "board": build.get("display_name") or build.get("title") or _prettify_name(build["name"]),
        "version": build.get("version") or version,
        "description": build.get("description", ""),
        "manifest": manifest_rel,
        "target": build.get("target"),
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return metadata


def sync_webflasher_roms(output_path: Path | None = None) -> list[dict[str, str]]:
    """Đọc metadata trong Rom/*/metadata.json và ghi ra webflasher/roms.json"""

    rom_dir = _ROM_DIR
    if output_path is None:
        output_path = (_REPO_ROOT / "webflasher" / "roms.json").resolve()

    entries: list[dict[str, str]] = []
    if rom_dir.exists():
        for metadata_file in sorted(rom_dir.glob("*/metadata.json")):
            try:
                data = json.loads(metadata_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                print(f"[CẢNH BÁO] Không thể đọc {metadata_file}: {exc}", file=sys.stderr)
                continue
            entries.append(data)

    entries.sort(key=lambda item: item.get("id", ""))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(entries, ensure_ascii=False, indent=2)
    output_path.write_text(f"{serialized}\n", encoding="utf-8")
    print(f"Đã cập nhật {output_path} với {len(entries)} ROM")
    return entries


def release(board_type: str, config_filename: str = "config.json", *, filter_name: Optional[str] = None) -> list[dict[str, str]]:
    """Biên dịch và đóng gói tất cả/các biến thể được chỉ định của board_type được chỉ định

    Đối số:
        board_type: tên thư mục trong main/boards
        config_filename: tên config.json (mặc định: config.json)
        filter_name: nếu được chỉ định, chỉ biên dịch build["name"] phù hợp
    """
    cfg_path = _BOARDS_DIR / board_type / config_filename
    if not cfg_path.exists():
        print(f"[CẢNH BÁO] {cfg_path} không tồn tại, bỏ qua {board_type}")
        return []

    project_version = get_project_version()
    print(f"Phiên bản dự án: {project_version} ({cfg_path})")

    with cfg_path.open() as f:
        cfg = json.load(f)
    target = cfg["target"]
    project_name = get_project_name()

    builds = cfg.get("builds", [])
    if filter_name:
        builds = [b for b in builds if b["name"] == filter_name]
        if not builds:
            print(f"[LỖI] Không tìm thấy biến thể {filter_name} trong {config_filename} của {board_type}", file=sys.stderr)
            sys.exit(1)

    board_root = cfg_path.parent

    _ensure_idf_tools()

    metadata_entries: list[dict[str, str]] = []

    for build in builds:
        name = build["name"]
        if not name.startswith(board_type):
            raise ValueError(f"build.name {name} phải bắt đầu bằng {board_type}")

        version_label = build.get("version") or project_version or "0.0.0"
        output_path = Path("releases") / f"v{version_label}_{name}.zip"
        rom_root = _ROM_DIR / name
        metadata_path_existing = rom_root / "metadata.json"
        if output_path.exists() and metadata_path_existing.exists():
            print(f"Bỏ qua {name} vì {output_path} đã tồn tại")
            try:
                metadata_entries.append(json.loads(metadata_path_existing.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                print(f"[CẢNH BÁO] metadata hiện có của {name} bị hỏng, sẽ build lại", file=sys.stderr)
            else:
                continue

        # Xử lý sdkconfig_append
        board_type_config = _find_board_config(board_type)
        sdkconfig_append = [f"{board_type_config}=y"]
        sdkconfig_append.extend(build.get("sdkconfig_append", []))
        sdkconfig_files = build.get("sdkconfig_files", [])

        chip_family = _chip_family_from_target(target)

        print("-" * 80)
        print(f"tên: {name}")
        print(f"mục tiêu: {target}")
        for item in sdkconfig_append:
            print(f"sdkconfig_append: {item}")
        for item in sdkconfig_files:
            print(f"sdkconfig_file: {item}")

        os.environ.pop("IDF_TARGET", None)

        # Gọi set-target
        if os.system(f"idf.py set-target {target}") != 0:
            print("set-target không thành công", file=sys.stderr)
            sys.exit(1)

        with _temporary_sdkconfig(board_root, sdkconfig_files, sdkconfig_append):
            # Xây dựng với macro BOARD_NAME được định nghĩa thành name
            if os.system(f"idf.py -DBOARD_NAME={name} build") != 0:
                print("xây dựng không thành công")
                sys.exit(1)

            # merge-bin
            merge_bin()

        # Sao chép các thành phần để phục vụ webflasher
        rom_root.mkdir(parents=True, exist_ok=True)
        artifacts = {
            "bootloader.bin": Path("build") / "bootloader" / "bootloader.bin",
            "partitions.bin": Path("build") / "partition_table" / "partition-table.bin",
            "app.bin": Path("build") / f"{project_name}.bin" if project_name else None,
            "merged-binary.bin": Path("build") / "merged-binary.bin",
        }
        for label, src in artifacts.items():
            if src is None:
                continue
            if not src.exists():
                print(f"[CẢNH BÁO] Không tìm thấy tệp {label} ({src}) cho {name}")
                continue
            dest = rom_root / label
            shutil.copy2(src, dest)
            print(f"Đã sao chép {src} -> {dest}")

        manifest_path = _create_manifest(
            rom_root,
            chip_family=chip_family,
            version=version_label,
            build=build,
        )
        metadata = _write_metadata(
            rom_root,
            build={**build, "target": target},
            manifest_path=manifest_path,
            version=version_label,
        )
        metadata_entries.append(metadata)

        # Zip
        zip_bin(name, version_label)

    return metadata_entries

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
    parser.add_argument(
        "--sync-roms",
        action="store_true",
        help="Chỉ đồng bộ webflasher/roms.json từ metadata sẵn có trong thư mục Rom",
    )

    args = parser.parse_args()

    if args.sync_roms:
        sync_webflasher_roms()
        sys.exit(0)

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
        _ensure_idf_tools()
        merge_bin()
        curr_board_type = get_board_type_from_compile_commands()
        if curr_board_type is None:
            print("Không thể phân tích cú pháp board_type từ compile_commands.json", file=sys.stderr)
            sys.exit(1)
        project_ver = get_project_version()
        zip_bin(curr_board_type, project_ver)
        sync_webflasher_roms()
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

    built_any = False
    for bt in sorted(target_board_types):
        if not _board_type_exists(bt):
            print(f"[LỖI] Không tìm thấy board_type {bt} trong main/CMakeLists.txt", file=sys.stderr)
            sys.exit(1)
        cfg_path = _BOARDS_DIR / bt / args.config
        if bt == board_type_input and not cfg_path.exists():
            print(f"Board {bt} không có tệp cấu hình {args.config} được định nghĩa, bỏ qua")
            sys.exit(0)
        metadata_entries = release(
            bt,
            config_filename=args.config,
            filter_name=name_filter if bt == board_type_input else None,
        )
        if metadata_entries:
            built_any = True

    if built_any:
        sync_webflasher_roms()
    elif _ROM_DIR.exists():
        # Không build mới nhưng vẫn đảm bảo roms.json tồn tại
        sync_webflasher_roms()

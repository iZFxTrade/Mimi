#! /usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

import os
import struct
import zipfile
import oss2
import json
import requests
from requests.exceptions import RequestException

# Chuyển sang thư mục gốc của dự án
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_chip_id_string(chip_id):
    return {
        0x0000: "esp32",
        0x0002: "esp32s2",
        0x0005: "esp32c3",
        0x0009: "esp32s3",
        0x000C: "esp32c2",
        0x000D: "esp32c6",
        0x0010: "esp32h2",
        0x0011: "esp32c5",
        0x0012: "esp32p4",
        0x0017: "esp32c5",
    }[chip_id]

def get_flash_size(flash_size):
    MB = 1024 * 1024
    return {
        0x00: 1 * MB,
        0x01: 2 * MB,
        0x02: 4 * MB,
        0x03: 8 * MB,
        0x04: 16 * MB,
        0x05: 32 * MB,
        0x06: 64 * MB,
        0x07: 128 * MB,
    }[flash_size]

def get_app_desc(data):
    magic = struct.unpack("<I", data[0x00:0x04])[0]
    if magic != 0xabcd5432:
        raise Exception("Mô tả ứng dụng không hợp lệ")
    version = data[0x10:0x30].decode("utf-8").strip('\0')
    project_name = data[0x30:0x50].decode("utf-8").strip('\0')
    time = data[0x50:0x60].decode("utf-8").strip('\0')
    date = data[0x60:0x70].decode("utf-8").strip('\0')
    idf_ver = data[0x70:0x90].decode("utf-8").strip('\0')
    elf_sha256 = data[0x90:0xb0].hex()
    return {
        "name": project_name,
        "version": version,
        "compile_time": date + "T" + time,
        "idf_version": idf_ver,
        "elf_sha256": elf_sha256,
    }

def get_board_name(folder):
    basename = os.path.basename(folder)
    if basename.startswith("v0.2"):
        return "bread-simple"
    if basename.startswith("v0.3") or basename.startswith("v0.4") or basename.startswith("v0.5") or basename.startswith("v0.6"):
        if "ML307" in basename:
            return "bread-compact-ml307"
        elif "WiFi" in basename:
            return "bread-compact-wifi"
        elif "KevinBox1" in basename:
            return "kevin-box-1"
    if basename.startswith("v0.7") or basename.startswith("v0.8") or basename.startswith("v0.9") or basename.startswith("v1.") or basename.startswith("v2."):
        return basename.split("_")[1]
    raise Exception(f"Tên board không xác định: {basename}")

def find_app_partition(data):
    partition_begin = 0x8000
    partition_end = partition_begin + 0x4000
    # tìm phân vùng đầu tiên có loại 0x00
    for i in range(partition_begin, partition_end, 0x20):
        # magic là aa 50
        if data[i] == 0xaa and data[i + 1] == 0x50:
            # loại là ứng dụng
            if data[i + 2] == 0x00:
                # đọc offset và kích thước
                offset = struct.unpack("<I", data[i + 4:i + 8])[0]
                size = struct.unpack("<I", data[i + 8:i + 12])[0]
                # sau đó 16 byte là nhãn
                label = data[i + 12:i + 28].decode("utf-8").strip('\0')
                print(f"tìm thấy phân vùng ứng dụng tại 0x{i:08x}, offset: 0x{offset:08x}, kích thước: 0x{size:08x}, nhãn: {label}")
                return {
                    "offset": offset,
                    "size": size,
                    "label": label,
                }
    return None

def read_binary(dir_path):
    merged_bin_path = os.path.join(dir_path, "merged-binary.bin")
    merged_bin_data = open(merged_bin_path, "rb").read()

    # tìm phân vùng ứng dụng
    app_partition = find_app_partition(merged_bin_data)
    if app_partition is None:
        print("không tìm thấy phân vùng ứng dụng")
        return
    app_data = merged_bin_data[app_partition["offset"]:app_partition["offset"] + app_partition["size"]]
    # kiểm tra magic
    if app_data[0] != 0xE9:
        print("không phải là hình ảnh hợp lệ")
        return
    # lấy kích thước flash
    flash_size = get_flash_size(app_data[0x3] >> 4)
    chip_id = get_chip_id_string(app_data[0xC])
    # lấy các phân đoạn
    segment_count = app_data[0x1]
    segments = []
    offset = 0x18
    image_size = 0x18
    for i in range(segment_count):
        segment_size = struct.unpack("<I", app_data[offset + 4:offset + 8])[0]
        image_size += 8 + segment_size
        offset += 8
        segment_data = app_data[offset:offset + segment_size]
        offset += segment_size
        segments.append(segment_data)
    assert offset < len(app_data), "offset nằm ngoài giới hạn"

    # thêm kích thước tổng kiểm
    image_size += 1
    image_size = (image_size + 15) & ~15
    #ハッシュが追加されました
    if app_data[0x17] == 1:
        image_size += 32
    print(f"kích thước hình ảnh: {image_size}")

    # xác minh dữ liệu còn lại đều là 0xFF
    for i in range(image_size, len(app_data)):
        if app_data[i] != 0xFF:
            print(f"Không thể xác minh hình ảnh, dữ liệu tại 0x{i:08x} không phải là 0xFF")
            return

    image_data = app_data[:image_size]
    
    # trích xuất tệp bin
    bin_path = os.path.join(dir_path, "xiaozhi.bin")
    if not os.path.exists(bin_path):
        print("trích xuất tệp bin vào", bin_path)
        open(bin_path, "wb").write(image_data)

    # Mô tả ứng dụng nằm trong phân đoạn đầu tiên
    desc = get_app_desc(segments[0])
    return {
        "chip_id": chip_id,
        "flash_size": flash_size,
        "board": get_board_name(dir_path),
        "application": desc,
        "firmware_size": image_size,
    }

def extract_zip(zip_path, extract_path):
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    print(f"Đang giải nén {zip_path} vào {extract_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def upload_dir_to_oss(source_dir, target_dir):
    auth = oss2.Auth(os.environ['OSS_ACCESS_KEY_ID'], os.environ['OSS_ACCESS_KEY_SECRET'])
    bucket = oss2.Bucket(auth, os.environ['OSS_ENDPOINT'], os.environ['OSS_BUCKET_NAME'])
    for filename in os.listdir(source_dir):
        oss_key = os.path.join(target_dir, filename)
        print('đang tải lên', oss_key)
        bucket.put_object(oss_key, open(os.path.join(source_dir, filename), 'rb'))

def post_info_to_server(info):
    """
    Gửi thông tin phần mềm cơ sở đến máy chủ
    
    Args:
        info: Từ điển chứa thông tin phần mềm cơ sở
    """
    try:
        # Lấy URL máy chủ và mã thông báo từ các biến môi trường
        server_url = os.environ.get('VERSIONS_SERVER_URL')
        server_token = os.environ.get('VERSIONS_TOKEN')
        
        if not server_url or not server_token:
            raise Exception("Thiếu SERVER_URL hoặc TOKEN trong các biến môi trường")

        # Chuẩn bị tiêu đề và dữ liệu yêu cầu
        headers = {
            'Authorization': f'Bearer {server_token}',
            'Content-Type': 'application/json'
        }
        
        # Gửi yêu cầu POST
        response = requests.post(
            server_url,
            headers=headers,
            json={'jsonData': json.dumps(info)}
        )
        
        # Kiểm tra trạng thái phản hồi
        response.raise_for_status()
        
        print(f"Đã tải lên thành công thông tin phiên bản cho thẻ: {info['tag']}")
        
    except RequestException as e:
        if hasattr(e.response, 'json'):
            error_msg = e.response.json().get('error', str(e))
        else:
            error_msg = str(e)
        print(f"Không thể tải lên thông tin phiên bản: {error_msg}")
        raise
    except Exception as e:
        print(f"Lỗi khi tải lên thông tin phiên bản: {str(e)}")
        raise

def main():
    release_dir = "releases"
    # tìm các tệp zip bắt đầu bằng "v"
    for name in os.listdir(release_dir):
        if name.startswith("v") and name.endswith(".zip"):
            tag = name[:-4]
            folder = os.path.join(release_dir, tag)
            info_path = os.path.join(folder, "info.json")
            if not os.path.exists(info_path):
                if not os.path.exists(folder):
                    os.makedirs(folder)
                    extract_zip(os.path.join(release_dir, name), folder)
                info = read_binary(folder)
                target_dir = os.path.join("firmwares", tag)
                info["tag"] = tag
                info["url"] = os.path.join(os.environ['OSS_BUCKET_URL'], target_dir, "xiaozhi.bin")
                open(info_path, "w").write(json.dumps(info, indent=4))
                # tải tất cả các tệp lên oss
                upload_dir_to_oss(folder, target_dir)
                # đọc info.json
                info = json.load(open(info_path))
                # đăng info.json lên máy chủ
                post_info_to_server(info)



if __name__ == "__main__":
    main()
# Thư mục Rom

Các gói firmware sau khi chạy `python3 firmware/scripts/release.py <board>` sẽ được sao chép vào đây theo dạng `Rom/<tên-build>/`.
Mỗi thư mục con chứa tối thiểu các thành phần:

- `bootloader.bin`
- `partitions.bin`
- `app.bin`
- `merged-binary.bin`
- `manifest.json`: Manifest tự sinh cho ESP Web Tools (tham chiếu tới các tệp nhị phân ở trên)
- `metadata.json`: Thông tin mô tả (tên hiển thị, phiên bản, mô tả) dùng để tạo `webflasher/roms.json`

Sau khi build, `release.py` sẽ tự động đồng bộ `webflasher/roms.json` dựa trên các tệp `metadata.json`, vì vậy chỉ cần deploy thư mục `Rom/` lên webflasher là danh sách firmware sẽ được cập nhật.

## Hướng dẫn build firmware

Để tự tạo các bản ROM và đồng bộ vào thư mục này, cần chuẩn bị môi trường ESP-IDF đầy đủ:

1. Cài đặt ESP-IDF 5.x theo hướng dẫn chính thức từ Espressif.
2. Nếu chưa có ESP-IDF, hãy chạy script `./setup_build_env.sh` (yêu cầu quyền sudo và kết nối Internet) để cài đặt bộ công cụ cùng
   clone ESP-IDF vào `Mimi/esp-idf`. Bạn cũng có thể tự chuẩn bị ESP-IDF theo hướng dẫn chính thức của Espressif.
3. Đảm bảo có thể gọi `idf.py` từ terminal bằng một trong các cách sau:
   - Thêm ESP-IDF vào biến môi trường `PATH`.
   - Xuất biến `IDF_PY_PATH` trỏ tới tệp `idf.py`.
   - Xuất biến `IDF_PATH` trỏ tới thư mục gốc ESP-IDF.
   - Đặt thư mục `esp-idf/` bên cạnh repo (ví dụ `Mimi/esp-idf`).
4. Kích hoạt môi trường ESP-IDF bằng cách chạy script `export.sh` của ESP-IDF (ví dụ: `. $IDF_PATH/export.sh`).
5. Từ thư mục gốc repo, chạy `python3 firmware/scripts/release.py <board>` với `<board>` là một trong các bảng được hỗ trợ trong `firmware/main/Kconfig.projbuild`.

Script sẽ build firmware, thu thập các tệp nhị phân và metadata rồi sao chép vào `Rom/<tên-build>/`. Nếu công cụ không tìm thấy `idf.py`, kiểm tra lại các biến môi trường ở bước 2.

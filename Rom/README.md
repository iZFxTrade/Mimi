# Thư mục Rom

Các gói firmware sau khi chạy `python3 firmware/scripts/release.py <board>` sẽ được sao chép vào đây theo dạng `Rom/<tên-build>/`. Mỗi thư mục con chứa tối thiểu các thành phần:

- `bootloader.bin`
- `partitions.bin`
- `app.bin`
- `merged-binary.bin`
- `manifest.json`: Manifest tự sinh cho ESP Web Tools (tham chiếu tới các tệp nhị phân ở trên)
- `metadata.json`: Thông tin mô tả (tên hiển thị, phiên bản, mô tả) dùng để tạo `webflasher/roms.json`

Sau khi build, `release.py` sẽ tự động đồng bộ `webflasher/roms.json` dựa trên các tệp `metadata.json`, vì vậy chỉ cần deploy thư mục `Rom/` lên webflasher là danh sách firmware sẽ được cập nhật.

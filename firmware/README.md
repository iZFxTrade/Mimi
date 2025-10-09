# Tổng quan về Firmware

Thư mục này chứa mã nguồn cho firmware của thiết bị, chạy trên các vi điều khiển dòng ESP32. Firmware được xây dựng dựa trên framework [ESP-IDF](https://github.com/espressif/esp-idf) của Espressif và sử dụng nhiều thư viện khác nhau để quản lý các chức năng như âm thanh, hiển thị, kết nối mạng và các chức năng cốt lõi của ứng dụng.

## Cấu trúc thư mục chi tiết

```
firmware/
│
├── CMakeLists.txt: Tệp cấu hình CMake chính cho toàn bộ firmware, điều phối việc biên dịch các thành phần và mã nguồn.
│
├── LICENSE: Tệp giấy phép phần mềm cho mã nguồn firmware.
│
├── README.md: (Tệp này) - Cung cấp tổng quan về cấu trúc, cách xây dựng và luồng hoạt động của firmware.
│
├── sdkconfig.defaults*: Chứa các giá trị cấu hình mặc định cho ESP-IDF. Các giá trị này có thể được ghi đè bởi cấu hình của từng bo mạch.
│
├── docs/: Chứa tài liệu thiết kế, hướng dẫn bổ sung, và các sơ đồ liên quan đến firmware.
│
├── main/: Thư mục cốt lõi chứa logic chính của ứng dụng và các module chức năng. (Xem `main/README.md` để biết thêm chi tiết).
│
├── partitions/: Chứa các tệp `.csv` định nghĩa bảng phân vùng bộ nhớ flash cho các kích thước và yêu cầu khác nhau. (Xem `partitions/README.md` để biết thêm chi tiết).
│
└── scripts/: Chứa các tập lệnh Python và shell để tự động hóa các tác vụ như chuyển đổi tài nguyên, xây dựng và phát hành. (Xem `scripts/README.md` để biết thêm chi tiết).
```

## Luồng công việc & Xây dựng

1.  **Cài đặt Môi trường**: Bạn cần cài đặt và cấu hình môi trường phát triển ESP-IDF theo hướng dẫn của Espressif. Có thể sử dụng
    script `./setup_build_env.sh` để cài đặt nhanh (yêu cầu Internet và quyền sudo) hoặc tự cài đặt theo tài liệu chính thức. Nếu chưa thêm
    `idf.py` vào `PATH`, có thể chỉ định trực tiếp đường dẫn bằng biến môi trường `IDF_PY_PATH` hoặc `IDF_PATH`. Tập lệnh
    `scripts/release.py` sẽ tự động dò tìm trong các biến này cũng như thư mục `esp-idf/tools/idf.py` đặt cạnh repo. Trên GitHub Codespaces/
    GitHub Workspace, `setup_build_env.sh` cài ESP-IDF vào `/workspaces/Mimi/esp-idf`; hãy `source` tệp `export.sh` trong thư mục này trước khi build.

2.  **Chọn Bo mạch và Biên dịch**: Hệ thống xây dựng sử dụng CMake. Để biên dịch cho một bo mạch cụ thể, bạn cần chỉ định tên bo mạch đó. Ví dụ, để xây dựng cho `esp-box-3`:

    ```sh
    # Tùy chọn 1: Sử dụng idf.py với biến tùy chỉnh
    idf.py set-target esp32s3 -D BOARD_NAME="esp-box-3"
    idf.py build
    
    # Tùy chọn 2: Sử dụng tập lệnh phát hành được cung cấp
    python scripts/release.py esp-box-3
    ```

3.  **Quản lý Tài nguyên**: Các tài nguyên trong `main/assets/` không được biên dịch trực tiếp. Thay vào đó, chúng được đóng gói vào một hình ảnh hệ thống tệp (SPIFFS hoặc LittleFS) bằng cách sử dụng các tập lệnh trong `scripts/spiffs_assets/`. Hình ảnh này sau đó được nạp vào phân vùng `spiffs` trên bộ nhớ flash của thiết bị.

## Lưu ý Quan trọng khi Tùy chỉnh Bo mạch

> **Cảnh báo**: Đối với các bảng mạch phát triển tùy chỉnh, khi cấu hình IO khác với bảng mạch ban đầu, tuyệt đối không ghi đè trực tiếp lên cấu hình của bảng mạch ban đầu để biên dịch firmware. Phải tạo một loại bảng mạch mới, hoặc phân biệt thông qua các cấu hình `name` và macro sdkconfig khác nhau trong tệp `config.json`. Sử dụng `python scripts/release.py [tên_thư_mục_bảng_mạch]` để biên dịch và đóng gói firmware.
> 
> Nếu bạn ghi đè trực tiếp lên cấu hình ban đầu, trong tương lai khi nâng cấp OTA, firmware tùy chỉnh của bạn có thể bị ghi đè bởi firmware tiêu chuẩn của bảng mạch ban đầu, dẫn đến thiết bị của bạn không hoạt động bình thường. Mỗi bảng mạch phát triển có một mã định danh duy nhất và kênh nâng cấp firmware tương ứng, việc duy trì tính duy nhất của mã định danh bảng mạch là rất quan trọng.

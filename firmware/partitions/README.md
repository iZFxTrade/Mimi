# Thư mục `partitions`

Thư mục này chứa các tệp `.csv` (Comma-Separated Values) định nghĩa bảng phân vùng cho bộ nhớ flash của các thiết bị ESP32. Bảng phân vùng chia bộ nhớ flash thành các vùng logic khác nhau để lưu trữ mã ứng dụng, dữ liệu, hệ thống tệp, và các thành phần quan trọng khác.

Việc lựa chọn bảng phân vùng nào phụ thuộc vào kích thước bộ nhớ flash của bo mạch và các yêu cầu về tính năng (ví dụ: có cần phân vùng lớn cho mô hình nhận dạng giọng nói tùy chỉnh hay không).

## Cấu trúc thư mục và Chức năng

Thư mục này được chia thành các phiên bản (`v1`, `v2`) có thể tương ứng với các thay đổi lớn trong cấu trúc hoặc sơ đồ bố trí.

```
firmware/partitions/
│
├── v1/
│   ├── 4m.csv: Bảng phân vùng cho bộ nhớ flash 4MB.
│   ├── 8m.csv: Bảng phân vùng cho bộ nhớ flash 8MB.
│   ├── 16m.csv: Bảng phân vùng cho bộ nhớ flash 16MB.
│   ├── 32m.csv: Bảng phân vùng cho bộ nhớ flash 32MB.
│   ├── 16m_custom_wakeword.csv: Phân vùng 16MB với một vùng lớn hơn cho mô hình từ khóa đánh thức tùy chỉnh.
│   ├── 16m_echoear.csv: Phân vùng 16MB được tối ưu hóa cho bo mạch EchoEar.
│   └── 4m_esp-hi.csv: Phân vùng 4MB dành riêng cho bo mạch ESP-Hi.
│
└── v2/
    ├── 4m.csv
    ├── 8m.csv
    ├── 16m.csv
    ├── 16m_c3.csv: Phân vùng 16MB cho các biến thể ESP32-C3.
    ├── 32m.csv
    ├── README.md
    └── README.vi.md
```

### Cấu trúc của một tệp `.csv` phân vùng

Mỗi dòng trong tệp `.csv` đại diện cho một phân vùng và tuân theo định dạng sau:

`Tên, Loại, Kiểu con, Độ lệch, Kích thước, Cờ`

-   **`Tên` (Name)**: Tên của phân vùng (ví dụ: `app0`, `spiffs`, `nvs`).
-   **`Loại` (Type)**: `app` (cho mã thực thi) hoặc `data` (cho dữ liệu).
-   **`Kiểu con` (SubType)**: `factory`, `ota_0`, `ota_1` (cho phân vùng ứng dụng), hoặc `nvs`, `spiffs`, `coredump` (cho phân vùng dữ liệu).
-   **`Độ lệch` (Offset)**: Địa chỉ bắt đầu của phân vùng trong bộ nhớ flash. Có thể để trống để tự động tính toán.
-   **`Kích thước` (Size)**: Kích thước của phân vùng (ví dụ: `1M`, `2048K`, `16M`).
-   **`Cờ` (Flags)**: `encrypted` (để bật mã hóa flash).

**Ví dụ từ `16m.csv`:**

```csv
# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     ,        24K,
phy_init, data, phy,     ,        4K,
otadata,  data, ota,     ,        8K,
app0,     app,  ota_0,   ,        4M,
app1,     app,  ota_1,   ,        4M,
spiffs,   data, spiffs,  ,        7M,
coredump, data, coredump,,        64K,
```

## Luồng công việc (Workflow)

1.  **Lựa chọn bảng phân vùng**:
    *   Bảng phân vùng được chọn trong quá trình cấu hình dự án ESP-IDF (thường thông qua `menuconfig` hoặc các biến trong `CMake`).
    *   Việc lựa chọn phụ thuộc vào `config.json` của bo mạch đang được xây dựng. Hệ thống xây dựng sẽ đọc `config.json` để xác định kích thước bộ nhớ flash và chọn tệp `.csv` phù hợp.

2.  **Tùy chỉnh một bảng phân vùng**:
    *   Nếu một bo mạch có yêu cầu lưu trữ đặc biệt (ví dụ: cần một phân vùng `spiffs` lớn hơn), bạn có thể sao chép một tệp `.csv` hiện có, đổi tên nó (ví dụ: `16m_my_special_board.csv`) và điều chỉnh các giá trị `Kích thước`.
    *   Sau đó, bạn cần cập nhật cấu hình của bo mạch (ví dụ: trong `CMakeLists.txt` hoặc `config.json`) để trỏ đến tệp phân vùng tùy chỉnh này khi xây dựng cho bo mạch đó.

3.  **Quá trình xây dựng**:
    *   Trong khi biên dịch, công cụ `gen_esp32part.py` của ESP-IDF sẽ xử lý tệp `.csv` đã chọn để tạo ra một bảng phân vùng nhị phân (`partitions.bin`).
    *   Tệp `partitions.bin` này sau đó được nạp vào địa chỉ `0x8000` (đối với sơ đồ mặc định) trong bộ nhớ flash của thiết bị. Bootloader sẽ đọc bảng này khi khởi động để biết vị trí và kích thước của từng phân vùng.
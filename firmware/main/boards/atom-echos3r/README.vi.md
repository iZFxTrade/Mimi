# AtomEchoS3R
## Giới thiệu

AtomEchoS3R là một bộ điều khiển lập trình được IoT do M5Stack ra mắt, dựa trên ESP32-S3-PICO-1-N8R8. Nó sử dụng một giải pháp tích hợp của bộ giải mã âm thanh đơn kênh ES8311, micrô MEMS và bộ khuếch đại công suất NS4150B.

Phiên bản phát triển **không có màn hình và không có nút bấm bổ sung**. Cần phải sử dụng tính năng đánh thức bằng giọng nói. Khi cần, hãy sử dụng `idf.py monitor` để xem nhật ký và xác định trạng thái hoạt động.

## Lệnh cấu hình và biên dịch

**Đặt mục tiêu biên dịch thành ESP32S3**

```bash
idf.py set-target esp32s3
```

**Mở menuconfig và cấu hình**

```bash
idf.py menuconfig
```

Cấu hình các tùy chọn sau:

- `Xiaozhi Assistant` → `Board Type` → chọn `AtomEchoS3R`
- `Partition Table` → `Custom partition CSV file` → xóa nội dung hiện có, nhập `partitions/v2/8m.csv`
- `Serial flasher config` → `Flash size` → chọn `8 MB`
- `Component config` → `ESP PSRAM` → `Support for external, SPI-connected RAM` → `SPI RAM config` → chọn `Octal Mode PSRAM`

Nhấn `S` để lưu, nhấn `Q` để thoát.

**Biên dịch**

```bash
idf.py build
```

**Nạp chương trình**

Kết nối AtomEchoS3R với máy tính, nhấn và giữ nút RESET ở bên cạnh cho đến khi đèn xanh bên dưới nút RESET nhấp nháy.

```bash
idf.py flash
```

Sau khi nạp xong, nhấn nút RESET một lần để khởi động lại thiết bị.

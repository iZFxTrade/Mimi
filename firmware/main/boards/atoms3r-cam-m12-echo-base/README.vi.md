# AtomS3R CAM/M12 + Echo Base

## Giới thiệu

<div align="center">
    <a href="https://docs.m5stack.com/zh_CN/core/AtomS3R%20Cam"><b> Trang chủ sản phẩm AtomS3R CAM </b></a>
    |
    <a href="https://docs.m5stack.com/zh_CN/core/AtomS3R-M12"><b> Trang chủ sản phẩm AtomS3R M12 </b></a>
    |
    <a href="https://docs.m5stack.com/zh_CN/atom/Atomic%20Echo%20Base"><b> Trang chủ sản phẩm Echo Base </b></a>
</div>

AtomS3R CAM và AtomS3R M12 là các bộ điều khiển lập trình được IoT do M5Stack ra mắt, dựa trên ESP32-S3-PICO-1-N8R8 và được trang bị camera. Atomic Echo Base là một đế nhận dạng giọng nói được thiết kế đặc biệt cho dòng máy chủ M5 Atom, sử dụng giải pháp tích hợp của bộ giải mã âm thanh đơn kênh ES8311, micrô MEMS và bộ khuếch đại công suất NS4150B.

Cả hai phiên bản phát triển đều **không có màn hình và không có nút bấm bổ sung**, cần phải sử dụng tính năng đánh thức bằng giọng nói. Khi cần, hãy sử dụng `idf.py monitor` để xem nhật ký và xác định trạng thái hoạt động.

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

- `Xiaozhi Assistant` → `Board Type` → chọn `AtomS3R CAM/M12 + Echo Base`
- `Xiaozhi Assistant` → `IoT Protocol` → chọn `Giao thức MCP` để bật chức năng nhận dạng camera
- `Partition Table` → `Custom partition CSV file` → xóa nội dung hiện có, nhập `partitions/v2/8m.csv`
- `Serial flasher config` → `Flash size` → chọn `8 MB`

Nhấn `S` để lưu, nhấn `Q` để thoát.

**Biên dịch**

```bash
idf.py build
```

**Nạp chương trình**

Kết nối AtomS3R CAM/M12 với máy tính, nhấn và giữ nút RESET ở bên cạnh cho đến khi đèn xanh bên dưới nút RESET nhấp nháy.

```bash
idf.py flash
```

Sau khi nạp xong, nhấn nút RESET một lần để khởi động lại.

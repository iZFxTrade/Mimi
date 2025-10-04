# Thư mục `assets`

Thư mục này là kho chứa các tài nguyên tĩnh được ứng dụng firmware sử dụng. Các tài nguyên này bao gồm các tệp âm thanh, hình ảnh, phông chữ và các tệp ngôn ngữ cần thiết cho giao diện người dùng và các chức năng khác của thiết bị.

## Cấu trúc thư mục và Chức năng

```
firmware/main/assets/
│
├── common/
│   ├── exclamation.ogg: Âm thanh thông báo (ví dụ: cảnh báo).
│   ├── low_battery.ogg: Âm thanh cảnh báo pin yếu.
│   ├── popup.ogg: Âm thanh khi có cửa sổ bật lên.
│   ├── success.ogg: Âm thanh thông báo thành công.
│   └── vibration.ogg: Âm thanh cho hiệu ứng rung.
│
├── images/
│   ├── emotion_custom.c: Dữ liệu hình ảnh tùy chỉnh cho các biểu cảm, ở dạng mảng C.
│   └── emotion_custom.h: Tệp tiêu đề cho `emotion_custom.c`.
│
└── locales/
    ├── ar-SA/, cs-CZ/, de-DE/, en-US/, es-ES/, ... (các thư mục ngôn ngữ)
    │   ├── 0.ogg, 1.ogg, ...: Các tệp âm thanh cho các số đếm.
    │   ├── activation.ogg: Âm thanh khi kích hoạt.
    │   ├── err_pin.ogg: Âm thanh báo lỗi mã PIN.
    │   ├── err_reg.ogg: Âm thanh báo lỗi đăng ký.
    │   ├── language.json: Tệp cấu hình ngôn ngữ, chứa các chuỗi văn bản đã dịch.
    │   ├── upgrade.ogg: Âm thanh thông báo nâng cấp.
    │   ├── welcome.ogg: Âm thanh chào mừng.
    │   └── wificonfig.ogg: Âm thanh hướng dẫn cấu hình Wi-Fi.
    └── README.vi.md: (Tệp này sẽ được thay thế)
```

## Luồng công việc (Workflow)

1.  **Thêm hoặc cập nhật tài nguyên**:
    *   **Âm thanh**: Đặt các tệp âm thanh (thường là định dạng `.ogg`) vào thư mục `common` (cho các âm thanh chung) hoặc thư mục `locales/<mã_ngôn_ngữ>` (cho các âm thanh cụ thể theo ngôn ngữ).
    *   **Hình ảnh**: Các hình ảnh thường được chuyển đổi thành mảng C (sử dụng công cụ trong thư mục `scripts/Image_Converter`) và đặt trong thư mục `images`.
    *   **Bản dịch**: Cập nhật tệp `language.json` trong thư mục `locales` tương ứng với các chuỗi văn bản mới hoặc đã sửa đổi.

2.  **Sử dụng tài nguyên trong mã**:
    *   Các tài nguyên này được biên dịch và đưa vào firmware. Mã nguồn C/C++ sẽ tham chiếu đến các tài nguyên này thông qua các tên biến hoặc định danh được tạo ra trong quá trình xây dựng.

3.  **Xây dựng Firmware**:
    *   Khi xây dựng firmware, các tài nguyên trong `assets` sẽ được đóng gói bằng cách sử dụng các tập lệnh trong thư mục `scripts/spiffs_assets`. Các tập lệnh này tạo ra một hình ảnh hệ thống tệp (SPIFFS hoặc LittleFS) chứa tất cả tài nguyên. Hình ảnh này sau đó được nạp vào bộ nhớ flash của thiết bị cùng với mã ứng dụng.

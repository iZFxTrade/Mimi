# Tổng quan về Firmware

Thư mục này chứa mã nguồn cho firmware của MiMi, chạy trên vi điều khiển ESP32. Firmware được xây dựng dựa trên framework [ESP-IDF](https://github.com/espressif/esp-idf) của Espressif và sử dụng nhiều thư viện khác nhau để quản lý các chức năng như âm thanh, hiển thị, kết nối mạng và các chức năng cốt lõi của ứng dụng.

## Cấu trúc thư mục

- **`main/`**: Chứa mã nguồn chính của ứng dụng.
  - **`application.cc/h`**: Logic cốt lõi của ứng dụng, quản lý trạng thái, sự kiện và tương tác giữa các thành phần khác nhau.
  - **`audio/`**: Quản lý việc thu, xử lý và phát lại âm thanh. Bao gồm các trình điều khiển cho codec âm thanh, xử lý tín hiệu (như khử tiếng vọng) và mã hóa/giải mã Opus.
  - **`boards/`**: Các tệp cấu hình dành riêng cho phần cứng cho các bo mạch ESP32 khác nhau được hỗ trợ.
  - **`display/`**: Quản lý giao diện người dùng (UI) bằng thư viện đồ họa LVGL. Điều này bao gồm hiển thị khuôn mặt cảm xúc, menu cài đặt và các yếu tố hình ảnh khác.
  - **`network/`**: Xử lý kết nối Wi-Fi và giao tiếp với các dịch vụ back-end (ví dụ: MQTT, WebSocket).
  - **`utils/`**: Các chức năng và lớp tiện ích được sử dụng trong toàn bộ dự án.
- **`components/`**: Chứa các thành phần và thư viện của bên thứ ba được dự án sử dụng. Điều này có thể bao gồm các trình điều khiển tùy chỉnh, các thư viện được port hoặc các thành phần dành riêng cho dự án không phải là một phần của ESP-IDF cốt lõi.
- **`partitions/`**: Sơ đồ bảng phân vùng cho các cấu hình flash khác nhau (ví dụ: 8MB, 16MB). Điều này xác định cách bộ nhớ flash của ESP32 được phân bổ cho các phần khác nhau của ứng dụng (ví dụ: NVS, OTA, ứng dụng chính, lưu trữ tệp).

## Các thành phần chính

- **Application (`application.cc`)**: Đóng vai trò là điểm vào chính và bộ điều phối trung tâm của firmware. Nó khởi tạo tất cả các dịch vụ khác và quản lý vòng đời của ứng dụng.
- **AudioService (`audio/audio_service.cc`)**: Chịu trách nhiệm về toàn bộ đường ống âm thanh, từ việc thu dữ liệu PCM thô từ micrô đến mã hóa nó thành Opus để truyền và giải mã các luồng âm thanh đến để phát lại.
- **Display (`display/display.cc`)**: Quản lý mọi thứ được vẽ trên màn hình. Nó sử dụng LVGL để tạo một giao diện người dùng phong phú và tương tác.
- **Network Protocols (`network/`)**: Triển khai các giao thức truyền thông (MQTT và WebSocket) để tương tác với máy chủ. Chúng xử lý việc trao đổi tin nhắn điều khiển và truyền phát dữ liệu âm thanh.
- **Board Support Package (BSP) (`boards/`)**: Lớp trừu tượng hóa phần cứng cho phép firmware chạy trên các thiết kế phần cứng khác nhau với những thay đổi tối thiểu. Mỗi bo mạch có cấu hình chân và trình điều khiển ngoại vi riêng.

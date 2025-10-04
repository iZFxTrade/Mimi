# AI Project Blueprint: ESP32 Voice Assistant Firmware

**Mục đích của tệp này:** Cung cấp cho các trợ lý AI một bản thiết kế chi tiết và toàn diện về cấu trúc, chức năng và luồng hoạt động của dự án. Đây là bản đồ chi tiết để xác định chính xác vị trí mã nguồn cần thiết cho việc bảo trì, sửa lỗi hoặc phát triển tính năng mới.

---

## 1. Tổng quan dự án và Chức năng cốt lõi

Đây là một dự án firmware mã nguồn mở dành cho các thiết bị phần cứng dựa trên vi điều khiển ESP32, với mục tiêu chính là tạo ra một trợ lý giọng nói thông minh và có khả năng tùy biến cao.

### Các chức năng chính và vị trí mã nguồn tương ứng:
- **Trợ lý giọng nói**:
    - **Nhận dạng từ khóa (Wake Word)**: `firmware/main/audio/wake_word.cc`
    - **Thu âm giọng nói**: `firmware/main/audio/audio_input.cc`
    - **Gửi dữ liệu âm thanh tới máy chủ**: `firmware/main/protocols/ws_client.cc` (qua WebSocket)
    - **Phát lại phản hồi âm thanh**: `firmware/main/audio/audio_output.cc`
- **Hỗ trợ đa bo mạch (Multi-Board)**:
    - **Cấu hình phần cứng**: `firmware/main/boards/[tên-bo-mạch]/config.h`
    - **Triển khai logic bo mạch**: `firmware/main/boards/[tên-bo-mạch]/[tên-bo-mạch]_board.cc`
- **Giao diện người dùng (UI)**:
    - **Quản lý các màn hình (Views)**: `firmware/main/display/view_manager.cc`
    - **Triển khai từng màn hình**: `firmware/main/display/ui_*.cc` (ví dụ: `ui_assistant.cc`, `ui_settings.cc`)
    - **Thư viện đồ họa**: LVGL (được tích hợp như một component của ESP-IDF)
- **Kết nối mạng**:
    - **Quản lý Wi-Fi**: `firmware/main/boards/common/wifi_board.cc`
    - **Giao thức MQTT**: `firmware/main/protocols/mqtt_client.cc`
    - **Giao thức WebSocket**: `firmware/main/protocols/ws_client.cc`
- **Cập nhật qua mạng (OTA)**: `firmware/main/ota.cc`
- **Quản lý cài đặt**: `firmware/main/settings.cc` (sử dụng bộ nhớ NVS).
- **Mở rộng và Tùy chỉnh**:
    - **Hành động tùy chỉnh (Custom Actions)**: `firmware/main/custom_action.cc`

---

## 2. Luồng hoạt động (Workflow) của ứng dụng

1.  **Khởi động (Boot)**: Bootloader của ESP32 khởi chạy ứng dụng. Điểm vào là hàm `app_main` trong `firmware/main/main.cc`.
2.  **Khởi tạo `Application`**: `app_main` tạo một đối tượng của lớp `Application` (`firmware/main/application.cc`), đây là lớp điều phối chính.
3.  **Khởi tạo phần cứng (Board Init)**: `Application` khởi tạo đối tượng bo mạch phần cứng cụ thể (ví dụ: `EspBox3Board` từ `firmware/main/boards/esp-box-3/`). Lớp bo mạch này chịu trách nhiệm khởi tạo các ngoại vi như màn hình, codec âm thanh, nút bấm dựa trên `config.h`.
4.  **Khởi tạo các dịch vụ (Services Init)**: `Application` khởi tạo các dịch vụ cốt lõi như `AudioService` (để quản lý micro và loa) và `ViewManager` (để quản lý giao diện màn hình).
5.  **Kết nối mạng**: Ứng dụng kết nối vào mạng Wi-Fi đã được cấu hình.
6.  **Kết nối máy chủ**: Thiết bị thiết lập kết nối đến máy chủ backend thông qua MQTT hoặc WebSocket.
7.  **Vòng lặp chính & Máy trạng thái**: `Application` chạy một vòng lặp vô tận, hoạt động như một máy trạng thái (state machine). Nó lắng nghe các sự kiện từ phần cứng (nút bấm), dịch vụ âm thanh (từ khóa đánh thức), và mạng (tin nhắn từ máy chủ) để chuyển đổi giữa các trạng thái như `IDLE`, `LISTENING`, `SPEAKING`, và điều phối hành động của các dịch vụ tương ứng.

---

## 3. Bản đồ cấu trúc thư mục chi tiết

```
./
├── .idx/
│   └── dev.nix: Tệp cấu hình cho môi trường phát triển Nix, đảm bảo môi trường phát triển nhất quán.
│
├── firmware/
│   ├── CMakeLists.txt: Tệp cấu hình CMake chính, điều phối quá trình xây dựng toàn bộ firmware.
│   ├── LICENSE: Giấy phép phần mềm của dự án.
│   ├── README.md: Tài liệu tổng quan về thư mục firmware.
│   ├── sdkconfig.defaults*: Các giá trị cấu hình mặc định cho ESP-IDF.
│   ├── docs/: Chứa các tài liệu thiết kế, hình ảnh, sơ đồ kỹ thuật.
│   ├── main/: Thư mục mã nguồn cốt lõi của ứng dụng.
│   │   ├── application.cc/.h: Lớp ứng dụng chính, quản lý trạng thái và luồng sự kiện.
│   │   ├── main.cc: Điểm vào chính của chương trình (hàm app_main).
│   │   ├── assets/: Tài nguyên tĩnh (âm thanh, hình ảnh, phông chữ, ngôn ngữ).
│   │   ├── audio/: Module quản lý âm thanh (thu âm, xử lý, phát lại, nhận dạng wake word).
│   │   ├── boards/: Cấu hình cho các bo mạch phần cứng được hỗ trợ. Mỗi bo mạch có thư mục riêng.
│   │   ├── display/: Module quản lý giao diện người dùng trên màn hình (sử dụng LVGL).
│   │   ├── led/: Module điều khiển đèn LED trạng thái.
│   │   ├── protocols/: Triển khai các giao thức giao tiếp (MQTT, WebSocket).
│   │   └── ... (các file chức năng khác như settings.cc, ota.cc, ...)
│   │
│   ├── partitions/: Chứa các tệp .csv định nghĩa bảng phân vùng bộ nhớ flash.
│   │
│   └── scripts/: Các tập lệnh (Python, shell) để tự động hóa các tác vụ (build, release, chuyển đổi tài nguyên).
│
├── sdcard_template/: Cấu trúc thư mục mẫu cho thẻ SD, chứa các cấu hình và dữ liệu người dùng.
│   ├── actions.json: Định nghĩa các hành động tùy chỉnh.
│   ├── config.json: Tệp cấu hình chính trên thẻ SD.
│   └── timetable.json: Dữ liệu lịch biểu.
│
├── UI/: Chứa các tài sản liên quan đến thiết kế giao diện người dùng (hình ảnh, tài liệu).
│   ├── emotion.png: Hình ảnh ví dụ về biểu cảm.
│   └── README.md: Ghi chú về thư mục UI.
│
├── README.md: Tệp README chính của dự án, cung cấp thông tin chung và điểm khởi đầu cho người dùng.
│
└── todo.md: Danh sách các công việc cần làm cho dự án.
```

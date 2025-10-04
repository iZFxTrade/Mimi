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

`./`
├── **.idx/**: Chứa các tệp cấu hình môi trường phát triển (ví dụ: `dev.nix` cho Nix).
│
├── **firmware/**: Thư mục chứa toàn bộ mã nguồn của firmware.
│   ├── **CMakeLists.txt**: Tệp cấu hình CMake chính, điều phối việc biên dịch toàn bộ firmware.
│   ├── **LICENSE**: Tệp giấy phép phần mềm của dự án.
│   ├── **README.md**: Tài liệu tổng quan về thư mục firmware.
│   ├── **sdkconfig.defaults***: Chứa các giá trị cấu hình mặc định cho ESP-IDF.
│   │
│   ├── **docs/**: Chứa tài liệu thiết kế, hình ảnh, sơ đồ kỹ thuật.
│   │
│   ├── **main/**: Thư mục mã nguồn cốt lõi của ứng dụng.
│   │   ├── **CMakeLists.txt**: Cấu hình biên dịch cho các tệp trong thư mục `main`.
│   │   ├── **idf_component.yml**: Khai báo các thành phần phụ thuộc cho ESP-IDF.
│   │   │
│   │   ├── **application.cc/.h**: Lớp ứng dụng chính, quản lý trạng thái và luồng sự kiện của toàn bộ hệ thống.
│   │   ├── **custom_action.cc/.h**: Triển khai logic thực thi các hành động tùy chỉnh (Custom Actions).
│   │   ├── **device_state.h**: Định nghĩa các trạng thái hoạt động của thiết bị (ví dụ: `IDLE`, `LISTENING`).
│   │   ├── **factory_reset.cc/.h**: Logic để thực hiện khôi phục cài đặt gốc.
│   │   ├── **main.cc**: Điểm vào chính của chương trình (hàm `app_main`), nơi khởi tạo và chạy lớp `Application`.
│   │   ├── **mcp_server.cc/.h**: Triển khai "Magic-Control-Protocol" để điều khiển và giao tiếp với thiết bị.
│   │   ├── **ota.cc/.h**: Xử lý cập nhật firmware qua mạng (Over-The-Air).
│   │   ├── **settings.cc/.h**: Quản lý việc đọc/ghi các cài đặt của thiết bị vào bộ nhớ NVS.
│   │   ├── **speech.cc/.h**: Xử lý logic liên quan đến nhận dạng giọng nói và tổng hợp giọng nói.
│   │   ├── **system_info.cc/.h**: Cung cấp thông tin hệ thống (phiên bản fw, bộ nhớ,...).
│   │   │
│   │   ├── **assets/**: Tài nguyên tĩnh (âm thanh, hình ảnh, ngôn ngữ).
│   │   │
│   │   ├── **audio/**: Module quản lý âm thanh.
│   │   │   ├── `audio_input.cc/.h`: Logic thu âm từ microphone.
│   │   │   ├── `audio_output.cc/.h`: Logic phát âm thanh ra loa.
│   │   │   ├── `audio_service.cc/.h`: Dịch vụ chính điều phối hoạt động thu/phát.
│   │   │   ├── `i2s_driver.cc/.h`: Trình điều khiển phần cứng cho giao tiếp I2S với codec.
│   │   │   └── `wake_word.cc/.h`: Logic phát hiện từ khóa đánh thức.
│   │   │
│   │   ├── **boards/**: Cấu hình cho các bo mạch phần cứng.
│   │   │   ├── `common/`: Chứa mã nguồn chung (lớp `Board` cơ sở, `WifiBoard`, `Button`,...).
│   │   │   └── `[tên-bo-mạch]/`: Mỗi bo mạch có thư mục riêng chứa `config.h`, `config.json`, và file `.cc` triển khai logic.
│   │   │
│   │   ├── **display/**: Module quản lý giao diện người dùng trên màn hình.
│   │   │   ├── `display_driver.cc/.h`: Trình điều khiển phần cứng cho màn hình (LCD).
│   │   │   ├── `ui_assistant.cc/.h`: Giao diện màn hình khi trợ lý hoạt động.
│   │   │   ├── `ui_clock.cc/.h`: Giao diện màn hình đồng hồ.
│   │   │   ├── `ui_settings.cc/.h`: Giao diện màn hình cài đặt.
│   │   │   ├── `ui_wifi_config.cc/.h`: Giao diện màn hình cấu hình Wi-Fi.
│   │   │   └── `view_manager.cc/.h`: Quản lý việc chuyển đổi giữa các màn hình (views).
│   │   │
│   │   ├── **led/**: Module điều khiển đèn LED.
│   │   │   └── `led_strip.cc/.h`: Logic điều khiển dải đèn LED (ví dụ: WS2812).
│   │   │
│   │   └── **protocols/**: Triển khai các giao thức giao tiếp mạng.
│   │       ├── `http_client.cc/.h`: Trình khách HTTP để gửi yêu cầu GET/POST.
│   │       ├── `mqtt_client.cc/.h`: Trình khách MQTT để giao tiếp với broker.
│   │       └── `ws_client.cc/.h`: Trình khách WebSocket để giao tiếp hai chiều thời gian thực.
│   │
│   ├── **partitions/**: Các tệp `.csv` định nghĩa bảng phân vùng bộ nhớ flash.
│   │
│   └── **scripts/**: Các tập lệnh Python/shell để tự động hóa tác vụ (build, release, đóng gói tài nguyên).
│
├── **sdcard_template/**: Cấu trúc thư mục mẫu cho thẻ SD.
│   ├── `actions.json`: Định nghĩa các hành động tùy chỉnh.
│   ├── `config.json`: Tệp cấu hình chính trên thẻ SD.
│   └── `timetable.json`: Dữ liệu lịch biểu.
│
├── **UI/**: Chứa các tài sản liên quan đến thiết kế giao diện người dùng.
│   ├── `emotion.png`: Hình ảnh ví dụ.
│   └── `README.md`: Tài liệu về các màn hình và thiết kế UI.
│
├── **PROJECT_BLUEPRINT.md**: (Tệp này) Bản đồ chi tiết của toàn bộ dự án.
├── **README.md**: Tệp giới thiệu chung về dự án.
└── **todo.md**: Danh sách các công việc cần làm cho dự án.

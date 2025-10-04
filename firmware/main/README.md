# Thư mục `main`

Đây là thư mục cốt lõi của toàn bộ firmware, chứa điểm khởi đầu của ứng dụng (`main.cc`) và logic chính điều phối hoạt động của thiết bị. Nó tích hợp tất cả các module con như âm thanh, màn hình, kết nối mạng và quản lý phần cứng dành riêng cho bo mạch.

## Cấu trúc thư mục và Chức năng

```
firmware/main/
│
├── assets/         # Chứa tài nguyên tĩnh (âm thanh, hình ảnh, ngôn ngữ). (Đã có README)
├── audio/          # Quản lý tất cả các chức năng liên quan đến âm thanh (thu, phát, xử lý).
├── boards/         # Cấu hình và mã nguồn dành riêng cho từng bo mạch phần cứng. (Đã có README)
├── display/        # Quản lý giao diện người dùng (UI) trên màn hình.
├── led/            # Điều khiển đèn LED trạng thái.
├── protocols/      # Triển khai các giao thức giao tiếp (MQTT, WebSocket).
│
├── application.cc / .h: Lớp ứng dụng chính, quản lý trạng thái và luồng sự kiện của toàn bộ hệ thống.
├── main.cc:         Điểm khởi đầu của chương trình (hàm `app_main`), nơi khởi tạo và chạy lớp `Application`.
├── settings.cc / .h:  Quản lý việc đọc và ghi các cài đặt của thiết bị vào bộ nhớ NVS (Non-Volatile Storage).
├── mcp_server.cc / .h: Triển khai "Magic-Control-Protocol" (MCP), một giao thức tùy chỉnh để điều khiển và giao tiếp với thiết bị.
├── ota.cc / .h:       Xử lý cập nhật firmware qua mạng (Over-The-Air).
├── system_info.cc / .h: Cung cấp thông tin hệ thống như phiên bản firmware, trạng thái bộ nhớ.
├── device_state.h:  Định nghĩa các trạng thái hoạt động của thiết bị (ví dụ: đang khởi động, đang nghe, đang nói).
├── idf_component.yml: Tệp cấu hình thành phần cho ESP-IDF, khai báo các phụ thuộc.
└── CMakeLists.txt:  Tệp cấu hình xây dựng cho CMake, chỉ định cách biên dịch các tệp nguồn và liên kết các thư viện.
```

## Luồng công việc (Workflow)

1.  **Khởi động (Boot)**:
    *   Sau khi bootloader chạy, hệ điều hành FreeRTOS sẽ gọi hàm `app_main` trong `main.cc`.
    *   `app_main` tạo một đối tượng duy nhất của lớp `Application` từ `application.h`.
    *   Hàm `run()` của đối tượng `Application` được gọi, bắt đầu vòng lặp chính của ứng dụng.

2.  **Khởi tạo (Initialization)**:
    *   Bên trong hàm khởi tạo hoặc hàm `run()` của `Application`, các thành phần cốt lõi được khởi tạo:
        *   **Cài đặt (Settings)**: `Settings::get()` được gọi để tải các cài đặt đã lưu từ NVS.
        *   **Bo mạch (Board)**: Dựa trên cấu hình xây dựng, một đối tượng bo mạch cụ thể (ví dụ: `EspBox3Board`) được tạo. Hàm `init()` của bo mạch này sẽ khởi tạo phần cứng (màn hình, codec âm thanh, nút bấm).
        *   **Module con**: Các module như `AudioService`, `ViewManager` (quản lý màn hình) được khởi tạo và truyền vào đối tượng bo mạch để chúng có thể tương tác với phần cứng.
        *   **Kết nối mạng**: Lớp `Application` khởi tạo Wi-Fi và kết nối đến mạng đã được cấu hình.
        *   **Giao thức**: Các giao thức như MQTT hoặc WebSocket được khởi tạo để kết nối đến máy chủ.

3.  **Vòng lặp chính và Xử lý sự kiện**:
    *   Lớp `Application` hoạt động như một máy trạng thái (state machine), chuyển đổi giữa các trạng thái được định nghĩa trong `device_state.h`.
    *   Các sự kiện từ phần cứng (như nhấn nút), từ máy chủ (qua MQTT/WebSocket), hoặc từ các module nội bộ được xử lý.
    *   Dựa trên sự kiện và trạng thái hiện tại, `Application` sẽ điều phối các hành động, ví dụ:
        *   Nếu phát hiện từ khóa đánh thức (wake word), `Application` sẽ chuyển sang trạng thái "đang nghe" và yêu cầu `AudioService` bắt đầu ghi âm.
        *   Khi nhận được phản hồi từ máy chủ, nó sẽ yêu cầu `AudioService` phát âm thanh và `ViewManager` cập nhật giao diện trên màn hình.
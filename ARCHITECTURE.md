# Tổng quan Kiến trúc - Model Context Protocol (MCP)

Đây là tài liệu kỹ thuật cấp cao mô tả kiến trúc và triết lý đằng sau dự án, với mục tiêu xây dựng một nền tảng trợ lý AI linh hoạt, có khả năng duy trì ngữ cảnh và hỗ trợ đa người dùng.

## 1. Triết lý Cốt lõi: "Tách biệt Ngữ cảnh"

Kiến trúc được xây dựng dựa trên một nguyên tắc cơ bản: tách biệt giữa **ngữ cảnh thiết bị** và **ngữ cảnh người dùng**.

- **Thiết bị (`Device`):** Là một thực thể vật lý (ví dụ: loa thông minh ESP32) hoặc ảo (ví dụ: một bot Telegram). Mỗi thiết bị có một định danh duy nhất (`Device-ID`) và có các cấu hình riêng như tên trợ lý, giọng nói, nhà cung cấp AI, và chức năng (ví dụ: điều khiển các đèn trong phòng khách).
- **Người dùng (`User`):** Là người đang tương tác với thiết bị. Mỗi người dùng có một định danh duy nhất (`User-ID`) và có lịch sử hội thoại riêng với từng thiết bị.

Điều này cho phép server "nhớ" các cuộc trò chuyện trong quá khứ của một người dùng cụ thể trên một thiết bị cụ thể, tạo ra trải nghiệm liền mạch và cá nhân hóa.

## 2. Các Thành phần Chính (Kiến trúc Hiện tại)

- **`DeviceProfile` & `UserProfile`:** Các đối tượng JSON lưu trữ cấu hình thiết bị và lịch sử hội thoại người dùng.
- **`ProfileManager`:** Lớp quản lý việc đọc/ghi các hồ sơ này từ một tệp JSON duy nhất (`device_profiles.json`). **Lưu ý: Cách tiếp cận này sẽ được thay thế trong kiến trúc đa người dùng để tăng hiệu suất và khả năng mở rộng.**

## 3. Lộ trình Nâng cấp: Nền tảng Quản lý Đa người dùng (Self-Hosted & Docker-Ready)

Để phát triển từ một server giao thức thành một nền tảng hoàn chỉnh, kiến trúc sẽ được nâng cấp để có thể tự vận hành, không phụ thuộc vào dịch vụ bên ngoài và dễ dàng đóng gói.

### 3.1. Công nghệ Nền tảng

-   **Xác thực (Authentication):** **JWT (JSON Web Tokens)**. Server sẽ tự cung cấp endpoint đăng ký/đăng nhập và quản lý việc tạo/xác thực token.
-   **Cơ sở dữ liệu (Database):** **SQLite**. Đây là một CSDL quan hệ gọn nhẹ, dựa trên file. Nó không yêu cầu tiến trình riêng, dễ dàng tích hợp và hoàn hảo cho việc đóng gói bằng Docker.
-   **Tương tác CSDL:** Sử dụng thư viện **SQLAlchemy** để tạo và tương tác với các bảng dữ liệu một cách an toàn và hiệu quả.
-   **Backend (MCP-Server):** Server FastAPI sẽ chứa toàn bộ logic xác thực JWT và giao tiếp với CSDL SQLite.
-   **Frontend:** Một ứng dụng web (SPA) sẽ được xây dựng để làm giao diện quản lý.

### 3.2. Cấu trúc Dữ liệu trên SQLite

-   **Bảng `users`:** Chứa thông tin người dùng (`id`, `username`, `hashed_password`, `is_admin`).
-   **Bảng `devices`:** Chứa thông tin về các trợ lý (`id`, `name`, `system_prompt`, ...). Quan trọng nhất, nó sẽ có một trường `owner_id` (foreign key) để trỏ tới `id` của người dùng trong bảng `users`.

Kiến trúc này đảm bảo dữ liệu được phân quyền rõ ràng: người dùng chỉ có thể truy cập các thiết bị mà họ sở hữu.

## 4. Luồng Giao tiếp & Dữ liệu (Kiến trúc Hiện tại)

Luồng giao tiếp được thiết kế để linh hoạt và có khả năng mở rộng mà không phá vỡ các client hiện có.

### 4.1. Giai đoạn Kích hoạt & Đồng bộ (HTTP POST)

- **Endpoint:** `POST /api/ota/`
- **Mục đích:** Đây là "cái bắt tay" đầu tiên. Client gửi thông tin cơ bản của nó lên server.
- **Chiến lược Mở rộng:** Client **có thể gửi kèm** các khối cấu hình bổ sung dưới dạng các trường JSON **tùy chọn** (ví dụ: `"telegram": {...}`). Server được lập trình để xử lý sự hiện diện hoặc vắng mặt của các trường này.

### 4.2. Giao tiếp Giọng nói (WebSocket)

- **Endpoint:** `GET /api/v1/voice_chat`
- **Mục đích:** Kênh giao tiếp hai chiều cho việc truyền-nhận âm thanh thời gian thực.
- **Handshake:** Client gửi một message `hello` (JSON) chứa `device_id` và `user_id` (tùy chọn).

### 4.3. Giao tiếp Văn bản (HTTP POST)

- **Endpoint:** `POST /api/v1/chat`
- **Mục đích:** Cung cấp một API thống nhất cho các client dựa trên văn bản (Web UI, app di động, script).

### 4.4. Giao tiếp qua Bot (ví dụ: Telegram)

- **Cơ chế:** `BotManager` trên server sẽ đọc cấu hình `telegram` trong các `DeviceProfile`.
- **Luồng dữ liệu:** Bot nhận tin nhắn từ người dùng Telegram, lấy `chat_id` của họ làm `user_id`, và chuyển tiếp yêu cầu đến lõi AI của server.

## 5. Sơ đồ Luồng Dữ liệu Tổng quan (Kiến trúc Hiện tại)

```
+-----------------+     +--------------------------+     +-----------------------+
| Client (ESP32,  |     |   MCP-Server (FastAPI)   |     |   Các Dịch vụ AI      |
| Web, Telegram)  |     |                          |     | (OpenAI, Google, ...) |
+-----------------+     +--------------------------+     +-----------------------+
        |                         |                                |
        |---- 1. Request --------->|                                |
        | (Voice/Text/Bot)        |                                |
        | (device_id, user_id)    |                                |
        |                         |                                |
        |                         |--- 2. Lấy Profile (ProfileManager) --> (device_profiles.json)
        |                         |                                |
        |                         |--- 3. Chọn AI Provider & Xây dựng Prompt (với ngữ cảnh) 
        |                         |                                |
        |                         |---------------- 4. Gửi Yêu cầu AI ------------->|
        |                         |                                |
        |                         |<--------------- 5. Nhận Phản hồi AI --------------|
        |                         |                                |
        |                         |--- 6. Cập nhật Lịch sử Hội thoại (ProfileManager) -> (device_profiles.json)
        |                         |                                |
        |<--- 7. Response --------|                                |
        | (Audio/Text)            |                                |

```

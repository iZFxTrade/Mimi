# Máy chủ Giao thức Ngữ cảnh Mô hình (Model Context Protocol Server)

Thư mục này chứa mã nguồn và tài liệu để triển khai máy chủ trung gian cho các trợ lý AI.

## 🎯 Mục đích

Máy chủ này đóng vai trò là "bộ não" backend, có các nhiệm vụ chính:

1.  **Cung cấp & Định danh (Provisioning & Identity):** Khi một thiết bị IoT khởi động, nó sẽ kết nối đến máy chủ này để:
    *   Kiểm tra phiên bản firmware mới (OTA).
    *   Lấy thông tin cấu hình kết nối cho các dịch vụ cốt lõi (MQTT, WebSocket).
    *   Đăng ký thông tin định danh của thiết bị (`Device-ID`) và tạo một "Hồ sơ Thiết bị" (`DeviceProfile`) để lưu trữ mọi cấu hình liên quan.

2.  **Trung gian Giao tiếp AI (Kiến trúc Mở):**
    *   Nhận luồng âm thanh (định dạng **Opus**) từ thiết bị và xử lý qua chuỗi STT -> LLM -> TTS.
    *   Hỗ trợ kiến trúc AI linh hoạt, cho phép người dùng tự do lựa chọn nhà cung cấp dịch vụ (OpenAI, Google Gemini, VietTTS, Ollama, v.v.) cho từng thành phần trong hồ sơ của thiết bị.

3.  **Quản lý Ngữ cảnh Đa tầng (Multi-Layered Context Management):**
    *   **Ngữ cảnh Người dùng:** Máy chủ nhận dạng **từng người dùng** (ví dụ: qua ID Telegram hoặc `user_id` do thiết bị cung cấp) và lưu trữ lịch sử hội thoại riêng cho mỗi người trong `UserProfile`. Trợ lý có thể "nhớ" các cuộc trò chuyện trong quá khứ với từng thành viên.
    *   **Ngữ cảnh Bền bỉ & Độc lập:** Lịch sử hội thoại được lưu trữ ở một định dạng trung gian (JSON). Điều này có nghĩa là khi người dùng thay đổi nhà cung cấp LLM (ví dụ: từ OpenAI sang Google Gemini), **toàn bộ ngữ cảnh trò chuyện vẫn được giữ nguyên** và sẽ được cung cấp cho mô hình mới. Tính năng này đảm bảo "trí nhớ" của trợ lý không bị mất đi khi "bộ não" được thay đổi.

4.  **Cầu nối Giao tiếp Đa kênh (Multi-channel Bridge):**
    *   **Trợ lý Server Tích hợp (Chat API):** Cung cấp một API endpoint để người dùng có thể chat trực tiếp với một trợ lý ảo "sống" ngay trên server. Điều này cho phép thử nghiệm nhanh các mô hình AI, ngữ cảnh và tính năng mà không cần thiết bị vật lý.
    *   **Tích hợp Telegram Bot:** Cho phép người dùng gửi lệnh, đặt câu hỏi (tương tác với chuỗi AI được cá nhân hóa), và nhận cảnh báo/trạng thái từ thiết bị thông qua một bot Telegram chuyên dụng.
    *   **Giao tiếp Giọng nói:** Xử lý luồng âm thanh hai chiều qua WebSocket cho các thiết bị trợ lý vật lý.

5.  **Tầm nhìn Tương lai - Nền tảng Nhà Thông minh Toàn diện:**
    *   **Giao diện Quản lý Web:** Xây dựng một ứng dụng web cho phép người dùng đăng nhập, quản lý các "Trợ lý" của mình, và **chat trực tiếp với bất kỳ trợ lý nào** ngay trên giao diện web đó.
    *   **Điều khiển Nhà thông minh:** Mở rộng giao diện web để người dùng có thể thiết lập sơ đồ nhà (phòng, khu vực) và đăng ký các thiết bị IoT (đèn, cảm biến, công tắc) vào từng phòng.
    *   **Tích hợp MQTT hai chiều:** Triển khai một cầu nối MQTT mạnh mẽ, cho phép Giao diện Web và Trợ lý AI có thể điều khiển các thiết bị IoT và nhận trạng thái của chúng theo thời gian thực.
    *   **Hỗ trợ Đa phương thức (Multimodal):** Nâng cấp để xử lý đầu vào là hình ảnh, video, cho phép các tính năng như nhận diện khuôn mặt, giám sát an ninh.

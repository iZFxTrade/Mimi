# Máy chủ Trung gian MiMi (MiMi Control Protocol Server)

Thư mục này chứa mã nguồn và tài liệu để triển khai máy chủ trung gian cho trợ lý AI MiMi.

## 🎯 Mục đích

Máy chủ này đóng vai trò là "bộ não" backend, có các nhiệm vụ chính:

1.  **Cung cấp Cấu hình (OTA & Provisioning):** Khi thiết bị ESP32 khởi động, nó sẽ kết nối đến máy chủ này để:
    *   Kiểm tra phiên bản firmware mới (OTA).
    *   Lấy thông tin cấu hình kết nối cho dịch vụ AI (MQTT hoặc WebSocket).

2.  **Trung gian Giao tiếp với AI:**
    *   Nhận âm thanh giọng nói từ thiết bị ESP32.
    *   Gửi âm thanh đến dịch vụ Speech-to-Text (STT) để chuyển thành văn bản.
    *   Gửi văn bản đến các mô hình ngôn ngữ lớn (LLM) như OpenAI, Google Gemini, v.v.
    *   Nhận phản hồi văn bản từ LLM.
    *   Sử dụng dịch vụ Text-to-Speech (TTS) để chuyển phản hồi thành âm thanh.
    *   Gửi lại cả âm thanh và văn bản cho thiết bị ESP32.

3.  **Quản lý Logic Phụ trợ:**
    *   Xử lý các hành động tùy chỉnh (Custom Actions).
    *   Tích hợp với các dịch vụ bên thứ ba (Telegram, Home Assistant, n8n...).
    *   Lưu trữ dữ liệu người dùng và tiến trình học tập.

## 📜 Đặc tả API (Dựa trên dự án gốc)

Để xây dựng một máy chủ tương thích, bạn cần tuân thủ đặc tả kỹ thuật được cung cấp bởi dự án gốc `xiaozhi-esp32`.

**Liên kết đến tài liệu đặc tả:** **[Feishu Wiki](https://ccnphfhqs21z.feishu.cn/wiki/FjW6wZmisimNBBkov6OcmfvknVd)**

Tài liệu này mô tả chi tiết:
*   Các endpoint mà máy chủ cần phải có.
*   Cấu trúc của các gói tin JSON được gửi và nhận.
*   Luồng xác thực và kích hoạt thiết bị.

## 🚀 Lộ trình Phát triển Phía Máy chủ (Server-side Roadmap)

-   [ ] **Phát triển Máy chủ cơ bản:** Xây dựng một máy chủ tuân thủ đặc tả trên, sử dụng các công nghệ phổ biến như Node.js/Express, Python/FastAPI, hoặc Golang.
-   [ ] **Tích hợp đa AI:** Cho phép dễ dàng chuyển đổi giữa các nhà cung cấp LLM khác nhau (OpenAI, Gemini, Azure AI).
-   [ ] **Container hóa (Docker):** Đóng gói máy chủ vào một Docker image để người dùng có thể dễ dàng tự triển khai (self-host).
-   [ ] **Cung cấp bản dựng công khai:** Triển khai một phiên bản máy chủ `ota.mimi.ai` công khai làm máy chủ mặc định cho các thiết bị MiMi.
-   [ ] **Giao diện Quản lý:** Xây dựng một trang web đơn giản để quản lý các thiết bị đã kết nối và cấu hình hệ thống.

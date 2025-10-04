### Kế hoạch Phát triển Máy chủ Điều khiển MiMi (MCP-Server)

Đây là danh sách các công việc cần thực hiện để xây dựng và hoàn thiện máy chủ.

---

-   [x] **Phần A: Nâng cao Logic Cập nhật Firmware (OTA)**
    -   [x] **Bước 1:** Giới thiệu Cập nhật Bắt buộc.
    -   [x] **Bước 2:** Xử lý Tùy chọn Từ chối Tự động Cập nhật của Client.

-   [x] **Phần B: Hiện thực hóa Logic Cấp phát Cấu hình Động**
    -   [x] **Bước 1:** Tạo `server_config.json`.
    -   [x] **Bước 2:** Cập nhật `main.py` để đọc cấu hình.
    -   [x] **Bước 3:** Cấp phát cấu hình động trong `handle_ota_request`.

-   [x] **Phần C (Refactored): Xây dựng Lõi Giao tiếp AI Module hóa**
    -   **Mục tiêu:** Tái cấu trúc lõi AI để trở nên linh hoạt, tuân thủ giao thức và dễ mở rộng.
    -   [x] **Bước 1: Phân tích Giao thức Firmware:** Đọc tài liệu để hiểu đúng luồng giao tiếp và định dạng dữ liệu (Opus).
    -   [x] **Bước 2: Thiết kế Kiến trúc Module hóa:** Tạo các lớp cơ sở trừu tượng (`STTService`, `LLMService`, `TTSService`) trong thư mục `ai_services`.
    -   [x] **Bước 3: Hiện thực hóa Dịch vụ Cụ thể (OpenAI):** Tạo các lớp triển khai cho OpenAI, đóng gói logic API vào các module riêng.
    -   [x] **Bước 4: Cập nhật Cấu hình:** Sửa đổi `server_config.json` để hỗ trợ lựa chọn nhà cung cấp dịch vụ.
    -   [x] **Bước 5: Tái cấu trúc `main.py`:** Viết lại `main.py` để sử dụng kiến trúc factory, tuân thủ giao thức WebSocket và xử lý đúng định dạng âm thanh.

-   [ ] **Phần D: Mở rộng Dịch vụ AI**
    -   **Mục tiêu:** Tích hợp các nhà cung cấp dịch vụ thay thế và miễn phí.
    -   [ ] **Bước 1: Tích hợp TTS Tiếng Việt Miễn phí:** Nghiên cứu và tích hợp `vietTTS` hoặc một giải pháp tương tự làm một tùy chọn TTS.
    -   [ ] **Bước 2: Tích hợp LLM Miễn phí/Tự Host:** Thêm hỗ trợ cho các endpoint tương thích OpenAI (ví dụ: LM Studio, OpenRouter).

-   [ ] **Phần E: Đóng gói và Triển khai**
    -   **Mục tiêu:** Chuẩn bị để triển khai máy chủ một cách dễ dàng.
    -   [x] **Bước 1:** Hoàn thiện và tạo tệp `requirements.txt`.
    -   [ ] **Bước 2:** Viết `Dockerfile` để container hóa ứng dụng.
    -   [ ] **Bước 3:** Cập nhật `README.md` với hướng dẫn Docker chi tiết.

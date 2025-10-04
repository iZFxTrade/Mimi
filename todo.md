# ✅ Danh sách công việc dự án MiMi

Đây là danh sách các công việc cần làm để hoàn thành dự án, dựa trên `Roadmap ToDo` trong file README.md. Tôi sẽ thực hiện tuần tự, chi tiết và đánh dấu khi hoàn thành.

## Giai đoạn 0: Kiểm tra và Phân tích Hiện trạng

-   [x] **Phân tích cấu trúc file và tài liệu**
-   [x] **Kiểm tra mã nguồn driver phần cứng**
-   [x] **Kiểm tra luồng hoạt động của ứng dụng**

**==> Giai đoạn 0 hoàn tất. Đã có đủ thông tin để bắt đầu Giai đoạn 1.**

---

## Giai đoạn 1: Xây dựng Máy chủ MCP (MCP-Server)

-   [x] **Khởi tạo cấu trúc dự án máy chủ:** Tạo thư mục `MCP-Server` với `main.py` và `requirements.txt`.
-   [x] **Hiện thực hóa API và cấu trúc dữ liệu:** Xây dựng endpoint `/api/ota/` với Pydantic models và logic giả lập trong `main.py`.
-   [x] **Cấu hình môi trường phát triển Python:** Chỉnh sửa tệp `.idx/dev.nix` để cài đặt Python, Pip và tự động hóa việc cài đặt thư viện cũng như chạy máy chủ.
-   [ ] **Tải lại môi trường và khởi chạy máy chủ:** *BẠN CẦN TẢI LẠI MÔI TRƯỜNG NGAY BÂY GIỜ.* Sau khi tải lại, tôi sẽ xác minh môi trường và khởi chạy máy chủ FastAPI bằng trình xem trước (Preview).
-   [ ] **Kiểm thử API Endpoint `/api/ota/`:** Gửi yêu cầu mẫu đến máy chủ đang chạy để xác nhận nó hoạt động đúng như logic giả lập.
-   [ ] **Hiện thực hóa logic nghiệp vụ thực tế:** Thay thế logic giả bằng logic thực, bao gồm việc truy vấn cơ sở dữ liệu để tìm phiên bản firmware mới nhất.

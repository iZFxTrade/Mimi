# Giao diện Quản trị MCP-Server (Admin Dashboard)

Đây là một giao diện Single-Page Application (SPA) được xây dựng bằng HTML, CSS (Bootstrap) và JavaScript thuần.

## Mục tiêu

Cung cấp một giao diện web trực quan cho phép quản trị viên (Admin) thực hiện các tác vụ sau:

- **Quản lý Toàn diện (CRUD):** Thêm, Sửa, Xóa và Xem tất cả các tài nguyên của hệ thống, bao gồm Users, Assistants, Homes, Devices, AI Models, v.v.
- **Tương tác & Thử nghiệm:** Cung cấp một khung chat tích hợp để có thể tương tác trực tiếp với các trợ lý AI đã được cấu hình, giúp cho việc thử nghiệm và gỡ lỗi trở nên nhanh chóng.

## Tình trạng hiện tại (2025-10-04)

- **Layout mong muốn:** Một giao diện 3 cột:
    1.  **Sidebar (trái):** Menu điều hướng chính.
    2.  **Main Content (giữa):** Hiển thị danh sách và form cho các mục quản lý.
    3.  **Chat Panel (phải):** Khung chat lớn, cố định, có thể thu gọn, để tương tác với trợ lý.

- **Tiến độ:**
    - Backend cho việc quản lý User đã hoàn tất.
    - Frontend (`admin.html`) đang trong quá trình xây dựng lại để đáp ứng đúng layout 3 cột và hiển thị đầy đủ dữ liệu (bao gồm cả dữ liệu demo).
    - Phiên bản hiện tại đang gặp nhiều lỗi và chưa hoàn thiện giao diện như mong muốn.

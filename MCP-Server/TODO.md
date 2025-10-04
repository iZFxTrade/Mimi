# MCP-Server TODO List

## Giai đoạn 1: Nền tảng & Hiển thị Dữ liệu

- [x] Thiết lập CSDL với SQLAlchemy.
- [x] Định nghĩa models và schemas Pydantic.
- [x] `database_init.py`: Tạo dữ liệu demo (mock data) cho tất cả các bảng.
- [x] API Authentication (`/api/auth/token`).
- [x] API bảo mật: Yêu cầu token, phân quyền Admin.
- [x] API endpoints (GET): Xây dựng các endpoint để đọc toàn bộ dữ liệu từ CSDL.
- [x] Cấu hình CORS Middleware để cho phép frontend kết nối.

## Giai đoạn 2: Hoàn thiện CRUD

- **User Management**
    - [x] Backend: Hoàn thiện `POST`, `PUT`, `DELETE` cho `/api/users/`.
    - [x] Backend: Hoàn thiện logic `create_user`, `update_user`, `delete_user` trong `crud.py`.
    - [ ] Frontend: Hoàn thiện giao diện `admin.html` cho User CRUD (hiện đang lỗi).

- **Assistant Management**
    - [ ] Backend: Xây dựng `POST`, `PUT`, `DELETE` cho `/api/assistants/`.
    - [ ] Backend: Viết logic `create/update/delete` trong `crud.py`.
    - [ ] Frontend: Xây dựng giao diện cho Assistant CRUD.

- **Smart Home Management (Tương tự)**
    - [ ] Backend & Frontend CRUD cho Homes, Rooms, Devices, Scenes.

- **AI Capabilities Management (Tương tự)**
    - [ ] Backend & Frontend CRUD cho AIModels, Tools.

## Giai đoạn 3: Logic nghiệp vụ cốt lõi

- [ ] Xây dựng API endpoint `/api/chat` để xử lý logic trò chuyện với trợ lý.
- [ ] Tích hợp với các dịch vụ AI bên ngoài (ví dụ: OpenAI, Gemini).
- [ ] ...

---
*Cập nhật lần cuối: 2025-10-04*

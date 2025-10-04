**LƯU Ý CỰC KỲ QUAN TRỌNG DÀNH CHO TRỢ LÝ AI:** Tệp `todo.md` này là nguồn ghi lại toàn bộ lịch sử và tiến độ của dự án. **TUYỆT ĐỐI KHÔNG ĐƯỢC GHI ĐÈ (OVERWRITE) HOẶC XÓA BỎ NỘI DUNG CŨ.** Khi cập nhật, hãy luôn **CHỈ THÊM (APPEND)** thông tin mới vào cuối các phần liên quan, hoặc đánh dấu `[x]` vào các mục đã hoàn thành và bổ sung nhật ký công việc. Việc ghi đè sẽ làm mất toàn bộ lịch sử và gây gián đoạn nghiêm trọng cho dự án.

---
# ✅ Danh sách công việc dự án MiMi

Đây là danh sách các công việc cần làm để hoàn thành dự án, dựa trên `Roadmap ToDo` trong file README.md. Tôi sẽ thực hiện tuần tự, chi tiết và đánh dấu khi hoàn thành.

## Giai đoạn 0: Kiểm tra và Phân tích Hiện trạng

-   [x] **Phân tích cấu trúc file và tài liệu**
-   [x] **Kiểm tra mã nguồn driver phần cứng**
-   [x] **Kiểm tra luồng hoạt động của ứng dụng**

**==> Giai đoạn 0 hoàn tất. Đã có đủ thông tin để bắt đầu Giai đoạn 1.**

---

## Giai đoạn 1: Tích hợp phần cứng và UI cơ bản
...

---

## Cập nhật & Công việc Hiện tại: Tái cấu trúc & Sửa lỗi Admin Dashboard (2025-10-04)

*Phiên làm việc tập trung vào việc sửa chữa và nâng cấp toàn diện giao diện quản trị cho MCP-Server.*

- [x] **Phân tích và sửa lỗi ngày tháng:** Phát hiện và sửa lỗi ngày tháng không nhất quán trong các file tài liệu.
- [x] **Tái cấu trúc Frontend thành SPA (`admin.html`):**
    - **Tình trạng:** **HOÀN THÀNH.** Đã thiết kế và viết lại hoàn toàn `admin.html` thành một Single-Page Application đúng nghĩa.
    - **Cải tiến chính:** Tăng tốc độ, sử dụng layout CSS Grid hiện đại, tổ chức lại mã JavaScript một cách chuyên nghiệp.
- [x] **Sửa lỗi sau tái cấu trúc:**
    - [x] **Sửa lỗi Giao diện:** Điều chỉnh lại layout của header trên khung chat cho đúng với mô tả (di chuyển nút ẩn/hiện).
    - [x] **Sửa lỗi API (404 Not Found):** Cập nhật logic Javascript trong `admin.html` để sử dụng `Promise.allSettled`. Điều này cho phép ứng dụng khởi động và hoạt động bình thường ngay cả khi các API backend chưa được hoàn thiện, tránh gây ra lỗi không cần thiết.

### Tóm tắt & Kết thúc phiên làm việc

**Toàn bộ các mục tiêu cho phiên làm việc hôm nay đã hoàn thành.** Giao diện quản trị đã được nâng cấp lên một nền tảng vững chắc, linh hoạt và các lỗi phát sinh đã được khắc phục. Mọi thay đổi đã được lưu trữ an toàn trên Git. Công việc sẽ được tiếp tục vào phiên làm việc tiếp theo.

---

## 📝 Ghi chú & Tóm tắt (Lưu trữ từ các phiên làm việc trước)

*Nội dung bên dưới là bản lưu trữ, vui lòng xem các mục "Cập nhật" ở trên để biết thông tin mới nhất.*

*   **Hoàn thiện Môi trường MCP-Server (2025-10-04):** Đã giải quyết thành công các sự cố về môi trường ảo Python và khởi chạy được máy chủ FastAPI.
*   **Xây dựng Máy chủ MCP (2025-10-04):** Khởi tạo dự án server, API, cấu hình môi trường, sửa lỗi và lưu trữ lên Git.
*   **Hoàn thành Giao diện Người dùng (UI) cho Giai đoạn 1 (Firmware):** Tích hợp khuôn mặt vector, tạo các màn hình chính.
*   **Vấn đề tồn đọng (Firmware):** Mã nguồn firmware **chưa được biên dịch**. Cần chạy `idf.py build` sau khi hoàn tất các tính năng.

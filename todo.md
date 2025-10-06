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

-   [x] **1.1. Tích hợp `mimi-cyd` vào hệ thống build:**
    -   [x] **1.1.1.** Chỉnh sửa file `firmware/main/Kconfig.projbuild` để thêm lựa chọn `BOARD_TYPE_MIMI_CYD`.
-   [x] **1.2. Hoàn thiện lớp Board `mimi-cyd`:**
    -   [x] Implement lớp `MimiCydBoard` và các phương thức cần thiết.
-   [x] **1.3. Xây dựng bộ giao diện người dùng (UI):**
    -   [x] **1.3.1. Màn hình Biểu cảm Trợ lý (Assistant Face):** Giao diện tương tác chính, hiển thị biểu cảm và cho phép tương tác chạm.
    -   [x] **1.3.2. Màn hình Trò chuyện (Chat):** Hiển thị lịch sử hội thoại giữa người dùng và AI.
    -   [x] **1.3.3. Màn hình Tổng quan (Dashboard):** Tích hợp đồng hồ, lịch/thời khóa biểu và thời tiết.
    -   [ ] **1.3.4. Màn hình Gia sư (Learning Tutor):** Giao diện dành riêng cho việc học tập.
    -   [x] **1.3.5. Màn hình Báo cáo & Thống kê (Reports & Stats):** Hiển thị tiến độ, kết quả học tập và các số liệu thống kê.
    -   [ ] **1.3.6. Màn hình Nhà thông minh (Smart Home):** Giao diện điều khiển các thiết bị smarthome.
    -   [x] **1.3.7. Màn hình Media Player:** Giao diện điều khiển nhạc/podcast.
    -   [ ] **1.3.8. Màn hình Cài đặt (Settings):** Cấu hình hệ thống và các kết nối.
    -   [x] **1.3.9. Màn hình Tính năng Mở rộng (Extensions):** Giao diện quản lý các hành động tùy chỉnh.

---

## Giai đoạn 2 – Thông minh & Kết nối

-   [ ] **2.1. Tích hợp AI Backend:**
    -   [ ] Kết nối ASR/TTS.
-   [ ] **2.2. Cá nhân hóa người dùng:**
    -   [ ] Xây dựng cấu trúc profile và lưu tiến trình học trên thẻ SD.
-   [ ] **2.3. Tích hợp Telegram (Cốt lõi):**
    -   [ ] Xây dựng Module Telegram để gửi cảnh báo và nhận lệnh.
-   [ ] **2.4. Tích hợp Smarthome:**
    -   [ ] Thiết lập kết nối MQTT tới Home Assistant.

---

## Giai đoạn 3 – Nền tảng Mở rộng

-   [ ] **3.1. Xây dựng Hệ thống Mở rộng (Custom Actions):**
    -   [ ] **3.1.1. Thiết kế Cấu trúc Dữ liệu:**
        -   [ ] Định nghĩa cấu trúc file `actions.json` trên thẻ SD để lưu các hành động tùy chỉnh (tên lệnh, phương thức, URL, mẫu body).
    -   [ ] **3.1.2. Giao diện Người dùng (UI):**
        -   [ ] Tạo màn hình "Cài đặt" -> "Hành động tùy chỉnh".
        -   [ ] UI để thêm/sửa/xóa các hành động (nhập tên lệnh, URL, v.v.).
    -   [ ] **3.1.3. Service Quản lý Hành động:**
        -   [ ] Viết lớp `ActionService` để đọc/ghi file `actions.json`.
        -   [ ] Cung cấp phương thức để tìm kiếm một hành động dựa trên lệnh thoại.
    -   [ ] **3.1.4. Tích hợp vào Luồng AI:**
        -   [ ] Sửa đổi luồng xử lý sau khi nhận diện giọng nói (ASR).
        -   [ ] Ưu tiên kiểm tra xem lệnh thoại có khớp với một hành động tùy chỉnh nào không.
        -   [ ] Nếu có, thực hiện gọi HTTP request theo cấu hình và xử lý kết quả trả về (đọc to bằng TTS).

-   [ ] **3.2. Hoàn thiện Robot mở rộng (ESP32-CAM):**
    -   [ ] Tích hợp sâu hơn với hệ thống cảnh báo và hành động tùy chỉnh (ví dụ: hành động "chụp ảnh" sẽ kích hoạt ESP32-CAM và gửi ảnh qua Telegram).

---

## 📝 Ghi chú & Tóm tắt (Lưu trữ từ phiên làm việc trước)

### Tóm tắt công việc đã làm:

*   **Hoàn thành Giao diện Người dùng (UI) cho Giai đoạn 1:**
    *   Tích hợp thành công thư viện vẽ khuôn mặt vector `emotion_custom.c` vào `AssistantFaceView`, thay thế hoàn toàn giao diện cũ.
    *   Khuôn mặt trợ lý giờ đây có thể biểu cảm (`happy`, `sad`, `thinking`...) và phản hồi lại các tương tác chạm (xoa đầu, chọc mũi).
    *   Tạo và triển khai mã nguồn cho các màn hình giao diện chính: `HomeView` (Dashboard), `ReportsView`, `MediaView`, `ExtensionsView`, và `ChatView`.

### Vấn đề tồn đọng & Việc cần làm tiếp theo:

*   **[QUAN TRỌNG] Chưa Biên dịch (Build) Dự án:** Toàn bộ mã nguồn mới được viết và tích hợp nhưng **chưa được biên dịch và kiểm tra**. Đây là ưu tiên hàng đầu cho ngày làm việc tiếp theo để phát hiện và sửa các lỗi cú pháp, lỗi liên kết (linker errors) hoặc các vấn đề tương thích khác. Cần chạy lệnh `idf.py build` để bắt đầu.

---

## Cập nhật & Công việc Hiện tại: Xây dựng Máy chủ MCP (Bắt đầu: 2025-10-04 07:50:53 UTC)

*Đây là nhật ký các công việc liên quan đến việc xây dựng máy chủ backend cho dự án.*

- [x] **Khởi tạo cấu trúc dự án:** Tạo thư mục `MCP-Server` với các tệp `main.py`, `requirements.txt`, và tài liệu API.
- [x] **Hiện thực hóa API OTA (Bản nháp):** Xây dựng endpoint `POST /api/ota/` với Pydantic models và logic giả lập trong `main.py`.
- [x] **Cấu hình Môi trường Python:** Chỉnh sửa tệp `.idx/dev.nix` để thêm Python 3.11, Pip, extension `ms-python.python`, và cấu hình tự động cài đặt, chạy thử máy chủ.
- [x] **Lưu trạng thái vào Git:** Thêm, commit (`f19c6ee`) và push tất cả các thay đổi lên kho lưu trữ từ xa để đảm bảo an toàn.
- [x] **Sửa lỗi Cấu hình Môi trường (lần 1):** Phát hiện và sửa lỗi cú pháp trong tệp `.idx/dev.nix` sau khi môi trường không khởi động được. Cấu hình `previews` đã được điều chỉnh lại cho chính xác.
- [x] **Sửa lỗi Thiếu Thư viện Python (lần 2):**
    - **Vấn đề:** Lệnh `python3 -m uvicorn MCP-Server.main:app` thất bại với lỗi `No module named uvicorn`.
    - **Nguyên nhân:** File `.idx/dev.nix` chỉ cài đặt Python mà không cài đặt các thư viện trong `requirements.txt`.
    - **Giải pháp:** Cập nhật `.idx/dev.nix` để tự động tạo môi trường ảo (`.venv`) và chạy `pip install -r MCP-Server/requirements.txt` khi khởi động hoặc khi file thay đổi. Cũng đã cấu hình sẵn một preview để chạy server.
- [x] **Tải lại môi trường & Xác minh:** **(ĐÃ HOÀN THÀNH TRONG PHIÊN LÀM VIỆC MỚI)**
- [x] **Khởi chạy và kiểm thử máy chủ:** **(ĐÃ HOÀN THÀNH TRONG PHIÊN LÀM VIỆC MỚI)**
- [ ] **Kiểm thử API Endpoint `/api/ota/`:** Gửi một yêu cầu `curl` hoặc sử dụng một công cụ khác để kiểm tra phản hồi từ logic giả lập.

---

## Cập nhật & Công việc Hiện tại: Hoàn thiện Môi trường MCP-Server (Bắt đầu: 2025-10-04 09:30:00 UTC)

*Tiếp nối công việc từ phiên trước, tập trung vào việc khởi chạy và ổn định máy chủ MCP.*

- [x] **Xác minh sự cố môi trường:** Chạy lệnh `python3 -m uvicorn ...` và xác nhận lỗi `No module named uvicorn` vẫn tồn tại, cho thấy quá trình tự động tạo môi trường ảo đã không thành công.
- [x] **Giải quyết sự cố môi trường (Thủ công):**
    - **Bước 1:** Tạo thủ công môi trường ảo (`python3 -m venv MCP-Server/.venv`).
    - **Bước 2:** Cài đặt các thư viện cần thiết vào môi trường ảo (`MCP-Server/.venv/bin/pip install -r MCP-Server/requirements.txt`).
- [x] **Khởi chạy và kiểm thử máy chủ:** Khởi chạy thành công máy chủ FastAPI bằng cách sử dụng trình thông dịch Python từ môi trường ảo (`MCP-Server/.venv/bin/python -m uvicorn ...`). **==> Máy chủ đã hoạt động!**
- [x] **Tổ chức lại Quản lý Công việc cho MCP-Server:**
    - **Bước 1:** Tạo một tệp `todo.md` chuyên dụng tại `MCP-Server/todo.md` để theo dõi các công việc, mục tiêu và sự cố riêng của máy chủ.
    - **Bước 2:** Cập nhật tệp `MCP-Server/README.md` để thêm liên kết đến tệp `todo.md` mới.
- [ ] **Công việc tiếp theo (Theo `MCP-Server/todo.md`):** Kiểm thử API Endpoint `/api/ota/` bằng `curl`.

---

## LƯU Ý QUAN TRỌNG VỀ ĐỊNH HƯỚNG DỰ ÁN

**Mục tiêu hiện tại:** Tập trung 100% vào việc hoàn thiện mã nguồn cho các tính năng đã được vạch ra trong danh sách công việc (ToDo list).

**Quy trình làm việc:**
*   **KHÔNG cài đặt** bất kỳ trình biên dịch, toolchain (như ESP-IDF), hoặc các công cụ phụ trợ nào trong giai đoạn này.
*   Mọi nỗ lực sẽ tập trung vào việc viết, chỉnh sửa và hoàn thiện các tệp mã nguồn (`.cc`, `.h`, `.py`, v.v.).
*   Giai đoạn **biên dịch (build), gỡ lỗi (debug) và nạp firmware (flash)** sẽ chỉ được bắt đầu sau khi tất cả các mục trong `todo.md` được đánh dấu là hoàn thành.

Lý do: Để đảm bảo luồng phát triển được tập trung, tránh phát sinh các vấn.đề về môi trường và công cụ khi các tính năng cốt lõi chưa hoàn thiện.

---

## Cập nhật & Công việc Hiện tại: Xây dựng Admin Dashboard (2025-10-04)

*Tập trung vào việc xây dựng giao diện quản trị cho MCP-Server.*

- [x] **Backend - Database:**
    - [x] Cấu trúc CSDL (`models.py`, `schemas.py`).
    - [x] Tạo dữ liệu demo ban đầu (`database_init.py`).
    - [x] Hoàn thiện CRUD backend cho Users (`crud.py`, `main.py`).
- [x] **Backend - Connectivity:**
    - [x] Kích hoạt `CORSMiddleware` trong `main.py` để cho phép kết nối từ frontend.
- [x] **Frontend - Admin Dashboard (`admin.html`):**
    - **Tình trạng:** Đã xây dựng lại.
    - **Công việc đã làm:** Thiết kế lại hoàn toàn `admin.html` để có layout 3 cột và logic SPA.
---

## Cập nhật & Công việc Hiện tại: Tái cấu trúc & Sửa lỗi Admin Dashboard (2025-10-04, cuối ngày)

*Phiên làm việc tập trung vào việc sửa chữa và nâng cấp toàn diện giao diện quản trị cho MCP-Server.*

- [x] **Sửa lỗi nghiêm trọng trong quản lý `todo.md`:** Phục hồi lại file `todo.md` từ lịch sử Git sau khi vô tình ghi đè.
- [x] **Tái cấu trúc Frontend thành SPA (`admin.html`):**
    - **Tình trạng:** **HOÀN THÀNH.** Đã thiết kế và viết lại hoàn toàn `admin.html` thành một Single-Page Application đúng nghĩa, thay thế cho kiến trúc cũ.
- [x] **Sửa lỗi sau tái cấu trúc:**
    - [x] **Sửa lỗi Giao diện:** Điều chỉnh lại layout của header trên khung chat cho đúng với mô tả (di chuyển nút ẩn/hiện vào trong header).
    - [x] **Sửa lỗi API (404 Not Found):** Cập nhật logic Javascript trong `admin.html` để sử dụng `Promise.allSettled`, giúp ứng dụng khởi động mượt mà ngay cả khi các API backend chưa được hoàn thiện.

### Tóm tắt & Kết thúc phiên làm việc

**Toàn bộ các mục tiêu cho phiên làm việc hôm nay đã hoàn thành.** Giao diện quản trị đã được nâng cấp lên một nền tảng vững chắc, linh hoạt và các lỗi phát sinh đã được khắc phục. Mọi thay đổi sẽ được lưu trữ an toàn trên Git.

---

# TODO

- [ ] Implement UART driver
- [ ] Add SPI communication
- [ ] Write application main loop
- [ ] Setup CI for firmware build
- [ ] Add unit tests for drivers
- [ ] Document flashing instructions

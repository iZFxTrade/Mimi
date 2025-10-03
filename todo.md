# ✅ Danh sách công việc dự án MiMi

Đây là danh sách các công việc cần làm để hoàn thành dự án, dựa trên `Roadmap ToDo` trong file README.md. Tôi sẽ thực hiện tuần tự, chi tiết và đánh dấu khi hoàn thành.

## Giai đoạn 0: Kiểm tra và Phân tích Hiện trạng

-   [x] **Phân tích cấu trúc file và tài liệu**
-   [x] **Kiểm tra mã nguồn driver phần cứng**
-   [x] **Kiểm tra luồng hoạt động của ứng dụng**

**==> Giai đoạn 0 hoàn tất. Đã có đủ thông tin để bắt đầu Giai đoạn 1.**

---

## Giai đoạn 1: Tích hợp phần cứng và UI cơ bản

-   [ ] **1.1. Tích hợp `mimi-cyd` vào hệ thống build:**
    -   [ ] **1.1.1.** Chỉnh sửa file `firmware/main/Kconfig.projbuild` để thêm lựa chọn `BOARD_TYPE_MIMI_CYD`.
-   [ ] **1.2. Hoàn thiện lớp Board `mimi-cyd`:**
    -   [ ] Implement lớp `MimiCydBoard` và các phương thức cần thiết.
-   [ ] **1.3. Xây dựng giao diện UI cơ bản:**
    -   [ ] Hiển thị màn hình chính với đồng hồ, thời tiết.
    -   [ ] Hiển thị popup nhắc lịch.

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

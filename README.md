# 🎀 MiMi – Trợ lý Học tập & Gia đình Thông minh

> **Lưu ý:** Đây là một phiên bản tùy biến (fork) của dự án [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32), được tối ưu hóa riêng cho phần cứng **ESP32-CYD (Cheap Yellow Display)** và bổ sung các tính năng dành cho dự án MiMi.

**MiMi** là một **trợ lý AI cá nhân hóa** chạy trên **ESP32-CYD**. MiMi không chỉ là **loa AI để bàn**, mà còn là **gia sư học tập, thư ký lịch trình, và một trung tâm giám sát, điều khiển ngôi nhà từ xa** có khả năng mở rộng không giới hạn.

---

## ✨ Tính năng chính

*   📚 **Gia sư học tập**
    *   Học ngoại ngữ, toán, vật lý... theo giáo trình có sẵn trên thẻ SD.
    *   Flashcard, quiz, và các bài kiểm tra tương tác.
    *   Lưu và báo cáo tiến trình học của từng thành viên.

*   🗓️ **Quản lý lịch học & công việc**
    *   Nhắc nhở lịch học, lịch làm việc, và các sự kiện quan trọng.
    *   Hỗ trợ xác nhận và theo dõi hoàn thành công việc.

*   📱 **Giám sát & Điều khiển từ xa qua Telegram**
    *   **Cảnh báo an ninh:** Gửi tin nhắn kèm hình ảnh khi phát hiện người lạ (với ESP32-CAM).
    *   **Báo cáo từ xa:** Nhận báo cáo tình hình học tập, trạng thái thiết bị theo yêu cầu.
    *   **Điều khiển từ xa:** Ra lệnh cho MiMi thực hiện các tác vụ từ bất cứ đâu.

*   🔌 **Hệ thống Mở rộng & Tự động hóa (Custom Actions)**
    *   **Tùy biến không giới hạn:** Người dùng có thể tự tạo các lệnh thoại mới ngay trên giao diện của MiMi.
    *   **Kết nối mọi thứ:** Mỗi lệnh thoại có thể được gắn với một API endpoint (HTTP GET/POST) để kết nối với các dịch vụ như **n8n, Zapier, IFTTT**, hoặc server cá nhân.
    *   **Ví dụ:**
        *   Tạo lệnh "*tạo ảnh*" để gọi đến API tạo ảnh AI.
        *   Tạo lệnh "*đọc báo*" để gọi đến API tổng hợp tin tức.
        *   Tạo lệnh "*bật đèn làm việc*" để gọi đến webhook của Home Assistant.

*   🏠 **Smarthome & Âm nhạc**
    *   Kết nối trực tiếp với Home Assistant qua MQTT.
    *   Phát nhạc theo ngữ cảnh (học tập, thư giãn, tập thể dục).

*   🤖 **Robot mở rộng (ESP32-CAM)**
    *   Khi được tích hợp, MiMi có thể điều khiển một robot tuần tra, nhận diện khuôn mặt và gửi cảnh báo an ninh qua Telegram.

---

## 📈 Roadmap ToDo

### Giai đoạn 1 – Nền tảng & Giao diện
*   [ ] Cấu hình phần cứng (LCD, Touch, Loa, Mic, SD).
*   [ ] UI Home (Đồng hồ, thời tiết) + Popup nhắc lịch.
*   [ ] Học offline qua Flashcard & Quiz từ thẻ SD.
*   [ ] Lưu tiến trình học cơ bản.

### Giai đoạn 2 – Thông minh & Kết nối
*   [ ] Tích hợp AI backend (ASR/TTS).
*   [ ] Cá nhân hóa nhiều người dùng.
*   [ ] **Tích hợp Telegram (Cốt lõi):** Gửi cảnh báo và nhận lệnh.
*   [ ] Tích hợp Smarthome MQTT.

### Giai đoạn 3 – Nền tảng Mở rộng
*   [ ] **Xây dựng Hệ thống Mở rộng (Custom Actions):**
    *   [ ] Giao diện UI để người dùng tự tạo/quản lý các hành động.
    *   [ ] Cơ chế lưu/tải cấu hình hành động từ thẻ SD.
    *   [ ] Engine thực thi: nhận diện lệnh thoại tùy chỉnh và gọi API tương ứng.
*   [ ] **Hoàn thiện Robot mở rộng (ESP32-CAM):**
    *   Tích hợp sâu hơn với hệ thống cảnh báo và hành động tùy chỉnh.

---
*Các phần còn lại như Hướng dẫn triển khai, Quản lý thẻ SD, Cấu trúc dữ liệu sẽ được giữ nguyên và chi tiết hóa trong quá trình phát triển.*

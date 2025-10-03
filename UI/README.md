# Tài liệu Thiết kế Giao diện Người dùng (UI)

Thư mục này chứa các tài liệu thiết kế, mockups, và tài nguyên liên quan đến giao diện người dùng của thiết bị. Giao diện được xây dựng bằng thư viện LVGL cho màn hình 320x240.

## Cấu trúc Giao diện Chính

Giao diện bao gồm các thành phần cốt lõi sau:

1.  **Vùng Nội dung (Content Area):** Khu vực trung tâm (320x200), nơi hiển thị nội dung của màn hình hiện tại.
2.  **Thanh Điều hướng (Navigation Bar):** Nằm cố định ở dưới cùng (320x40), chứa các biểu tượng để chuyển đổi nhanh giữa các màn hình (views).

---

## Mô tả Chi tiết 9 Màn hình Chức năng

Dưới đây là mô tả cho từng màn hình theo bản thiết kế chi tiết.

### 1. Màn hình Biểu cảm Trợ lý (Assistant Face)

*   **Tên View:** `face`
*   **Mục đích:** Giao diện tương tác chính, hiển thị trạng thái và thu thập lệnh thoại.
*   **Bố cục:** 
    *   Một khuôn mặt biểu cảm lớn (dạng Canvas hoặc Image) kích thước 180x180 được đặt ở trung tâm.
    *   Thông tin đồng hồ hoặc thời tiết được hiển thị nhỏ ở góc trên.
*   **Tương tác:** Có một nút/biểu tượng Micro để kích hoạt chế độ nghe lệnh thoại, đi kèm với các biểu cảm động của khuôn mặt.

### 2. Màn hình Trò chuyện (Chat)

*   **Tên View:** `chat`
*   **Mục đích:** Hiển thị lịch sử hội thoại giữa người dùng và AI, bao gồm cả tin nhắn từ bot Telegram.
*   **Bố cục:** Sử dụng danh sách hoặc bảng có thể cuộn để hiển thị các "bubble chat".
    *   Tin nhắn của người dùng (nhập từ màn hình hoặc qua mic) hiển thị bên phải.
    *   Tin nhắn của AI hoặc từ Telegram hiển thị bên trái.
*   **Tương tác:** Một thanh nhập liệu văn bản ở cuối màn hình để kích hoạt bàn phím ảo của LVGL.

### 3. Màn hình Tổng quan (Dashboard)

*   **Tên View:** `dashboard`
*   **Mục đích:** Tích hợp đồng hồ, lịch/thời khóa biểu và thông tin thời tiết.
*   **Bố cục:** Chia thành 3 vùng chính:
    1.  **Trên cùng:** Đồng hồ và ngày tháng với font chữ lớn.
    2.  **Giữa:** Thông tin thời tiết và dữ liệu từ cảm biến (ví dụ: Nhiệt độ/Độ ẩm từ GPIO34).
    3.  **Dưới cùng:** Danh sách các sự kiện/lịch trình trong ngày, được lấy từ file `timetable.json`.

### 4. Màn hình Gia sư (Learning Tutor)

*   **Tên View:** `learning`
*   **Mục đích:** Cung cấp giao diện cho các hoạt động học tập như Flashcard, Quiz, và bài giảng.
*   **Bố cục:** 
    *   Thanh tiêu đề để hiển thị hoặc chọn bài học.
    *   Vùng nội dung lớn ở trung tâm để hiển thị câu hỏi/nội dung bài học.
    *   Các nút tương tác như "Next", "Hint", và nút Micro ở phía dưới.

### 5. Màn hình Báo cáo & Thống kê (Reports & Stats)

*   **Tên View:** `reports`
*   **Mục đích:** Trực quan hóa tiến trình học tập và các số liệu thống kê.
*   **Bố cục:**
    *   Biểu đồ (cột hoặc tròn) chiếm phần lớn diện tích, hiển thị các thông số như điểm trung bình, tỷ lệ hoàn thành.
    *   Một khu vực nhỏ để tóm tắt hoặc chọn hồ sơ người học.

### 6. Màn hình Nhà thông minh (Smart Home)

*   **Tên View:** `smarthome`
*   **Mục đích:** Giao diện điều khiển các thiết bị nhà thông minh.
*   **Bố cục:**
    *   Sử dụng các tab để phân loại thiết bị theo phòng (ví dụ: Phòng khách, Phòng ngủ).
    *   Bố cục dạng lưới (grid) để hiển thị các thiết bị.
    *   Các nút chế độ nhanh (ví dụ: "Về nhà", "Đi ngủ") ở dưới cùng.
*   **Tương tác:** Chạm vào biểu tượng thiết bị để bật/tắt. Chạm giữ để mở popup điều khiển chi tiết (ví dụ: slider điều chỉnh độ sáng đèn).

### 7. Màn hình Media Player

*   **Tên View:** `media`
*   **Mục đích:** Điều khiển phát nhạc, sách nói, hoặc nội dung TTS.
*   **Bố cục:**
    *   Ảnh bìa album hoặc biểu tượng ở trung tâm.
    *   Thanh trượt hiển thị thời gian phát.
    *   Hàng nút điều khiển: Play/Pause, Next/Previous, Tăng/Giảm âm lượng.

### 8. Màn hình Cài đặt (Settings)

*   **Tên View:** `settings`
*   **Mục đích:** Cấu hình các thông số hệ thống, kết nối mạng và robot.
*   **Bố cục:** Sử dụng các tab để phân chia: "Hệ thống", "Mạng", "Robot".
*   **Thành phần:**
    *   **Mạng:** Cấu hình Wi-Fi, MQTT, token cho Telegram Bot.
    *   **Robot:** Các thanh trượt để điều chỉnh tốc độ, các nút để kiểm tra motor.
    *   Nút "Lưu" để áp dụng các thay đổi.

### 9. Màn hình Tính năng Mở rộng (Extensions)

*   **Tên View:** `extensions`
*   **Mục đích:** Quản lý và kích hoạt các hành động tùy chỉnh, tích hợp API bên ngoài (n8n, Webhooks).
*   **Bố cục:** Một danh sách có thể cuộn, mỗi mục là một nút lớn tương ứng với một hành động.
*   **Tương tác:** Khi nhấn một nút, thiết bị sẽ gửi một yêu cầu (MQTT, HTTP, Webhook) đã được cấu hình trước để thực thi một hành động (ví dụ: kích hoạt luồng "pha cà phê" trên n8n).

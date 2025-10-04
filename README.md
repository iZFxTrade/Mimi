# 🎀 MiMi – Trợ lý Học tập & Gia đình Thông minh

> **Lưu ý:** Đây là một phiên bản tùy biến (fork) của dự án [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32), được tối ưu hóa riêng cho phần cứng **ESP32-CYD (Cheap Yellow Display)** và bổ sung các tính năng dành cho dự án MiMi.

**MiMi** là một **trợ lý AI cá nhân hóa** chạy trên **ESP32-CYD**. MiMi không chỉ là **loa AI để bàn**, mà còn là một **người bạn đồng hành, gia sư thông minh, và trung tâm điều khiển ngôi nhà từ xa**, được thiết kế để trở thành một thành viên ảo trong gia đình bạn.

---

## 📖 Bản thiết kế dự án (Project Blueprint)

Để có cái nhìn tổng quan về mặt kỹ thuật, kiến trúc, cấu trúc tệp và luồng công việc của dự án, vui lòng tham khảo **[Bản thiết kế dự án (PROJECT_BLUEPRINT.md)](./PROJECT_BLUEPRINT.md)**. Tài liệu này được thiết kế đặc biệt để cung cấp thông tin chuyên sâu cho các nhà phát triển và trợ lý AI.

---

## ✨ Tính năng chính

*   💖 **Người bạn đồng hành trong gia đình**
    *   Luôn lắng nghe và trò chuyện cùng các thành viên với cá tính riêng.
    *   Ghi nhớ sở thích và thói quen để đưa ra các gợi ý phù hợp.
    *   Kết nối các thành viên trong gia đình thông qua các hoạt động chung và lời nhắc.

*   📚 **Gia sư thông minh hai chế độ**
    *   **Học theo giáo trình có sẵn:** Tự động đọc và dạy theo các file bài học (`.json`) được chuẩn bị sẵn trên thẻ nhớ, đảm bảo lộ trình học tập chi tiết.
    *   **Học theo chủ đề do AI tạo:** Chỉ cần ra lệnh với chủ đề và mục tiêu (ví dụ: "MiMi, dạy bé về các loại khủng long ăn thịt"), MiMi sẽ tự động biên soạn bài giảng, câu đố và flashcard để đạt được mục tiêu học tập đó.

*   📱 **Giám sát & Điều khiển từ xa qua Telegram**
    *   **Cảnh báo an ninh:** Gửi tin nhắn kèm hình ảnh khi phát hiện người lạ (với ESP32-CAM).
    *   **Báo cáo từ xa:** Nhận báo cáo tình hình học tập của con, trạng thái thiết bị theo yêu cầu.
    *   **Điều khiển từ xa:** Ra lệnh cho MiMi thực hiện các tác vụ từ bất cứ đâu.

*   🔌 **Hệ thống Mở rộng & Tự động hóa (Custom Actions)**
    *   **Tùy biến không giới hạn:** Người dùng có thể tự tạo các lệnh thoại mới ngay trên giao diện của MiMi để kết nối với bất kỳ dịch vụ nào có API (n8n, Home Assistant, Google, v.v.).

*   🏠 **Smarthome & Âm nhạc**
    *   Kết nối trực tiếp với Home Assistant qua MQTT.
    *   Phát nhạc theo ngữ cảnh (học tập, thư giãn, tập thể dục).

---

## 🚀 Hướng dẫn triển khai

Để đưa MiMi vào cuộc sống trên thiết bị ESP32-CYD của bạn, hãy làm theo các bước dưới đây.

### Phương pháp 1: Sử dụng WebFlasher (Đơn giản nhất)

> **Lưu ý:** Tính năng này đang được phát triển và sẽ sớm ra mắt!

Chúng tôi đang phát triển một công cụ WebFlasher cho phép bạn nạp firmware trực tiếp từ trình duyệt mà không cần cài đặt môi trường lập trình phức tạp.

1.  Kết nối ESP32-CYD với máy tính của bạn qua cổng USB.
2.  Truy cập trang WebFlasher của dự án (sẽ được cập nhật).
3.  Chọn đúng cổng COM và nhấn "Flash".
4.  Chờ quá trình hoàn tất.

### Phương pháp 2: Triển khai thủ công (Dành cho nhà phát triển)

Nếu bạn là nhà phát triển và muốn tùy chỉnh mã nguồn, bạn có thể làm theo cách thủ công.

**Yêu cầu:**

*   **ESP-IDF:** Cài đặt [môi trường phát triển của Espressif](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/).
*   **Git:** Để sao chép mã nguồn dự án.

**Các bước thực hiện:**

1.  **Sao chép mã nguồn:**
    ```bash
    git clone https://github.com/iZFxTrade/Mimi.git
    cd Mimi/firmware
    ```

2.  **Cấu hình thiết bị:**
    Chạy menu cấu hình để chọn đúng bo mạch và các cài đặt khác.
    ```bash
    idf.py set-target esp32
    idf.py menuconfig
    ```
    *Trong menuconfig, hãy chắc chắn rằng bạn đã cấu hình đúng các chân (pin) cho màn hình, cảm ứng và các ngoại vi khác nếu bạn dùng phần cứng khác ESP32-CYD.*

3.  **Biên dịch và Nạp firmware:**
    ```bash
    idf.py build flash monitor
    ```

### Chuẩn bị Thẻ nhớ (SD Card)

Sau khi nạp firmware, bạn cần chuẩn bị thẻ nhớ để MiMi có thể hoạt động.

1.  Định dạng thẻ nhớ theo chuẩn `FAT32`.
2.  Tạo cấu trúc thư mục và các tệp cấu hình như trong phần [Cấu trúc dữ liệu trên thẻ SD](#-cấu-trúc-dữ-liệu-trên-thẻ-sd).
3.  **Quan trọng:** Tạo tệp `config.json` ở thư mục gốc của thẻ nhớ và điền thông tin Wi-Fi, MQTT, Telegram của bạn.
4.  Cắm thẻ nhớ vào thiết bị và khởi động lại.

---

## 📈 Roadmap (Lộ trình phát triển)

Đây là những tính năng và cải tiến mà chúng tôi dự định sẽ thực hiện trong tương lai.

*   [ ] **🚀 WebFlasher cho ESP32:**
    *   **Mục tiêu:** Đơn giản hóa tối đa quá trình nạp firmware cho người dùng cuối. Người dùng chỉ cần kết nối thiết bị và flash trực tiếp từ trình duyệt mà không cần cài đặt công cụ.

*   [ ] **🗣️ Cải thiện Nhận dạng Giọng nói:**
    *   **Mục tiêu:** Tích hợp các mô hình nhận dạng giọng nói cục bộ (local) để giảm độ trễ và tăng tính riêng tư.

*   [ ] **🌐 Hỗ trợ Đa ngôn ngữ:**
    *   **Mục tiêu:** Mở rộng khả năng của MiMi để hỗ trợ các ngôn ngữ khác ngoài tiếng Việt.

*   [ ] **📱 Ứng dụng di động đồng hành (Companion App):**
    *   **Mục tiêu:** Xây dựng một ứng dụng trên điện thoại để dễ dàng cấu hình, quản lý tệp trên thẻ nhớ và tương tác với MiMi.

*   [ ] **🧩 Mở rộng tích hợp Smarthome:**
    *   **Mục tiêu:** Hỗ trợ thêm nhiều loại thiết bị và kịch bản tự động hóa phức tạp hơn với Home Assistant và các nền tảng khác.

*   [ ] **🎨 Giao diện người dùng nâng cao:**
    *   **Mục tiêu:** Cải tiến UI/UX trên màn hình của thiết bị, thêm nhiều hiệu ứng và tùy chọn cá nhân hóa hơn.

---

## 📂 Cấu trúc dữ liệu trên thẻ SD

Thư mục gốc của thẻ SD sẽ chứa các file cấu hình và thư mục dữ liệu sau:

```
/
├── config.json
├── timetable.json
├── actions.json
├── learning/
│   └── ... (các file bài học .json)
├── music/
│   └── ... (các file nhạc .mp3, .wav)
├── system/
│   └── ... (file hệ thống, log, v.v.)
└── profiles/
    └── {user_name}/
        ├── images/
        │   └── ... (hình ảnh của người dùng)
        └── progress.json
```

### `config.json`

File cấu hình chung cho thiết bị.

```json
{
  "wifi_ssid": "Your_SSID",
  "wifi_password": "Your_Password",
  "mqtt_server": "your_mqtt_broker_ip",
  "telegram_bot_token": "Your_Bot_Token",
  "telegram_chat_id": "Your_Chat_ID"
}
```

### `timetable.json`

Chứa lịch học, lịch làm việc và các sự kiện.

```json
[
  {
    "time": "08:00",
    "days": ["Mon", "Wed", "Fri"],
    "event_type": "Học bài",
    "details": "Toán - Chương 3: Hình học không gian"
  },
  {
    "time": "20:00",
    "days": ["Tue", "Thu"],
    "event_type": "Làm bài tập",
    "details": "Vật lý - Bài tập về nhà"
  }
]
```

### `learning/{subject}/{lesson_name}.json`

Cấu trúc của một file bài học cho chế độ học theo giáo trình.

```json
{
  "title": "Bài 1: Các hành tinh trong Hệ Mặt Trời",
  "subject": "Thiên văn học",
  "objective": "Nhận biết và nhớ tên 8 hành tinh.",
  "activities": [
    {
      "type": "lecture",
      "content": "Hôm nay chúng ta sẽ tìm hiểu về các hành tinh trong hệ mặt trời của chúng ta. Có tất cả 8 hành tinh, bắt đầu từ Sao Thủy, gần Mặt Trời nhất."
    },
    {
      "type": "flashcard",
      "cards": [
        {"front": "Hành tinh lớn nhất?", "back": "Sao Mộc"},
        {"front": "Hành tinh có vành đai rõ nhất?", "back": "Sao Thổ"}
      ]
    },
    {
      "type": "quiz",
      "questions": [
        {
          "question": "Hành tinh nào được gọi là 'Hành tinh Đỏ'?",
          "options": ["Sao Kim", "Sao Hỏa", "Sao Mộc"],
          "answer": "Sao Hỏa"
        }
      ]
    }
  ]
}
```

### `actions.json`

Lưu trữ các hành động tùy chỉnh do người dùng tạo.

```json
[
  {
    "voice_command": "tạo ảnh",
    "method": "POST",
    "url": "https://api.your-n8n.com/webhook/generate-image",
    "body_template": "{\"prompt\": \"{data}\"}"
  },
  {
    "voice_command": "đọc báo",
    "method": "GET",
    "url": "https://api.your-news.com/latest-news"
  }
]
```

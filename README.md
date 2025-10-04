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

---

## 📈 Roadmap ToDo

*(Roadmap không thay đổi)*

---

*Các phần Hướng dẫn triển khai sẽ được giữ nguyên.*

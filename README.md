# 🎀 MiMi – Smart Learning & Home Assistant

> **MiMi** là một **trợ lý AI cá nhân hóa** chạy trên **ESP32-CYD (Cheap Yellow Display)**.
> MiMi không chỉ là **loa AI để bàn**, mà còn là **gia sư học tập, thư ký lịch trình, trợ lý gia đình** và có thể mở rộng thành **robot thông minh** với ESP32-CAM.

---

## 🚀 Hướng dẫn triển khai

### 1. Chuẩn bị linh kiện

* ESP32-2432S028R (CYD) – mainboard.
* INMP441 (mic I2S).
* Loa tích hợp NS4168.
* SD Card (SPI).
* ESP32-CAM (tùy chọn robot).
* Driver động cơ (TB6612FNG hoặc PCA9685, nếu làm robot).
* Cảm biến tránh vật cản, nhiệt độ/độ ẩm (tùy chọn).

### 2. Clone firmware nền tảng

Dự án MiMi tùy biến từ [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32):

```bash
git clone https://github.com/78/xiaozhi-esp32.git
cd xiaozhi-esp32
```

Sau đó tùy biến code để thêm UI học tập, nhắc lịch, quản lý dữ liệu SD và tích hợp smarthome.

### 3. Đấu dây INMP441 (Mic I2S)

| Pin INMP441 | ESP32 CYD GPIO |
| ----------- | -------------- |
| WS          | GPIO15         |
| SCK         | GPIO14         |
| SD          | GPIO32         |
| VCC         | 3.3V           |
| GND         | GND            |

👉 Mic có thể kết nối trực tiếp, không cần module trung gian.

### 4. Build & Flash

* Sử dụng **ESP-IDF** hoặc **Arduino IDE**.
* Chọn board: `ESP32 Dev Module`.
* Flash firmware đã tùy biến.

### 5. Chuẩn bị SD Card

* Tạo thư mục `/learning/`, `/profiles/`, `/progress/` trên SD.
* Copy các file JSON mẫu (curriculum, timetable, lessons).

---

## ✨ Tính năng chính

* 📚 **Gia sư học tập**

  * Học ngoại ngữ, toán, vật lý... theo giáo trình.
  * Flashcard, quiz, câu hỏi vấn đáp.
  * Kiểm tra & chấm điểm sau bài học (trả bài).
  * Lưu tiến trình học của từng thành viên.

* 🗓️ **Quản lý lịch học & công việc**

  * Nhắc học/bài tập theo `timetable.json`.
  * Người dùng xác nhận bằng giọng nói hoặc bấm trên màn hình.
  * Bài tập thực hành → MiMi bấm giờ, lưu thời gian hoàn thành.

* 🎶 **Âm nhạc theo ngữ cảnh**

  * Học → Lo-fi tập trung.
  * Ngủ → White noise/piano.
  * Tập thể dục → Upbeat.
  * Có thể phát nhạc từ SD hoặc gửi lệnh Google Home (MQTT/HA).

* 🏠 **Smarthome**

  * Kết nối MQTT/Home Assistant.
  * Điều khiển đèn, quạt, thiết bị IoT bằng giọng nói.

* 👨‍👩‍👧‍👦 **Cá nhân hóa nhiều người dùng**

  * Profile riêng cho từng thành viên (cha/mẹ/chị/em).
  * Nhận diện qua giọng nói, camera (ESP32-CAM) hoặc chọn trên UI.
  * Cha mẹ có thể yêu cầu MiMi báo cáo tình hình học tập của con.

* 🤖 **Robot mở rộng (ESP32-CAM)**

  * Tuần tra trong nhà.
  * Gửi video đến AI backend nhận diện người lạ.
  * MiMi hiển thị cảnh báo và phát thông báo.
  * CYD có thể gắn lên robot làm “khuôn mặt biểu cảm”.

---

## 💾 Quản lý thẻ SD

### 1. Khi **không phát hiện SD card**

* Hiển thị popup: *“⚠️ Vui lòng gắn thẻ SD để sử dụng đầy đủ tính năng học tập & lưu trữ dữ liệu.”*
* Giọng nói thông báo tương tự.
* Chỉ chạy chế độ tối giản: đồng hồ, thời tiết, biểu cảm cơ bản, smarthome MQTT (nếu có cấu hình).

### 2. Khi **cắm SD card lần đầu**

* Tự động tạo các thư mục hệ thống:

  ```
  /profiles/
  /profiles/images/
  /progress/
  /learning/
  /music/
  /system/
  ```
* Sinh file mặc định:

  * `config.json` (WiFi, MQTT, AI backend).
  * `timetable.json` (rỗng).
  * `curriculum.json` (mẫu).
  * `lessons/` (chứa vài bài demo).

### 3. Khi **SD card có dữ liệu cũ**

* Đọc file cấu hình & dữ liệu.
* Nếu thiếu thư mục/file → bổ sung.
* Nếu file hỏng → tạo lại file mặc định và thông báo: *“Một số file bị lỗi, MiMi đã tạo lại file mặc định.”*

### 4. Lưu trữ dữ liệu

* **Tiến trình học**: `/profiles/<user>/progress/`.
* **Ảnh profile**: `/profiles/images/<user>.jpg`.
* **Giáo trình**: `/learning/curriculum.json`.
* **Nhạc**: `/music/`.
* **Cấu hình hệ thống**: `/system/config.json`.

👉 Mọi dữ liệu load theo nhu cầu, tránh chiếm RAM.

---

## 📚 Cấu trúc dữ liệu

### 📖 curriculum.json

```json
{
  "program": "English Beginner",
  "levels": [
    {
      "id": "A1",
      "title": "Beginner",
      "lessons": [
        {"id": "travel", "title": "Travel Basics", "file": "lessons/travel.json"}
      ]
    }
  ]
}
```

### 📖 lesson.json

```json
{
  "lesson": "Physics - Temperature",
  "subject": "Physics",
  "objective": "Hiểu khái niệm nhiệt độ và các đơn vị đo",
  "mode": "manual",
  "parts": [
    {
      "title": "Khái niệm cơ bản",
      "content": [
        {"concept": "Nhiệt độ", "explain": "Độ nóng/lạnh của vật."}
      ],
      "flashcards": [
        {"front": "Temperature", "back": "Nhiệt độ"}
      ],
      "questions": [
        {"type": "quiz", "q": "Đơn vị SI của nhiệt độ?", "options": ["°C","K","°F"], "answer": "K"},
        {"type": "open", "q": "Trình bày sự khác nhau giữa °C và K."}
      ]
    }
  ]
}
```

👉 Với `"mode": "ai_generated"`, chỉ cần nhập `lesson`, `subject`, `objective`, AI sẽ sinh flashcard + quiz + câu hỏi vấn đáp.

### 🗓️ timetable.json

```json
{
  "2025-10-05": [
    {"time": "19:00", "activity": "English Lesson", "lesson": "Travel Basics", "mood": "focus", "music": "lofi.mp3"},
    {"time": "21:00", "activity": "Math Homework", "duration": 45, "type": "practice"}
  ]
}
```

### 📊 progress.json

```json
{
  "date": "2025-10-05",
  "lesson": "Math Homework - Algebra",
  "type": "practice",
  "start_time": "21:00",
  "end_time": "21:45",
  "duration_min": 45,
  "checked": true,
  "score": 9,
  "mistakes": [
    {"q": "Giải 2x+3=7", "error": "Sai lần 1, đúng lần 2"}
  ],
  "status": "completed"
}
```

---

## 🖼️ Thiết kế giao diện người dùng

### 1. Trang **Biểu cảm MiMi**

* Hiển thị khuôn mặt MiMi (emoji-style): 😀 vui, 😐 bình thường, 😴 buồn ngủ, 😡 cảnh báo.
* Nút cảm ứng: 🔊 bật/tắt giọng nói, ⚙️ vào Setting.

### 2. Trang **Đồng hồ + Thời tiết**

* Hiển thị giờ, ngày, thời tiết (icon + nhiệt độ).
* Nút: 📅 mở lịch, 🔄 refresh thời tiết, 🎶 bật nhạc nhanh.

### 3. Trang **Lịch + Thời khóa biểu**

* Hiển thị lịch tháng + lịch trình trong ngày.
* Nút: ➕ thêm lịch, ✏️ chỉnh sửa, ❌ xóa.
* Popup reminder: ✅ Bắt đầu | ⏰ Hoãn | ❌ Bỏ qua.

### 4. Trang **Học + Tập**

* **Học lý thuyết**: flashcard, quiz, nút ▶️ nghe phát âm, ✅ trả lời, 🔄 thử lại.
* **Thực hành**: timer, nút “Đã hoàn thành”, popup gợi ý kiểm tra lại.

### 5. Trang **Setting (Cấu hình)**

* Cấu hình: WiFi, MQTT, chọn AI backend, quản lý profile, quản lý SD.
* Nút: 💾 lưu, 🔄 reset.

### 6. Trang **Báo cáo học tập**

* Biểu đồ cột + tròn (tiến trình, điểm số).
* Danh sách lỗi phổ biến.
* Nút: 📤 xuất báo cáo, 🔍 chọn thành viên.

### 7. Trang **Trình phát nhạc**

* Playlist từ SD + online, hiển thị bài hát đang phát.
* Nút: ⏮️ | ▶️ | ⏭️, 🔊 volume, 🎵 chọn playlist.

---

## 👨‍👩‍👧‍👦 Cá nhân hóa

* Hồ sơ riêng cho từng thành viên: `/profiles/father/`, `/profiles/mother/`, `/profiles/sister/`, `/profiles/brother/`.
* Profile chứa lịch học, timetable, progress riêng.
* Hỗ trợ ảnh profile trong `/profiles/images/`.
* Cha mẹ có thể hỏi:

  * “MiMi, báo cáo tình hình học của Nam tuần này.”
  * “Lan có hoàn thành bài tập hôm nay không?”

---

## 📈 Roadmap ToDo

### Giai đoạn 1 – Cơ bản

* [ ] Cấu hình phần cứng (LCD, Touch, Loa, Mic, SD).
* [ ] WebUI upload JSON.
* [ ] UI Home + Reminder popup.
* [ ] Flashcard + quiz offline.
* [ ] Lưu progress.

### Giai đoạn 2 – Thông minh

* [ ] Tích hợp AI backend (ASR/TTS, quiz generator).
* [ ] Cá nhân hóa nhiều người dùng.
* [ ] Báo cáo học tập cho cha mẹ.
* [ ] Trả bài sau khi học hoặc làm bài tập.
* [ ] Phát nhạc theo ngữ cảnh.
* [ ] Smarthome MQTT.

### Giai đoạn 3 – Robot mở rộng

* [ ] ESP32-CAM tuần tra.
* [ ] Nhận diện khuôn mặt, cảnh báo người lạ.
* [ ] CYD gắn lên robot làm mặt biểu cảm.

---



## 📈 Roadmap ToDo

### Giai đoạn 1 – Cơ bản

* [ ] Cấu hình phần cứng (LCD, Touch, Loa, Mic, SD).
* [ ] WebUI upload JSON.
* [ ] UI Home + Reminder popup.
* [ ] Flashcard + quiz offline.
* [ ] Lưu progress.

### Giai đoạn 2 – Thông minh

* [ ] Tích hợp AI backend (ASR/TTS, quiz generator).
* [ ] Cá nhân hóa nhiều người dùng.
* [ ] Báo cáo học tập cho cha mẹ.
* [ ] Trả bài sau khi học hoặc làm bài tập.
* [ ] Phát nhạc theo ngữ cảnh.
* [ ] Smarthome MQTT.

### Giai đoạn 3 – Robot mở rộng

* [ ] ESP32-CAM tuần tra.
* [ ] Nhận diện khuôn mặt, cảnh báo người lạ.
* [ ] CYD gắn lên robot làm mặt biểu cảm.

---

## 🔗 Tham khảo & Tùy biến

Dự án MiMi dựa trên [**xiaozhi-esp32**](https://github.com/78/xiaozhi-esp32) – một firmware mã nguồn mở cho ESP32 hỗ trợ:

* 🎙️ ASR (Speech-to-Text)
* 🔊 TTS (Text-to-Speech)
* 🧑‍🤝‍🧑 Voiceprint Recognition (nhận diện giọng nói)
* 🌐 MQTT/WebSocket

👉 MiMi sẽ tùy biến lại firmware này:

* Thêm **UI học tập + nhắc lịch** bằng LVGL.
* Quản lý dữ liệu SD (giáo án, timetable, progress).
* Cá nhân hóa nhiều thành viên.
* Tích hợp smarthome MQTT.

---

## ✅ Kết luận

MiMi là dự án **AI trợ lý học tập & gia đình** hoàn chỉnh, với khả năng:

* Trợ giúp học tập có lộ trình, nhắc nhở thông minh.
* Cá nhân hóa cho từng thành viên trong nhà.
* Quản lý tiến trình học và báo cáo lại cho cha mẹ.
* Kết hợp Smarthome & Robot mở rộng.

MiMi không chỉ là một thiết bị phần cứng, mà là **một thành viên ảo trong gia đình** – vừa là gia sư, vừa là thư ký, vừa là bạn đồng hành.

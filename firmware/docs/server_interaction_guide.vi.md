# Hướng dẫn Tương tác với MCP-Server cho Firmware

Đây là tài liệu hướng dẫn cho các nhà phát triển firmware (ví dụ: trên ESP32) về cách giao tiếp với MCP-Server.

## Luồng hoạt động tổng thể

1.  **Giai đoạn 1: Kích hoạt & Lấy Cấu hình (HTTP)**
    - Thiết bị gửi một yêu cầu `POST /api/ota/` để đăng ký và kiểm tra cập nhật.
    - Server trả về toàn bộ cấu hình cần thiết, bao gồm endpoint và token cho WebSocket.

2.  **Giai đoạn 2: Giao tiếp Giọng nói (WebSocket)**
    - Thiết bị sử dụng thông tin từ Giai đoạn 1 để kết nối vào kênh WebSocket.
    - Toàn bộ quá trình STT -> LLM -> TTS diễn ra trên kênh này.

---

## 1. Giai đoạn Kích hoạt (HTTP `POST /api/ota/`)

Đây là bước đầu tiên và tiên quyết.

- **Mục đích:** Đăng ký thiết bị, kiểm tra OTA, và lấy cấu hình kết nối.
- **Chi tiết:** Vui lòng tham khảo tài liệu `MCP-Server/ota_api_vietnamese.md` để biết cấu trúc request và response chi tiết.

### Gửi cấu hình mở rộng

Firmware có thể đọc các cấu hình bổ sung (ví dụ: `telegram.json`, `smarthome.json` từ bộ nhớ flash) và nhúng chúng vào body của request `POST /api/ota/`. Đây là cách an toàn để kích hoạt các tính năng mới trên server mà không phá vỡ tương thích.

```c++
// Ví dụ mã giả trên Arduino/ESP-IDF

// ... tạo JSON object chính ...

if (configFileExists("/telegram.json")) {
  String telegramConfig = readFile("/telegram.json");
  // Gắn chuỗi JSON này vào trường "telegram" của request chính
  mainRequest.set("telegram", JSON.parse(telegramConfig)); 
}

// ... gửi request ...
```

---

## 2. Giai đoạn Giao tiếp Giọng nói (WebSocket)

Sau khi có được URL và token từ bước 1, firmware sẽ tiến hành kết nối WebSocket.

### 2.1. Bắt tay (Handshake)

Ngay sau khi kết nối thành công, client **PHẢI** gửi một message "hello" dưới dạng text (JSON) để định danh.

**Cấu trúc message `hello`:**

```json
{
  "type": "hello",
  "device_id": "your_device_id_from_mac_address",
  "user_id": "user_who_is_speaking_id", // <-- TÙY CHỌN
  "audio_params": {
    "format": "opus",
    "sample_rate": 16000,
    "channels": 1
  }
}
```

### 💡 Vai trò của `user_id` (Tùy chọn nhưng Quan trọng)

Trường `user_id` là chìa khóa để kích hoạt **tính năng ngữ cảnh đa người dùng** trên server.

-   **Nếu firmware không gửi `user_id`:** Server sẽ tự động sử dụng một "người dùng mặc định" cho thiết bị này. Mọi cuộc hội thoại sẽ được lưu vào chung một ngữ cảnh. Điều này đảm bảo **tương thích ngược** với các client đơn giản.
-   **Nếu firmware gửi một `user_id`:** Server sẽ tìm hoặc tạo một hồ sơ người dùng riêng biệt (`UserProfile`) cho `user_id` đó, trong phạm vi của `device_id`. Điều này cho phép server "nhớ" các cuộc trò chuyện trong quá khứ với từng người, mang lại trải nghiệm cá nhân hóa.

**Trong tương lai,** firmware có thể được nâng cấp với các thuật toán nhận dạng giọng nói tại biên (voice recognition on the edge) để xác định ai đang nói và gửi `user_id` tương ứng lên server.

### 2.2. Luồng Âm thanh

-   **Client gửi đi:**
    1.  Sau khi bắt đầu thu âm (ví dụ: người dùng nhấn nút hoặc nói wake-word), client gửi liên tục các gói tin **binary** chứa dữ liệu âm thanh (khuyến nghị định dạng **Opus**).
    2.  Khi người dùng ngừng nói, client gửi một gói tin **text (JSON)** duy nhất: `{"type": "listen", "state": "stop"}`.

-   **Server trả về:**
    1.  `{"type": "stt", "text": "..."}`: Kết quả nhận dạng giọng nói.
    2.  `{"type": "llm", "text": "..."}`: Phản hồi từ mô hình ngôn ngữ lớn.
    3.  `{"type": "tts", "state": "start"}`: Báo hiệu bắt đầu luồng âm thanh trả về.
    4.  Các gói tin **binary** chứa âm thanh phản hồi (TTS).
    5.  `{"type": "tts", "state": "stop"}`: Báo hiệu kết thúc luồng âm thanh trả về.

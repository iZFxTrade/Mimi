# Tài liệu API OTA và Kích hoạt Thiết bị

Đây là tài liệu mô tả chi tiết về endpoint `POST /api/ota/`, là điểm giao tiếp đầu tiên và quan trọng nhất giữa một thiết bị (client) và MCP Server.

## 1. Tổng quan

- **Endpoint:** `POST /api/ota/`
- **Method:** `POST`
- **Mục đích:**
    1.  Để client tự giới thiệu và đăng ký với server.
    2.  Để client kiểm tra xem có bản cập nhật firmware (OTA) mới hay không.
    3.  Để client **đồng bộ hóa các cấu hình mở rộng** (như Telegram, Nhà thông minh) lên server.
    4.  Để server cung cấp các thông tin kết nối cần thiết (MQTT, WebSocket) cho client.

## 2. Cấu trúc Request

### Headers

| Header          | Bắt buộc | Mô tả                                                                   |
| --------------- | -------- | ----------------------------------------------------------------------- |
| `Device-Id`     | Có       | Mã định danh duy nhất của phần cứng thiết bị (ví dụ: MAC address).     |
| `Client-Id`     | Có       | Mã định danh duy nhất của phiên cài đặt phần mềm, tạo khi flash.        |
| `User-Agent`    | Có       | Thông tin về loại client (ví dụ: `ESP32-S3-BOX-3-OTA-Agent/1.0.0`).      |
| `Content-Type`  | Có       | Luôn là `application/json`.                                             |

### Body (JSON)

Đây là cấu trúc JSON mà client gửi lên server.

```json
{
  "application": {
    "version": "1.0.0",
    "elf_sha256": "sha256_hash_of_firmware_file"
  },
  "board": {
    "type": "esp32-s3-box-3",
    "name": "esp32-s3-box-3_16mb"
  },
  "auto_update_enabled": true,
  "uuid": "client_id_from_header",

  "telegram": { // <-- Trường tùy chọn để kích hoạt bot Telegram
    "bot_token": "YOUR_TELEGRAM_BOT_TOKEN_HERE",
    "allowed_chat_ids": ["your_telegram_chat_id"]
  },

  "smart_home": { // <-- Ví dụ về một trường tùy chọn khác trong tương lai
      "rooms": [
          {
              "name": "Phòng khách",
              "devices": [
                  { "topic": "living_room/light1", "name": "Đèn chùm", "type": "light" }
              ]
          }
      ]
  }
}
```

### 💡 Chiến lược Mở rộng Không Phá vỡ (Non-Breaking Extension)

Điểm quan trọng nhất của API này là tính linh hoạt của nó.

- **Các trường cốt lõi** (`application`, `board`, `uuid`) là bắt buộc và phải được gửi bởi mọi client để đảm bảo tương thích ngược với kiến trúc gốc.
- **Các trường mở rộng** (`telegram`, `smart_home`, v.v.) là **tùy chọn (optional)**. Client gốc của `xiaozhi` sẽ không gửi các trường này, và server sẽ bỏ qua chúng một cách an toàn. Các client được nâng cấp của chúng ta có thể gửi kèm một hoặc nhiều trường này để kích hoạt các tính năng tương ứng trên server.

Cách tiếp cận này cho phép chúng ta liên tục thêm các tính năng mới vào hệ sinh thái mà không làm ảnh hưởng đến các thiết bị cũ đang hoạt động.

## 3. Cấu trúc Response

Server sẽ phản hồi một cấu trúc JSON chi tiết, cung cấp mọi thông tin client cần để đi vào hoạt động.

```json
{
  "has_update": false, // true nếu có bản firmware mới
  "activation": {
    "code": "MIM123456",
    "message": "Vui lòng kích hoạt."
  },
  "mqtt": {
    "endpoint": "mqtt.yourserver.com",
    "client_id": "GID_test@@@device_id@@@uuid",
    "username": "mqtt_user",
    "password": "mqtt_password"
  },
  "websocket": {
    "url": "ws://yourserver.com/api/v1/voice_chat",
    "token": "websocket_access_token"
  },
  "server_time": {
    "timestamp": 1678886400000,
    "timezone": "Asia/Ho_Chi_Minh",
    "timezone_offset": 25200
  },
  "firmware": null // Hoặc chứa thông tin firmware nếu has_update là true
}
```

| Trường          | Kiểu      | Mô tả                                                                                             |
| --------------- | --------- | ------------------------------------------------------------------------------------------------- |
| `has_update`    | boolean   | Báo hiệu có bản cập nhật firmware mới hay không.                                                  |
| `activation`    | object    | Thông tin mã kích hoạt (ít dùng trong kiến trúc của chúng ta).                                    |
| `mqtt`          | object    | Cấu hình để client kết nối tới MQTT broker.                                                      |
| `websocket`     | object    | URL và token để client kết nối tới kênh WebSocket giao tiếp giọng nói.                             |
| `server_time`   | object    | Thông tin thời gian hiện tại của server để đồng bộ.                                               |
| `firmware`      | object/null | Nếu `has_update` là `true`, trường này sẽ chứa URL và changelog của bản cập nhật. Nếu không, nó là `null`. |

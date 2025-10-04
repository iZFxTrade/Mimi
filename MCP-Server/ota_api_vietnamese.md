## Tài liệu API OTA

### Tổng quan
API này được sử dụng để xử lý yêu cầu nâng cấp OTA (Over-The-Air) của thiết bị. Thiết bị gửi thông tin và phiên bản firmware hiện tại, máy chủ sẽ trả về thông tin phiên bản firmware mới nhất cùng đường dẫn tải (nếu có bản cập nhật).

Ngoài ra, phản hồi của phiên bản mới cũng có thể bao gồm thông tin về máy chủ MQTT, WebSocket và mã kích hoạt của thiết bị.

---

### Phương thức yêu cầu
`POST /api/ota/`

---

### Header yêu cầu
- **Device-Id**: Mã định danh duy nhất của thiết bị (bắt buộc, có thể là địa chỉ MAC hoặc mã giả MAC được tạo từ ID phần cứng)
- **Client-Id**: Mã định danh duy nhất của client, được tạo tự động (UUID v4). Sẽ thay đổi khi xóa Flash hoặc cài đặt lại.
- **User-Agent**: Tên và phiên bản phần mềm client (bắt buộc, ví dụ `esp-box-3/1.5.6`)
- **Accept-Language**: Ngôn ngữ hiện tại của client (tùy chọn, ví dụ `zh-CN`)

---

### Request Body
Yêu cầu phải ở định dạng JSON và chứa các trường sau:

```json
{
  "application": {
    "version": "1.0.1",          // Phiên bản firmware hiện tại
    "elf_sha256": "<hash>"       // Mã SHA256 dùng để kiểm tra tính toàn vẹn firmware
  },
  "mac_address": "11:22:33:44:55:66",   // Địa chỉ MAC (tùy chọn)
  "uuid": "<Client-Id>",               // Client UUID (tùy chọn)
  "chip_model_name": "esp32s3",        // Model chip (tùy chọn)
  "flash_size": 16777216,               // Dung lượng flash (tùy chọn)
  "psram_size": 4194304,                // Dung lượng PSRAM (tùy chọn)
  "partition_table": [...],             // Bảng phân vùng thiết bị (tùy chọn)
  "board": {
    "type": "xingzhi-cube-1.54tft-wifi",  // Loại bo mạch
    "name": "xingzhi-cube-1.54tft-wifi",  // Tên SKU bo mạch
    "ssid": "PhongNgu",                    // Tên Wi-Fi kết nối
    "rssi": -55                             // Cường độ tín hiệu Wi-Fi
  }
}
```

---

### Phản hồi thành công
Phản hồi được trả về ở định dạng JSON:

```json
{
  "activation": {
    "code": "ABC123",          // Mã kích hoạt thiết bị
    "message": "Vui lòng kích hoạt trên màn hình"
  },
  "mqtt": {
    "endpoint": "mqtt.example.com",
    "client_id": "GID_test@@@device-id@@@uuid",
    "username": "device_12345",
    "password": "password"
  },
  "websocket": {
    "url": "wss://api.tenclass.net/xiaozhi/v1/",
    "token": "test-token"
  },
  "server_time": {
    "timestamp": 1633024800000,
    "timezone": "Asia/Shanghai",
    "timezone_offset": -480
  },
  "firmware": {
    "version": "1.0.2",              // Phiên bản firmware mới nhất
    "url": "https://example.com/firmware/1.0.2.bin"  // Đường dẫn tải firmware
  }
}
```

---

### Phản hồi lỗi
- **400 Bad Request** – Yêu cầu thiếu trường bắt buộc hoặc trường không hợp lệ
  ```json
  { "error": "Device ID is required" }
  ```

- **500 Internal Server Error** – Lỗi hệ thống
  ```json
  { "error": "Failed to read device auto_update status" }
  ```

---

### Ví dụ yêu cầu ESP32 đầy đủ
```http
POST /xiaozhi/ota/ HTTP/1.1
Host: api.tenclass.net
Content-Type: application/json
User-Agent: xingzhi-cube-1.54tft-wifi/1.0.1
Device-Id: 11:22:33:44:55:66
Client-Id: 7b94d69a-9808-4c59-9c9b-704333b38aff

{
  "version": 2,
  "language": "zh-CN",
  "flash_size": 16777216,
  "minimum_free_heap_size": 8457848,
  "mac_address": "11:22:33:44:55:66",
  "chip_model_name": "esp32s3",
  "uuid": "7b94d69a-9808-4c59-9c9b-704333b38aff",
  "application": {
    "name": "xiaozhi",
    "version": "1.0.1",
    "compile_time": "Feb 1 2025T23:02:27Z",
    "idf_version": "v5.4-dirty",
    "elf_sha256": "c8a8ecb6d6fbcda682494d9675cd1ead240ecf38bdde75282a42365a0e396033"
  }
}
```

---

### Ghi chú
- Các thiết bị có firmware phiên bản **0.9.8** và loại bắt đầu bằng `bread-` sẽ bị **buộc cập nhật** do lỗi mã hóa âm thanh.
- Nếu thiết bị **tắt tự động cập nhật**, máy chủ sẽ không trả về bản firmware mới.
- Nếu loại thiết bị **không xác định hoặc không có bản firmware phù hợp**, phản hồi sẽ trả lại phiên bản hiện tại và đường dẫn tải rỗng.
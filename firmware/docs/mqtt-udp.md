# Tài liệu Giao thức Giao tiếp Hỗn hợp MQTT + UDP

Tài liệu giao thức giao tiếp hỗn hợp MQTT + UDP được biên soạn dựa trên việc triển khai mã, phác thảo cách tương tác giữa thiết bị và máy chủ, trong đó MQTT được sử dụng để truyền tin nhắn điều khiển và UDP được sử dụng để truyền dữ liệu âm thanh.

---

## 1. Tổng quan về Giao thức

Giao thức này sử dụng phương thức truyền hỗn hợp:
- **MQTT**: Dùng cho tin nhắn điều khiển, đồng bộ hóa trạng thái, trao đổi dữ liệu JSON
- **UDP**: Dùng cho truyền dữ liệu âm thanh thời gian thực, hỗ trợ mã hóa

### 1.1 Đặc điểm của Giao thức

- **Thiết kế kênh đôi**: Tách biệt điều khiển và dữ liệu, đảm bảo tính thời gian thực
- **Truyền mã hóa**: Dữ liệu âm thanh UDP được mã hóa bằng AES-CTR
- **Bảo vệ bằng số thứ tự**: Ngăn chặn phát lại và mất trật tự gói tin
- **Tự động kết nối lại**: Tự động kết nối lại khi kết nối MQTT bị ngắt

---

## 2. Tổng quan về Quy trình Tổng thể

```mermaid
sequenceDiagram
    participant Device as Thiết bị ESP32
    participant MQTT as Máy chủ MQTT
    participant UDP as Máy chủ UDP

    Note over Device, UDP: 1. Thiết lập kết nối MQTT
    Device->>MQTT: MQTT Connect
    MQTT->>Device: Connected

    Note over Device, UDP: 2. Yêu cầu kênh âm thanh
    Device->>MQTT: Tin nhắn Hello (type: "hello", transport: "udp")
    MQTT->>Device: Phản hồi Hello (Thông tin kết nối UDP + Khóa mã hóa)

    Note over Device, UDP: 3. Thiết lập kết nối UDP
    Device->>UDP: UDP Connect
    UDP->>Device: Connected

    Note over Device, UDP: 4. Truyền dữ liệu âm thanh
    loop Truyền luồng âm thanh
        Device->>UDP: Dữ liệu âm thanh được mã hóa (Opus)
        UDP->>Device: Dữ liệu âm thanh được mã hóa (Opus)
    end

    Note over Device, UDP: 5. Trao đổi tin nhắn điều khiển
    par Tin nhắn điều khiển
        Device->>MQTT: Tin nhắn Listen/TTS/MCP
        MQTT->>Device: Phản hồi STT/TTS/MCP
    end

    Note over Device, UDP: 6. Đóng kết nối
    Device->>MQTT: Tin nhắn Goodbye
    Device->>UDP: Disconnect
```

---

## 3. Kênh Điều khiển MQTT

### 3.1 Thiết lập Kết nối

Thiết bị kết nối với máy chủ qua MQTT, các tham số kết nối bao gồm:
- **Endpoint**: Địa chỉ và cổng máy chủ MQTT
- **Client ID**: Định danh duy nhất của thiết bị
- **Username/Password**: Thông tin xác thực
- **Keep Alive**: Khoảng thời gian giữ kết nối (mặc định 240 giây)

### 3.2 Trao đổi Tin nhắn Hello

#### 3.2.1 Thiết bị gửi Hello

```json
{
  "type": "hello",
  "version": 3,
  "transport": "udp",
  "features": {
    "mcp": true
  },
  "audio_params": {
    "format": "opus",
    "sample_rate": 16000,
    "channels": 1,
    "frame_duration": 60
  }
}
```

#### 3.2.2 Máy chủ phản hồi Hello

```json
{
  "type": "hello",
  "transport": "udp",
  "session_id": "xxx",
  "audio_params": {
    "format": "opus",
    "sample_rate": 24000,
    "channels": 1,
    "frame_duration": 60
  },
  "udp": {
    "server": "192.168.1.100",
    "port": 8888,
    "key": "0123456789ABCDEF0123456789ABCDEF",
    "nonce": "0123456789ABCDEF0123456789ABCDEF"
  }
}
```

**Giải thích các trường:**
- `udp.server`: Địa chỉ máy chủ UDP
- `udp.port`: Cổng máy chủ UDP
- `udp.key`: Khóa mã hóa AES (chuỗi hex)
- `udp.nonce`: Số ngẫu nhiên mã hóa AES (chuỗi hex)

### 3.3 Loại Tin nhắn JSON

#### 3.3.1 Thiết bị → Máy chủ

1. **Tin nhắn Listen**
   ```json
   {
     "session_id": "xxx",
     "type": "listen",
     "state": "start",
     "mode": "manual"
   }
   ```

2. **Tin nhắn Abort**
   ```json
   {
     "session_id": "xxx",
     "type": "abort",
     "reason": "wake_word_detected"
   }
   ```

3. **Tin nhắn MCP**
   ```json
   {
     "session_id": "xxx",
     "type": "mcp",
     "payload": {
       "jsonrpc": "2.0",
       "id": 1,
       "result": {...}
     }
   }
   ```

4. **Tin nhắn Goodbye**
   ```json
   {
     "session_id": "xxx",
     "type": "goodbye"
   }
   ```

#### 3.3.2 Máy chủ → Thiết bị

Các loại tin nhắn được hỗ trợ tương tự như giao thức WebSocket, bao gồm:
- **STT**: Kết quả nhận dạng giọng nói
- **TTS**: Điều khiển tổng hợp giọng nói
- **LLM**: Điều khiển biểu cảm cảm xúc
- **MCP**: Điều khiển IoT
- **System**: Điều khiển hệ thống
- **Custom**: Tin nhắn tùy chỉnh (tùy chọn)

---

## 4. Kênh Âm thanh UDP

### 4.1 Thiết lập Kết nối

Sau khi nhận được phản hồi Hello từ MQTT, thiết bị sử dụng thông tin kết nối UDP trong đó để thiết lập kênh âm thanh:
1. Phân tích địa chỉ và cổng máy chủ UDP
2. Phân tích khóa mã hóa và số ngẫu nhiên
3. Khởi tạo ngữ cảnh mã hóa AES-CTR
4. Thiết lập kết nối UDP

### 4.2 Định dạng Dữ liệu Âm thanh

#### 4.2.1 Cấu trúc Gói Âm thanh được Mã hóa

```
|type 1byte|flags 1byte|payload_len 2bytes|ssrc 4bytes|timestamp 4bytes|sequence 4bytes|
|payload payload_len bytes|
```

**Giải thích các trường:**
- `type`: Loại gói tin, cố định là 0x01
- `flags`: Cờ hiệu, hiện không sử dụng
- `payload_len`: Độ dài tải trọng (thứ tự byte mạng)
- `ssrc`: Định danh nguồn đồng bộ hóa
- `timestamp`: Dấu thời gian (thứ tự byte mạng)
- `sequence`: Số thứ tự (thứ tự byte mạng)
- `payload`: Dữ liệu âm thanh Opus được mã hóa

#### 4.2.2 Thuật toán Mã hóa

Sử dụng chế độ **AES-CTR** để mã hóa:
- **Khóa**: 128 bit, do máy chủ cung cấp
- **Số ngẫu nhiên**: 128 bit, do máy chủ cung cấp
- **Bộ đếm**: Chứa thông tin dấu thời gian và số thứ tự

### 4.3 Quản lý Số thứ tự

- **Bên gửi**: `local_sequence_` tăng đơn điệu
- **Bên nhận**: `remote_sequence_` xác minh tính liên tục
- **Chống phát lại**: Từ chối các gói tin có số thứ tự nhỏ hơn giá trị mong đợi
- **Xử lý lỗi**: Cho phép các bước nhảy số thứ tự nhỏ, ghi lại cảnh báo

### 4.4 Xử lý Lỗi

1. **Giải mã thất bại**: Ghi lại lỗi, loại bỏ gói tin
2. **Bất thường về số thứ tự**: Ghi lại cảnh báo, nhưng vẫn xử lý gói tin
3. **Lỗi định dạng gói tin**: Ghi lại lỗi, loại bỏ gói tin

---

## 5. Quản lý Trạng thái

### 5.1 Trạng thái Kết nối

```mermaid
stateDiagram
    direction TB
    [*] --> Disconnected
    Disconnected --> MqttConnecting: StartMqttClient()
    MqttConnecting --> MqttConnected: MQTT Connected
    MqttConnecting --> Disconnected: Connect Failed
    MqttConnected --> RequestingChannel: OpenAudioChannel()
    RequestingChannel --> ChannelOpened: Hello Exchange Success
    RequestingChannel --> MqttConnected: Hello Timeout/Failed
    ChannelOpened --> UdpConnected: UDP Connect Success
    UdpConnected --> AudioStreaming: Start Audio Transfer
    AudioStreaming --> UdpConnected: Stop Audio Transfer
    UdpConnected --> ChannelOpened: UDP Disconnect
    ChannelOpened --> MqttConnected: CloseAudioChannel()
    MqttConnected --> Disconnected: MQTT Disconnect
```

### 5.2 Kiểm tra Trạng thái

Thiết bị xác định xem kênh âm thanh có khả dụng hay không thông qua các điều kiện sau:
```cpp
bool IsAudioChannelOpened() const {
    return udp_ != nullptr && !error_occurred_ && !IsTimeout();
}
```

---

## 6. Tham số Cấu hình

### 6.1 Cấu hình MQTT

Các mục cấu hình được đọc từ cài đặt:
- `endpoint`: Địa chỉ máy chủ MQTT
- `client_id`: Định danh máy khách
- `username`: Tên người dùng
- `password`: Mật khẩu
- `keepalive`: Khoảng thời gian giữ kết nối (mặc định 240 giây)
- `publish_topic`: Chủ đề xuất bản

### 6.2 Tham số Âm thanh

- **Định dạng**: Opus
- **Tốc độ lấy mẫu**: 16000 Hz (phía thiết bị) / 24000 Hz (phía máy chủ)
- **Số kênh**: 1 (đơn âm)
- **Thời lượng khung**: 60ms

---

## 7. Xử lý Lỗi và Kết nối lại

### 7.1 Cơ chế Kết nối lại MQTT

- Tự động thử lại khi kết nối thất bại
- Hỗ trợ điều khiển báo cáo lỗi
- Kích hoạt quy trình dọn dẹp khi ngắt kết nối

### 7.2 Quản lý Kết nối UDP

- Không tự động thử lại khi kết nối thất bại
- Phụ thuộc vào kênh MQTT để đàm phán lại
- Hỗ trợ truy vấn trạng thái kết nối

### 7.3 Xử lý Thời gian chờ

Lớp cơ sở `Protocol` cung cấp tính năng phát hiện thời gian chờ:
- Thời gian chờ mặc định: 120 giây
- Tính toán dựa trên thời gian nhận cuối cùng
- Tự động đánh dấu là không khả dụng khi hết thời gian chờ

---

## 8. Cân nhắc về Bảo mật

### 8.1 Mã hóa Truyền

- **MQTT**: Hỗ trợ mã hóa TLS/SSL (cổng 8883)
- **UDP**: Sử dụng AES-CTR để mã hóa dữ liệu âm thanh

### 8.2 Cơ chế Xác thực

- **MQTT**: Xác thực bằng tên người dùng/mật khẩu
- **UDP**: Phân phối khóa qua kênh MQTT

### 8.3 Chống Tấn công Phát lại

- Số thứ tự tăng đơn điệu
- Từ chối các gói tin đã hết hạn
- Xác minh dấu thời gian

---

## 9. Tối ưu hóa Hiệu suất

### 9.1 Kiểm soát Đồng thời

Sử dụng khóa mutex để bảo vệ kết nối UDP:
```cpp
std::lock_guard<std::mutex> lock(channel_mutex_);
```

### 9.2 Quản lý Bộ nhớ

- Tạo/hủy động các đối tượng mạng
- Quản lý gói dữ liệu âm thanh bằng con trỏ thông minh
- Giải phóng ngữ cảnh mã hóa kịp thời

### 9.3 Tối ưu hóa Mạng

- Tái sử dụng kết nối UDP
- Tối ưu hóa kích thước gói tin
- Kiểm tra tính liên tục của số thứ tự

---

## 10. So sánh với Giao thức WebSocket

| Đặc điểm | MQTT + UDP | WebSocket |
|---|---|---|
| Kênh điều khiển | MQTT | WebSocket |
| Kênh âm thanh | UDP (mã hóa) | WebSocket (nhị phân) |
| Tính thời gian thực | Cao (UDP) | Trung bình |
| Độ tin cậy | Trung bình | Cao |
| Độ phức tạp | Cao | Thấp |
| Mã hóa | AES-CTR | TLS |
| Mức độ thân thiện với tường lửa | Thấp | Cao |

---

## 11. Đề xuất Triển khai

### 11.1 Môi trường Mạng

- Đảm bảo cổng UDP có thể truy cập
- Cấu hình quy tắc tường lửa
- Cân nhắc vượt NAT

### 11.2 Cấu hình Máy chủ

- Cấu hình MQTT Broker
- Triển khai máy chủ UDP
- Hệ thống quản lý khóa

### 11.3 Chỉ số Giám sát

- Tỷ lệ kết nối thành công
- Độ trễ truyền âm thanh
- Tỷ lệ mất gói tin
- Tỷ lệ giải mã thất bại

---

## 12. Tổng kết

Giao thức hỗn hợp MQTT + UDP thực hiện giao tiếp âm thanh và video hiệu quả thông qua các thiết kế sau:

- **Kiến trúc tách biệt**: Tách biệt kênh điều khiển và dữ liệu, mỗi kênh thực hiện chức năng riêng
- **Bảo vệ bằng mã hóa**: AES-CTR đảm bảo truyền dữ liệu âm thanh an toàn
- **Quản lý tuần tự**: Ngăn chặn tấn công phát lại và mất trật tự dữ liệu
- **Tự động khôi phục**: Hỗ trợ tự động kết nối lại sau khi ngắt kết nối
- **Tối ưu hóa hiệu suất**: Truyền UDP đảm bảo tính thời gian thực của dữ liệu âm thanh

Giao thức này phù hợp với các kịch bản tương tác giọng nói có yêu cầu cao về tính thời gian thực, nhưng cần phải cân bằng giữa độ phức tạp của mạng và hiệu suất truyền. 

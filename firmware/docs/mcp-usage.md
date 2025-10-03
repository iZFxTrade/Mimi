# Hướng dẫn sử dụng Giao thức MCP để điều khiển IoT

> Tài liệu này mô tả cách triển khai điều khiển thiết bị ESP32 qua IoT dựa trên giao thức MCP. Để biết quy trình giao thức chi tiết, vui lòng tham khảo [`mcp-protocol.md`](./mcp-protocol.md).

## Giới thiệu

MCP (Model Context Protocol) là giao thức thế hệ mới được đề xuất để điều khiển IoT. Giao thức này sử dụng định dạng JSON-RPC 2.0 tiêu chuẩn để khám phá và gọi các "công cụ" (Tool) giữa backend và thiết bị, cho phép điều khiển thiết bị một cách linh hoạt.

## Quy trình sử dụng điển hình

1. Sau khi khởi động, thiết bị thiết lập kết nối với backend thông qua giao thức cơ bản (ví dụ: WebSocket/MQTT).
2. Backend khởi tạo phiên làm việc bằng phương thức `initialize` của giao thức MCP.
3. Backend sử dụng `tools/list` để lấy tất cả các công cụ (chức năng) được hỗ trợ bởi thiết bị và mô tả tham số của chúng.
4. Backend sử dụng `tools/call` để gọi một công cụ cụ thể, thực hiện việc điều khiển thiết bị.

Để biết định dạng và tương tác giao thức chi tiết, vui lòng xem [`mcp-protocol.md`](./mcp-protocol.md).

## Hướng dẫn đăng ký công cụ phía thiết bị

Thiết bị đăng ký các "công cụ" có thể được backend gọi thông qua phương thức `McpServer::AddTool`. Chữ ký hàm thường dùng như sau:

```cpp
void AddTool(
    const std::string& name,           // Tên công cụ, nên là duy nhất và có cấu trúc, ví dụ: self.dog.forward
    const std::string& description,    // Mô tả công cụ, giải thích ngắn gọn chức năng để mô hình lớn dễ hiểu
    const PropertyList& properties,    // Danh sách tham số đầu vào (có thể rỗng), hỗ trợ các kiểu: boolean, integer, string
    std::function<ReturnValue(const PropertyList&)> callback // Hàm callback được thực thi khi công cụ được gọi
);
```
- `name`: Định danh duy nhất của công cụ, khuyến nghị sử dụng quy tắc đặt tên "mô-đun.chức-năng".
- `description`: Mô tả bằng ngôn ngữ tự nhiên để AI/người dùng dễ hiểu.
- `properties`: Danh sách tham số, hỗ trợ các kiểu boolean, integer, string, có thể chỉ định phạm vi và giá trị mặc định.
- `callback`: Logic thực thi thực tế khi nhận được yêu cầu gọi, giá trị trả về có thể là bool/int/string.

## Ví dụ đăng ký điển hình (lấy ESP-Hi làm ví dụ)

```cpp
void InitializeTools() {
    auto& mcp_server = McpServer::GetInstance();
    // Ví dụ 1: Không có tham số, điều khiển robot tiến về phía trước
    mcp_server.AddTool("self.dog.forward", "Di chuyển robot về phía trước", PropertyList(), [this](const PropertyList&) -> ReturnValue {
        servo_dog_ctrl_send(DOG_STATE_FORWARD, NULL);
        return true;
    });
    // Ví dụ 2: Có tham số, đặt màu RGB của đèn
    mcp_server.AddTool("self.light.set_rgb", "Đặt màu RGB", PropertyList({
        Property("r", kPropertyTypeInteger, 0, 255),
        Property("g", kPropertyTypeInteger, 0, 255),
        Property("b", kPropertyTypeInteger, 0, 255)
    }), [this](const PropertyList& properties) -> ReturnValue {
        int r = properties["r"].value<int>();
        int g = properties["g"].value<int>();
        int b = properties["b"].value<int>();
        led_on_ = true;
        SetLedColor(r, g, b);
        return true;
    });
}
```

## Ví dụ về các lệnh gọi công cụ JSON-RPC phổ biến

### 1. Lấy danh sách công cụ
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": { "cursor": "" },
  "id": 1
}
```

### 2. Điều khiển khung gầm tiến về phía trước
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.chassis.go_forward",
    "arguments": {}
  },
  "id": 2
}
```

### 3. Chuyển đổi chế độ đèn
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.chassis.switch_light_mode",
    "arguments": { "light_mode": 3 }
  },
  "id": 3
}
```

### 4. Lật camera
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "self.camera.set_camera_flipped",
    "arguments": {}
  },
  "id": 4
}
```

## Ghi chú
- Tên công cụ, tham số và giá trị trả về phải dựa trên đăng ký `AddTool` phía thiết bị.
- Khuyến nghị tất cả các dự án mới nên thống nhất sử dụng giao thức MCP để điều khiển IoT.
- Để biết giao thức chi tiết và cách sử dụng nâng cao, vui lòng tham khảo [`mcp-protocol.md`](./mcp-protocol.md).

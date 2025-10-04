# Thư mục Protocols

Thư mục `protocols` chứa mã nguồn triển khai các giao thức giao tiếp mạng khác nhau mà thiết bị sử dụng để kết nối và trao đổi dữ liệu với máy chủ.

## Cấu trúc và Chức năng

- **`protocol.h/.cc`**: Định nghĩa một lớp cơ sở (base class) trừu tượng cho các giao thức. Lớp này cung cấp một giao diện chung cho việc khởi tạo, kết nối, ngắt kết nối và xử lý dữ liệu. Các lớp giao thức cụ thể sẽ kế thừa từ lớp này.

- **`mqtt_protocol.h/.cc`**: Triển khai giao thức MQTT (Message Queuing Telemetry Transport). MQTT là một giao thức nhắn tin publish-subscribe nhẹ, rất phù hợp cho các thiết bị IoT. Lớp này xử lý việc kết nối đến một MQTT broker, đăng ký các chủ đề (topic), và gửi/nhận tin nhắn.

- **`websocket_protocol.h/.cc`**: Triển khai giao thức WebSocket. WebSocket cung cấp một kênh giao tiếp hai chiều, song công (full-duplex) qua một kết nối TCP duy nhất. Nó cho phép giao tiếp thời gian thực hiệu quả giữa thiết bị và máy chủ.

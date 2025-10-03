# Thư mục `main`

Đây là thư mục cốt lõi của dự án, chứa toàn bộ logic ứng dụng của chatbot.

## Cấu trúc thư mục

- `application.cc`/`.h`: Tệp chính điều phối các thành phần của ứng dụng.
- `main.cc`: Điểm khởi đầu của chương trình.
- `mcp_server.cc`/`.h`: Triển khai máy chủ MCP (Master Control Program) để xử lý các lệnh điều khiển.
- `audio/`: Quản lý tất cả các chức năng liên quan đến âm thanh, từ thu âm, xử lý đến phát lại.
- `display/`: Chịu trách nhiệm hiển thị giao diện người dùng, biểu cảm và các thông tin khác.
- `led/`: Điều khiển các hiệu ứng đèn LED.
- `protocols/`: Quản lý các giao thức kết nối mạng như MQTT và WebSocket.
- `assets/`: Chứa các tài nguyên tĩnh như âm thanh, font chữ, và ngôn ngữ.
- `boards/`: Định nghĩa và cấu hình cho các bo mạch phần cứng khác nhau. Chúng ta sẽ tạo một cấu hình mới cho MiMi trong này.

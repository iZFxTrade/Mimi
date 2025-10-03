# Thư mục `boards`

Thư mục này chứa các tệp cấu hình dành riêng cho từng bo mạch phần cứng mà dự án hỗ trợ.

## Mục đích

Mỗi bo mạch có cách kết nối chân (pinout), trình điều khiển (driver) cho các linh kiện ngoại vi (màn hình, micro, loa) khác nhau. Thư mục này giúp tách biệt phần cấu hình phần cứng ra khỏi logic chính của ứng dụng.

## Cách hoạt động

Khi biên dịch dự án, chúng ta sẽ chọn một cấu hình bo mạch cụ thể. Trình biên dịch sẽ chỉ sử dụng các tệp trong thư mục con tương ứng với bo mạch đó.

## Tùy biến cho MiMi (ESP32-CYD)

Chúng ta sẽ tạo một thư mục con mới ở đây, ví dụ là `mimi-cyd`, để chứa các tệp sau:

- `config.h`: Định nghĩa các chân GPIO cho màn hình, micro (I2S), loa, và các linh kiện khác của ESP32-CYD.
- `config.json`: Cấu hình các thông số mặc định khác.
- `mimi-cyd.cc`: Khởi tạo và đăng ký bo mạch vào hệ thống.

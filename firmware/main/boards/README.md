# Thư mục `boards`

Thư mục này chứa các tệp cấu hình dành riêng cho từng bo mạch phần cứng mà dự án hỗ trợ.

## Mục đích

Mỗi bo mạch có sơ đồ chân và trình điều khiển khác nhau cho các thành phần ngoại vi (màn hình, micrô, loa). Thư mục này giúp tách biệt cấu hình phần cứng khỏi logic ứng dụng chính.

## Cách thức hoạt động

Khi biên dịch dự án, chúng tôi sẽ chọn một cấu hình bo mạch cụ thể. Trình biên dịch sẽ chỉ sử dụng các tệp trong thư mục con tương ứng với bo mạch đó.

## Tùy chỉnh cho MiMi (ESP32-CYD)

Chúng tôi sẽ tạo một thư mục con mới ở đây, ví dụ `mimi-cyd`, để chứa các tệp sau:

- `config.h`: Xác định các chân GPIO cho màn hình, micrô (I2S), loa và các thành phần khác của ESP32-CYD.
- `config.json`: Cấu hình các tham số mặc định khác.
- `mimi-cyd.cc`: Khởi tạo và đăng ký bo mạch với hệ thống.

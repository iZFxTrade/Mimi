# Thư mục LED

Thư mục `led` chứa các lớp và mã nguồn để điều khiển các loại đèn LED khác nhau được sử dụng làm chỉ báo trạng thái trên thiết bị.

## Cấu trúc và Chức năng

- **`led.h`**: Định nghĩa một giao diện (interface) trừu tượng cho việc điều khiển đèn LED. Bất kỳ lớp điều khiển LED cụ thể nào cũng phải kế thừa từ lớp `Led` này và triển khai các phương thức của nó.

- **`single_led.h/.cc`**: Triển khai việc điều khiển một đèn LED đơn. Nó cung cấp các phương thức để bật, tắt, và nhấp nháy đèn LED.

- **`circular_strip.h/.cc`**: Triển khai việc điều khiển một dải đèn LED tròn (circular LED strip), thường là các dải LED định địa chỉ như NeoPixel. Lớp này cho phép tạo ra các hiệu ứng ánh sáng phức tạp hơn.

- **`gpio_led.h/.cc`**: Một lớp triển khai cụ thể sử dụng các chân GPIO để điều khiển đèn LED.

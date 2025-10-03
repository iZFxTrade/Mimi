# Bảng phân vùng phiên bản 2

Phiên bản này giới thiệu những cải tiến đáng kể so với v1 bằng cách thêm phân vùng `assets` để hỗ trợ nội dung có thể tải qua mạng và tối ưu hóa bố cục phân vùng cho các kích thước flash khác nhau.

## Những thay đổi chính so với v1

### Cải tiến chính
1. **Đã thêm phân vùng tài sản**: Phân vùng `assets` mới cho nội dung có thể tải qua mạng
2. **Đã thay thế phân vùng mô hình**: Phân vùng `model` cũ (960KB) được thay thế bằng phân vùng `assets` lớn hơn
3. **Các phân vùng ứng dụng được tối ưu hóa**: Giảm kích thước phân vùng ứng dụng để chứa tài sản
4. **Tăng cường tính linh hoạt**: Hỗ trợ cập nhật nội dung động mà không cần flash lại

### Các tính năng của phân vùng tài sản
Phân vùng `assets` lưu trữ:
- **Mô hình từ đánh thức**: Các mô hình từ đánh thức có thể tùy chỉnh có thể được tải từ mạng
- **Tệp chủ đề**: Hệ thống chủ đề hoàn chỉnh bao gồm:
  - Phông chữ (phông chữ văn bản và biểu tượng)
  - Hiệu ứng âm thanh và tệp âm thanh
  - Hình nền và các yếu tố giao diện người dùng
  - Gói biểu tượng cảm xúc tùy chỉnh
  - Tệp cấu hình ngôn ngữ
- **Nội dung động**: Tất cả nội dung có thể được cập nhật qua mạng thông qua tải xuống HTTP

## So sánh bố cục phân vùng

### Bố cục v1 (16MB)
- `nvs`: 16KB (bộ nhớ không bay hơi)
- `otadata`: 8KB (dữ liệu OTA)
- `phy_init`: 4KB (dữ liệu khởi tạo PHY)
- `model`: 960KB (lưu trữ mô hình - nội dung cố định)
- `ota_0`: 6MB (phân vùng ứng dụng 0)
- `ota_1`: 6MB (phân vùng ứng dụng 1)

### Bố cục v2 (16MB)
- `nvs`: 16KB (bộ nhớ không bay hơi)
- `otadata`: 8KB (dữ liệu OTA)
- `phy_init`: 4KB (dữ liệu khởi tạo PHY)
- `ota_0`: 4MB (phân vùng ứng dụng 0)
- `ota_1`: 4MB (phân vùng ứng dụng 1)
- `assets`: 8MB (tài sản có thể tải qua mạng)

## Các cấu hình có sẵn

### Thiết bị flash 8MB (`8m.csv`)
- `nvs`: 16KB
- `otadata`: 8KB
- `phy_init`: 4KB
- `ota_0`: 3MB
- `ota_1`: 3MB
- `assets`: 2MB

### Thiết bị flash 16MB (`16m.csv`) - Tiêu chuẩn
- `nvs`: 16KB
- `otadata`: 8KB
- `phy_init`: 4KB
- `ota_0`: 4MB
- `ota_1`: 4MB
- `assets`: 8MB

### Thiết bị flash 16MB (`16m_c3.csv`) - Tối ưu hóa cho ESP32-C3
- `nvs`: 16KB
- `otadata`: 8KB
- `phy_init`: 4KB
- `ota_0`: 4MB
- `ota_1`: 4MB
- `assets`: 4MB (4000K - bị giới hạn bởi các trang mmap có sẵn)

### Thiết bị flash 32MB (`32m.csv`)
- `nvsfactory`: 200KB
- `nvs`: 840KB
- `otadata`: 8KB
- `phy_init`: 4KB
- `ota_0`: 4MB
- `ota_1`: 4MB
- `assets`: 16MB

## Lợi ích

1. **Quản lý nội dung động**: Người dùng có thể tải xuống và cập nhật các mô hình từ đánh thức, chủ đề và các tài sản khác mà không cần flash lại thiết bị
2. **Giảm kích thước ứng dụng**: Các phân vùng ứng dụng được tối ưu hóa, cho phép có nhiều không gian hơn cho nội dung động
3. **Tăng cường tùy chỉnh**: Hỗ trợ các chủ đề, từ đánh thức và gói ngôn ngữ tùy chỉnh giúp nâng cao trải nghiệm người dùng
4. **Tính linh hoạt của mạng**: Tài sản có thể được cập nhật độc lập với chương trình cơ sở ứng dụng chính
5. **Sử dụng tài nguyên tốt hơn**: Sử dụng hiệu quả bộ nhớ flash với bộ nhớ tài sản có thể định cấu hình
6. **Cập nhật tài sản OTA**: Tài sản có thể được cập nhật qua mạng thông qua tải xuống HTTP

## Chi tiết kỹ thuật

- **Loại phân vùng**: Phân vùng tài sản sử dụng kiểu con `spiffs` để tương thích với hệ thống tệp SPIFFS
- **Ánh xạ bộ nhớ**: Tài sản được ánh xạ bộ nhớ để truy cập hiệu quả trong thời gian chạy
- **Xác thực tổng kiểm tra**: Kiểm tra tính toàn vẹn tích hợp đảm bảo tính hợp lệ của dữ liệu tài sản
- **Tải xuống lũy tiến**: Tài sản có thể được tải xuống lũy tiến với theo dõi tiến trình
- **Hỗ trợ dự phòng**: Quay trở lại tài sản mặc định một cách duyên dáng nếu cập nhật mạng không thành công

## Di chuyển từ v1

Khi nâng cấp từ v1 lên v2:
1. **Sao lưu dữ liệu quan trọng**: Đảm bảo mọi dữ liệu quan trọng trong phân vùng `model` cũ đều được sao lưu
2. **Flash bảng phân vùng mới**: Sử dụng bảng phân vùng v2 thích hợp cho kích thước flash của bạn
3. **Tải xuống tài sản**: Thiết bị sẽ tự động tải xuống các tài sản cần thiết trong lần khởi động đầu tiên
4. **Xác minh chức năng**: Đảm bảo tất cả các tính năng hoạt động chính xác với bố cục phân vùng mới

## Ghi chú sử dụng

- Kích thước phân vùng `assets` thay đổi theo cấu hình để tối ưu hóa cho các kích thước flash khác nhau
- Các thiết bị ESP32-C3 sử dụng phân vùng tài sản nhỏ hơn (4MB) do số lượng trang mmap có sẵn trong hệ thống bị giới hạn
- Các thiết bị 32MB có phân vùng tài sản lớn nhất (16MB) để lưu trữ nội dung tối đa
- Tất cả các bảng phân vùng đều duy trì sự căn chỉnh phù hợp để có hiệu suất flash tối ưu

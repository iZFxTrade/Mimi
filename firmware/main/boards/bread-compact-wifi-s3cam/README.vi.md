Phần cứng dựa trên bo mạch phát triển ESP32S3CAM, mã được sửa đổi từ bread-compact-wifi-lcd
Camera được sử dụng là OV2640
Lưu ý rằng vì camera chiếm nhiều chân IO nên nó chiếm hai chân USB 19 và 20 của ESP32S3
Để biết phương pháp nối dây, hãy tham khảo định nghĩa chân trong tệp config.h

 
# Lệnh cấu hình biên dịch

**Đặt mục tiêu biên dịch thành ESP32S3:**

```bash
idf.py set-target esp32s3
```

**Mở menuconfig:**

```bash
idf.py menuconfig
```

**Chọn bo mạch:**

```
Xiaozhi Assistant -> Board Type ->配線 phiên bản mới của bảng mạch (WiFi) + LCD + Camera
```

**Biên dịch và nạp:**

```bash
idf.py build flash
```
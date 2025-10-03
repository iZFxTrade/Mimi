minsi-k08-wifi và minsi-k08-ml307 là các giải pháp robot trò chuyện AI Xiaozhi mang phong cách punk với loa lớn và pin lớn, do Minsi Technology ra mắt. Chúng dựa trên ESP32S3N16R8, được trang bị bộ khuếch đại công suất âm thanh MAX98357 và mô-đun micrô đa hướng INMP441, và được tạo ra bằng cách sửa đổi loa pháo cơ trong suốt K08.

<a href="https://item.taobao.com/item.htm?id=889892765588" target="_blank" title="SenseCAP Watcher">Minsi-k08</a>

  <a href="minsi-k08.jpg" target="_blank" title="Minsi-k08">
    <img src="minsi-k08.jpg" width="240" />
  </a>



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
Xiaozhi Assistant -> Board Type ->Minsi Technology K08(DUAL)
```

**Biên dịch và nạp:**

```bash
idf.py build flash
```
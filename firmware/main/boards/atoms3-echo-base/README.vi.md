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
Xiaozhi Assistant -> Board Type -> AtomS3 + Echo Base
```

**Tắt tính năng đánh thức bằng giọng nói:**

```
Xiaozhi Assistant -> [ ] Bật tính năng đánh thức bằng giọng nói và xử lý âm thanh -> Bỏ chọn
```

**Sửa đổi kích thước flash:**

```
Serial flasher config -> Flash size -> 8 MB
```

**Sửa đổi bảng phân vùng:**

```
Partition Table -> Custom partition CSV file -> partitions/v2/8m.csv
```

**Tắt PSRAM ngoài:**

```
Component config -> ESP PSRAM -> [ ] Hỗ trợ RAM ngoài, kết nối qua SPI -> Bỏ chọn
```

**Biên dịch:**

```bash
idf.py build
```

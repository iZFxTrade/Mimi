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
Xiaozhi Assistant -> Board Type -> AtomS3R + Echo Base
```

**Sửa đổi kích thước flash:**

```
Serial flasher config -> Flash size -> 8 MB
```

**Sửa đổi bảng phân vùng:**

```
Partition Table -> Custom partition CSV file -> partitions/v2/8m.csv
```

**Sửa đổi cấu hình psram:**

```
Component config -> ESP PSRAM -> SPI RAM config -> Mode (QUAD/OCT) -> Octal Mode PSRAM
```

**Biên dịch:**

```bash
idf.py build
```

# DFRobot Xingkong K10

## Cấu hình nút
* A: Nhấn nhanh - ngắt/đánh thức, nhấn giữ 1 giây - tăng âm lượng
* B: Nhấn nhanh - ngắt/đánh thức, nhấn giữ 1 giây - giảm âm lượng

## Lệnh cấu hình biên dịch

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
Xiaozhi Assistant -> Board Type -> DFRobot Xingkong K10
```

**Sửa đổi cấu hình psram:**

```
Component config -> ESP PSRAM -> SPI RAM config -> Mode (QUAD/OCT) -> Octal Mode PSRAM
```

**Biên dịch:**

```bash
idf.py build
```
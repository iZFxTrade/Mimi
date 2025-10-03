# Hộp đồng hành AI của Sibo Zhilian

# Tính năng
* Sử dụng micrô PDM
* Sử dụng đèn LED cực dương chung

## Cấu hình nút
* BUTTON3: Nhấn nhanh - ngắt/đánh thức
* BUTTON1: Âm lượng+
* BUTTON2: Âm lượng-

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
Xiaozhi Assistant -> Board Type -> Hộp đồng hành AI của Sibo Zhilian
```

**Sửa đổi cấu hình psram:**

```
Component config -> ESP PSRAM -> SPI RAM config -> Mode (QUAD/OCT) -> Octal Mode PSRAM
```

**Biên dịch:**

```bash
idf.py build
```
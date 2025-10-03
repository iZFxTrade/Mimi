# Mô-đun Camera AI DFRobot ESP32-S3

## Giới thiệu
ESP32-S3 AI CAM là một mô-đun camera thông minh được thiết kế dựa trên chip ESP32-S3, chuyên dùng để xử lý hình ảnh video và tương tác bằng giọng nói, phù hợp cho các dự án AI như giám sát video, nhận dạng hình ảnh ở vùng biên và đối thoại bằng giọng nói.
![](https://ws.dfrobot.com.cn/FsTrGbrX2NZAwzWS8OSQGOGikuYA)

[Nhấp để xem giới thiệu chi tiết](https://wiki.dfrobot.com.cn/SKU_DFR1154_ESP32_S3_AI_CAM)

[Nhấp để xem trình diễn chức năng thị giác](https://www.bilibili.com/video/BV1ktjSzNEUU/)

# Tính năng
* Sử dụng micrô PDM
* Camera OV3660 tích hợp

## Cấu hình nút
* BOOT: Nhấn nhanh - ngắt/đánh thức

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
Xiaozhi Assistant -> Board Type -> Mô-đun Camera AI DFRobot ESP32-S3
```

**Sửa đổi cấu hình psram:**

```
Component config -> ESP PSRAM -> SPI RAM config -> Mode (QUAD/OCT) -> Octal Mode PSRAM
```

**Sửa đổi công suất phát WiFi thành 10:**

```
Component config -> PHY -> (10)Max WiFi TX power (dBm)
```

**Biên dịch:**

```bash
idf.py build
```
# ESP-BOX-3

## Giới thiệu

<div align="center">
    <a href="https://github.com/espressif/esp-box"><b> ESP-BOX GitHub </b></a>
</div>

ESP-BOX-3 là bộ công cụ phát triển AIoT do Espressif Systems chính thức phát triển, được trang bị mô-đun ESP32-S3-WROOM-1, màn hình ILI9341 2.4 inch 320x240, mảng micrô kép, hỗ trợ đánh thức bằng giọng nói ngoại tuyến và chức năng khử tiếng vọng phía thiết bị (AEC).

## Tính năng phần cứng

- **Bộ điều khiển chính**: ESP32-S3-WROOM-1 (16MB Flash, 8MB PSRAM)
- **Màn hình**: 2.4 inch IPS LCD (320x240, ILI9341)
- **Âm thanh**: ES8311 Audio Codec + ES7210 Dual-mic ADC
- **Chức năng âm thanh**: Hỗ trợ AEC phía thiết bị (Khử tiếng vọng)
- **Nút bấm**: Nút Boot (chức năng nhấn một lần/nhấn đúp)
- **Khác**: Cấp nguồn và giao tiếp qua USB-C

## Lệnh cấu hình và biên dịch

**Đặt mục tiêu biên dịch thành ESP32S3**

```bash
idf.py set-target esp32s3
```

**Mở menuconfig và cấu hình**

```bash
idf.py menuconfig
```

Cấu hình các tùy chọn sau:

### Cấu hình cơ bản
- `Xiaozhi Assistant` → `Board Type` → chọn `ESP BOX 3`

### Lựa chọn phong cách giao diện người dùng (UI)

ESP-BOX-3 hỗ trợ nhiều phong cách hiển thị UI khác nhau, được cấu hình thông qua menuconfig:

- `Xiaozhi Assistant` → `Select display style` → chọn phong cách hiển thị

#### Các phong cách tùy chọn

##### Phong cách hoạt hình biểu cảm (Emote animation style) - Khuyến nghị
- **Tùy chọn cấu hình**: `USE_EMOTE_MESSAGE_STYLE`
- **Đặc điểm**: Sử dụng hệ thống hiển thị biểu cảm `EmoteDisplay` tùy chỉnh
- **Chức năng**: Hỗ trợ hoạt hình biểu cảm phong phú, hoạt hình mắt, hiển thị biểu tượng trạng thái
- **Áp dụng**: Các tình huống trợ lý thông minh, mang lại trải nghiệm tương tác người-máy sống động hơn
- **Lớp**: `emote::EmoteDisplay`

**⚠️ Quan trọng**: Chọn phong cách này yêu cầu cấu hình thêm tệp tài nguyên tùy chỉnh:
1. `Xiaozhi Assistant` → `Flash Assets` → chọn `Flash Custom Assets`
2. `Xiaozhi Assistant` → `Custom Assets File` → điền địa chỉ tệp tài nguyên:
   ```
   https://dl.espressif.com/AE/wn9_nihaoxiaozhi_tts-font_puhui_common_20_4-esp-box-3.bin
   ```

##### Phong cách tin nhắn mặc định (Enable default message style)
- **Tùy chọn cấu hình**: `USE_DEFAULT_MESSAGE_STYLE` (mặc định)
- **Đặc điểm**: Sử dụng giao diện hiển thị tin nhắn tiêu chuẩn
- **Chức năng**: Giao diện hiển thị văn bản và biểu tượng truyền thống
- **Áp dụng**: Các tình huống hội thoại tiêu chuẩn
- **Lớp**: `SpiLcdDisplay`

##### Phong cách tin nhắn WeChat (Enable WeChat Message Style)
- **Tùy chọn cấu hình**: `USE_WECHAT_MESSAGE_STYLE`
- **Đặc điểm**: Phong cách giao diện trò chuyện mô phỏng WeChat
- **Chức năng**: Hiển thị bong bóng tin nhắn tương tự như WeChat
- **Áp dụng**: Dành cho người dùng yêu thích phong cách WeChat
- **Lớp**: `SpiLcdDisplay`

### Cấu hình chức năng âm thanh

#### Khử tiếng vọng phía thiết bị (AEC)
- `Xiaozhi Assistant` → `Enable Device-Side AEC` → Bật

Phần cứng ESP-BOX-3 hỗ trợ chức năng AEC phía thiết bị, có thể loại bỏ hiệu quả nhiễu từ âm thanh phát ra từ loa đến micrô, cải thiện độ chính xác của nhận dạng giọng nói.

**Chuyển đổi trong khi chạy**: Nhấn đúp vào nút Boot để bật/tắt chức năng AEC trong khi chạy.

> **Lưu ý**: AEC phía thiết bị cần một đường dẫn tham chiếu đầu ra loa sạch và cách ly vật lý tốt giữa micrô và loa để hoạt động bình thường. Phần cứng ESP-BOX-3 đã được tối ưu hóa thiết kế.

### Cấu hình từ đánh thức

ESP-BOX-3 hỗ trợ nhiều cách triển khai từ đánh thức:

- `Xiaozhi Assistant` → `Wake Word Implementation Type` → chọn loại từ đánh thức

Khuyến nghị chọn:
- **Wakenet model with AFE** (`USE_AFE_WAKE_WORD`) - Phát hiện từ đánh thức hỗ trợ AEC

Nhấn `S` để lưu, nhấn `Q` để thoát.

**Biên dịch**

```bash
idf.py build
```

**Nạp chương trình**

Kết nối ESP-BOX-3 với máy tính và chạy:

```bash
idf.py flash
```

## Hướng dẫn sử dụng nút bấm

### Chức năng nút Boot

#### Nhấn một lần
- **Trạng thái cấu hình mạng**: Vào chế độ cấu hình WiFi
- **Trạng thái rảnh**: Bắt đầu hội thoại
- **Trong khi hội thoại**: Ngắt hoặc dừng hội thoại hiện tại

#### Nhấn đúp (cần bật AEC phía thiết bị)
- **Trạng thái rảnh**: Chuyển đổi bật/tắt AEC

## Câu hỏi thường gặp

### 1. Tại sao cần AEC phía thiết bị?
AEC phía thiết bị có thể loại bỏ nhiễu từ âm thanh phát ra từ loa đến micrô trong thời gian thực tại chỗ, cho phép nhận dạng chính xác các lệnh thoại ngay cả khi đang phát nhạc hoặc phản hồi TTS.

### 2. Phong cách hoạt hình biểu cảm không hiển thị?
Vui lòng đảm bảo rằng bạn đã cấu hình đúng địa chỉ tệp tài nguyên tùy chỉnh và thiết bị có thể truy cập URL đó để tải xuống tài nguyên.

### 3. Làm cách nào để khôi phục cài đặt gốc?
Nhấn và giữ nút Boot trong hơn 3 giây, thiết bị sẽ xóa tất cả cấu hình và khởi động lại.

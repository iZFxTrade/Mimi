# ✅ Danh sách công việc dự án MiMi

Đây là danh sách các công việc cần làm để hoàn thành dự án, dựa trên `Roadmap ToDo` trong file README.md. Tôi sẽ thực hiện tuần tự, chi tiết và đánh dấu khi hoàn thành.

## Giai đoạn 0: Kiểm tra và Phân tích Hiện trạng

-   [x] **Phân tích cấu trúc file và tài liệu**:
    -   [x] Đọc các file `README.md`, `README.vi.md` và các tài liệu trong thư mục `docs`.
    -   [x] Xác định hệ thống build dùng Kconfig và CMake.
    -   [x] Xác định UI dùng LVGL.
    -   [x] Xác định giao thức giao tiếp là WebSocket/MQTT.
-   [x] **Kiểm tra mã nguồn driver phần cứng**:
    -   [x] Phân tích `display/lcd_display.cc` -> **Kết luận: Tương thích** thông qua `esp_lcd` và `lvgl_port`, không cần sửa đổi.
    -   [x] Tìm hiểu cách tích hợp driver cảm ứng -> **Kết luận: Tương thích** thông qua `esp_lcd_touch` và `lvgl_port`.
-   [x] **Kiểm tra luồng hoạt động của ứng dụng**:
    -   [x] Phân tích `main.cc` -> **Kết luận:** Luồng chính được bắt đầu bởi `Application::GetInstance().Start()`.
    -   [x] Phân tích `application.cc` -> **Kết luận:** Nắm rõ luồng khởi tạo (Board -> Display -> Audio -> Network -> Protocol).

**==> Giai đoạn 0 hoàn tất. Đã có đủ thông tin để bắt đầu Giai đoạn 1.**

---

## Giai đoạn 1: Tích hợp phần cứng và UI cơ bản

Mục tiêu: Khởi động thiết bị, màn hình hiển thị "Xin chào MiMi!" và cảm ứng hoạt động.

-   [ ] **1.1. Tích hợp `mimi-cyd` vào hệ thống build:**
    -   [ ] **1.1.1.** Chỉnh sửa file `firmware/main/Kconfig.projbuild` để thêm lựa chọn `BOARD_TYPE_MIMI_CYD` trong menu cấu hình.
    -   [ ] **1.1.2.** (Dành cho người dùng) Hướng dẫn người dùng chạy `idf.py menuconfig`, chọn board "MiMi CYD" và lưu lại cấu hình.
-   [ ] **1.2. Hoàn thiện lớp Board `mimi-cyd`:**
    -   [ ] **1.2.1.** Cập nhật `firmware/main/boards/mimi-cyd/config.h` với đầy đủ các chân GPIO cho màn hình (SPI) và cảm ứng (SPI, IRQ).
    -   [ ] **1.2.2.** Chỉnh sửa `firmware/main/boards/mimi-cyd/mimi-cyd.cc` để implement lớp `MimiCydBoard`:
        -   [ ] **a.** Khai báo class `MimiCydBoard` kế thừa từ `WifiBoard`.
        -   [ ] **b.** Implement phương thức `_create_display()`:
            -   [ ] Khởi tạo bus SPI cho màn hình (MOSI, CLK, CS).
            -   [ ] Khởi tạo panel IO handle cho màn hình (`esp_lcd_panel_io_spi_create`).
            -   [ ] Khởi tạo driver `esp_lcd` cho ILI9341 (`esp_lcd_new_panel_ili9341`).
            -   [ ] Khởi tạo bus SPI riêng cho cảm ứng (nếu cần, hoặc dùng chung bus).
            -   [ ] Khởi tạo driver `esp_lcd_touch` cho XPT2046 (`esp_lcd_touch_new_spi_xpt2046`).
            -   [ ] Tạo đối tượng `SpiLcdDisplay` và trả về.
        -   [ ] **c.** Implement phương thức `Start()` kế thừa:
            -   [ ] Gọi `WifiBoard::Start()`.
            -   [ ] Đăng ký driver cảm ứng với `lvgl_port` (`lvgl_port_add_touch`).
        -   [ ] **d.** Implement các phương thức `_create_audio_codec()` (trả về `NoAudioCodec`) và `_create_led()` (trả về `nullptr`).
        -   [ ] **e.** Viết hàm `board_register_mimi_cyd()` để tạo instance của `MimiCydBoard`.
    -   [ ] **1.2.3.** Chỉnh sửa `firmware/main/boards/common/board.cc` để gọi `board_register_mimi_cyd()` khi `CONFIG_BOARD_TYPE_MIMI_CYD` được định nghĩa.
-   [ ] **1.3. Xây dựng giao diện UI "Xin chào MiMi!":**
    -   [ ] **1.3.1.** (Tùy chọn) Tạo một file UI mới (ví dụ: `mimi_ui.cc`) để chứa code giao diện.
    -   [ ] **1.3.2.** Chỉnh sửa hàm `LcdDisplay::SetupUI()` trong `lcd_display.cc` để thêm code tạo một `lv_label` với nội dung "Xin chào MiMi!".
-   [ ] **1.4. Hoàn tất Giai đoạn 1:**
    -   [ ] **1.4.1.** Thông báo cho người dùng về việc hoàn thành, hướng dẫn cách biên dịch và nạp firmware.
    -   [ ] **1.4.2.** Kiểm tra lại toàn bộ các bước đã đánh dấu `[x]`.

---

## Giai đoạn 2 – Tích hợp thông minh
...

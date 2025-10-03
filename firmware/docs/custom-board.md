# Hướng dẫn tùy chỉnh bo mạch phát triển

Hướng dẫn này mô tả cách tùy chỉnh một chương trình khởi tạo bo mạch phát triển mới cho dự án robot trò chuyện bằng giọng nói AI Xiaozhi. Xiaozhi AI hỗ trợ hơn 70 loại bo mạch phát triển dòng ESP32, mã khởi tạo cho mỗi bo mạch được đặt trong thư mục tương ứng.

## Lưu ý quan trọng

> **Cảnh báo**: Đối với bo mạch phát triển tùy chỉnh, khi cấu hình IO khác với bo mạch phát triển ban đầu, tuyệt đối không được ghi đè trực tiếp lên cấu hình của bo mạch ban đầu để biên dịch firmware. Phải tạo một loại bo mạch mới, hoặc sử dụng cấu hình `builds` trong tệp `config.json` để phân biệt bằng các tên và macro sdkconfig khác nhau. Sử dụng `python scripts/release.py [tên thư mục bo mạch phát triển]` để biên dịch và đóng gói firmware.
>
> Nếu bạn ghi đè trực tiếp lên cấu hình ban đầu, trong tương lai khi nâng cấp OTA, firmware tùy chỉnh của bạn có thể bị ghi đè bởi firmware tiêu chuẩn của bo mạch phát triển ban đầu, dẫn đến việc thiết bị của bạn không thể hoạt động bình thường. Mỗi bo mạch phát triển có một định danh duy nhất và kênh nâng cấp firmware tương ứng, việc giữ cho định danh của bo mạch phát triển là duy nhất rất quan trọng.

## Cấu trúc thư mục

Mỗi thư mục bo mạch phát triển thường bao gồm các tệp sau:

- `xxx_board.cc` - Mã khởi tạo cấp bo mạch chính, thực hiện khởi tạo và các chức năng liên quan đến bo mạch
- `config.h` - Tệp cấu hình cấp bo mạch, định nghĩa ánh xạ chân phần cứng và các tùy chọn cấu hình khác
- `config.json` - Cấu hình biên dịch, chỉ định chip mục tiêu và các tùy chọn biên dịch đặc biệt
- `README.md` - Tài liệu hướng dẫn liên quan đến bo mạch phát triển

## Các bước tùy chỉnh bo mạch phát triển

### 1. Tạo thư mục bo mạch phát triển mới

Đầu tiên, tạo một thư mục mới trong thư mục `boards/`, đặt tên theo định dạng `[tên thương hiệu]-[loại bo mạch]`, ví dụ `m5stack-tab5`:

```bash
mkdir main/boards/my-custom-board
```

### 2. Tạo tệp cấu hình

#### config.h

Trong `config.h`, định nghĩa tất cả các cấu hình phần cứng, bao gồm:

- Tốc độ lấy mẫu âm thanh và cấu hình chân I2S
- Địa chỉ chip codec âm thanh và cấu hình chân I2C
- Cấu hình chân nút bấm và đèn LED
- Tham số và cấu hình chân màn hình hiển thị

Tham khảo ví dụ (từ lichuang-c3-dev):

```c
#ifndef _BOARD_CONFIG_H_
#define _BOARD_CONFIG_H_

#include <driver/gpio.h>

// Cấu hình âm thanh
#define AUDIO_INPUT_SAMPLE_RATE  24000
#define AUDIO_OUTPUT_SAMPLE_RATE 24000

#define AUDIO_I2S_GPIO_MCLK GPIO_NUM_10
#define AUDIO_I2S_GPIO_WS   GPIO_NUM_12
#define AUDIO_I2S_GPIO_BCLK GPIO_NUM_8
#define AUDIO_I2S_GPIO_DIN  GPIO_NUM_7
#define AUDIO_I2S_GPIO_DOUT GPIO_NUM_11

#define AUDIO_CODEC_PA_PIN       GPIO_NUM_13
#define AUDIO_CODEC_I2C_SDA_PIN  GPIO_NUM_0
#define AUDIO_CODEC_I2C_SCL_PIN  GPIO_NUM_1
#define AUDIO_CODEC_ES8311_ADDR  ES8311_CODEC_DEFAULT_ADDR

// Cấu hình nút bấm
#define BOOT_BUTTON_GPIO        GPIO_NUM_9

// Cấu hình màn hình hiển thị
#define DISPLAY_SPI_SCK_PIN     GPIO_NUM_3
#define DISPLAY_SPI_MOSI_PIN    GPIO_NUM_5
#define DISPLAY_DC_PIN          GPIO_NUM_6
#define DISPLAY_SPI_CS_PIN      GPIO_NUM_4

#define DISPLAY_WIDTH   320
#define DISPLAY_HEIGHT  240
#define DISPLAY_MIRROR_X true
#define DISPLAY_MIRROR_Y false
#define DISPLAY_SWAP_XY true

#define DISPLAY_OFFSET_X  0
#define DISPLAY_OFFSET_Y  0

#define DISPLAY_BACKLIGHT_PIN GPIO_NUM_2
#define DISPLAY_BACKLIGHT_OUTPUT_INVERT true

#endif // _BOARD_CONFIG_H_
```

#### config.json

Trong `config.json`, định nghĩa cấu hình biên dịch, tệp này được sử dụng bởi script `scripts/release.py` để tự động hóa quá trình biên dịch:

```json
{
    "target": "esp32s3",  // Mẫu chip mục tiêu: esp32, esp32s3, esp32c3, esp32c6, esp32p4, v.v.
    "builds": [
        {
            "name": "my-custom-board",  // Tên bo mạch phát triển, được sử dụng để tạo gói firmware
            "sdkconfig_append": [
                // Cấu hình kích thước Flash đặc biệt
                "CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y",
                // Cấu hình bảng phân vùng đặc biệt
                "CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/8m.csv\""
            ]
        }
    ]
}
```

**Giải thích cấu hình:**
- `target`: Mẫu chip mục tiêu, phải khớp với phần cứng
- `name`: Tên gói firmware đầu ra của quá trình biên dịch, nên giống với tên thư mục
- `sdkconfig_append`: Mảng các tùy chọn cấu hình sdkconfig bổ sung, sẽ được thêm vào cấu hình mặc định

**Các cấu hình sdkconfig_append thường dùng:**
```json
// Kích thước Flash
"CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y"   // 4MB Flash
"CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y"   // 8MB Flash
"CONFIG_ESPTOOLPY_FLASHSIZE_16MB=y"  // 16MB Flash

// Bảng phân vùng
"CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/4m.csv\""  // Bảng phân vùng 4MB
"CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/8m.csv\""  // Bảng phân vùng 8MB
"CONFIG_PARTITION_TABLE_CUSTOM_FILENAME=\"partitions/v2/16m.csv\"" // Bảng phân vùng 16MB

// Cấu hình ngôn ngữ
"CONFIG_LANGUAGE_EN_US=y"  // Tiếng Anh
"CONFIG_LANGUAGE_ZH_CN=y"  // Tiếng Trung giản thể

// Cấu hình từ đánh thức
"CONFIG_USE_DEVICE_AEC=y"          // Bật AEC phía thiết bị
"CONFIG_WAKE_WORD_DISABLED=y"      // Tắt từ đánh thức
```

### 3. Viết mã khởi tạo cấp bo mạch

Tạo một tệp `my_custom_board.cc`, triển khai tất cả logic khởi tạo của bo mạch phát triển.

Một định nghĩa lớp bo mạch phát triển cơ bản bao gồm các phần sau:

1. **Định nghĩa lớp**: Kế thừa từ `WifiBoard` hoặc `Ml307Board`
2. **Hàm khởi tạo**: Bao gồm khởi tạo các thành phần như I2C, màn hình hiển thị, nút bấm, IoT, v.v.
3. **Ghi đè hàm ảo**: Chẳng hạn như `GetAudioCodec()`, `GetDisplay()`, `GetBacklight()`, v.v.
4. **Đăng ký bo mạch phát triển**: Sử dụng macro `DECLARE_BOARD` để đăng ký bo mạch phát triển

```cpp
#include "wifi_board.h"
#include "codecs/es8311_audio_codec.h"
#include "display/lcd_display.h"
#include "application.h"
#include "button.h"
#include "config.h"
#include "mcp_server.h"

#include <esp_log.h>
#include <driver/i2c_master.h>
#include <driver/spi_common.h>

#define TAG "MyCustomBoard"

class MyCustomBoard : public WifiBoard {
private:
    i2c_master_bus_handle_t codec_i2c_bus_;
    Button boot_button_;
    LcdDisplay* display_;

    // Khởi tạo I2C
    void InitializeI2c() {
        i2c_master_bus_config_t i2c_bus_cfg = {
            .i2c_port = I2C_NUM_0,
            .sda_io_num = AUDIO_CODEC_I2C_SDA_PIN,
            .scl_io_num = AUDIO_CODEC_I2C_SCL_PIN,
            .clk_source = I2C_CLK_SRC_DEFAULT,
            .glitch_ignore_cnt = 7,
            .intr_priority = 0,
            .trans_queue_depth = 0,
            .flags = {
                .enable_internal_pullup = 1,
            },
        };
        ESP_ERROR_CHECK(i2c_new_master_bus(&i2c_bus_cfg, &codec_i2c_bus_));
    }

    // Khởi tạo SPI (cho màn hình hiển thị)
    void InitializeSpi() {
        spi_bus_config_t buscfg = {};
        buscfg.mosi_io_num = DISPLAY_SPI_MOSI_PIN;
        buscfg.miso_io_num = GPIO_NUM_NC;
        buscfg.sclk_io_num = DISPLAY_SPI_SCK_PIN;
        buscfg.quadwp_io_num = GPIO_NUM_NC;
        buscfg.quadhd_io_num = GPIO_NUM_NC;
        buscfg.max_transfer_sz = DISPLAY_WIDTH * DISPLAY_HEIGHT * sizeof(uint16_t);
        ESP_ERROR_CHECK(spi_bus_initialize(SPI2_HOST, &buscfg, SPI_DMA_CH_AUTO));
    }

    // Khởi tạo nút bấm
    void InitializeButtons() {
        boot_button_.OnClick([this]() {
            auto& app = Application::GetInstance();
            if (app.GetDeviceState() == kDeviceStateStarting && !WifiStation::GetInstance().IsConnected()) {
                ResetWifiConfiguration();
            }
            app.ToggleChatState();
        });
    }

    // Khởi tạo màn hình hiển thị (ví dụ với ST7789)
    void InitializeDisplay() {
        esp_lcd_panel_io_handle_t panel_io = nullptr;
        esp_lcd_panel_handle_t panel = nullptr;
        
        esp_lcd_panel_io_spi_config_t io_config = {};
        io_config.cs_gpio_num = DISPLAY_SPI_CS_PIN;
        io_config.dc_gpio_num = DISPLAY_DC_PIN;
        io_config.spi_mode = 2;
        io_config.pclk_hz = 80 * 1000 * 1000;
        io_config.trans_queue_depth = 10;
        io_config.lcd_cmd_bits = 8;
        io_config.lcd_param_bits = 8;
        ESP_ERROR_CHECK(esp_lcd_new_panel_io_spi(SPI2_HOST, &io_config, &panel_io));

        esp_lcd_panel_dev_config_t panel_config = {};
        panel_config.reset_gpio_num = GPIO_NUM_NC;
        panel_config.rgb_ele_order = LCD_RGB_ELEMENT_ORDER_RGB;
        panel_config.bits_per_pixel = 16;
        ESP_ERROR_CHECK(esp_lcd_new_panel_st7789(panel_io, &panel_config, &panel));
        
        esp_lcd_panel_reset(panel);
        esp_lcd_panel_init(panel);
        esp_lcd_panel_invert_color(panel, true);
        esp_lcd_panel_swap_xy(panel, DISPLAY_SWAP_XY);
        esp_lcd_panel_mirror(panel, DISPLAY_MIRROR_X, DISPLAY_MIRROR_Y);
        
        // Tạo đối tượng màn hình hiển thị
        display_ = new SpiLcdDisplay(panel_io, panel,
                                    DISPLAY_WIDTH, DISPLAY_HEIGHT, 
                                    DISPLAY_OFFSET_X, DISPLAY_OFFSET_Y, 
                                    DISPLAY_MIRROR_X, DISPLAY_MIRROR_Y, DISPLAY_SWAP_XY);
    }

    // Khởi tạo MCP Tools
    void InitializeTools() {
        // Tham khảo tài liệu MCP
    }

public:
    // Hàm khởi tạo
    MyCustomBoard() : boot_button_(BOOT_BUTTON_GPIO) {
        InitializeI2c();
        InitializeSpi();
        InitializeDisplay();
        InitializeButtons();
        InitializeTools();
        GetBacklight()->SetBrightness(100);
    }

    // Lấy codec âm thanh
    virtual AudioCodec* GetAudioCodec() override {
        static Es8311AudioCodec audio_codec(
            codec_i2c_bus_, 
            I2C_NUM_0, 
            AUDIO_INPUT_SAMPLE_RATE, 
            AUDIO_OUTPUT_SAMPLE_RATE,
            AUDIO_I2S_GPIO_MCLK, 
            AUDIO_I2S_GPIO_BCLK, 
            AUDIO_I2S_GPIO_WS, 
            AUDIO_I2S_GPIO_DOUT, 
            AUDIO_I2S_GPIO_DIN,
            AUDIO_CODEC_PA_PIN, 
            AUDIO_CODEC_ES8311_ADDR);
        return &audio_codec;
    }

    // Lấy màn hình hiển thị
    virtual Display* GetDisplay() override {
        return display_;
    }
    
    // Lấy điều khiển đèn nền
    virtual Backlight* GetBacklight() override {
        static PwmBacklight backlight(DISPLAY_BACKLIGHT_PIN, DISPLAY_BACKLIGHT_OUTPUT_INVERT);
        return &backlight;
    }
};

// Đăng ký bo mạch phát triển
DECLARE_BOARD(MyCustomBoard);
```

### 4. Thêm cấu hình hệ thống xây dựng

#### Thêm tùy chọn bo mạch phát triển trong Kconfig.projbuild

Mở tệp `main/Kconfig.projbuild`, trong phần `choice BOARD_TYPE`, thêm tùy chọn cấu hình bo mạch phát triển mới:

```kconfig
choice BOARD_TYPE
    prompt "Board Type"
    default BOARD_TYPE_BREAD_COMPACT_WIFI
    help
        Board type. Loại bo mạch phát triển
    
    # ... các tùy chọn bo mạch phát triển khác ...
    
    config BOARD_TYPE_MY_CUSTOM_BOARD
        bool "My Custom Board (Bo mạch tùy chỉnh của tôi)"
        depends on IDF_TARGET_ESP32S3  # Sửa đổi tùy theo chip mục tiêu của bạn
endchoice
```

**Lưu ý:**
- `BOARD_TYPE_MY_CUSTOM_BOARD` là tên tùy chọn cấu hình, cần viết hoa toàn bộ và sử dụng dấu gạch dưới để phân tách
- `depends on` chỉ định loại chip mục tiêu (chẳng hạn như `IDF_TARGET_ESP32S3`, `IDF_TARGET_ESP32C3`, v.v.)
- Văn bản mô tả có thể sử dụng tiếng Việt và tiếng Anh

#### Thêm cấu hình bo mạch phát triển trong CMakeLists.txt

Mở tệp `main/CMakeLists.txt`, trong phần phán đoán loại bo mạch phát triển, thêm cấu hình mới:

```cmake
# Thêm cấu hình bo mạch phát triển của bạn trong chuỗi elseif
elseif(CONFIG_BOARD_TYPE_MY_CUSTOM_BOARD)
    set(BOARD_TYPE "my-custom-board")  // Giống với tên thư mục
    set(BUILTIN_TEXT_FONT font_puhui_basic_20_4)  // Chọn phông chữ phù hợp với kích thước màn hình
    set(BUILTIN_ICON_FONT font_awesome_20_4)
    set(DEFAULT_EMOJI_COLLECTION twemoji_64)  // Tùy chọn, nếu cần hiển thị biểu tượng cảm xúc
endif()
```

**Giải thích cấu hình phông chữ và biểu tượng cảm xúc:**

Chọn kích thước phông chữ phù hợp với độ phân giải màn hình:
- Màn hình nhỏ (128x64 OLED): `font_puhui_basic_14_1` / `font_awesome_14_1`
- Màn hình vừa và nhỏ (240x240): `font_puhui_basic_16_4` / `font_awesome_16_4`
- Màn hình trung bình (240x320): `font_puhui_basic_20_4` / `font_awesome_20_4`
- Màn hình lớn (480x320+): `font_puhui_basic_30_4` / `font_awesome_30_4`

Các tùy chọn bộ sưu tập biểu tượng cảm xúc:
- `twemoji_32` - Biểu tượng cảm xúc 32x32 pixel (màn hình nhỏ)
- `twemoji_64` - Biểu tượng cảm xúc 64x64 pixel (màn hình lớn)

### 5. Cấu hình và biên dịch

#### Phương pháp một: Sử dụng idf.py để cấu hình thủ công

1. **Đặt chip mục tiêu** (lần cấu hình đầu tiên hoặc khi thay đổi chip):
   ```bash
   # Đối với ESP32-S3
   idf.py set-target esp32s3
   
   # Đối với ESP32-C3
   idf.py set-target esp32c3
   
   # Đối với ESP32
   idf.py set-target esp32
   ```

2. **Xóa cấu hình cũ**:
   ```bash
   idf.py fullclean
   ```

3. **Vào menu cấu hình**:
   ```bash
   idf.py menuconfig
   ```
   
   Trong menu, điều hướng đến: `Xiaozhi Assistant` -> `Board Type`, chọn bo mạch phát triển tùy chỉnh của bạn.

4. **Biên dịch và nạp**:
   ```bash
   idf.py build
   idf.py flash monitor
   ```

#### Phương pháp hai: Sử dụng script release.py (khuyến nghị)

Nếu thư mục bo mạch phát triển của bạn có tệp `config.json`, bạn có thể sử dụng script này để tự động hoàn thành cấu hình và biên dịch:

```bash
python scripts/release.py my-custom-board
```

Script này sẽ tự động:
- Đọc `target` trong `config.json` và đặt chip mục tiêu
- Áp dụng các tùy chọn biên dịch trong `sdkconfig_append`
- Hoàn thành biên dịch và đóng gói firmware

### 6. Tạo README.md

Trong README.md, giải thích các tính năng, yêu cầu phần cứng, các bước biên dịch và nạp của bo mạch phát triển:


## Các thành phần bo mạch phát triển phổ biến

### 1. Màn hình hiển thị

Dự án hỗ trợ nhiều trình điều khiển màn hình, bao gồm:
- ST7789 (SPI)
- ILI9341 (SPI)
- SH8601 (QSPI)
- v.v...

### 2. Codec âm thanh

Các codec được hỗ trợ bao gồm:
- ES8311 (thường dùng)
- ES7210 (mảng micro)
- AW88298 (bộ khuếch đại công suất)
- v.v...

### 3. Quản lý nguồn

Một số bo mạch phát triển sử dụng chip quản lý nguồn:
- AXP2101
- Các PMIC khác có sẵn

### 4. Điều khiển thiết bị MCP

Bạn có thể thêm các công cụ MCP khác nhau để AI có thể sử dụng:
- Speaker (điều khiển loa)
- Screen (điều chỉnh độ sáng màn hình)
- Battery (đọc mức pin)
- Light (điều khiển đèn)
- v.v...

## Mối quan hệ kế thừa của các lớp bo mạch phát triển

- `Board` - Lớp bo mạch cơ sở
  - `WifiBoard` - Bo mạch phát triển kết nối Wi-Fi
  - `Ml307Board` - Bo mạch phát triển sử dụng mô-đun 4G
  - `DualNetworkBoard` - Bo mạch phát triển hỗ trợ chuyển đổi giữa mạng Wi-Fi và 4G

## Mẹo phát triển

1. **Tham khảo các bo mạch phát triển tương tự**: Nếu bo mạch mới của bạn có những điểm tương đồng với các bo mạch hiện có, bạn có thể tham khảo các triển khai hiện có
2. **Gỡ lỗi từng bước**: Trước tiên, triển khai các chức năng cơ bản (chẳng hạn như hiển thị), sau đó thêm các chức năng phức tạp hơn (chẳng hạn như âm thanh)
3. **Ánh xạ chân**: Đảm bảo cấu hình chính xác tất cả các ánh xạ chân trong config.h
4. **Kiểm tra tính tương thích của phần cứng**: Xác nhận tính tương thích của tất cả các chip và trình điều khiển

## Các vấn đề có thể gặp phải

1. **Màn hình hiển thị không bình thường**: Kiểm tra cấu hình SPI, cài đặt phản chiếu và cài đặt đảo ngược màu
2. **Không có đầu ra âm thanh**: Kiểm tra cấu hình I2S, chân bật PA và địa chỉ codec
3. **Không thể kết nối mạng**: Kiểm tra thông tin đăng nhập Wi-Fi và cấu hình mạng
4. **Không thể giao tiếp với máy chủ**: Kiểm tra cấu hình MQTT hoặc WebSocket

## Tài liệu tham khảo

- Tài liệu ESP-IDF: https://docs.espressif.com/projects/esp-idf/
- Tài liệu LVGL: https://docs.lvgl.io/
- Tài liệu ESP-SR: https://github.com/espressif/esp-sr

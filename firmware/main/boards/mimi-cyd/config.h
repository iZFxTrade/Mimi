#ifndef MIMI_CYD_CONFIG_H
#define MIMI_CYD_CONFIG_H

// =================================================================
// ==           PINOUT CONFIGURATION FOR MIMI-CYD                 ==
// ==         (Based on ESP32-2432S028R - Cheap Yellow Display)    ==
// =================================================================

// -- 1. TFT Display (ILI9341 - SPI)
#define LCD_HOST         SPI2_HOST
#define PIN_NUM_MISO     12
#define PIN_NUM_MOSI     13
#define PIN_NUM_CLK      14
#define PIN_NUM_CS       15
#define PIN_NUM_DC       2
#define PIN_NUM_RST      -1 // Not connected
#define PIN_NUM_BCKL     21

// -- 2. Touchscreen (XPT2046 - SPI)
// Note: Shares SPI bus with the display
#define TOUCH_HOST       SPI3_HOST
#define TOUCH_PIN_NUM_MISO  39
#define TOUCH_PIN_NUM_MOSI  32
#define TOUCH_PIN_NUM_CLK   25
#define TOUCH_PIN_NUM_CS    33
#define TOUCH_PIN_IRQ    36

// -- 3. SD Card (SPI)
#define SD_HOST          SPI1_HOST
#define SD_PIN_NUM_MISO  19
#define SD_PIN_NUM_MOSI  23
#define SD_PIN_NUM_CLK   18
#define SD_PIN_NUM_CS    5

// -- 4. Audio - I2S Microphone (INMP441)
#define I2S_MIC_HOST         I2S_NUM_0
#define I2S_MIC_PIN_BCK      27
#define I2S_MIC_PIN_WS       22
#define I2S_MIC_PIN_DATA     35

// -- 5. Audio - Speaker Output (NS4168 using I2S)
#define I2S_SPEAKER_HOST     I2S_NUM_1
#define I2S_SPEAKER_PIN_BCK  -1 // Not used in DAC mode
#define I2S_SPEAKER_PIN_WS   -1 // Not used in DAC mode
#define I2S_SPEAKER_PIN_DATA 26 // DAC_1

// -- 6. On-board RGB LED
#define RGB_LED_PIN_R    4
#define RGB_LED_PIN_G    16
#define RGB_LED_PIN_B    17

#endif // MIMI_CYD_CONFIG_H

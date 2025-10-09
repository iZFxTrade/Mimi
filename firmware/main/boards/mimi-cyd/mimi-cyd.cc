#include "application.h"
#include "mcp_server.h"
#include "display/lcd_display.h"
#include "audio/audio_service.h"
#include "audio/codecs/no_audio_codec.h"
#include "audio/processors/default_audio_processor.h" // Use the default processor
#include "audio/wake_words/no_wake_word.h"
#include "common/wifi_board.h"
#include "common/i2c_device.h"
#include "led/rgb_led.h" // Include the RGB LED header

#include "mimi-cyd/config.h"

// Board-specific class implementing the Board interface
class MimiCydBoard : public WifiBoard {
public:
    const char *GetName() override {
        return "mimi-cyd";
    }

    void Init() override {
        WifiBoard::Init();
        // Board-specific initialization
        led->SetColor(255, 0, 0); // Set initial color to Red
    }

    Display *GetDisplay() override {
        return display;
    }

    AudioService *GetAudio() override {
        return audio_service;
    }

    Led *GetLed() override {
        return led;
    }

    MimiCydBoard() {
        // Initialize I2C for potential expansions
        i2c = new I2cDevice(I2C_NUM_0, -1, -1);

        // Initialize the LCD display with touch
        display = new LcdDisplay(
            PIN_NUM_BCKL,
            LCD_HOST,
            PIN_NUM_CS,
            PIN_NUM_DC,
            PIN_NUM_CLK,
            PIN_NUM_MOSI,
            PIN_NUM_MISO,
            PIN_NUM_RST,
            TOUCH_PIN_IRQ,
            TOUCH_HOST,
            TOUCH_PIN_NUM_CS,
            TOUCH_PIN_NUM_CLK,
            TOUCH_PIN_NUM_MOSI,
            TOUCH_PIN_NUM_MISO,
            -1 // Touch IRQ already passed above
        );

        // Initialize the Audio Service with I2S microphone and DAC speaker
        audio_service = new AudioService(
            new NoWakeWord(),
            new DefaultAudioProcessor(), // Use the default audio processor
            new NoAudioCodecSimplex(
                16000, // input sample rate
                16000, // output sample rate
                I2S_SPEAKER_PIN_BCK,
                I2S_SPEAKER_PIN_WS,
                (gpio_num_t)I2S_SPEAKER_PIN_DATA,
                I2S_MIC_PIN_BCK,
                I2S_MIC_PIN_WS,
                I2S_MIC_PIN_DATA
            )
        );

        // Initialize the RGB LED
        led = new RgbLed(RGB_LED_PIN_R, RGB_LED_PIN_G, RGB_LED_PIN_B, 3, true);
    }

    ~MimiCydBoard() {
        delete display;
        delete audio_service;
        delete i2c;
        delete led;
    }

private:
    LcdDisplay *display;
    AudioService *audio_service;
    I2cDevice *i2c;
    RgbLed *led;
};

// Function to register the board with the system
void board_register_mimi_cyd() {
    static MimiCydBoard board;
    Board::Register(&board);
    printf("Board '%s' registered\n", board.GetName());
}

// Register MiMi CYD as the default board implementation when this target is selected.
DECLARE_BOARD(MimiCydBoard);

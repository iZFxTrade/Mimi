
#include "application.h"
#include "mcp_server.h"
#include "display/lcd_display.h"
#include "audio/audio_service.h"
#include "audio/codecs/no_audio_codec.h"
#include "audio/processors/no_audio_processor.h"
#include "audio/wake_words/no_wake_word.h"
#include "common/wifi_board.h"
#include "common/i2c_device.h"

#include "mimi-cyd/config.h"

// Board-specific class implementing the Board interface
class MimiCydBoard : public WifiBoard {
public:
    const char *GetName() override {
        return "mimi-cyd";
    }

    void Init() override {
        WifiBoard::Init();
        // Here you can add any board-specific initialization code
    }

    Display *GetDisplay() override {
        return display;
    }

    AudioService *GetAudio() override {
        // Audio is disabled for now, will be implemented in the next steps
        return audio_service;
    }

    Led *GetLed() override {
        // TODO: Implement RGB LED control
        return nullptr;
    }

    MimiCydBoard() {
        // Initialize I2C for potential expansions, even if not used by default
        i2c = new I2cDevice(I2C_NUM_0, -1, -1);

        // Initialize the LCD display
        display = new LcdDisplay(
            PIN_NUM_BCKL,
            LCD_HOST,
            PIN_NUM_CS,
            PIN_NUM_DC,
            PIN_NUM_CLK,
            PIN_NUM_MOSI,
            -1, // MISO not used
            PIN_NUM_RST,
            -1, // IRQ not used
            TOUCH_HOST,
            TOUCH_PIN_NUM_CS,
            TOUCH_PIN_NUM_CLK,
            TOUCH_PIN_NUM_MOSI,
            TOUCH_PIN_NUM_MISO,
            TOUCH_PIN_IRQ
        );

        // Initialize a placeholder audio service (NoAudio)
        // This will be replaced with the actual I2S implementation later
        audio_service = new AudioService(
            new NoWakeWord(),
            new NoAudioProcessor(),
            new NoAudioCodec()
        );
    }

    ~MimiCydBoard() {
        delete display;
        delete audio_service;
        delete i2c;
    }

private:
    LcdDisplay *display;
    AudioService *audio_service;
    I2cDevice *i2c;
};

// Function to register the board
void board_register_mimi_cyd() {
    static MimiCydBoard board;
    Board::Register(&board);
    printf("Board '%s' registered\n", board.GetName());
}

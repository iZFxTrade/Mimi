#ifndef LCD_DISPLAY_H
#define LCD_DISPLAY_H

#include "lvgl_display/lvgl_display.h"
#include "view_manager.h"

#include <memory>
#include <vector>

#include <esp_lcd_panel_io.h>
#include <esp_lcd_panel_ops.h>

class LcdDisplay : public LvglDisplay {
public:
    LcdDisplay(esp_lcd_panel_io_handle_t panel_io, esp_lcd_panel_handle_t panel, int width, int height);
    virtual ~LcdDisplay();

    void SetChatMessage(const char* role, const char* content);
    void SetEmotion(const char* emotion);
    void SetTheme(Theme* theme) override;

protected:
    bool Lock(int timeout_ms) override;
    void Unlock() override;

    void InitializeLcdThemes();
    void SetupUI();

    esp_lcd_panel_io_handle_t panel_io_ = nullptr;
    esp_lcd_panel_handle_t panel_ = nullptr;
    
    int width_ = 0;
    int height_ = 0;

    // UI Objects
    lv_obj_t* container_ = nullptr;
    lv_obj_t* status_bar_ = nullptr;
    lv_obj_t* content_ = nullptr;
    lv_obj_t* nav_bar_ = nullptr; // Navigation bar

    // Chat-related UI objects that might be part of a future ChatView
    lv_obj_t* chat_message_label_ = nullptr; // Temporary, for basic chat display

    // Preview image handling
    lv_obj_t* preview_image_ = nullptr;
    esp_timer_handle_t preview_timer_ = nullptr;
    std::unique_ptr<LvglImage> preview_image_cached_;
};

class SpiLcdDisplay : public LcdDisplay {
public:
    SpiLcdDisplay(esp_lcd_panel_io_handle_t panel_io, esp_lcd_panel_handle_t panel,
                  int width, int height, int offset_x, int offset_y,
                  bool mirror_x, bool mirror_y, bool swap_xy);
};

class RgbLcdDisplay : public LcdDisplay {
public:
    RgbLcdDisplay(esp_lcd_panel_io_handle_t panel_io, esp_lcd_panel_handle_t panel,
                  int width, int height, int offset_x, int offset_y,
                  bool mirror_x, bool mirror_y, bool swap_xy);
};

class MipiLcdDisplay : public LcdDisplay {
public:
    MipiLcdDisplay(esp_lcd_panel_io_handle_t panel_io, esp_lcd_panel_handle_t panel,
                   int width, int height, int offset_x, int offset_y,
                   bool mirror_x, bool mirror_y, bool swap_xy);
};


#endif // LCD_DISPLAY_H

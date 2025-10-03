#include "lcd_display.h"
#include "settings.h"
#include "lvgl_theme.h"
#include "assets/lang_config.h"
#include "view_manager.h"
#include "assistant_face_view.h"
#include "chat_view.h"
#include "dashboard_view.h"
#include "learning_tutor_view.h"
#include "reports_view.h"
#include "smart_home_view.h"
#include "settings_view.h"
#include "media_view.h"
#include "extensions_view.h"

#include <vector>
#include <algorithm>
#include <font_awesome.h>
#include <esp_log.h>
#include <esp_err.h>
#include <esp_lvgl_port.h>
#include <esp_psram.h>
#include <cstring>

#include "board.h"

#define TAG "LcdDisplay"

LV_FONT_DECLARE(BUILTIN_TEXT_FONT);
LV_FONT_DECLARE(BUILTIN_ICON_FONT);
LV_FONT_DECLARE(font_awesome_30_4);

// Event handler for navigation buttons
static void nav_btn_event_cb(lv_event_t * e)
{
    lv_obj_t * btn = lv_event_get_target(e);
    const char* view_name = (const char*)lv_event_get_user_data(e);
    if (btn && view_name) {
        ViewManager::GetInstance().SetView(view_name);
    }
}

// Forward declaration
void LcdDisplay::InitializeLcdThemes() {
    auto text_font = std::make_shared<LvglBuiltInFont>(&BUILTIN_TEXT_FONT);
    auto icon_font = std::make_shared<LvglBuiltInFont>(&BUILTIN_ICON_FONT);
    auto large_icon_font = std::make_shared<LvglBuiltInFont>(&font_awesome_30_4);

    // light theme
    auto light_theme = new LvglTheme("light");
    light_theme->set_background_color(lv_color_hex(0xFFFFFF));
    light_theme->set_text_color(lv_color_hex(0x000000));
    light_theme->set_text_font(text_font);
    light_theme->set_icon_font(icon_font);
    light_theme->set_large_icon_font(large_icon_font);

    // dark theme
    auto dark_theme = new LvglTheme("dark");
    dark_theme->set_background_color(lv_color_hex(0x000000));
    dark_theme->set_text_color(lv_color_hex(0xFFFFFF));
    dark_theme->set_text_font(text_font);
    dark_theme->set_icon_font(icon_font);
    dark_theme->set_large_icon_font(large_icon_font);

    auto& theme_manager = LvglThemeManager::GetInstance();
    theme_manager.RegisterTheme("light", light_theme);
    theme_manager.RegisterTheme("dark", dark_theme);
}

LcdDisplay::LcdDisplay(esp_lcd_panel_io_handle_t panel_io, esp_lcd_panel_handle_t panel, int width, int height)
    : panel_io_(panel_io), panel_(panel) {
    width_ = width;
    height_ = height;

    InitializeLcdThemes();

    Settings settings("display", false);
    std::string theme_name = settings.GetString("theme", "light");
    current_theme_ = LvglThemeManager::GetInstance().GetTheme(theme_name);

     esp_timer_create_args_t preview_timer_args = {
        .callback = [](void* arg) {
            LcdDisplay* display = static_cast<LcdDisplay*>(arg);
            display->SetPreviewImage(nullptr);
        },
        .arg = this,
        .dispatch_method = ESP_TIMER_TASK,
        .name = "preview_timer",
        .skip_unhandled_events = false,
    };
    esp_timer_create(&preview_timer_args, &preview_timer_);
}

SpiLcdDisplay::SpiLcdDisplay(esp_lcd_panel_io_handle_t panel_io, esp_lcd_panel_handle_t panel,
                           int width, int height, int offset_x, int offset_y, bool mirror_x, bool mirror_y, bool swap_xy)
    : LcdDisplay(panel_io, panel, width, height) {

    // ... (LVGL and display initialization as before) ...
    ESP_ERROR_CHECK(esp_lcd_panel_disp_on_off(panel_, true));
    lv_init();
    lvgl_port_cfg_t port_cfg = ESP_LVGL_PORT_INIT_CONFIG();
    lvgl_port_init(&port_cfg);
    const lvgl_port_display_cfg_t display_cfg = {
        .io_handle = panel_io_,
        .panel_handle = panel_,
        // ...
    };
    display_ = lvgl_port_add_disp(&display_cfg);
    
    SetupUI();
}

LcdDisplay::~LcdDisplay() {
     if (preview_timer_ != nullptr) {
        esp_timer_stop(preview_timer_);
        esp_timer_delete(preview_timer_);
    }

    if (nav_bar_) lv_obj_del(nav_bar_);
    if (content_) lv_obj_del(content_);
    if (status_bar_) lv_obj_del(status_bar_);
    if (container_) lv_obj_del(container_);
    
    // ... (rest of destructor)
}

bool LcdDisplay::Lock(int timeout_ms) {
    return lvgl_port_lock(timeout_ms);
}

void LcdDisplay::Unlock() {
    lvgl_port_unlock();
}

void LcdDisplay::SetupUI() {
    DisplayLockGuard lock(this);

    auto lvgl_theme = static_cast<LvglTheme*>(current_theme_);
    auto screen = lv_screen_active();
    lv_obj_set_style_bg_color(screen, lvgl_theme->background_color(), 0);

    container_ = lv_obj_create(screen);
    lv_obj_set_size(container_, LV_HOR_RES, LV_VER_RES);
    lv_obj_set_flex_flow(container_, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(container_, 0, 0);
    lv_obj_set_style_border_width(container_, 0, 0);

    status_bar_ = lv_obj_create(container_);
    lv_obj_set_size(status_bar_, LV_HOR_RES, LV_SIZE_CONTENT);

    content_ = lv_obj_create(container_);
    lv_obj_set_style_radius(content_, 0, 0);
    lv_obj_set_width(content_, LV_HOR_RES);
    lv_obj_set_flex_grow(content_, 1);
    lv_obj_set_style_pad_all(content_, 0, 0);

    // Setup ViewManager
    auto& vm = ViewManager::GetInstance();
    vm.RegisterView("face", std::make_shared<AssistantFaceView>());
    vm.RegisterView("chat", std::make_shared<ChatView>());
    vm.RegisterView("dashboard", std::make_shared<DashboardView>());
    vm.RegisterView("learning", std::make_shared<LearningTutorView>());
    vm.RegisterView("reports", std::make_shared<ReportsView>());
    vm.RegisterView("smarthome", std::make_shared<SmartHomeView>());
    vm.RegisterView("media", std::make_shared<MediaView>());
    vm.RegisterView("settings", std::make_shared<SettingsView>());
    vm.RegisterView("extensions", std::make_shared<ExtensionsView>());
    vm.Create(content_);

    // Navigation Bar
    nav_bar_ = lv_obj_create(container_);
    lv_obj_set_size(nav_bar_, LV_HOR_RES, 40);
    lv_obj_set_flex_flow(nav_bar_, LV_FLEX_FLOW_ROW);
    lv_obj_set_style_pad_all(nav_bar_, 0, 0);
    lv_obj_set_style_main_place(nav_bar_, LV_MAIN_AXIS_ALIGN_SPACE_AROUND, 0);
    lv_obj_set_style_cross_place(nav_bar_, LV_CROSS_AXIS_ALIGN_CENTER, 0);

    const auto& views = vm.GetViews();
    for(const auto& pair : views) {
        const char* view_name = pair.first.c_str();
        lv_obj_t* btn = lv_btn_create(nav_bar_);
        lv_obj_add_event_cb(btn, nav_btn_event_cb, LV_EVENT_CLICKED, (void*)view_name);
        lv_obj_t* label = lv_label_create(btn);

        if (strcmp(view_name, "face") == 0) {
            lv_label_set_text(label, FONT_AWESOME_USER);
        } else if (strcmp(view_name, "chat") == 0) {
            lv_label_set_text(label, FONT_AWESOME_COMMENT);
        } else if (strcmp(view_name, "dashboard") == 0) {
            lv_label_set_text(label, FONT_AWESOME_TH_LARGE);
        } else if (strcmp(view_name, "learning") == 0) {
            lv_label_set_text(label, FONT_AWESOME_BOOK);
        } else if (strcmp(view_name, "reports") == 0) {
            lv_label_set_text(label, FONT_AWESOME_BAR_CHART);
        } else if (strcmp(view_name, "smarthome") == 0) {
            lv_label_set_text(label, FONT_AWESOME_HOME);
        } else if (strcmp(view_name, "media") == 0) {
            lv_label_set_text(label, FONT_AWESOME_PLAY_CIRCLE);
        } else if (strcmp(view_name, "settings") == 0) {
            lv_label_set_text(label, FONT_AWESOME_COG);
        } else if (strcmp(view_name, "extensions") == 0) {
            lv_label_set_text(label, FONT_AWESOME_PLUG);
        }
        lv_obj_center(label);
    }

    vm.SetView("face"); // Set initial view
}

void LcdDisplay::SetEmotion(const char* emotion) {
    DisplayLockGuard lock(this);
    auto& vm = ViewManager::GetInstance();
    View* current_view = vm.GetCurrentView();
    if (auto face_view = dynamic_cast<AssistantFaceView*>(current_view)) {
        face_view->SetEmotion(emotion);
    }
}

void LcdDisplay::SetChatMessage(const char* role, const char* content) {
    DisplayLockGuard lock(this);
    auto& vm = ViewManager::GetInstance();
    View* view = vm.GetViews().at("chat").get();
    if (auto chat_view = dynamic_cast<ChatView*>(view)) {
        chat_view->AddMessage(role, content);
    }
}

// ... (rest of the file remains the same)


#include "settings_view.h"
#include "lvgl_theme.h"
#include "settings.h"

// Forward declaration for the event handler
static void server_dd_event_cb(lv_event_t * e);
static void save_btn_event_cb(lv_event_t * e);

// Helper to create a setting entry
static lv_obj_t* create_setting_entry(lv_obj_t* parent, const char* name, const char* value) {
    lv_obj_t* cont = lv_obj_create(parent);
    lv_obj_remove_style_all(cont);
    lv_obj_set_width(cont, lv_pct(100));
    lv_obj_set_height(cont, LV_SIZE_CONTENT);
    lv_obj_set_flex_flow(cont, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_bottom(cont, 10, 0);

    lv_obj_t* label = lv_label_create(cont);
    lv_label_set_text(label, name);

    lv_obj_t* ta = lv_textarea_create(cont);
    lv_textarea_set_one_line(ta, true);
    lv_textarea_set_text(ta, value);
    lv_obj_set_width(ta, lv_pct(100));

    return ta;
}

void SettingsView::Create(lv_obj_t* parent) {
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));
    lv_obj_set_flex_flow(container_, LV_FLEX_FLOW_COLUMN);

    lv_obj_t* tabview = lv_tabview_create(container_, LV_DIR_TOP, 40);
    lv_obj_set_flex_grow(tabview, 1);

    // Add tabs
    lv_obj_t* network_tab = lv_tabview_add_tab(tabview, "Network");
    lv_obj_t* server_tab = lv_tabview_add_tab(tabview, "Server");
    lv_obj_t* robot_tab = lv_tabview_add_tab(tabview, "Robot");
    lv_obj_t* system_tab = lv_tabview_add_tab(tabview, "System");

    // Setup tab layouts
    lv_obj_set_flex_flow(network_tab, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(network_tab, 5, 0);
    lv_obj_set_flex_flow(server_tab, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(server_tab, 5, 0);
    lv_obj_set_flex_flow(robot_tab, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(robot_tab, 5, 0);
    lv_obj_set_flex_flow(system_tab, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(system_tab, 5, 0);

    // -- Network Tab Content --
    wifi_ssid_ta_ = create_setting_entry(network_tab, "WiFi SSID", "");
    wifi_pass_ta_ = create_setting_entry(network_tab, "WiFi Password", "");
    mqtt_host_ta_ = create_setting_entry(network_tab, "MQTT Host", "");
    telegram_token_ta_ = create_setting_entry(network_tab, "Telegram Token", "");

    // -- Server Tab Content --
    lv_obj_t* server_label = lv_label_create(server_tab);
    lv_label_set_text(server_label, "OTA Server");
    server_dd_ = lv_dropdown_create(server_tab);
    lv_dropdown_set_options(server_dd_, "MiMi Server\nXiaozhi Server\nCustom Server");
    lv_obj_set_width(server_dd_, lv_pct(100));
    lv_obj_add_event_cb(server_dd_, server_dd_event_cb, LV_EVENT_VALUE_CHANGED, this);

    server_custom_url_ta_ = create_setting_entry(server_tab, "Custom Server URL", "");
    // Initially hide the custom URL field
    lv_obj_add_flag(lv_obj_get_parent(server_custom_url_ta_), LV_OBJ_FLAG_HIDDEN);

    // -- Robot Tab Content --
    lv_obj_t* speed_label = lv_label_create(robot_tab);
    lv_label_set_text(speed_label, "Robot Speed");
    robot_speed_slider_ = lv_slider_create(robot_tab);
    lv_obj_set_width(robot_speed_slider_, lv_pct(90));
    lv_obj_align(robot_speed_slider_, LV_ALIGN_CENTER, 0, 0);
    lv_slider_set_range(robot_speed_slider_, 0, 100);
    
    // -- System Tab Content --
    lv_obj_t* theme_label = lv_label_create(system_tab);
    lv_label_set_text(theme_label, "Theme");
    theme_dd_ = lv_dropdown_create(system_tab);
    lv_dropdown_set_options(theme_dd_, "Light\nDark");

    // -- Save Button --
    lv_obj_t* save_btn = lv_btn_create(container_);
    lv_obj_set_width(save_btn, lv_pct(95));
    lv_obj_align(save_btn, LV_ALIGN_BOTTOM_MID, 0, 0);
    lv_obj_add_event_cb(save_btn, save_btn_event_cb, LV_EVENT_CLICKED, this);
    lv_obj_t* save_label = lv_label_create(save_btn);
    lv_label_set_text(save_label, "Save & Reboot");
    lv_obj_center(save_label);

    OnHide();
}

void SettingsView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
        
        Settings settings("wifi", false);
        std::string ota_url = settings.GetString("ota_url");
        
        int selected_server = 0; // Default to MiMi
        if (ota_url == "https://ota.xiaozhi.ai") {
            selected_server = 1;
        } else if (ota_url != "https://mimi.izfx-trade.workers.dev/" && !ota_url.empty()) {
            selected_server = 2;
            lv_textarea_set_text(server_custom_url_ta_, ota_url.c_str());
        }

        lv_dropdown_set_selected(server_dd_, selected_server);
        // Manually trigger event to set initial visibility of custom URL field
        lv_event_send(server_dd_, LV_EVENT_VALUE_CHANGED, NULL);
    }
}

void SettingsView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

// -- Event Handlers --

static void server_dd_event_cb(lv_event_t * e) {
    SettingsView* view = (SettingsView*)lv_event_get_user_data(e);
    lv_obj_t* dropdown = lv_event_get_target(e);
    int selected_id = lv_dropdown_get_selected(dropdown);

    // Get the parent of the text area, which is the container we created
    lv_obj_t* custom_url_container = lv_obj_get_parent(view->server_custom_url_ta_);

    if (selected_id == 2) { // Custom Server
        lv_obj_clear_flag(custom_url_container, LV_OBJ_FLAG_HIDDEN);
    } else {
        lv_obj_add_flag(custom_url_container, LV_OBJ_FLAG_HIDDEN);
    }
}

static void save_btn_event_cb(lv_event_t * e) {
    SettingsView* view = (SettingsView*)lv_event_get_user_data(e);
    
    Settings settings("wifi", true);

    int server_choice = lv_dropdown_get_selected(view->server_dd_);
    std::string ota_url;
    switch(server_choice) {
        case 0: // MiMi Server
            ota_url = "https://mimi.izfx-trade.workers.dev/";
            break;
        case 1: // Xiaozhi Server
            ota_url = "https://ota.xiaozhi.ai";
            break;
        case 2: // Custom Server
            ota_url = lv_textarea_get_text(view->server_custom_url_ta_);
            break;
    }
    settings.SetString("ota_url", ota_url);

    // Save other settings here in the future...

    ESP_LOGI("SettingsView", "Settings saved. Rebooting...");
    // Display a notification before rebooting
    // lv_msgbox_create(...)
    esp_restart();
}

#include "settings_view.h"
#include "lvgl_theme.h"

// Hàm trợ giúp để tạo một cặp label và text area
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

    return ta; // Trả về text area để có thể truy cập sau này
}

// Hàm xử lý sự kiện cho nút Lưu
static void save_btn_event_cb(lv_event_t * e) {
    // Tạm thời chỉ in ra log, sẽ triển khai logic lưu file sau
    ESP_LOGI("SettingsView", "Save button clicked");
}

// Hàm tạo giao diện chính
void SettingsView::Create(lv_obj_t* parent) {
    // 1. Container chính
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));
    lv_obj_set_flex_flow(container_, LV_FLEX_FLOW_COLUMN);

    // 2. Tạo Tab View
    lv_obj_t* tabview = lv_tabview_create(container_, LV_DIR_TOP, 40);
    lv_obj_set_flex_grow(tabview, 1);

    // 3. Thêm các tab
    lv_obj_t* network_tab = lv_tabview_add_tab(tabview, "Network");
    lv_obj_t* robot_tab = lv_tabview_add_tab(tabview, "Robot");
    lv_obj_t* system_tab = lv_tabview_add_tab(tabview, "System");

    // Thiết lập layout cho các tab
    lv_obj_set_flex_flow(network_tab, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(network_tab, 5, 0);
    lv_obj_set_flex_flow(robot_tab, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(robot_tab, 5, 0);
     lv_obj_set_flex_flow(system_tab, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(system_tab, 5, 0);

    // 4. Nội dung Tab "Network"
    wifi_ssid_ta_ = create_setting_entry(network_tab, "WiFi SSID", "");
    wifi_pass_ta_ = create_setting_entry(network_tab, "WiFi Password", "");
    mqtt_host_ta_ = create_setting_entry(network_tab, "MQTT Host", "");
    telegram_token_ta_ = create_setting_entry(network_tab, "Telegram Token", "");

    // 5. Nội dung Tab "Robot"
    lv_obj_t* speed_label = lv_label_create(robot_tab);
    lv_label_set_text(speed_label, "Robot Speed");
    robot_speed_slider_ = lv_slider_create(robot_tab);
    lv_obj_set_width(robot_speed_slider_, lv_pct(90));
    lv_obj_align(robot_speed_slider_, LV_ALIGN_CENTER, 0, 0);
    lv_slider_set_range(robot_speed_slider_, 0, 100);

    lv_obj_t* test_btn_cont = lv_obj_create(robot_tab);
    lv_obj_remove_style_all(test_btn_cont);
    lv_obj_set_width(test_btn_cont, lv_pct(100));
    lv_obj_set_height(test_btn_cont, LV_SIZE_CONTENT);
    lv_obj_set_flex_flow(test_btn_cont, LV_FLEX_FLOW_ROW);
    lv_obj_set_flex_align(test_btn_cont, LV_FLEX_ALIGN_SPACE_AROUND, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_top(test_btn_cont, 20, 0);

    lv_obj_t* test_forward_btn = lv_btn_create(test_btn_cont);
    lv_obj_t* label_fwd = lv_label_create(test_forward_btn);
    lv_label_set_text(label_fwd, "Test Forward");

    lv_obj_t* test_turn_btn = lv_btn_create(test_btn_cont);
    lv_obj_t* label_turn = lv_label_create(test_turn_btn);
    lv_label_set_text(label_turn, "Test Turn");

    // 6. Nội dung Tab "System"
    lv_obj_t* theme_label = lv_label_create(system_tab);
    lv_label_set_text(theme_label, "Theme");
    theme_dd_ = lv_dropdown_create(system_tab);
    lv_dropdown_set_options(theme_dd_, "Light\nDark");

    // 7. Nút Lưu
    lv_obj_t* save_btn = lv_btn_create(container_);
    lv_obj_set_width(save_btn, lv_pct(95));
    lv_obj_align(save_btn, LV_ALIGN_BOTTOM_MID, 0, 0);
    lv_obj_add_event_cb(save_btn, save_btn_event_cb, LV_EVENT_CLICKED, NULL);
    lv_obj_t* save_label = lv_label_create(save_btn);
    lv_label_set_text(save_label, "Save Settings");
    lv_obj_center(save_label);

    OnHide();
}

// Các hàm khác giữ nguyên
void SettingsView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
        // TODO: Load settings from file and populate fields
    }
}

void SettingsView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

#include "smart_home_view.h"
#include "font_awesome.h"

// Hàm xử lý sự kiện khi chạm vào một thiết bị
static void device_card_event_cb(lv_event_t * e) {
    lv_obj_t* card = lv_event_get_target(e);
    // Đảo trạng thái active (ví dụ: thay đổi màu sắc để mô phỏng bật/tắt)
    if (lv_obj_has_state(card, LV_STATE_CHECKED)) {
        lv_obj_set_style_bg_color(card, lv_palette_main(LV_PALETTE_GREY), 0);
         lv_obj_set_style_border_color(card, lv_palette_darken(LV_PALETTE_GREY, 2), 0);
    } else {
        lv_obj_set_style_bg_color(card, lv_palette_main(LV_PALETTE_BLUE), 0);
        lv_obj_set_style_border_color(card, lv_palette_darken(LV_PALETTE_BLUE, 2), 0);
    }
    ESP_LOGI("SmartHome", "Device toggled");
}

// Hàm trợ giúp để tạo một thẻ điều khiển thiết bị
static lv_obj_t* create_device_card(lv_obj_t* parent, const char* icon, const char* name, bool is_on) {
    lv_obj_t* card = lv_obj_create(parent);
    lv_obj_set_size(card, 100, 80);
    lv_obj_set_flex_flow(card, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_flex_align(card, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_add_flag(card, LV_OBJ_FLAG_CLICKABLE | LV_OBJ_FLAG_CHECKABLE);
    lv_obj_add_event_cb(card, device_card_event_cb, LV_EVENT_CLICKED, NULL);

    // Style ban đầu
    lv_obj_set_style_radius(card, 10, 0);
    lv_obj_set_style_border_width(card, 2, 0);

    lv_obj_t* icon_label = lv_label_create(card);
    lv_obj_set_style_text_font(icon_label, &lv_font_montserrat_24, 0);
    lv_label_set_text(icon_label, icon);

    lv_obj_t* name_label = lv_label_create(card);
    lv_label_set_text(name_label, name);

    // Cập nhật trạng thái và màu sắc ban đầu
    if (is_on) {
        lv_obj_add_state(card, LV_STATE_CHECKED);
        lv_obj_set_style_bg_color(card, lv_palette_main(LV_PALETTE_BLUE), 0);
        lv_obj_set_style_border_color(card, lv_palette_darken(LV_PALETTE_BLUE, 2), 0);
    } else {
        lv_obj_clear_state(card, LV_STATE_CHECKED);
        lv_obj_set_style_bg_color(card, lv_palette_main(LV_PALETTE_GREY), 0);
        lv_obj_set_style_border_color(card, lv_palette_darken(LV_PALETTE_GREY, 2), 0);
    }

    return card;
}

void SmartHomeView::Create(lv_obj_t* parent) {
    // 1. Container chính
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));
    lv_obj_set_flex_flow(container_, LV_FLEX_FLOW_COLUMN);

    // 2. Tab View cho các phòng
    lv_obj_t* tabview = lv_tabview_create(container_, LV_DIR_TOP, 35);
    lv_obj_set_flex_grow(tabview, 1);

    lv_obj_t* living_room_tab = lv_tabview_add_tab(tabview, "Living Room");
    lv_obj_t* bedroom_tab = lv_tabview_add_tab(tabview, "Bedroom");
    lv_obj_t* kitchen_tab = lv_tabview_add_tab(tabview, "Kitchen");

    // Thiết lập layout cho các tab
    lv_obj_set_flex_flow(living_room_tab, LV_FLEX_FLOW_ROW_WRAP);
    lv_obj_set_style_pad_all(living_room_tab, 5, 0);
    lv_obj_set_flex_flow(bedroom_tab, LV_FLEX_FLOW_ROW_WRAP);
    lv_obj_set_style_pad_all(bedroom_tab, 5, 0);
    lv_obj_set_flex_flow(kitchen_tab, LV_FLEX_FLOW_ROW_WRAP);
    lv_obj_set_style_pad_all(kitchen_tab, 5, 0);

    // 3. Thêm các thiết bị vào từng phòng (dữ liệu giả)
    // Phòng khách
    create_device_card(living_room_tab, FONT_AWESOME_LIGHTBULB_O, "Main Light", true);
    create_device_card(living_room_tab, FONT_AWESOME_TELEVISION, "Smart TV", false);
    create_device_card(living_room_tab, FONT_AWESOME_VOLUME_UP, "Speaker", true);
    create_device_card(living_room_tab, FONT_AWESOME_FAN, "Fan", false);

    // Phòng ngủ
    create_device_card(bedroom_tab, FONT_AWESOME_LIGHTBULB_O, "Bedside Lamp", false);

    // Bếp
    create_device_card(kitchen_tab, FONT_AWESOME_LIGHTBULB_O, "Kitchen Light", true);

    // 4. Các nút chế độ nhanh (Quick Modes)
    lv_obj_t* mode_cont = lv_obj_create(container_);
    lv_obj_remove_style_all(mode_cont);
    lv_obj_set_size(mode_cont, lv_pct(100), LV_SIZE_CONTENT);
    lv_obj_set_style_pad_all(mode_cont, 5, 0);
    lv_obj_set_flex_flow(mode_cont, LV_FLEX_FLOW_ROW);
    lv_obj_set_flex_align(mode_cont, LV_FLEX_ALIGN_SPACE_EVENLY, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);

    lv_obj_t* sleep_btn = lv_btn_create(mode_cont);
    lv_obj_t* sleep_label = lv_label_create(sleep_btn);
    lv_label_set_text(sleep_label, FONT_AWESOME_BED " Go to Sleep");
    lv_obj_center(sleep_label);

    lv_obj_t* away_btn = lv_btn_create(mode_cont);
    lv_obj_t* away_label = lv_label_create(away_btn);
    lv_label_set_text(away_label, FONT_AWESOME_SIGN_OUT " Away Mode");
    lv_obj_center(away_label);

    OnHide();
}

void SmartHomeView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
        // TODO: Load actual device states
    }
}

void SmartHomeView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

#include "extensions_view.h"
#include "font_awesome.h"

// Forward declaration
static void install_btn_event_cb(lv_event_t* e);

// Helper function to add items to the list
static void AddExtensionToList(lv_obj_t* list, const char* icon, const char* name, bool installed) {
    lv_obj_t* btn = lv_list_add_btn(list, icon, name);
    lv_obj_t* install_btn = lv_btn_create(btn);
    lv_obj_align(install_btn, LV_ALIGN_RIGHT_MID, -10, 0);
    lv_obj_add_event_cb(install_btn, install_btn_event_cb, LV_EVENT_CLICKED, (void*)name); // Pass name for logging

    lv_obj_t* label = lv_label_create(install_btn);
    if (installed) {
        lv_label_set_text(label, "Remove");
        lv_obj_set_style_bg_color(install_btn, lv_palette_main(LV_PALETTE_RED), 0);
    } else {
        lv_label_set_text(label, "Install");
        lv_obj_set_style_bg_color(install_btn, lv_palette_main(LV_PALETTE_BLUE), 0);
    }
}

void ExtensionsView::Create(lv_obj_t* parent) {
    // 1. Main container
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));

    // 2. List object
    list_ = lv_list_create(container_);
    lv_obj_set_size(list_, lv_pct(100), lv_pct(100));
    lv_obj_center(list_);

    // 3. Add items using the helper
    AddExtensionToList(list_, FONT_AWESOME_CLOUD, "Weather Forecast", true);
    AddExtensionToList(list_, FONT_AWESOME_CALENDAR, "Google Calendar", false);
    AddExtensionToList(list_, FONT_AWESOME_CHECK, "To-Do List", true);
    AddExtensionToList(list_, FONT_AWESOME_LIGHTBULB, "Philips Hue", false);

    OnHide();
}

// Event handler for install/remove buttons
static void install_btn_event_cb(lv_event_t* e) {
    lv_obj_t* btn = lv_event_get_target(e);
    lv_obj_t* label = lv_obj_get_child(btn, 0);
    const char* text = lv_label_get_text(label);
    const char* name = (const char*)lv_event_get_user_data(e);

    if (strcmp(text, "Install") == 0) {
        ESP_LOGI("ExtensionsView", "Installing %s...", name);
        lv_label_set_text(label, "Remove");
        lv_obj_set_style_bg_color(btn, lv_palette_main(LV_PALETTE_RED), 0);
    } else {
        ESP_LOGI("ExtensionsView", "Removing %s...", name);
        lv_label_set_text(label, "Install");
        lv_obj_set_style_bg_color(btn, lv_palette_main(LV_PALETTE_BLUE), 0);
    }
}

void ExtensionsView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

void ExtensionsView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

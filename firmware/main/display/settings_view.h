#ifndef SETTINGS_VIEW_H
#define SETTINGS_VIEW_H

#include "view.h"

class SettingsView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

private:
    lv_obj_t* container_ = nullptr;

    // Network Tab
    lv_obj_t* wifi_ssid_ta_ = nullptr;
    lv_obj_t* wifi_pass_ta_ = nullptr;
    lv_obj_t* mqtt_host_ta_ = nullptr;
    lv_obj_t* telegram_token_ta_ = nullptr;

    // Server Tab
    lv_obj_t* server_dd_ = nullptr;
    lv_obj_t* server_custom_url_ta_ = nullptr;

    // Robot Tab
    lv_obj_t* robot_speed_slider_ = nullptr;

    // System Tab
    lv_obj_t* theme_dd_ = nullptr;
};

#endif // SETTINGS_VIEW_H

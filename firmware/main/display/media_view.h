#ifndef MEDIA_VIEW_H
#define MEDIA_VIEW_H

#include "view.h"
#include <esp_log.h>

class MediaView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

    void TogglePlayPause();

private:
    lv_obj_t* container_ = nullptr;
    lv_obj_t* song_label_ = nullptr;
    lv_obj_t* artist_label_ = nullptr;
    lv_obj_t* progress_slider_ = nullptr;
    lv_obj_t* play_pause_btn_ = nullptr;
    lv_obj_t* play_pause_label_ = nullptr;

    bool is_playing_ = true;
};

#endif // MEDIA_VIEW_H

#include "media_view.h"
#include "font_awesome.h"

// Forward declarations
static void play_pause_btn_event_cb(lv_event_t * e);
static void prev_btn_event_cb(lv_event_t * e);
static void next_btn_event_cb(lv_event_t * e);

void MediaView::Create(lv_obj_t* parent) {
    // 1. Main container
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));
    lv_obj_set_layout(container_, &lv_flex_column_nowrap);
    lv_obj_set_flex_align(container_, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_row(container_, 10, 0);

    // 2. Album art placeholder
    lv_obj_t* art_label = lv_label_create(container_);
    lv_obj_set_style_text_font(art_label, &lv_font_montserrat_48, 0);
    lv_label_set_text(art_label, FONT_AWESOME_MUSIC);
    lv_obj_set_style_text_color(art_label, lv_palette_main(LV_PALETTE_GREY), 0);

    // 3. Song and artist labels
    song_label_ = lv_label_create(container_);
    lv_label_set_text(song_label_, "Song Title");
    lv_obj_set_style_text_font(song_label_, &lv_font_montserrat_20, 0);

    artist_label_ = lv_label_create(container_);
    lv_label_set_text(artist_label_, "Artist Name");

    // 4. Progress slider
    progress_slider_ = lv_slider_create(container_);
    lv_obj_set_width(progress_slider_, lv_pct(80));

    // 5. Controls container
    lv_obj_t* ctrl_cont = lv_obj_create(container_);
    lv_obj_remove_style_all(ctrl_cont);
    lv_obj_set_width(ctrl_cont, lv_pct(100));
    lv_obj_set_height(ctrl_cont, LV_SIZE_CONTENT);
    lv_obj_set_flex_flow(ctrl_cont, LV_FLEX_FLOW_ROW);
    lv_obj_set_flex_align(ctrl_cont, LV_FLEX_ALIGN_SPACE_EVENLY, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);

    // 6. Control buttons
    lv_obj_t* prev_btn = lv_btn_create(ctrl_cont);
    lv_obj_t* prev_label = lv_label_create(prev_btn);
    lv_label_set_text(prev_label, FONT_AWESOME_STEP_BACKWARD);
    lv_obj_add_event_cb(prev_btn, prev_btn_event_cb, LV_EVENT_CLICKED, NULL);

    play_pause_btn_ = lv_btn_create(ctrl_cont);
    lv_obj_set_style_bg_color(play_pause_btn_, lv_palette_main(LV_PALETTE_BLUE), 0);
    play_pause_label_ = lv_label_create(play_pause_btn_);
    lv_label_set_text(play_pause_label_, FONT_AWESOME_PAUSE);
    lv_obj_add_event_cb(play_pause_btn_, play_pause_btn_event_cb, LV_EVENT_CLICKED, this);

    lv_obj_t* next_btn = lv_btn_create(ctrl_cont);
    lv_obj_t* next_label = lv_label_create(next_btn);
    lv_label_set_text(next_label, FONT_AWESOME_STEP_FORWARD);
    lv_obj_add_event_cb(next_btn, next_btn_event_cb, LV_EVENT_CLICKED, NULL);

    OnHide();
}

void MediaView::TogglePlayPause() {
    const char* current_symbol = lv_label_get_text(play_pause_label_);
    if (strcmp(current_symbol, FONT_AWESOME_PAUSE) == 0) {
        lv_label_set_text(play_pause_label_, FONT_AWESOME_PLAY);
        is_playing_ = false;
    } else {
        lv_label_set_text(play_pause_label_, FONT_AWESOME_PAUSE);
        is_playing_ = true;
    }
}

// Event Handlers
static void play_pause_btn_event_cb(lv_event_t * e) {
    MediaView* view = (MediaView*)lv_event_get_user_data(e);
    if (view) {
        view->TogglePlayPause();
    }
}

static void prev_btn_event_cb(lv_event_t * e) {
    ESP_LOGI("MediaView", "Previous button pressed");
}

static void next_btn_event_cb(lv_event_t * e) {
    ESP_LOGI("MediaView", "Next button pressed");
}

void MediaView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

void MediaView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

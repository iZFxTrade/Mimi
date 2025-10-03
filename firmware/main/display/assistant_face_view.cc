#include "assistant_face_view.h"
#include <map>

// Mapping from string to mimi_emo_t
static const std::map<std::string, mimi_emo_t> emotion_map = {
    {"happy", EMO_HAPPY},
    {"sad", EMO_SAD},
    {"surprised", EMO_SURPRISED},
    {"thinking", EMO_THINKING},
    {"sleepy", EMO_SLEEPY},
    {"listening", EMO_LISTENING},
    {"battery_low", EMO_BATTERY_LOW},
    {"disconnected", EMO_DISCONNECTED},
    {"loading", EMO_LOADING},
    {"excited", EMO_EXCITED},
    {"bliss", EMO_BLISS},
    {"neutral", EMO_NEUTRAL}
};

mimi_emo_t AssistantFaceView::string_to_emotion(const std::string& s) {
    auto it = emotion_map.find(s);
    if (it != emotion_map.end()) {
        return it->second;
    }
    return EMO_NEUTRAL; // Default to neutral if not found
}

void AssistantFaceView::touch_event_cb(lv_event_t* e) {
    lv_indev_t* indev = lv_indev_get_act();
    if (indev == nullptr) return;

    lv_point_t point;
    lv_indev_get_point(indev, &point);
    
    // The canvas is the direct child of the container created by mimi_emotion_create
    lv_obj_t* cont = static_cast<lv_obj_t*>(lv_event_get_user_data(e));
    lv_obj_t* canvas = lv_obj_get_child(cont, 0);

    // Convert screen coordinates to canvas local coordinates
    lv_area_t canvas_area;
    lv_obj_get_coords(canvas, &canvas_area);
    point.x -= canvas_area.x1;
    point.y -= canvas_area.y1;

    bool is_pressed = (lv_indev_get_state(indev) == LV_INDEV_STATE_PRESSED);

    // Call the reaction function from the C library
    mimi_touch_react(point.x, point.y, is_pressed);
}

void AssistantFaceView::Create(lv_obj_t* parent) {
    // The mimi_emotion_create function creates its own container
    mimi_container_ = mimi_emotion_create(parent, 320, 240);
    
    // We need to get the canvas object created inside mimi_emotion_create to add an event to it.
    // Based on the C code, the canvas is the first and only child of the container.
    if (mimi_container_ && lv_obj_get_child_cnt(mimi_container_) > 0) {
        lv_obj_t* canvas = lv_obj_get_child(mimi_container_, 0);
        lv_obj_add_event_cb(canvas, touch_event_cb, LV_EVENT_PRESSING, mimi_container_);
    }
    
    // Initially hide the view
    OnHide();
}

void AssistantFaceView::SetEmotion(const std::string& emotion) {
    mimi_emotion_set(string_to_emotion(emotion));
}

void AssistantFaceView::OnShow() {
    if (mimi_container_) {
        lv_obj_clear_flag(mimi_container_, LV_OBJ_FLAG_HIDDEN);
        // Set a default emotion when shown
        SetEmotion("neutral");
    }
}

void AssistantFaceView::OnHide() {
    if (mimi_container_) {
        lv_obj_add_flag(mimi_container_, LV_OBJ_FLAG_HIDDEN);
    }
}

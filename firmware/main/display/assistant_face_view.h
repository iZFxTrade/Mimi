#ifndef ASSISTANT_FACE_VIEW_H
#define ASSISTANT_FACE_VIEW_H

#include "view.h"
#include "assets/images/emotion_custom.h"
#include <string>

class AssistantFaceView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

    // Sets emotion based on a string identifier
    void SetEmotion(const std::string& emotion);

private:
    lv_obj_t* mimi_container_ = nullptr;
    static void touch_event_cb(lv_event_t* e);
    mimi_emo_t string_to_emotion(const std::string& s);
};

#endif // ASSISTANT_FACE_VIEW_H

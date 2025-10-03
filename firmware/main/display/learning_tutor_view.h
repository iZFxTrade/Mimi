#ifndef LEARNING_TUTOR_VIEW_H
#define LEARNING_TUTOR_VIEW_H

#include "view.h"

class LearningTutorView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

    void FlipCard();
    void LoadNextCard();

private:
    lv_obj_t* container_ = nullptr;
    lv_obj_t* card_ = nullptr;
    lv_obj_t* question_label_ = nullptr;
    lv_obj_t* answer_label_ = nullptr;
    lv_obj_t* flip_btn_ = nullptr;
    lv_obj_t* next_btn_ = nullptr;
};

#endif // LEARNING_TUTOR_VIEW_H

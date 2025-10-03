#include "learning_tutor_view.h"
#include "font_awesome.h"

// Forward declaration
static void flip_btn_event_cb(lv_event_t * e);
static void next_btn_event_cb(lv_event_t * e);

void LearningTutorView::Create(lv_obj_t* parent) {
    // 1. Container chính
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));
    lv_obj_set_layout(container_, &lv_flex_column_nowrap);
    lv_obj_set_flex_align(container_, LV_FLEX_ALIGN_SPACE_BETWEEN, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_all(container_, 10, 0);

    // 2. Card container
    card_ = lv_obj_create(container_);
    lv_obj_set_size(card_, lv_pct(95), lv_pct(70));
    lv_obj_center(card_);
    lv_obj_set_flex_flow(card_, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_flex_align(card_, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);

    // 3. Question and Answer Labels (inside the card)
    question_label_ = lv_label_create(card_);
    lv_label_set_text(question_label_, "..."); // Sẽ được cập nhật sau
    lv_obj_set_style_text_align(question_label_, LV_TEXT_ALIGN_CENTER, 0);

    answer_label_ = lv_label_create(card_);
    lv_label_set_text(answer_label_, "");
    lv_obj_add_flag(answer_label_, LV_OBJ_FLAG_HIDDEN); // Ẩn câu trả lời ban đầu
    lv_obj_set_style_text_align(answer_label_, LV_TEXT_ALIGN_CENTER, 0);

    // 4. Control buttons container
    lv_obj_t* ctrl_cont = lv_obj_create(container_);
    lv_obj_remove_style_all(ctrl_cont);
    lv_obj_set_width(ctrl_cont, lv_pct(100));
    lv_obj_set_height(ctrl_cont, LV_SIZE_CONTENT);
    lv_obj_set_flex_flow(ctrl_cont, LV_FLEX_FLOW_ROW);
    lv_obj_set_flex_align(ctrl_cont, LV_FLEX_ALIGN_SPACE_EVENLY, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);

    // 5. Flip Button
    flip_btn_ = lv_btn_create(ctrl_cont);
    lv_obj_t* flip_label = lv_label_create(flip_btn_);
    lv_label_set_text(flip_label, "Flip Card");
    lv_obj_add_event_cb(flip_btn_, flip_btn_event_cb, LV_EVENT_CLICKED, this);

    // 6. Next Button
    next_btn_ = lv_btn_create(ctrl_cont);
    lv_obj_t* next_label = lv_label_create(next_btn_);
    lv_label_set_text(next_label, "Next " FONT_AWESOME_FORWARD);
    lv_obj_add_event_cb(next_btn_, next_btn_event_cb, LV_EVENT_CLICKED, this);

    // Load the first card
    LoadNextCard();
    OnHide();
}

void LearningTutorView::FlipCard() {
    bool is_answer_hidden = lv_obj_has_flag(answer_label_, LV_OBJ_FLAG_HIDDEN);
    if (is_answer_hidden) {
        lv_obj_clear_flag(answer_label_, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(question_label_, LV_OBJ_FLAG_HIDDEN);
        lv_obj_t* label = lv_obj_get_child(flip_btn_, 0);
        lv_label_set_text(label, "Show Question");
    } else {
        lv_obj_add_flag(answer_label_, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(question_label_, LV_OBJ_FLAG_HIDDEN);
        lv_obj_t* label = lv_obj_get_child(flip_btn_, 0);
        lv_label_set_text(label, "Flip Card");
    }
}

void LearningTutorView::LoadNextCard() {
    // Đây là nơi để tải câu hỏi/trả lời mới từ một nguồn dữ liệu (ví dụ: mảng, file)
    // Hiện tại, chúng ta sẽ dùng dữ liệu giả
    static int card_index = 0;
    const char* questions[] = { "What is the capital of France?", "What is 2 + 2?", "Which planet is known as the Red Planet?" };
    const char* answers[] = { "Paris", "4", "Mars" };

    if (card_index >= 3) card_index = 0; // Loop back

    // Reset a card
    lv_label_set_text(question_label_, questions[card_index]);
    lv_label_set_text(answer_label_, answers[card_index]);
    card_index++;

    // Đảm bảo câu hỏi được hiển thị và câu trả lời bị ẩn
    lv_obj_clear_flag(question_label_, LV_OBJ_FLAG_HIDDEN);
    lv_obj_add_flag(answer_label_, LV_OBJ_FLAG_HIDDEN);
    lv_obj_t* label = lv_obj_get_child(flip_btn_, 0);
    lv_label_set_text(label, "Flip Card");
}

// Event handlers
static void flip_btn_event_cb(lv_event_t * e) {
    LearningTutorView* view = (LearningTutorView*)lv_event_get_user_data(e);
    if (view) view->FlipCard();
}

static void next_btn_event_cb(lv_event_t * e) {
    LearningTutorView* view = (LearningTutorView*)lv_event_get_user_data(e);
    if (view) view->LoadNextCard();
}

void LearningTutorView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

void LearningTutorView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

#include "chat_view.h"
#include "font_awesome.h"
#include <esp_log.h>

static const char* TAG = "ChatView";

// Forward declaration
static void send_btn_event_cb(lv_event_t * e);

// Hàm trợ giúp để thêm một bong bóng tin nhắn
static void add_message_bubble(lv_obj_t* parent, const char* text, bool is_user) {
    lv_obj_t* bubble = lv_label_create(parent);
    lv_label_set_text(bubble, text);
    lv_label_set_long_mode(bubble, LV_LABEL_LONG_WRAP);
    lv_obj_set_width(bubble, lv_pct(80));
    lv_obj_set_style_pad_all(bubble, 8, 0);
    lv_obj_set_style_radius(bubble, 10, 0);
    lv_obj_set_style_border_width(bubble, 1, 0);

    if (is_user) {
        lv_obj_align(bubble, LV_ALIGN_SELF_END, 0, 0);
        lv_obj_set_style_bg_color(bubble, lv_palette_main(LV_PALETTE_BLUE), 0);
        lv_obj_set_style_border_color(bubble, lv_palette_darken(LV_PALETTE_BLUE, 2), 0);
    } else {
        lv_obj_align(bubble, LV_ALIGN_SELF_START, 0, 0);
        lv_obj_set_style_bg_color(bubble, lv_palette_main(LV_PALETTE_GREY), 0);
        lv_obj_set_style_border_color(bubble, lv_palette_darken(LV_PALETTE_GREY, 2), 0);
    }

    // Tự động cuộn xuống tin nhắn mới nhất
    lv_obj_scroll_to_view(bubble, LV_ANIM_ON);
}

void ChatView::Create(lv_obj_t* parent) {
    // 1. Container chính
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));
    lv_obj_set_layout(container_, &lv_flex_column_nowrap); // Sử dụng layout macro mới

    // 2. Hộp chứa tin nhắn
    msg_box_ = lv_obj_create(container_);
    lv_obj_remove_style_all(msg_box_);
    lv_obj_set_size(msg_box_, lv_pct(100), LV_SIZE_CONTENT);
    lv_obj_set_flex_grow(msg_box_, 1);
    lv_obj_set_flex_flow(msg_box_, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_style_pad_all(msg_box_, 5, 0);
    lv_obj_set_scroll_dir(msg_box_, LV_DIR_VER);
    lv_obj_set_scrollbar_mode(msg_box_, LV_SCROLLBAR_MODE_AUTO);

    // Thêm tin nhắn chào mừng ban đầu
    add_message_bubble(msg_box_, "Hello! How can I help you today?", false);

    // 3. Container nhập liệu
    lv_obj_t* input_container = lv_obj_create(container_);
    lv_obj_remove_style_all(input_container);
    lv_obj_set_size(input_container, lv_pct(100), LV_SIZE_CONTENT);
    lv_obj_set_flex_flow(input_container, LV_FLEX_FLOW_ROW);
    lv_obj_set_flex_align(input_container, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_all(input_container, 5, 0);

    // 4. Text Area để nhập tin nhắn
    input_ta_ = lv_textarea_create(input_container);
    lv_obj_set_flex_grow(input_ta_, 1);
    lv_textarea_set_one_line(input_ta_, true);
    lv_textarea_set_placeholder_text(input_ta_, "Type a message...");

    // 5. Nút Gửi
    lv_obj_t* send_btn = lv_btn_create(input_container);
    lv_obj_t* send_label = lv_label_create(send_btn);
    lv_label_set_text(send_label, FONT_AWESOME_PAPER_PLANE);
    lv_obj_add_event_cb(send_btn, send_btn_event_cb, LV_EVENT_CLICKED, this);

    OnHide();
}

// Hàm xử lý sự kiện cho nút Gửi
static void send_btn_event_cb(lv_event_t * e) {
    ChatView* view = (ChatView*)lv_event_get_user_data(e);
    if (view) {
        view->SendMessage();
    }
}

// Hàm gửi tin nhắn (được gọi bởi event handler)
void ChatView::SendMessage() {
    const char* txt = lv_textarea_get_text(input_ta_);
    if (txt && strlen(txt) > 0) {
        // Thêm tin nhắn của người dùng vào UI
        add_message_bubble(msg_box_, txt, true);

        // Xóa nội dung trong text area
        lv_textarea_set_text(input_ta_, "");

        // TODO: Gửi tin nhắn `txt` đến AI/backend
        ESP_LOGI(TAG, "User sent: %s", txt);

        // TODO: Nhận và hiển thị phản hồi từ AI
        // add_message_bubble(msg_box_, "AI is thinking...", false);
    }
}


void ChatView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

void ChatView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

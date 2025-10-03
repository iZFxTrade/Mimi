#ifndef CHAT_VIEW_H
#define CHAT_VIEW_H

#include "view.h"

class ChatView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

    // Method to be called by the event handler to process and send a message
    void SendMessage();

private:
    lv_obj_t* container_ = nullptr;
    lv_obj_t* msg_box_ = nullptr; // Container for message bubbles
    lv_obj_t* input_ta_ = nullptr; // Text area for user input
};

#endif // CHAT_VIEW_H

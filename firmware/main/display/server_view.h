#pragma once

#include "view.h"

class ServerView : public View {
public:
    ServerView();
    ~ServerView();

    void OnDraw(Display* display) override;
    void OnClick(Display* display) override;
    void OnScroll(Display* display, int direction) override;

private:
    // Add private members here to store the state of the view,
    // for example, which option is currently selected.
    int selected_option_;
    char custom_url_[256];
    bool is_editing_;
};

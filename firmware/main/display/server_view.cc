#include "server_view.h"
#include "display.h"
#include "settings.h"
#include "lang.h"

ServerView::ServerView() : selected_option_(0), is_editing_(false) {
    // Load the current settings to initialize the view
    Settings settings("wifi", false);
    std::string current_url = settings.GetString("ota_url");

    if (current_url.empty() || current_url == "https://mimi.izfx-trade.workers.dev/") {
        selected_option_ = 0; // MiMi Server
    } else if (current_url == "https://ota.xiaozhi.ai") {
        selected_option_ = 1; // Xiaozhi Server
    } else {
        selected_option_ = 2; // Custom Server
        strncpy(custom_url_, current_url.c_str(), sizeof(custom_url_) - 1);
    }
}

ServerView::~ServerView() {
}

void ServerView::OnDraw(Display* display) {
    // This is where we will draw the UI elements:
    // - Title: "Server Settings"
    // - Radio buttons for "MiMi", "Xiaozhi", "Custom"
    // - Text input for the custom URL
    // - "Save" and "Cancel" buttons

    display->SetFont(FONT_TITLE);
    display->DrawText(10, 20, "Server Settings");

    display->SetFont(FONT_TEXT);
    // Implement drawing logic here based on selected_option_ and is_editing_
}

void ServerView::OnClick(Display* display) {
    // This function will handle clicks on radio buttons and the Save/Cancel buttons.
    // It will change the selected_option_ or save the settings and exit.

    // Example logic:
    // if (click is on Save button) {
    //     Settings settings("wifi", true);
    //     if (selected_option_ == 0) {
    //         settings.SetString("ota_url", "https://mimi.izfx-trade.workers.dev/");
    //     } else if (selected_option_ == 1) {
    //         settings.SetString("ota_url", "https://ota.xiaozhi.ai");
    //     } else if (selected_option_ == 2) {
    //         settings.SetString("ota_url", custom_url_);
    //     }
    //     display->ShowNotification("Settings saved. Please reboot.");
    //     // Code to go back to the previous view
    // }
}

void ServerView::OnScroll(Display* display, int direction) {
    // This will handle scrolling to change the selected option
    // or to move the cursor within the custom URL text input.
    if (!is_editing_) {
        selected_option_ = (selected_option_ + direction + 3) % 3;
    } else {
        // Handle cursor movement or character selection for the text input
    }
}

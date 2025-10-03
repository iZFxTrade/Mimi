#include "view_manager.h"

ViewManager& ViewManager::GetInstance() {
    static ViewManager instance;
    return instance;
}

void ViewManager::Create(lv_obj_t* parent) {
    container = parent;
    for (auto const& [name, view] : views) {
        view->Create(container);
        view->OnHide(); // Hide all views initially
    }
}

void ViewManager::RegisterView(const std::string& name, std::shared_ptr<View> view) {
    views[name] = view;
}

void ViewManager::SetView(const std::string& name) {
    auto it = views.find(name);
    if (it != views.end()) {
        if (current_view) {
            current_view->OnHide();
        }
        current_view = it->second.get();
        current_view->OnShow();
    } 
}

View* ViewManager::GetCurrentView() {
    return current_view;
}

const std::map<std::string, std::shared_ptr<View>>& ViewManager::GetViews() const {
    return views;
}

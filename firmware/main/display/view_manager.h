#ifndef VIEW_MANAGER_H
#define VIEW_MANAGER_H

#include "view.h"
#include <map>
#include <string>
#include <memory>

class ViewManager {
public:
    static ViewManager& GetInstance();

    void RegisterView(const std::string& name, std::shared_ptr<View> view);
    void SetView(const std::string& name);
    View* GetCurrentView();
    const std::map<std::string, std::shared_ptr<View>>& GetViews() const;
    void Create(lv_obj_t* parent);

private:
    ViewManager() = default;
    std::map<std::string, std::shared_ptr<View>> views;
    View* current_view = nullptr;
    lv_obj_t* container = nullptr;
};

#endif // VIEW_MANAGER_H

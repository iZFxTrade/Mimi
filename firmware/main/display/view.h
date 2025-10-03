#ifndef VIEW_H
#define VIEW_H

#include <lvgl.h>

class View {
public:
    virtual ~View() {}

    // Called when the view is created
    virtual void Create(lv_obj_t* parent) {
        container = parent;
    }

    // Called when the view becomes active
    virtual void OnShow() {
        if (container) {
            lv_obj_clear_flag(container, LV_OBJ_FLAG_HIDDEN);
        }
    }

    // Called when the view is hidden
    virtual void OnHide() {
        if (container) {
            lv_obj_add_flag(container, LV_OBJ_FLAG_HIDDEN);
        }
    }

    // Called periodically for updates
    virtual void OnUpdate() {}

protected:
    lv_obj_t* container = nullptr;
};

#endif // VIEW_H

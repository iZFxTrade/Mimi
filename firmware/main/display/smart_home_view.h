#ifndef SMART_HOME_VIEW_H
#define SMART_HOME_VIEW_H

#include "view.h"

class SmartHomeView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

private:
    lv_obj_t* container_ = nullptr;
};

#endif // SMART_HOME_VIEW_H

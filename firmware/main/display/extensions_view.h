#ifndef EXTENSIONS_VIEW_H
#define EXTENSIONS_VIEW_H

#include "view.h"
#include <esp_log.h>

class ExtensionsView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

private:
    lv_obj_t* container_ = nullptr;
    lv_obj_t* list_ = nullptr;
};

#endif // EXTENSIONS_VIEW_H

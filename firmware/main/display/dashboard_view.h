#ifndef DASHBOARD_VIEW_H
#define DASHBOARD_VIEW_H

#include "view.h"
#include <vector>
#include <string>

class DashboardView : public View {
public:
    DashboardView();
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

    // Public methods to update UI elements
    void UpdateClock(const char* time_str, const char* date_str);
    void UpdateSensorData(const char* temp_str, const char* humidity_str);
    void UpdateTimetable(const std::vector<std::pair<std::string, std::string>>& events);

private:
    lv_obj_t* container_ = nullptr;
    lv_obj_t* time_label_ = nullptr;
    lv_obj_t* date_label_ = nullptr;
    lv_obj_t* temp_label_ = nullptr;
    lv_obj_t* humidity_label_ = nullptr;
    lv_obj_t* timetable_container_ = nullptr;
};

#endif // DASHBOARD_VIEW_H

#ifndef REPORTS_VIEW_H
#define REPORTS_VIEW_H

#include "view.h"

class ReportsView : public View {
public:
    void Create(lv_obj_t* parent) override;
    void OnShow() override;
    void OnHide() override;

    void UpdateChartSeries(uint16_t index);

private:
    lv_obj_t* container_ = nullptr;
    lv_obj_t* chart_select_dd_ = nullptr; // Dropdown menu
    lv_obj_t* chart_ = nullptr;

    // Chart data series
    lv_chart_series_t* series_learning_ = nullptr;
    lv_chart_series_t* series_energy_ = nullptr;
};

#endif // REPORTS_VIEW_H

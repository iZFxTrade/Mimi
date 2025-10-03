#include "reports_view.h"

// Forward declaration
static void chart_select_dd_event_cb(lv_event_t * e);

void ReportsView::Create(lv_obj_t* parent) {
    // 1. Container chính
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100));
    lv_obj_set_layout(container_, &lv_flex_column_nowrap);
    lv_obj_set_style_pad_all(container_, 5, 0);

    // 2. Dropdown để chọn biểu đồ
    chart_select_dd_ = lv_dropdown_create(container_);
    lv_dropdown_set_options(chart_select_dd_, "Learning Time\nEnergy Usage");
    lv_obj_set_width(chart_select_dd_, lv_pct(80));
    lv_obj_align_self(chart_select_dd_, LV_ALIGN_CENTER, 0, 0);
    lv_obj_add_event_cb(chart_select_dd_, chart_select_dd_event_cb, LV_EVENT_VALUE_CHANGED, this);

    // 3. Chart object
    chart_ = lv_chart_create(container_);
    lv_obj_set_size(chart_, lv_pct(95), lv_pct(80));
    lv_obj_set_flex_grow(chart_, 1);
    lv_chart_set_type(chart_, LV_CHART_TYPE_LINE);
    lv_chart_set_range(chart_, LV_CHART_AXIS_PRIMARY_Y, 0, 100); // Đặt một thang đo chung
    lv_chart_set_point_count(chart_, 10);

    // 4. Tạo các series dữ liệu
    // Series cho Thời gian học
    series_learning_ = lv_chart_add_series(chart_, lv_palette_main(LV_PALETTE_BLUE), LV_CHART_AXIS_PRIMARY_Y);
    lv_coord_t data_learning[] = {10, 20, 30, 25, 40, 50, 60, 75, 80, 90};
    lv_chart_set_ext_y_array(chart_, series_learning_, data_learning);

    // Series cho Năng lượng
    series_energy_ = lv_chart_add_series(chart_, lv_palette_main(LV_PALETTE_RED), LV_CHART_AXIS_PRIMARY_Y);
    lv_coord_t data_energy[] = {80, 70, 65, 75, 50, 40, 30, 20, 15, 10};
    lv_chart_set_ext_y_array(chart_, series_energy_, data_energy);

    // Ban đầu, chỉ hiển thị series đầu tiên
    UpdateChartSeries(0);

    OnHide();
}

void ReportsView::UpdateChartSeries(uint16_t index) {
    if (index == 0) { // Learning Time
        lv_obj_clear_flag(series_learning_->y_points, LV_OBJ_FLAG_HIDDEN);
        lv_obj_add_flag(series_energy_->y_points, LV_OBJ_FLAG_HIDDEN);
    } else if (index == 1) { // Energy Usage
        lv_obj_add_flag(series_learning_->y_points, LV_OBJ_FLAG_HIDDEN);
        lv_obj_clear_flag(series_energy_->y_points, LV_OBJ_FLAG_HIDDEN);
    }
    lv_chart_refresh(chart_); // Bắt buộc phải gọi để cập nhật hiển thị
}

// Event handler for the dropdown
static void chart_select_dd_event_cb(lv_event_t * e) {
    ReportsView* view = (ReportsView*)lv_event_get_user_data(e);
    if (view) {
        uint16_t selected_index = lv_dropdown_get_selected(lv_event_get_target(e));
        view->UpdateChartSeries(selected_index);
    }
}

void ReportsView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

void ReportsView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

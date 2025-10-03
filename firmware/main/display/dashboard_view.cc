#include "dashboard_view.h"
#include <font_awesome.h>

// Hàm khởi tạo, có thể để trống nếu không có gì đặc biệt cần làm
DashboardView::DashboardView() {
    // Constructor
}

// Hàm tạo giao diện
void DashboardView::Create(lv_obj_t* parent) {
    // 1. Tạo container chính cho toàn bộ màn hình Dashboard
    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_); // Xóa tất cả style mặc định
    lv_obj_set_size(container_, lv_pct(100), lv_pct(100)); // Kích thước 100% parent
    lv_obj_set_flex_flow(container_, LV_FLEX_FLOW_COLUMN); // Sắp xếp các con theo cột
    lv_obj_set_style_pad_all(container_, 5, 0);

    // 2. Phần trên: Đồng hồ và Ngày tháng
    lv_obj_t* clock_container = lv_obj_create(container_);
    lv_obj_remove_style_all(clock_container);
    lv_obj_set_width(clock_container, lv_pct(100));
    lv_obj_set_flex_flow(clock_container, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_flex_align(clock_container, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_bottom(clock_container, 10, 0);

    time_label_ = lv_label_create(clock_container);
    lv_obj_set_style_text_font(time_label_, &lv_font_montserrat_36, 0);
    lv_label_set_text(time_label_, "10:10");

    date_label_ = lv_label_create(clock_container);
    lv_obj_set_style_text_font(date_label_, &lv_font_montserrat_16, 0);
    lv_label_set_text(date_label_, "Monday, 01/01/2024");

    // 3. Phần giữa: Cảm biến và Thời tiết
    lv_obj_t* sensor_container = lv_obj_create(container_);
    lv_obj_remove_style_all(sensor_container);
    lv_obj_set_size(sensor_container, lv_pct(100), LV_SIZE_CONTENT);
    lv_obj_set_flex_flow(sensor_container, LV_FLEX_FLOW_ROW);
    lv_obj_set_flex_align(sensor_container, LV_FLEX_ALIGN_SPACE_EVENLY, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_CENTER);
    lv_obj_set_style_pad_ver(sensor_container, 10, 0);

    // Cảm biến nhiệt độ
    temp_label_ = lv_label_create(sensor_container);
    lv_obj_set_style_text_font(temp_label_, &lv_font_montserrat_20, 0);
    lv_label_set_text_fmt(temp_label_, FONT_AWESOME_THERMOMETER_HALF " %s", "25 C");

    // Cảm biến độ ẩm
    humidity_label_ = lv_label_create(sensor_container);
    lv_obj_set_style_text_font(humidity_label_, &lv_font_montserrat_20, 0);
    lv_label_set_text_fmt(humidity_label_, FONT_AWESOME_TINT " %s", "60%");

    // 4. Phần dưới: Lịch trình/Thời khóa biểu
    timetable_container_ = lv_list_create(container_);
    lv_obj_set_size(timetable_container_, lv_pct(100), LV_SIZE_CONTENT);
    lv_obj_set_flex_grow(timetable_container_, 1);
    lv_obj_set_style_pad_all(timetable_container_, 5, 0);
    lv_obj_set_style_border_width(timetable_container_, 0, 0);

    lv_list_add_text(timetable_container_, "Today's Schedule");
    // Dữ liệu giả, sẽ được thay thế bằng dữ liệu từ timetable.json
    lv_list_add_btn(timetable_container_, FONT_AWESOME_CLOCK, "10:00 - Meeting");
    lv_list_add_btn(timetable_container_, FONT_AWESOME_BOOK, "14:00 - Study Session");
    lv_list_add_btn(timetable_container_, FONT_AWESOME_COFFEE, "16:30 - Coffee Break");

    // Ban đầu ẩn view đi
    OnHide();
}

// Hàm cập nhật đồng hồ
void DashboardView::UpdateClock(const char* time_str, const char* date_str) {
    if (time_label_ && date_label_) {
        lv_label_set_text(time_label_, time_str);
        lv_label_set_text(date_label_, date_str);
    }
}

// Hàm cập nhật dữ liệu cảm biến
void DashboardView::UpdateSensorData(const char* temp_str, const char* humidity_str) {
    if (temp_label_ && humidity_label_) {
        lv_label_set_text_fmt(temp_label_, FONT_AWESOME_THERMOMETER_HALF " %s", temp_str);
        lv_label_set_text_fmt(humidity_label_, FONT_AWESOME_TINT " %s", humidity_str);
    }
}

// Hàm cập nhật thời khóa biểu
void DashboardView::UpdateTimetable(const std::vector<std::pair<std::string, std::string>>& events) {
    if (timetable_container_) {
        lv_obj_clean(timetable_container_); // Xóa các mục cũ
        lv_list_add_text(timetable_container_, "Today's Schedule");
        for (const auto& event : events) {
            lv_list_add_btn(timetable_container_, FONT_AWESOME_CLOCK, (event.first + " - " + event.second).c_str());
        }
    }
}

void DashboardView::OnShow() {
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

void DashboardView::OnHide() {
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

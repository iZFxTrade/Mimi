# Công cụ chuyển đổi ảnh LVGL

Thư mục này chứa hai tập lệnh Python để xử lý và chuyển đổi hình ảnh sang định dạng LVGL:

## 1. LVGLImage (LVGLImage.py)

Tập lệnh chuyển đổi [LVGLImage.py](https://github.com/lvgl/lvgl/blob/master/scripts/LVGLImage.py) được trích dẫn từ [repo chính thức](https://github.com/lvgl/lvgl) của LVGL.

## 2. Công cụ chuyển đổi ảnh LVGL (lvgl_tools_gui.py)

Gọi `LVGLImage.py` để chuyển đổi hàng loạt hình ảnh sang định dạng ảnh LVGL.
Có thể được sử dụng để sửa đổi biểu cảm mặc định của trợ lý, hướng dẫn sửa đổi cụ thể [tại đây](https://www.bilibili.com/video/BV12FQkYeEJ3/).

### Tính năng

- Giao diện đồ họa, thân thiện với người dùng.
- Hỗ trợ chuyển đổi hàng loạt hình ảnh.
- Tự động nhận dạng định dạng hình ảnh và chọn định dạng màu tốt nhất để chuyển đổi.
- Hỗ trợ nhiều độ phân giải.

### Cách sử dụng

Tạo môi trường ảo
```bash
# Tạo venv
python -m venv venv
# Kích hoạt môi trường
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

Cài đặt các gói phụ thuộc
```bash
pip install -r requirements.txt
```

Chạy công cụ chuyển đổi

```bash
# Kích hoạt môi trường
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
# Chạy
python lvgl_tools_gui.py
```

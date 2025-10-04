# ogg_converter - Công cụ chuyển đổi hàng loạt OGG cho Trợ lý AI

Tập lệnh này là một công cụ chuyển đổi hàng loạt OGG, hỗ trợ chuyển đổi các tệp âm thanh đầu vào sang định dạng OGG mà trợ lý có thể sử dụng.
Được xây dựng dựa trên thư viện của bên thứ ba trong Python là `ffmpeg-python`.
Nó hỗ trợ chuyển đổi lẫn nhau giữa OGG và các định dạng âm thanh khác, cũng như các tính năng như điều chỉnh độ lớn (loudness).

# Tạo và kích hoạt môi trường ảo

```bash
# Tạo môi trường ảo
python -m venv venv
# Kích hoạt môi trường ảo
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows
```

# Cài đặt các gói phụ thuộc

Vui lòng thực thi trong môi trường ảo

```bash
pip install ffmpeg-python
```

# Chạy tập lệnh
```bash
python ogg_converter.py
```

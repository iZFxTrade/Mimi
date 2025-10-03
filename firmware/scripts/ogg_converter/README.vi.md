# ogg_converter: Trình chuyển đổi hàng loạt OGG cho MiMi AI

Tập lệnh này là một công cụ chuyển đổi hàng loạt OGG, hỗ trợ chuyển đổi các tệp âm thanh đầu vào sang định dạng OGG mà MiMi AI có thể sử dụng.
Nó được xây dựng dựa trên thư viện Python của bên thứ ba là `ffmpeg-python`.
Nó hỗ trợ chuyển đổi qua lại giữa OGG và các định dạng âm thanh khác, điều chỉnh độ lớn, v.v.

# Tạo và kích hoạt môi trường ảo

```bash
# Tạo môi trường ảo
python -m venv venv
# Kích hoạt môi trường ảo
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows
```

# Cài đặt các phụ thuộc

Vui lòng thực thi trong môi trường ảo

```bash
pip install ffmpeg-python
```

# Chạy tập lệnh
```bash
python xiaozhi_ogg_converter.py
```

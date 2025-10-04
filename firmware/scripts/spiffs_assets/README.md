# Trình tạo tài sản SPIFFS

Thư mục này chứa các tập lệnh để tạo hình ảnh hệ thống tệp SPIFFS, được sử dụng để đóng gói các tài sản mặc định như cài đặt ngôn ngữ và các tệp âm thanh nhắc nhở vào firmware.

## Cấu trúc thư mục

- **`build.py`**: Tập lệnh chính để xây dựng hình ảnh SPIFFS. Nó thu thập tất cả các tài sản cần thiết, xử lý các tệp ngôn ngữ và tạo ra hình ảnh nhị phân cuối cùng.
- **`build_all.py`**: Một tập lệnh trợ giúp để xây dựng hình ảnh tài sản cho tất cả các ngôn ngữ được hỗ trợ.
- **`pack_model.py`**: Đóng gói các tệp mô hình thành một định dạng phù hợp để đưa vào hình ảnh SPIFFS.
- **`spiffs_assets_gen.py`**: Tạo các tệp C header từ các tài sản, cho phép chúng được nhúng trực tiếp vào mã nguồn C++.

# Thư mục `scripts`

Thư mục này chứa các tập lệnh khác nhau được sử dụng để hỗ trợ quá trình phát triển, xây dựng và quản lý tài nguyên cho firmware. Các tập lệnh này tự động hóa các tác vụ, chuyển đổi tài nguyên và cung cấp các công cụ gỡ lỗi.

## Cấu trúc thư mục và Chức năng

```
firmware/scripts/
│
├── Image_Converter/
│   ├── LVGLImage.py: Chuyển đổi hình ảnh sang định dạng mảng C cho LVGL.
│   ├── README.md: Hướng dẫn sử dụng các công cụ chuyển đổi hình ảnh.
│   ├── lvgl_tools_gui.py: Giao diện đồ họa (GUI) cho các công cụ LVGL.
│   └── requirements.txt: Các thư viện Python cần thiết cho các công cụ chuyển đổi hình ảnh.
│
├── acoustic_check/
│   ├── demod.py: Kịch bản để giải điều chế tín hiệu âm thanh.
│   ├── graphic.py: Các thành phần đồ họa cho GUI kiểm tra âm thanh.
│   ├── main.py: Kịch bản chính để chạy GUI kiểm tra âm thanh.
│   ├── readme.md: Hướng dẫn sử dụng công cụ kiểm tra âm thanh.
│   └── requirements.txt: Các thư viện Python cần thiết cho công cụ kiểm tra âm thanh.
│
├── ogg_converter/
│   ├── README.md: Hướng dẫn sử dụng công cụ chuyển đổi OGG.
│   └── xiaozhi_ogg_converter.py: Kịch bản để chuyển đổi hàng loạt tệp âm thanh sang định dạng OGG.
│
├── p3_tools/
│   ├── README.md: Hướng dẫn sử dụng các công cụ P3.
│   ├── batch_convert_gui.py: GUI để chuyển đổi hàng loạt tệp âm thanh sang/từ P3.
│   ├── convert_audio_to_p3.py: Kịch bản để chuyển đổi tệp âm thanh sang định dạng P3.
│   ├── convert_p3_to_audio.py: Kịch bản để chuyển đổi tệp P3 sang định dạng âm thanh tiêu chuẩn.
│   ├── p3_gui_player.py: GUI để phát các tệp âm thanh P3.
│   ├── play_p3.py: Kịch bản dòng lệnh để phát tệp âm thanh P3.
│   └── requirements.txt: Các thư viện Python cần thiết cho các công cụ P3.
│
├── spiffs_assets/
│   ├── README.md: Hướng dẫn cách đóng gói tài nguyên vào SPIFFS.
│   ├── build.py: Kịch bản chính để xây dựng hình ảnh SPIFFS.
│   ├── build_all.py: Kịch bản để xây dựng tất cả các tài nguyên thành một hình ảnh SPIFFS duy nhất.
│   ├── pack_model.py: Kịch bản để đóng gói các mô hình (ví dụ: mô hình nhận dạng giọng nói).
│   └── spiffs_assets_gen.py: Kịch bản để tạo hình ảnh hệ thống tệp SPIFFS.
│
├── README.md: Tệp README đã được cập nhật.
├── audio_debug_server.py: Chạy một máy chủ để nhận dữ liệu âm thanh từ thiết bị cho mục đích gỡ lỗi.
├── build_default_assets.py: Tự động hóa quá trình xây dựng và đóng gói các tài nguyên mặc định.
├── gen_lang.py: Kịch bản để tạo các tệp ngôn ngữ cho firmware.
├── mp3_to_ogg.sh: Tập lệnh shell để chuyển đổi các tệp MP3 sang định dạng OGG.
├── release.py: Tự động hóa quá trình tạo bản phát hành (release) mới.
├── sonic_wifi_config.html: Trang HTML để cấu hình Wi-Fi của thiết bị thông qua "Sonic".
└── versions.py: Quản lý thông tin phiên bản cho các bản dựng firmware.
```


## Workflow (Luồng công việc)

1. **Chuẩn bị tài nguyên**:
    - Sử dụng `Image_Converter` để chuyển đổi hình ảnh.
    - Sử dụng `ogg_converter` hoặc `mp3_to_ogg.sh` để chuẩn bị các tệp âm thanh.
    - Sử dụng `p3_tools` nếu cần làm việc với định dạng âm thanh P3.

2. **Đóng gói tài nguyên**:
    - Chạy `build_default_assets.py` để xử lý và sắp xếp các tài nguyên.
    - Sau đó, sử dụng các kịch bản trong `spiffs_assets` (ví dụ: `build_all.py`) để tạo một hình ảnh SPIFFS chứa tất cả các tài nguyên.

3. **Xây dựng và Phát hành**:
    - Trong quá trình xây dựng firmware, hình ảnh SPIFFS đã tạo sẽ được đưa vào bản dựng cuối cùng.
    - Kịch bản `release.py` được sử dụng để gắn thẻ (tag) và đóng gói bản phát hành.

4. **Gỡ lỗi (Debugging)**:
    - Để gỡ lỗi âm thanh, chạy `audio_debug_server.py` trên máy tính và sử dụng GUI trong `acoustic_check` để phân tích dữ liệu âm thanh được gửi từ thiết bị.

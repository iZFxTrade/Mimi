# Trình tạo tài sản SPIFFS

Tập lệnh này được sử dụng để xây dựng phân vùng tài sản SPIFFS cho các dự án ESP32, đóng gói các tệp tài sản khác nhau thành một định dạng có thể sử dụng trên thiết bị.

## Tính năng

- Xử lý Mô hình mạng WakeNet (WakeNet Model)
- Tích hợp các tệp phông chữ văn bản
- Xử lý bộ sưu tập hình ảnh biểu tượng cảm xúc
- Tự động tạo tệp chỉ mục tài sản
- Đóng gói và tạo tệp `assets.bin` cuối cùng

## Yêu cầu phụ thuộc

- Python 3.6+
- Các tệp tài sản liên quan

## Cách sử dụng

### Cú pháp cơ bản

```bash
./build.py --wakenet_model <thư_mục_mô_hình_wakenet> \
    --text_font <tệp_phông_chữ_văn_bản> \
    --emoji_collection <thư_mục_bộ_sưu_tập_biểu_tượng_cảm_xúc>
```

### Mô tả tham số

| Tham số | Loại | Bắt buộc | Mô tả |
|---|---|---|---|
| `--wakenet_model` | Đường dẫn thư mục | Không | Đường dẫn đến thư mục mô hình mạng WakeNet |
| `--text_font` | Đường dẫn tệp | Không | Đường dẫn đến tệp phông chữ văn bản |
| `--emoji_collection` | Đường dẫn thư mục | Không | Đường dẫn đến thư mục bộ sưu tập hình ảnh biểu tượng cảm xúc |

### Ví dụ sử dụng

```bash
# Ví dụ với đầy đủ tham số
./build.py \
    --wakenet_model ../../managed_components/espressif__esp-sr/model/wakenet_model/wn9_nihaoxiaozhi_tts \
    --text_font ../../components/xiaozhi-fonts/build/font_puhui_common_20_4.bin \
    --emoji_collection ../../components/xiaozhi-fonts/build/emojis_64/

# Chỉ xử lý tệp phông chữ
./build.py --text_font ../../components/xiaozhi-fonts/build/font_puhui_common_20_4.bin

# Chỉ xử lý biểu tượng cảm xúc
./build.py --emoji_collection ../../components/xiaozhi-fonts/build/emojis_64/
```

## Quy trình làm việc

1.  **Tạo cấu trúc thư mục xây dựng**
    -   `build/` - Thư mục xây dựng chính
    -   `build/assets/` - Thư mục tệp tài sản
    -   `build/output/` - Thư mục tệp đầu ra

2.  **Xử lý mô hình mạng WakeNet**
    -   Sao chép các tệp mô hình vào thư mục xây dựng
    -   Sử dụng `pack_model.py` để tạo `srmodels.bin`
    -   Sao chép tệp mô hình đã tạo vào thư mục tài sản

3.  **Xử lý phông chữ văn bản**
    -   Sao chép tệp phông chữ vào thư mục tài sản
    -   Hỗ trợ các tệp phông chữ định dạng `.bin`

4.  **Xử lý bộ sưu tập biểu tượng cảm xúc**
    -   Quét các tệp hình ảnh trong thư mục được chỉ định
    -   Hỗ trợ các định dạng `.png` và `.gif`
    -   Tự động tạo chỉ mục biểu tượng cảm xúc

5.  **Tạo tệp cấu hình**
    -   `index.json` - Tệp chỉ mục tài sản
    -   `config.json` - Tệp cấu hình xây dựng

6.  **Đóng gói tài sản cuối cùng**
    -   Sử dụng `spiffs_assets_gen.py` để tạo `assets.bin`
    -   Sao chép vào thư mục gốc của bản dựng

## Tệp đầu ra

Sau khi quá trình xây dựng hoàn tất, các tệp sau sẽ được tạo trong thư mục `build/`:

-   `assets/` - Tất cả các tệp tài sản
-   `assets.bin` - Tệp tài sản SPIFFS cuối cùng
-   `config.json` - Cấu hình xây dựng
-   `output/` - Các tệp đầu ra trung gian

## Các định dạng tài sản được hỗ trợ

-   **Tệp mô hình**: `.bin` (được xử lý bởi pack_model.py)
-   **Tệp phông chữ**: `.bin`
-   **Tệp hình ảnh**: `.png`, `.gif`
-   **Tệp cấu hình**: `.json`

## Xử lý lỗi

Tập lệnh bao gồm một cơ chế xử lý lỗi hoàn chỉnh:

-   Kiểm tra xem tệp/thư mục nguồn có tồn tại không
-   Xác minh kết quả thực thi của tiến trình con
-   Cung cấp thông tin lỗi và cảnh báo chi tiết

## Lưu ý

1.  Đảm bảo tất cả các tập lệnh Python phụ thuộc đều nằm trong cùng một thư mục
2.  Sử dụng đường dẫn tuyệt đối hoặc đường dẫn tương đối đến thư mục tập lệnh cho các đường dẫn tệp tài sản
3.  Quá trình xây dựng sẽ xóa các tệp xây dựng trước đó
4.  Kích thước của tệp `assets.bin` được tạo bị giới hạn bởi kích thước của phân vùng SPIFFS

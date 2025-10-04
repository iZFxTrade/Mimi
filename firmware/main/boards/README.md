# Thư mục `boards`

Thư mục này là trung tâm để quản lý tất cả các cấu hình phần cứng dành riêng cho từng bo mạch mà firmware hỗ trợ. Mỗi bo mạch có một thư mục riêng chứa các tệp định nghĩa cách firmware tương tác với phần cứng cụ thể đó, chẳng hạn như cấu hình chân (pin), khởi tạo trình điều khiển (driver) và các tính năng đặc thù.

## Cấu trúc thư mục và Chức năng

Cấu trúc được tổ chức theo từng bo mạch, với một thư mục `common` chứa mã nguồn chung có thể tái sử dụng.

```
firmware/main/boards/
│
├── common/                 # Mã nguồn chung cho tất cả các bo mạch
│   ├── board.h / .cc:      Lớp cơ sở (base class) và các chức năng chung cho một bo mạch.
│   ├── button.h / .cc:     Thành phần xử lý nút bấm có thể tái sử dụng.
│   ├── wifi_board.h / .cc:   Logic chung để quản lý kết nối Wi-Fi.
│   ├── backlight.h / .cc:  Điều khiển đèn nền màn hình.
│   └── ... (các thành phần chung khác như quản lý pin, camera, I2C, ...)
│
├── esp-box-3/              # Ví dụ về một thư mục bo mạch cụ thể
│   ├── README.md:          Ghi chú riêng cho bo mạch ESP-BOX-3.
│   ├── config.h:           Tệp tiêu đề C++ định nghĩa cấu hình chân (pinout), các macro và tính năng phần cứng.
│   ├── config.json:        Tệp JSON mô tả các tính năng và cấu hình của bo mạch cho hệ thống xây dựng.
│   ├── esp_box3_board.cc:  Tệp mã nguồn C++ triển khai logic khởi tạo và xử lý dành riêng cho bo mạch này.
│   ├── emote.json:         Cấu hình cho các hiệu ứng biểu cảm (thường là cho màn hình hoặc đèn LED).
│   └── layout.json:        Định nghĩa bố cục giao diện người dùng cho màn hình của bo mạch.
│
├── m5stack-core-s3/        # Ví dụ về một thư mục bo mạch khác
│   ├── config.h
│   ├── config.json
│   └── m5stack_core_s3.cc
│
└── ... (nhiều thư mục bo mạch khác)
```

**Chức năng của các tệp chính trong mỗi thư mục bo mạch:**

-   **`*.cc` (ví dụ: `esp_box3_board.cc`)**: Đây là tệp triển khai chính cho bo mạch. Nó thường kế thừa từ lớp `Board` trong `common/board.h` và triển khai các phương thức ảo (virtual methods) để khởi tạo các ngoại vi (như màn hình, codec âm thanh, nút bấm), xử lý các sự kiện đầu vào và quản lý năng lượng.
-   **`config.h`**: Tệp cấu hình quan trọng nhất ở cấp độ mã nguồn. Nó định nghĩa các chân GPIO được sử dụng cho các chức năng khác nhau (I2C, SPI, các nút bấm), loại màn hình, loại codec âm thanh, và các cờ biên dịch (compile flags) khác để bật/tắt các tính năng.
-   **`config.json`**: Cung cấp thông tin cấu hình cho các tập lệnh và hệ thống xây dựng. Nó có thể chứa thông tin như tên bo mạch, kiến trúc, các tính năng được hỗ trợ (ví dụ: `"audio_codec": true`), giúp tự động hóa quá trình xây dựng mà không cần thay đổi mã nguồn.

## Luồng công việc (Workflow)

### 1. Để xây dựng firmware cho một bo mạch cụ thể:

Thông thường, bạn sẽ chỉ định bo mạch mục tiêu trong quá trình cấu hình hoặc biên dịch. Ví dụ, khi sử dụng công cụ `idf.py` của ESP-IDF, bạn có thể đặt một biến để chọn bo mạch:

```sh
idf.py set-target esp32s3 -D BOARD_NAME="esp-box-3"
idf.py build
```

Hệ thống xây dựng sẽ tự động tìm thư mục `esp-box-3`, bao gồm tệp `config.h` của nó và biên dịch tệp `esp_box3_board.cc` tương ứng.

### 2. Để thêm một bo mạch mới (ví dụ: `my-new-board`):

1.  **Tạo thư mục mới**: Tạo một thư mục mới trong `firmware/main/boards/` có tên là `my-new-board`.
2.  **Tạo các tệp cấu hình**:
    *   Tạo tệp `config.h` để định nghĩa cấu hình chân và các tính năng phần cứng của bo mạch mới.
    *   Tạo tệp `config.json` để mô tả bo mạch cho hệ thống xây dựng.
3.  **Viết mã triển khai**:
    *   Tạo tệp `my_new_board.cc`. Trong tệp này, tạo một lớp kế thừa từ một trong các lớp cơ sở trong `common` (ví dụ: `WifiBoard`).
    *   Triển khai các phương thức cần thiết để khởi tạo màn hình, các nút bấm, codec âm thanh, và bất kỳ phần cứng nào khác trên bo mạch của bạn.
    *   Sử dụng các thành phần từ thư mục `common` nếu có thể để tránh lặp lại mã.
4.  **Đăng ký bo mạch**: Bạn cần thêm logic vào hệ thống xây dựng (thường là trong `CMakeLists.txt` ở cấp cao hơn) để nhận diện và biên dịch mã cho bo mạch mới khi được chọn.

### 3. Để tùy chỉnh một bo mạch hiện có:

Chỉ cần sửa đổi các tệp trong thư mục của bo mạch đó. Ví dụ, để thay đổi chức năng của một nút bấm trên `esp-box-3`, bạn có thể cần phải chỉnh sửa `config.h` (nếu chân thay đổi) hoặc `esp_box3_board.cc` (nếu logic xử lý thay đổi).
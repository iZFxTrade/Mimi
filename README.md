# 🎀 MiMi – Trợ lý Học tập & Gia đình Thông minh

> **Lưu ý:** Đây là một phiên bản tùy biến (fork) của dự án [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32), được tối ưu hóa riêng cho phần cứng **ESP32-CYD (Cheap Yellow Display)** và bổ sung các tính năng dành cho dự án MiMi.

**MiMi** là một **trợ lý AI cá nhân hóa** chạy trên **ESP32-CYD**. MiMi không chỉ là **loa AI để bàn**, mà còn là một **người bạn đồng hành, gia sư thông minh, và trung tâm điều khiển ngôi nhà từ xa**, được thiết kế để trở thành một thành viên ảo trong gia đình bạn.

---

## 📖 Bản thiết kế dự án (Project Blueprint)

Để có cái nhìn tổng quan về mặt kỹ thuật, kiến trúc, cấu trúc tệp và luồng công việc của dự án, vui lòng tham khảo **[Bản thiết kế dự án (PROJECT_BLUEPRINT.md)](./PROJECT_BLUEPRINT.md)**. Tài liệu này được thiết kế đặc biệt để cung cấp thông tin chuyên sâu cho các nhà phát triển và trợ lý AI.

---

## ✨ Tính năng chính

*   💖 **Người bạn đồng hành trong gia đình**
*   📚 **Gia sư thông minh hai chế độ**
*   📱 **Giám sát & Điều khiển từ xa qua Telegram**
*   🔌 **Hệ thống Mở rộng & Tự động hóa (Custom Actions)**
*   🏠 **Smarthome & Âm nhạc**

---

## 🚀 Hướng dẫn triển khai Phần cứng (Firmware)

Để đưa MiMi vào cuộc sống trên thiết bị ESP32-CYD của bạn, hãy làm theo các bước dưới đây.

## 🔄 Quy trình cập nhật mã nguồn lên GitHub

Sau khi hoàn thành các bước phát triển hoặc build ROM, bạn cần tự đẩy (push) thay đổi lên kho GitHub của mình. Máy chủ build không thể thực hiện thao tác này thay bạn, vì vậy hãy chắc chắn rằng máy trạm đã được cấu hình quyền truy cập SSH/HTTPS hợp lệ.

1. **Kiểm tra những tệp đã sửa:**
   ```bash
   git status
   ```
2. **Thêm thay đổi vào commit:**
   ```bash
   git add <tệp hoặc thư mục>
   ```
3. **Tạo commit mô tả rõ ràng:**
   ```bash
   git commit -m "feat: mô tả ngắn gọn nội dung thay đổi"
   ```
4. **Đảm bảo bạn đang ở đúng nhánh từ xa:**
   ```bash
   git branch -vv
   ```
5. **(Tuỳ chọn) Khai báo remote nếu chưa có:**
   ```bash
   git remote add origin git@github.com:<tài-khoản>/<tên-kho>.git
   git remote -v  # xác nhận lại URL
   ```
6. **Đẩy thay đổi lên GitHub:**
   ```bash
   git push -u origin <tên-nhánh>
   ```

> 💡 Nếu gặp lỗi xác thực, hãy cấu hình lại token/SSH key và thử lại. Trong trường hợp Git báo "No configured push destination", hãy dùng bước 5 để thêm remote rồi chạy lại `git push`.

### Phương pháp 1: Sử dụng WebFlasher (Đơn giản nhất)

> Truy cập link để sử dụng.
https://izfxtrade.github.io/Mimi/

### Phương pháp 2: Triển khai thủ công (Dành cho nhà phát triển)

**Yêu cầu:**

*   **ESP-IDF:** Cài đặt [môi trường phát triển của Espressif](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/).
*   **Git:** Để sao chép mã nguồn dự án.

**Các bước thực hiện:**

1.  **Sao chép mã nguồn:**
    ```bash
    git clone https://github.com/iZFxTrade/Mimi.git
    cd Mimi/firmware
    ```

2.  **Cấu hình, Biên dịch và Nạp firmware:**
    ```bash
    idf.py set-target esp32
    idf.py menuconfig
    idf.py build flash monitor
    ```

### Chuẩn bị Thẻ nhớ (SD Card)

Sau khi nạp firmware, bạn cần chuẩn bị thẻ nhớ để MiMi có thể hoạt động. Chi tiết về cấu trúc thư mục và tệp vui lòng xem ở phần dưới.

---

## 🖥️ Hướng dẫn triển khai Phần mềm (MCP-Server)

`MCP-Server` là máy chủ phụ trợ (backend) được viết bằng Python (FastAPI). Nó đóng vai trò trung tâm, chịu trách nhiệm cho các nhiệm vụ quan trọng:

*   **Cập nhật Firmware qua mạng (OTA):** Cung cấp các bản cập nhật firmware mới nhất.
*   **Cấp phát Cấu hình Động:** Cung cấp cho thiết bị thông tin kết nối (MQTT, WebSocket, v.v.).

### 1. Chạy trong Môi trường Phát triển

**Yêu cầu:** Python 3.8+, `pip`, `venv`

**Các bước thực hiện:**

1.  **Đi đến thư mục máy chủ:**
    ```bash
    cd MCP-Server
    ```

2.  **Tạo và kích hoạt môi trường ảo:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Chạy máy chủ:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

### 2. Chạy với Docker (Production)

Phương pháp này đóng gói máy chủ vào một container, giúp việc triển khai trở nên nhất quán và dễ dàng.

**Yêu cầu:** Docker đã được cài đặt và đang chạy.

**Các bước thực hiện:**

1.  **Xây dựng Docker image:**
    Từ thư mục gốc của dự án, chạy lệnh sau:
    ```bash
    docker build -t mcp-server:latest -f MCP-Server/Dockerfile .
    ```

2.  **Chạy Docker container:**
    Lệnh này sẽ khởi động container, ánh xạ cổng 8000 của máy chủ ra cổng 8000 trên máy của bạn.
    ```bash
    docker run -d -p 8000:8000 --name mimi-server mcp-server:latest
    ```

---

## 📈 Roadmap (Lộ trình phát triển)

*   [ ] **🚀 WebFlasher cho ESP32**
*   [ ] **🗣️ Cải thiện Nhận dạng Giọng nói**
*   [ ] **🌐 Hỗ trợ Đa ngôn ngữ**
*   [ ] **📱 Ứng dụng di động đồng hành (Companion App)**

---

## 📂 Cấu trúc dữ liệu trên thẻ SD

Thư mục gốc của thẻ SD sẽ chứa các file cấu hình và thư mục dữ liệu sau:

```
/
├── config.json
├── timetable.json
├── actions.json
├── learning/
└── ...
```
(Chi tiết các tệp được lược bỏ để cho ngắn gọn)

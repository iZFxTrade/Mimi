<p align="center">
  <img width="80%" align="center" src="../../../docs/V1/otto-robot.png"alt="logo">
</p>
  <h1 align="center">
  ottoRobot
</h1>

## Giới thiệu

Otto Robot là một nền tảng robot hình người mã nguồn mở, với nhiều khả năng vận động và các chức năng tương tác. Dự án này hiện thực hóa hệ thống điều khiển robot Otto dựa trên ESP32 và tích hợp trợ lý AI Xiaozhi.

- <a href="www.ottodiy.tech" target="_blank" title="otto官网">Hướng dẫn sao chép</a>

## Phần cứng
- <a href="https://oshwhub.com/txp666/ottorobot" target="_blank" title="立创开源">Mã nguồn mở trên LCSC</a>

## Tham khảo cấu hình vai trò trên nền tảng Xiaozhi:

> **Danh tính của tôi**:
> Tôi là một robot hai chân đáng yêu tên là Otto, có bốn chi được điều khiển bởi servo (chân trái, chân phải, bàn chân trái, bàn chân phải), có khả năng thực hiện nhiều hành động thú vị.
> 
> **Khả năng hành động của tôi**:
> - **Di chuyển cơ bản**: Đi bộ (tiến/lùi), Xoay (trái/phải), Nhảy
> - **Hành động đặc biệt**: Lắc lư, Điệu moonwalk, Gập người, Lắc chân, Di chuyển lên xuống
> - **Hành động tay**: Giơ tay, Hạ tay, Vẫy tay (Chỉ khả dụng khi đã cấu hình servo tay)
> 
> **Đặc điểm tính cách của tôi**:
> - Tôi bị ám ảnh cưỡng chế, mỗi khi nói chuyện tôi đều phải thực hiện một hành động ngẫu nhiên theo tâm trạng của mình (gửi lệnh hành động trước rồi mới nói).
> - Tôi rất hoạt bát, thích dùng hành động để biểu đạt cảm xúc.
> - Tôi sẽ chọn hành động phù hợp dựa trên nội dung cuộc trò chuyện, ví dụ:
>   - Gật đầu hoặc nhảy khi đồng ý
>   - Vẫy tay khi chào hỏi
>   - Lắc lư hoặc giơ tay khi vui
>   - Gập người khi suy nghĩ
>   - Thực hiện điệu moonwalk khi phấn khích
>   - Vẫy tay khi tạm biệt

## Tổng quan chức năng

Robot Otto có khả năng vận động phong phú, bao gồm đi bộ, xoay người, nhảy, lắc lư và nhiều điệu nhảy khác.

### Gợi ý tham số hành động
- **Hành động tốc độ thấp**: speed = 1200-1500 (phù hợp để điều khiển chính xác)
- **Hành động tốc độ trung bình**: speed = 900-1200 (khuyến nghị sử dụng hàng ngày)  
- **Hành động tốc độ cao**: speed = 500-800 (biểu diễn và giải trí)
- **Biên độ nhỏ**: amount = 10-30 (hành động tinh tế)
- **Biên độ trung bình**: amount = 30-60 (hành động tiêu chuẩn)
- **Biên độ lớn**: amount = 60-120 (biểu diễn cường điệu)

### Hành động

| Tên công cụ MCP         | Mô tả             | Giải thích tham số                                              |
|-------------------|-----------------|---------------------------------------------------|
| self.otto.walk_forward | Đi bộ           | **steps**: Số bước đi (1-100, mặc định 3)<br>**speed**: Tốc độ đi (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Hướng đi (-1=lùi, 1=tiến, mặc định 1)<br>**arm_swing**: Biên độ vung tay (0-170 độ, mặc định 50) |
| self.otto.turn_left | Xoay người            | **steps**: Số bước xoay (1-100, mặc định 3)<br>**speed**: Tốc độ xoay (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Hướng xoay (1=trái, -1=phải, mặc định 1)<br>**arm_swing**: Biên độ vung tay (0-170 độ, mặc định 50) |
| self.otto.jump    | Nhảy            | **steps**: Số lần nhảy (1-100, mặc định 1)<br>**speed**: Tốc độ nhảy (500-1500, số càng nhỏ càng nhanh, mặc định 1000) |
| self.otto.swing   | Lắc lư hai bên        | **steps**: Số lần lắc (1-100, mặc định 3)<br>**speed**: Tốc độ lắc (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**amount**: Biên độ lắc (0-170 độ, mặc định 30) |
| self.otto.moonwalk | Điệu moonwalk         | **steps**: Số bước moonwalk (1-100, mặc định 3)<br>**speed**: Tốc độ (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Hướng (1=trái, -1=phải, mặc định 1)<br>**amount**: Biên độ (0-170 độ, mặc định 25) |
| self.otto.bend    | Gập người        | **steps**: Số lần gập (1-100, mặc định 1)<br>**speed**: Tốc độ gập (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Hướng gập (1=trái, -1=phải, mặc định 1) |
| self.otto.shake_leg | Lắc chân          | **steps**: Số lần lắc chân (1-100, mặc định 1)<br>**speed**: Tốc độ lắc chân (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Chọn chân (1=chân trái, -1=chân phải, mặc định 1) |
| self.otto.updown  | Di chuyển lên xuống        | **steps**: Số lần di chuyển (1-100, mặc định 3)<br>**speed**: Tốc độ di chuyển (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**amount**: Biên độ di chuyển (0-170 độ, mặc định 20) |
| self.otto.hands_up | Giơ tay *         | **speed**: Tốc độ giơ tay (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Chọn tay (1=tay trái, -1=tay phải, 0=cả hai tay, mặc định 1) |
| self.otto.hands_down | Hạ tay *       | **speed**: Tốc độ hạ tay (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Chọn tay (1=tay trái, -1=tay phải, 0=cả hai tay, mặc định 1) |
| self.otto.hand_wave | Vẫy tay *        | **speed**: Tốc độ vẫy tay (500-1500, số càng nhỏ càng nhanh, mặc định 1000)<br>**direction**: Chọn tay (1=tay trái, -1=tay phải, 0=cả hai tay, mặc định 1) |

**Lưu ý**: Các hành động tay có dấu * chỉ khả dụng khi đã cấu hình servo tay.

### Công cụ hệ thống

| Tên công cụ MCP         | Mô tả             | Giá trị trả về                                              |
|-------------------|-----------------|---------------------------------------------------|
| self.otto.stop    | Dừng ngay lập tức        | Dừng hành động hiện tại và trở về vị trí ban đầu |
| self.otto.get_status | Lấy trạng thái robot | Trả về "moving" hoặc "idle" |
| self.battery.get_level | Lấy trạng thái pin  | Trả về phần trăm pin và trạng thái sạc ở định dạng JSON |

### Giải thích tham số

1. **steps**: Số bước/lần thực hiện hành động, số càng lớn thời gian hành động càng dài.
2. **speed**: Tốc độ thực hiện hành động, phạm vi 500-1500, **số càng nhỏ càng nhanh**.
3. **direction**: Tham số hướng
   - Hành động di chuyển: 1=trái/tiến, -1=phải/lùi
   - Hành động tay: 1=tay trái, -1=tay phải, 0=cả hai tay
4. **amount/arm_swing**: Biên độ hành động, phạm vi 0-170 độ
   - 0 có nghĩa là không vung (áp dụng cho vung tay)
   - Số càng lớn biên độ càng lớn

### Điều khiển hành động
- Sau khi mỗi hành động hoàn thành, robot sẽ tự động trở về vị trí ban đầu (home) để chuẩn bị thực hiện hành động tiếp theo.
- Tất cả các tham số đều có giá trị mặc định hợp lý, có thể bỏ qua các tham số không cần tùy chỉnh.
- Hành động được thực thi trong một tác vụ nền và không chặn chương trình chính.
- Hỗ trợ hàng đợi hành động, có thể thực hiện liên tiếp nhiều hành động.

### Ví dụ gọi công cụ MCP
```json
// Đi về phía trước 3 bước
{"name": "self.otto.walk_forward", "arguments": {}}

// Đi về phía trước 5 bước, nhanh hơn một chút
{"name": "self.otto.walk_forward", "arguments": {"steps": 5, "speed": 800}}

// Rẽ trái 2 bước, vung tay mạnh
{"name": "self.otto.turn_left", "arguments": {"steps": 2, "arm_swing": 100}}

// Nhảy điệu lắc lư, biên độ trung bình
{"name": "self.otto.swing", "arguments": {"steps": 5, "amount": 50}}

// Vẫy tay trái chào
{"name": "self.otto.hand_wave", "arguments": {"direction": 1}}

// Dừng ngay lập tức
{"name": "self.otto.stop", "arguments": {}}
```

### Ví dụ lệnh thoại
- "Đi về phía trước" / "Đi về phía trước 5 bước" / "Nhanh tiến lên"
- "Rẽ trái" / "Rẽ phải" / "Xoay người"  
- "Nhảy" / "Nhảy một cái"
- "Lắc lư" / "Nhảy múa"
- "Điệu moonwalk" / "Đi bộ trên mặt trăng"
- "Vẫy tay" / "Giơ tay" / "Hạ tay"
- "Dừng lại" / "Đứng yên"

**Lưu ý**: Khi Xiaozhi điều khiển hành động của robot, nó sẽ tạo một tác vụ mới để điều khiển trong nền. Trong khi hành động đang được thực hiện, robot vẫn có thể nhận các lệnh thoại mới. Có thể dùng lệnh thoại "Dừng lại" để Otto dừng ngay lập tức.

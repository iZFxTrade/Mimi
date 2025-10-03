# Lệnh cấu hình biên dịch

**Đặt mục tiêu biên dịch thành ESP32:**

```bash
idf.py set-target esp32
```

**Mở menuconfig:**

```bash
idf.py menuconfig
```

**Chọn bo mạch:**

```
Xiaozhi Assistant -> Board Type -> AtomMatrix + Echo Base
```

**Biên dịch:**

```bash
idf.py build
```

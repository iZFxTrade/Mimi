# Hướng dẫn cấu hình biên dịch ESP32-S3

## Lệnh cơ bản

### Đặt chip mục tiêu

```bash
idf.py set-target esp32s3
```

### Mở giao diện cấu hình:

```bash
idf.py menuconfig
```
### Cấu hình Flash:

```
Serial flasher config -> Flash size -> 8 MB
```

### Cấu hình bảng phân vùng:

```
Partition Table -> Custom partition CSV file -> partitions/v2/8m.csv
```

### Lựa chọn bo mạch phát triển:

```
Xiaozhi Assistant -> Board Type -> Movecall CuiCan Mặt dây chuyền AI lấp lánh
```

### Bật tối ưu hóa biên dịch:

```
Component config → Compiler options → Optimization Level → Optimize for size (-Os)
```

### Biên dịch:

```bash
idf.py build
```
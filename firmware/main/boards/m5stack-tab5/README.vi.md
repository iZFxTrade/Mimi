# Hướng dẫn sử dụng

* [Tài liệu M5Stack Tab5](https://docs.m5stack.com/zh_CN/core/Tab5)

## Trải nghiệm nhanh

Tải xuống [phần mềm điều khiển](https://pan.baidu.com/s/1dgbUQtMyVLSCSBJLHARpwQ?pwd=1234) đã được biên dịch sẵn, mã lấy: 1234

```shell
esptool.py --chip esp32p4 -p /dev/ttyACM0 -b 460800 --before=default_reset --after=hard_reset write_flash --flash_mode dio --flash_freq 80m --flash_size 16MB 0x00 tab5_xiaozhi_v1_addr0.bin
```

## Sử dụng cơ bản

* Phiên bản idf: v5.5-dev

1. Đặt mục tiêu biên dịch thành esp32p4

```shell
idf.py set-target esp32p4
```

2. Sửa đổi cấu hình

```shell
cp main/boards/m5stack-tab5/sdkconfig.tab5 sdkconfig
```

3. Biên dịch và nạp chương trình

```shell
idf.py build flash monitor
```

> [!NOTE]
> Vào chế độ tải xuống: Nhấn và giữ nút reset (khoảng 2 giây), cho đến khi đèn LED chỉ báo màu xanh lá cây bên trong bắt đầu nhấp nháy nhanh, hãy thả nút ra.


## log

@2025/05/17 Vấn đề kiểm tra

1. listening... cần đợi vài giây để nhận được đầu vào giọng nói???
2. Điều chỉnh độ sáng không chính xác
3. Điều chỉnh âm lượng không chính xác

## TODO

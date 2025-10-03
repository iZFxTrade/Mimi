# Lệnh biên dịch

## Biên dịch bằng một cú nhấp

```bash
python scripts/release.py sensecap-watcher
```

## Cấu hình và biên dịch thủ công

```bash
idf.py set-target esp32s3
```

**Cấu hình**

```bash
idf.py menuconfig
```

Chọn bo mạch

```
Xiaozhi Assistant -> Board Type -> SenseCAP Watcher
```

Một số tùy chọn cấu hình bổ sung trong watcher như sau, cần được chọn trong menuconfig.

```
CONFIG_BOARD_TYPE_SENSECAP_WATCHER=y
CONFIG_ESPTOOLPY_FLASHSIZE_32MB=y
CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions/v2/32m.csv"
CONFIG_BOOTLOADER_CACHE_32BIT_ADDR_QUAD_FLASH=y
CONFIG_ESPTOOLPY_FLASH_MODE_AUTO_DETECT=n
CONFIG_IDF_EXPERIMENTAL_FEATURES=y
```

## Biên dịch và nạp

```bash
idf.py -DBOARD_NAME=sensecap-watcher build flash
```

Lưu ý: Nếu thiết bị hiện tại đã được cài đặt firmware SenseCAP (phiên bản không phải Xiaozhi) trước khi xuất xưởng, vui lòng xử lý địa chỉ phân vùng firmware flash một cách hết sức cẩn thận để tránh xóa nhầm thông tin thiết bị của SenseCAP Watcher (EUI, v.v.), nếu không, ngay cả khi thiết bị được khôi phục về firmware SenseCAP, nó cũng sẽ không thể kết nối đúng cách với máy chủ SenseCraft! Do đó, trước khi nạp firmware, hãy chắc chắn ghi lại thông tin cần thiết của thiết bị để đảm bảo có phương pháp khôi phục!

Bạn có thể sử dụng lệnh sau để sao lưu thông tin sản xuất

```bash
# firstly backup the factory information partition which contains the credentials for connecting the SenseCraft server
esptool.py --chip esp32s3 --baud 2000000 --before default_reset --after hard_reset --no-stub read_flash 0x9000 204800 nvsfactory.bin

```
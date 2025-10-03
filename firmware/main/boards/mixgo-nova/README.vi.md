# Bo mạch phát triển Mixgo_Nova(YuanKong·Youth)

<img src="https://mixly.cn/public/icon/2024/6/09705006c1c643beb96338791ee1dea0_m.png" alt="Mixgo_Nova" width="200"/>

&zwnj;**[Mixgo_Nova](https://mixly.cn/fredqian/mixgo_nova)**&zwnj; là một bo mạch phát triển đa chức năng được thiết kế đặc biệt cho các dự án IoT, giáo dục và nhà sản xuất, tích hợp các cảm biến phong phú và mô-đun giao tiếp không dây, hỗ trợ lập trình đồ họa (Mixly) và tương tác giọng nói ngoại tuyến, phù hợp để phát triển nguyên mẫu nhanh và giảng dạy.

---

## 🛠️ Lệnh cấu hình biên dịch

**Vấn đề thu thập MIC của CODEC ES8374:**

```
managed_components\espressif__esp_codec_dev\device\es8374

static int es8374_config_adc_input(audio_codec_es8374_t *codec, es_adc_input_t input)
{
    int ret = 0;
    int reg = 0;
    ret |= es8374_read_reg(codec, 0x21, &reg);
    if (ret == 0) {
        reg = (reg & 0xcf) | 0x24;
        ret |= es8374_write_reg(codec, 0x21, reg);
    }
    return ret;
}

PS: Dòng 386, thay đổi reg = (reg & 0xcf) | 0x14; thành reg = (reg & 0xcf) | 0x24;
```

**Đặt mục tiêu biên dịch thành ESP32S3:**

```bash
idf.py set-target esp32s3
```

**Mở menuconfig:**

```bash
idf.py menuconfig
```

**Chọn bo mạch:**

```
Xiaozhi Assistant -> Board Type -> YuanKong·Youth
```

**Sửa đổi cấu hình psram:**

```
Component config -> ESP PSRAM -> SPI RAM config -> Mode (QUAD/OCT) -> QUAD Mode PSRAM
```

**Sửa đổi cấu hình Flash:**

```
Serial flasher config -> Flash size -> 8 MB
Partition Table -> Custom partition CSV file -> partitions/v2/8m.csv
```

**Biên dịch:**

```bash
idf.py build
```

**Gộp file BIN:**

```bash
idf.py merge-bin -o xiaozhi-nova.bin -f raw
```
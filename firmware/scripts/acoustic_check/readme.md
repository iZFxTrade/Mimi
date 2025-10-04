# Kiểm tra âm thanh
GUI này được sử dụng để kiểm tra việc chuyển đổi PCM sang miền thời gian/tần số được gửi lại từ thiết bị thông qua `udp`, có thể lưu âm thanh theo độ dài cửa sổ, được sử dụng để đánh giá phân bố tần số tiếng ồn và kiểm tra độ chính xác của việc truyền ASCII bằng sóng âm.

Để kiểm tra firmware, cần bật `USE_AUDIO_DEBUGGER` và đặt `AUDIO_DEBUG_UDP_SERVER` thành địa chỉ của máy tính này.
Sóng âm `demod` có thể được xuất ra để kiểm tra bằng `sonic_wifi_config.html` hoặc tải lên [cấu hình mạng sóng âm Xiaozhi](https://iqf7jnhi.pinit.eth.limo) của `PinMe`.

# Nhật ký kiểm tra giải mã sóng âm

> `✓` có nghĩa là có thể giải mã thành công khi nhận tín hiệu PCM gốc từ I2S DIN, `△` có nghĩa là cần giảm nhiễu hoặc các thao tác bổ sung để giải mã ổn định, `X` có nghĩa là hiệu quả sau khi giảm nhiễu không tốt (có thể giải mã được một phần nhưng rất không ổn định).
> Một số ADC cần điều chỉnh giảm nhiễu chi tiết hơn trong giai đoạn cấu hình I2C, do thiết bị không phổ biến nên chỉ kiểm tra theo cấu hình được cung cấp trong `boards`.

| Thiết bị | ADC | MIC | Hiệu quả | Ghi chú |
| ---- | ---- | --- | --- | ---- |
| bread-compact | INMP441 | Tích hợp MEMEMIC | ✓ |
| atk-dnesp32s3-box | ES8311 | | ✓ |
| magiclick-2p5 | ES8311 | | ✓ |
| lichuang-dev  | ES7210 | | △ | Cần tắt INPUT_REFERENCE khi kiểm tra
| kevin-box-2 | ES7210 | | △ | Cần tắt INPUT_REFERENCE khi kiểm tra
| m5stack-core-s3 | ES7210 | | △ | Cần tắt INPUT_REFERENCE khi kiểm tra
| xmini-c3 | ES8311 | | △ | Cần giảm nhiễu
| atoms3r-echo-base | ES8311 | | △ | Cần giảm nhiễu
| atk-dnesp32s3-box0 | ES8311 | | X | Có thể nhận và giải mã, nhưng tỷ lệ mất gói rất cao
| movecall-moji-esp32s3 | ES8311 | | X | Có thể nhận và giải mã, nhưng tỷ lệ mất gói rất cao
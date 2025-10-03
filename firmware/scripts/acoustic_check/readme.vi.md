# Kiểm tra Sóng âm

GUI này được sử dụng để kiểm tra việc chuyển đổi `pcm` được gửi lại từ thiết bị MiMi AI qua `udp` sang miền thời gian/tần số. Nó có thể lưu lại âm thanh có độ dài bằng cửa sổ, dùng để xác định phân bố tần số nhiễu và kiểm tra độ chính xác của việc truyền ASCII bằng sóng âm.

Để kiểm tra firmware, cần bật `USE_AUDIO_DEBUGGER` và đặt `AUDIO_DEBUG_UDP_SERVER` thành địa chỉ của máy cục bộ.

`demod` sóng âm có thể được xuất ra để kiểm tra thông qua `sonic_wifi_config.html` hoặc tải lên [Cấu hình mạng bằng sóng âm MiMi AI](https://iqf7jnhi.pinit.eth.limo) của `PinMe`.

# Ghi nhận Kiểm tra Giải mã Sóng âm

> `✓` cho biết giải mã thành công khi nhận tín hiệu PCM gốc trên I2S DIN, `△` cho biết cần giảm nhiễu hoặc các thao tác bổ sung để giải mã ổn định, `X` cho biết hiệu quả sau khi giảm nhiễu không tốt (có thể giải mã được một phần nhưng rất không ổn định).
> Một số ADC cần điều chỉnh giảm nhiễu chi tiết hơn trong giai đoạn cấu hình I2C. Do các thiết bị không phổ biến, chúng tôi chỉ kiểm tra theo cấu hình được cung cấp trong thư mục `boards`.

| Thiết bị | ADC | MIC | Hiệu quả | Ghi chú |
|---|---|---|---|---|
| bread-compact | INMP441 | Tích hợp MEMEMIC | ✓ ||
| atk-dnesp32s3-box | ES8311 || ✓ ||
| magiclick-2p5 | ES8311 || ✓ ||
| lichuang-dev | ES7210 || △ | Cần tắt INPUT_REFERENCE khi kiểm tra |
| kevin-box-2 | ES7210 || △ | Cần tắt INPUT_REFERENCE khi kiểm tra |
| m5stack-core-s3 | ES7210 || △ | Cần tắt INPUT_REFERENCE khi kiểm tra |
| xmini-c3 | ES8311 || △ | Cần giảm nhiễu |
| atoms3r-echo-base | ES8311 || △ | Cần giảm nhiễu |
| atk-dnesp32s3-box0 | ES8311 || X | Có thể nhận và giải mã, nhưng tỷ lệ mất gói rất cao |
| movecall-moji-esp32s3 | ES8311 || X | Có thể nhận và giải mã, nhưng tỷ lệ mất gói rất cao |

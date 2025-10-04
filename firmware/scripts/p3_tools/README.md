# Công cụ chuyển đổi và phát lại định dạng âm thanh P3

Thư mục này chứa hai tập lệnh Python để xử lý các tệp âm thanh định dạng P3:

## 1. Công cụ chuyển đổi âm thanh (convert_audio_to_p3.py)

Chuyển đổi các tệp âm thanh thông thường sang định dạng P3 (cấu trúc luồng gồm 4 byte header + gói dữ liệu Opus) và chuẩn hóa độ lớn.

### Cách sử dụng

```bash
python convert_audio_to_p3.py <tệp âm thanh đầu vào> <tệp P3 đầu ra> [-l LUFS] [-d]
```

Trong đó, tùy chọn `-l` được sử dụng để chỉ định độ lớn mục tiêu để chuẩn hóa độ lớn, mặc định là -16 LUFS; tùy chọn `-d` có thể được sử dụng để tắt tính năng chuẩn hóa độ lớn.

Nếu tệp âm thanh đầu vào đáp ứng bất kỳ điều kiện nào sau đây, bạn nên sử dụng `-d` để tắt tính năng chuẩn hóa độ lớn:
- Âm thanh quá ngắn
- Độ lớn của âm thanh đã được điều chỉnh
- Âm thanh đến từ TTS mặc định (độ lớn mặc định của TTS hiện đang được sử dụng là -16 LUFS)

Ví dụ:
```bash
python convert_audio_to_p3.py input.mp3 output.p3
```

## 2. Công cụ phát lại âm thanh P3 (play_p3.py)

Phát các tệp âm thanh định dạng P3.

### Tính năng

- Giải mã và phát các tệp âm thanh định dạng P3
- Áp dụng hiệu ứng fade-out ở cuối quá trình phát lại hoặc khi người dùng ngắt, để tránh bị vỡ tiếng
- Hỗ trợ chỉ định tệp cần phát thông qua các tham số dòng lệnh

### Cách sử dụng

```bash
python play_p3.py <đường dẫn tệp P3>
```

Ví dụ:
```bash
python play_p3.py output.p3
```

## 3. Công cụ chuyển đổi ngược âm thanh (convert_p3_to_audio.py)

Chuyển đổi định dạng P3 trở lại tệp âm thanh thông thường.

### Cách sử dụng

```bash
python convert_p3_to_audio.py <tệp P3 đầu vào> <tệp âm thanh đầu ra>
```

Tệp âm thanh đầu ra cần có phần mở rộng.

Ví dụ:
```bash
python convert_p3_to_audio.py input.p3 output.wav
```
## 4. Công cụ chuyển đổi hàng loạt âm thanh/P3

Một công cụ đồ họa hỗ trợ chuyển đổi hàng loạt âm thanh sang P3, P3 sang âm thanh

![](./img/img.png)

### Cách sử dụng:
```bash
python batch_convert_gui.py
```

## Cài đặt các gói phụ thuộc

Trước khi sử dụng các tập lệnh này, hãy đảm bảo rằng bạn đã cài đặt các thư viện Python cần thiết:

```bash
pip install librosa opuslib numpy tqdm sounddevice pyloudnorm soundfile
```

Hoặc sử dụng tệp requirements.txt được cung cấp:

```bash
pip install -r requirements.txt
```

## Mô tả định dạng P3

Định dạng P3 là một định dạng âm thanh luồng đơn giản với cấu trúc như sau:
- Mỗi khung âm thanh bao gồm một header 4 byte và một gói dữ liệu được mã hóa Opus
- Định dạng header: [1 byte loại, 1 byte dự trữ, 2 byte độ dài]
- Tốc độ lấy mẫu được cố định ở 16000Hz, đơn âm
- Thời lượng mỗi khung là 60ms 
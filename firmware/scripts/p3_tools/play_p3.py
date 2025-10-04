# Phát tệp âm thanh định dạng p3
import opuslib
import struct
import numpy as np
import sounddevice as sd
import argparse

def play_p3_file(input_file):
    """
    Phát tệp âm thanh định dạng p3
    Định dạng p3: [1 byte loại, 1 byte dự trữ, 2 byte độ dài, dữ liệu Opus]
    """
    # Khởi tạo bộ giải mã Opus
    sample_rate = 16000  # Tốc độ lấy mẫu được cố định ở 16000Hz
    channels = 1  # Đơn kênh
    decoder = opuslib.Decoder(sample_rate, channels)
    
    # Kích thước khung (60ms)
    frame_size = int(sample_rate * 60 / 1000)
    
    # Mở luồng âm thanh
    stream = sd.OutputStream(
        samplerate=sample_rate,
        channels=channels,
        dtype='int16'
    )
    stream.start()

    try:
        with open(input_file, 'rb') as f:
            while True:
                # Đọc tiêu đề khung p3
                header = f.read(4)
                if not header:
                    break
                
                # Phân tích cú pháp tiêu đề khung p3
                frame_type, _, opus_len = struct.unpack('<BBH', header)
                
                if frame_type != 0x01:
                    print(f"Cảnh báo: Loại khung không xác định {frame_type}, bỏ qua")
                    f.seek(opus_len, 1) # Bỏ qua dữ liệu
                    continue

                # Đọc dữ liệu Opus
                opus_data = f.read(opus_len)
                if len(opus_data) < opus_len:
                    break
                
                # Giải mã dữ liệu Opus
                pcm_data = decoder.decode(opus_data, frame_size)
                
                # Phát dữ liệu PCM
                stream.write(np.frombuffer(pcm_data, dtype=np.int16))

    except FileNotFoundError:
        print(f"Lỗi: không tìm thấy tệp '{input_file}'")
    except Exception as e:
        print(f"Đã xảy ra lỗi trong khi phát: {e}")
    finally:
        # Dừng và đóng luồng âm thanh
        stream.stop()
        stream.close()
        print("Phát xong.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Phát tệp âm thanh định dạng p3.')
    parser.add_argument('input_file', help='Tên tệp p3 đầu vào')
    args = parser.parse_args()
    
    play_p3_file(args.input_file)

import socket
import wave
import argparse


'''
  Tạo một socket UDP và liên kết nó với IP của máy chủ:8000.
  Lắng nghe các tin nhắn đến và in chúng ra giao diện điều khiển.
  Lưu âm thanh vào tệp WAV.
'''
def main(samplerate, channels):
    # Tạo một socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 8000))

    # Tạo tệp WAV với các tham số
    filename = f"{samplerate}_{channels}.wav"
    wav_file = wave.open(filename, "wb")
    wav_file.setnchannels(channels)     # tham số kênh
    wav_file.setsampwidth(2)            # 2 byte mỗi mẫu (16-bit)
    wav_file.setframerate(samplerate)   # tham số samplerate

    print(f"Bắt đầu lưu âm thanh từ 0.0.0.0:8000 vào {filename}...")

    try:
        while True:
            # Nhận một tin nhắn từ máy khách
            message, address = server_socket.recvfrom(8000)

            # Ghi dữ liệu PCM vào tệp WAV
            wav_file.writeframes(message)

            # In độ dài của tin nhắn
            print(f"Đã nhận {len(message)} byte từ {address}")

    except KeyboardInterrupt:
        print("\nĐang dừng ghi âm...")

    finally:
        # Đóng tệp và socket
        wav_file.close()
        server_socket.close()
        print(f"Tệp WAV '{filename}' đã được lưu thành công")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bộ thu dữ liệu âm thanh UDP, lưu dưới dạng tệp WAV')
    parser.add_argument('--samplerate', '-s', type=int, default=16000,
                        help='Tốc độ lấy mẫu (mặc định: 16000)')
    parser.add_argument('--channels', '-c', type=int, default=2,
                        help='Số kênh (mặc định: 2)')

    args = parser.parse_args()
    main(args.samplerate, args.channels)

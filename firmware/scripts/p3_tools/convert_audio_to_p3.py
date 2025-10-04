# chuyển đổi tệp âm thanh sang luồng giao thức v3
import librosa
import opuslib
import struct
import sys
import tqdm
import numpy as np
import argparse
import pyloudnorm as pyln

def encode_audio_to_opus(input_file, output_file, target_lufs=None):
    # Tải tệp âm thanh bằng librosa
    audio, sample_rate = librosa.load(input_file, sr=None, mono=False, dtype=np.float32)

    # Chuyển đổi sang đơn âm nếu là âm thanh nổi
    if audio.ndim == 2:
        audio = librosa.to_mono(audio)

    if target_lufs is not None:
        print("Lưu ý: Điều chỉnh độ lớn tự động được bật, điều này có thể gây ra", file=sys.stderr)
        print("      méo âm thanh. Nếu âm thanh đầu vào đã được ", file=sys.stderr)
        print("      điều chỉnh độ lớn hoặc nếu âm thanh đầu vào là âm thanh TTS, ", file=sys.stderr)
        print("      vui lòng sử dụng tham số `-d` để tắt điều chỉnh độ lớn.", file=sys.stderr)
        meter = pyln.Meter(sample_rate)
        current_loudness = meter.integrated_loudness(audio)
        audio = pyln.normalize.loudness(audio, current_loudness, target_lufs)
        print(f"Độ lớn đã điều chỉnh: {current_loudness:.1f} LUFS -> {target_lufs} LUFS")

    # Chuyển đổi tốc độ lấy mẫu thành 16000Hz nếu cần
    target_sample_rate = 16000
    if sample_rate != target_sample_rate:
        audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=target_sample_rate)
        sample_rate = target_sample_rate

    # Chuyển đổi dữ liệu âm thanh trở lại int16 sau khi xử lý
    audio = (audio * 32767).astype(np.int16)

    # Khởi tạo bộ mã hóa Opus
    encoder = opuslib.Encoder(sample_rate, 1, opuslib.APPLICATION_AUDIO)

    # Mã hóa và lưu
    with open(output_file, 'wb') as f:
        duration = 60  # 60ms mỗi khung
        frame_size = int(sample_rate * duration / 1000)
        for i in tqdm.tqdm(range(0, len(audio) - frame_size, frame_size)):
            frame = audio[i:i + frame_size]
            opus_data = encoder.encode(frame.tobytes(), frame_size=frame_size)
            packet = struct.pack('>BBH', 0, 0, len(opus_data)) + opus_data
            f.write(packet)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chuyển đổi âm thanh sang Opus với chuẩn hóa độ lớn')
    parser.add_argument('input_file', help='Tệp âm thanh đầu vào')
    parser.add_argument('output_file', help='Tệp .opus đầu ra')
    parser.add_argument('-l', '--lufs', type=float, default=-16.0,
                       help='Độ lớn mục tiêu trong LUFS (mặc định: -16)')
    parser.add_argument('-d', '--disable-loudnorm', action='store_true',
                       help='Tắt chuẩn hóa độ lớn')
    args = parser.parse_args()

    target_lufs = None if args.disable_loudnorm else args.lufs
    encode_audio_to_opus(args.input_file, args.output_file, target_lufs)

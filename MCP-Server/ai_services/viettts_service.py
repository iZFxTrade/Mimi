import io
from typing import AsyncIterator

from pydub import AudioSegment
from vietTTS.nat.text_to_speech import text_to_wav

from .tts_service import TTSService

# Tải mô hình vietTTS một lần khi module được import
# Điều này giúp tránh việc tải lại mô hình cho mỗi yêu cầu
try:
    from vietTTS.nat.config importFLAGS
    print("INFO: Đang tải mô hình VietTTS...")
    # Thiết lập các tham số cần thiết cho mô hình
    FLAGS.ckpt = './assets/vits-laba-340k.pt'
    FLAGS.lexicon_file = './assets/lexicon.txt'
    FLAGS.silence_duration = 0.1
    print("INFO: Mô hình VietTTS đã được tải.")
except ImportError as e:
    print(f"CẢNH BÁO: Không thể import cờ cấu hình của VietTTS. Lỗi: {e}")
except Exception as e:
    print(f"CẢNH BÁO: Không thể tải mô hình VietTTS. Lỗi: {e}. Dịch vụ VietTTS sẽ không hoạt động.")
    # Đặt một biến cờ để kiểm tra trong lớp
    VIET_TTS_LOADED = False
else:
    VIET_TTS_LOADED = True


class VietTTS_TTS(TTSService):
    """Triển khai TTSService sử dụng thư viện VietTTS chạy cục bộ."""

    async def stream_audio(self, text: str, voice: str = 'default', output_format: str = 'opus') -> AsyncIterator[bytes]:
        """
        Chuyển đổi văn bản thành một luồng âm thanh Opus.

        Luồng xử lý:
        1. VietTTS tạo ra dữ liệu WAV trong bộ nhớ.
        2. Pydub đọc dữ liệu WAV từ bộ nhớ.
        3. Pydub chuyển đổi và xuất ra luồng Opus trong bộ nhớ.
        4. Stream các mẩu Opus cho client.
        """
        if not VIET_TTS_LOADED:
            print("LỖI [VietTTS]: Mô hình chưa được tải thành công. Không thể xử lý yêu cầu.")
            yield b''
            return

        try:
            # 1. Tạo dữ liệu WAV trong bộ nhớ
            wav_data = text_to_wav(text)
            wav_buffer = io.BytesIO(wav_data)

            # 2. Sử dụng Pydub để đọc WAV từ buffer
            audio = AudioSegment.from_wav(wav_buffer)

            # 3. Xuất ra định dạng Opus vào một buffer khác
            opus_buffer = io.BytesIO()
            audio.export(
                opus_buffer,
                format="opus",
                # Các tham số này quan trọng để tương thích với ESP32
                parameters=["-ac", "1", "-ar", "16000"]
            )
            opus_buffer.seek(0)

            # 4. Stream các mẩu dữ liệu Opus
            chunk_size = 1024
            while True:
                chunk = opus_buffer.read(chunk_size)
                if not chunk:
                    break
                yield chunk

        except Exception as e:
            print(f"LỖI [VietTTS]: {e}")
            # Đảm bảo hàm vẫn là một async generator ngay cả khi có lỗi
            yield b''

from abc import ABC, abstractmethod
from typing import AsyncIterator

class TTSService(ABC):
    """Lớp cơ sở trừu tượng cho các dịch vụ Text-to-Speech."""

    @abstractmethod
    async def stream_audio(
        self, text: str, voice: str = 'nova', output_format: str = 'opus'
    ) -> AsyncIterator[bytes]:
        """
        Chuyển đổi văn bản thành một luồng âm thanh.

        Args:
            text: Văn bản cần chuyển đổi.
            voice: Tên của giọng nói sẽ sử dụng.
            output_format: Định dạng âm thanh đầu ra mong muốn (ví dụ: 'opus', 'wav').

        Yields:
            Các mẩu (chunks) của dữ liệu âm thanh dưới dạng bytes.
        """
        # Cần một `yield` để biến hàm này thành một trình tạo bất đồng bộ (async generator)
        # khi được triển khai.
        yield b''

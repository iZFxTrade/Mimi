from abc import ABC, abstractmethod
from typing import Optional

class STTService(ABC):
    """Lớp cơ sở trừu tượng cho các dịch vụ Speech-to-Text."""

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, audio_format: str = 'opus') -> Optional[str]:
        """
        Chuyển đổi dữ liệu âm thanh thành văn bản.

        Args:
            audio_bytes: Dữ liệu âm thanh dưới dạng bytes.
            audio_format: Định dạng của dữ liệu âm thanh (ví dụ: 'opus', 'wav').

        Returns:
            Chuỗi văn bản đã được phiên âm, hoặc None nếu thất bại.
        """
        pass

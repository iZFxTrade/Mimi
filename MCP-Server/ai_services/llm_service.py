from abc import ABC, abstractmethod
from typing import Optional

class LLMService(ABC):
    """Lớp cơ sở trừu tượng cho các dịch vụ Mô hình Ngôn ngữ Lớn."""

    @abstractmethod
    async def get_response(self, text: str) -> Optional[str]:
        """
        Nhận phản hồi từ LLM dựa trên văn bản đầu vào.

        Args:
            text: Văn bản đầu vào từ người dùng (kết quả từ STT).

        Returns:
            Chuỗi văn bản phản hồi từ LLM, hoặc None nếu thất bại.
        """
        pass

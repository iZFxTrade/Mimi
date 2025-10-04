#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module này định nghĩa cấu trúc dữ liệu cho Hồ sơ Thiết bị (Device Profile)
và Hồ sơ Người dùng (UserProfile), tạo ra một kiến trúc đa người dùng.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ConversationTurn(BaseModel):
    """Một lượt hỏi và đáp trong hội thoại."""
    human: str
    ai: str


class UserProfile(BaseModel):
    """Mô hình cho một Hồ sơ Người dùng duy nhất trong một thiết bị."""
    user_id: str = Field(description="Khóa chính cho người dùng, vd: 'telegram_12345' hoặc 'dad'.")
    user_name: Optional[str] = Field(None, description="Tên định danh cho người dùng, vd: 'John'.")
    conversation_history: List[ConversationTurn] = Field(default_factory=list)

    def add_conversation_turn(self, human_message: str, ai_message: str, max_history: int = 20):
        """Thêm một lượt hội thoại mới vào lịch sử của người dùng."""
        self.conversation_history.append(ConversationTurn(human=human_message, ai=ai_message))
        if len(self.conversation_history) > max_history:
            self.conversation_history.pop(0)


class AIServicesConfig(BaseModel):
    """Cấu hình các dịch vụ AI cho một thiết bị."""
    llm_provider: str = Field(default="openai", description="Nhà cung cấp LLM: 'openai', 'gemini', 'ollama'...")
    stt_provider: str = Field(default="openai", description="Nhà cung cấp STT: 'openai'...")
    tts_provider: str = Field(default="viettts", description="Nhà cung cấp TTS: 'openai', 'viettts'...")


class TelegramConfig(BaseModel):
    """Cấu hình Telegram cho một thiết bị."""
    bot_token: Optional[str] = None
    allowed_chat_ids: List[str] = []


class DeviceProfile(BaseModel):
    """Mô hình hoàn chỉnh cho một Hồ sơ Thiết bị, giờ đây chứa nhiều người dùng."""
    device_id: str = Field(description="Khóa chính, ví dụ: địa chỉ MAC của thiết bị.")
    assistant_name: str = Field(default="MiMi", description="Tên gọi của trợ lý.")
    system_prompt_template: str = Field(
        default="Bạn là {assistant_name}, một trợ lý ảo thông minh và hữu ích.",
        description="Template cho system prompt, với {assistant_name} là biến thay thế."
    )
    ai_services: AIServicesConfig = Field(default_factory=AIServicesConfig)
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    users: Dict[str, UserProfile] = Field(default_factory=dict, description="Danh bạ các hồ sơ người dùng.")

    def get_system_prompt(self, user_profile: Optional[UserProfile] = None) -> str:
        """Tạo system prompt, có thể cá nhân hóa nếu có thông tin người dùng."""
        base_prompt = self.system_prompt_template.format(assistant_name=self.assistant_name)
        if user_profile and user_profile.user_name:
            return f"{base_prompt} Bạn đang nói chuyện với {user_profile.user_name}."
        return base_prompt

    def get_or_create_user(self, user_id: str, user_name: Optional[str] = None) -> UserProfile:
        """Lấy hoặc tạo một hồ sơ người dùng trong thiết bị."""
        if user_id not in self.users:
            self.users[user_id] = UserProfile(user_id=user_id, user_name=user_name)
        # Cập nhật tên nếu được cung cấp
        elif user_name and self.users[user_id].user_name != user_name:
             self.users[user_id].user_name = user_name
        return self.users[user_id]

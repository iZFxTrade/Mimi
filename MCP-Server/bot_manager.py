#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional

# Sửa đổi import
from profile_manager import ProfileManager
from ai_services.telegram_service import TelegramService

logger = logging.getLogger(__name__)

@dataclass
class BotContainer:
    service: TelegramService
    task: asyncio.Task = field(default=None)

class BotManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BotManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, profile_manager: Optional[ProfileManager] = None):
        if not hasattr(self, 'initialized'):
            self.bots: Dict[str, BotContainer] = {}
            self.profile_manager = profile_manager
            self.initialized = True
            logger.info("BotManager đã được khởi tạo.")

    def set_profile_manager(self, profile_manager: ProfileManager):
        """Thiết lập ProfileManager sau khi khởi tạo."""
        self.profile_manager = profile_manager

    async def run_all_bots_from_profiles(self):
        """Quét qua các hồ sơ và chạy các bot có cấu hình."""
        if not self.profile_manager:
            logger.warning("ProfileManager chưa được thiết lập, không thể chạy bot từ hồ sơ.")
            return

        logger.info("Đang quét hồ sơ để khởi chạy các bot Telegram...")
        count = 0
        for device_id, profile in self.profile_manager.profiles.items():
            if profile.telegram and profile.telegram.bot_token and profile.telegram.bot_token != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
                await self.register_and_run_bot(
                    device_id=device_id,
                    token=profile.telegram.bot_token,
                    allowed_chat_ids=profile.telegram.allowed_chat_ids
                )
                count += 1
        logger.info(f"Đã khởi chạy {count} bot từ các hồ sơ đã lưu.")

    async def register_and_run_bot(self, device_id: str, token: str, allowed_chat_ids: list):
        if device_id in self.bots:
            return

        logger.info(f"Đang đăng ký bot mới cho thiết bị: {device_id}")
        try:
            # Thay đổi ở đây: Truyền device_id và profile_manager vào service
            service = TelegramService(
                token=token,
                allowed_chat_ids=allowed_chat_ids,
                device_id=device_id, 
                profile_manager=self.profile_manager
            )
            
            task = asyncio.create_task(service.run())
            self.bots[device_id] = BotContainer(service=service, task=task)
            logger.info(f"Đã khởi chạy và đăng ký bot thành công cho thiết bị {device_id}.")

        except Exception as e:
            logger.error(f"Lỗi không mong muốn khi chạy bot cho {device_id}: {e}")

    async def stop_bot(self, device_id: str):
        if device_id in self.bots:
            logger.info(f"Đang dừng bot cho thiết bị {device_id}...")
            container = self.bots.pop(device_id)
            await container.service.stop()
            container.task.cancel()
            try:
                await container.task
            except asyncio.CancelledError:
                logger.info(f"Tác vụ bot cho {device_id} đã được hủy thành công.")

    async def shutdown_all(self):
        logger.info("Đang dừng tất cả các bot...")
        all_device_ids = list(self.bots.keys())
        for device_id in all_device_ids:
            await self.stop_bot(device_id)
        logger.info("Tất cả các bot đã được dừng.")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from profile_manager import ProfileManager
from main import get_ai_services_for_device # Vẫn cần factory này

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self, token: str, allowed_chat_ids: list, device_id: str, profile_manager: ProfileManager):
        if not token or token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
            raise ValueError("Token của Telegram Bot không hợp lệ.")
        
        self.allowed_chat_ids = allowed_chat_ids
        self.device_id = device_id
        self.profile_manager = profile_manager
        self.application = Application.builder().token(token).build()
        
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("ask", self.ask_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    # --- Hàm trợ giúp để lấy hồ sơ người dùng ---
    def _get_user_profile_from_update(self, update: Update):
        chat_id = update.effective_chat.id
        if not self._is_allowed(chat_id): return None, None

        user = update.effective_user
        user_id = f"telegram_{user.id}" # Tạo ID duy nhất cho người dùng Telegram
        user_name = user.full_name

        device_profile = self.profile_manager.get_or_create_profile(self.device_id)
        user_profile = device_profile.get_or_create_user(user_id, user_name)
        return device_profile, user_profile

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _, user_profile = self._get_user_profile_from_update(update)
        if not user_profile: return

        device_profile = self.profile_manager.get_profile(self.device_id)
        await update.message.reply_html(
            f"Xin chào {user_profile.user_name}!\n\n"
            f"Tôi là {device_profile.assistant_name}. "
            f"Gõ /help để xem các lệnh có sẵn."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_allowed(update.effective_chat.id): return
        help_text = (
            "Các lệnh có sẵn:\n"
            "/start - Bắt đầu tương tác với bot\n"
            "/help - Hiển thị tin nhắn này\n"
            "/ask <câu hỏi> - Hỏi AI một câu hỏi"
        )
        await update.message.reply_text(help_text)

    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        device_profile, user_profile = self._get_user_profile_from_update(update)
        if not user_profile: return

        question = ' '.join(context.args)
        if not question:
            await update.message.reply_text('Vui lòng nhập câu hỏi sau lệnh /ask.')
            return

        await update.message.reply_chat_action(action="typing")
        try:
            # 1. Lấy LLM service động, giờ đây có cả thông tin người dùng
            _, llm_service, _ = await get_ai_services_for_device(self.device_id, user_profile.user_id)

            if not llm_service:
                await update.message.reply_text('Lỗi: Không thể cấu hình dịch vụ AI cho thiết bị của bạn.')
                return

            # 2. Lấy câu trả lời
            llm_response = await llm_service.get_response(question)
            
            # 3. Lưu lịch sử hội thoại vào hồ sơ người dùng
            user_profile.add_conversation_turn(human_message=question, ai_message=llm_response)
            self.profile_manager.save_profiles() # Lưu lại toàn bộ CSDL hồ sơ

            # 4. Gửi câu trả lời
            await update.message.reply_text(llm_response)

        except Exception as e:
            logger.error(f"Lỗi khi xử lý lệnh /ask cho {self.device_id} (User: {user_profile.user_id}): {e}")
            await update.message.reply_text('Đã có lỗi xảy ra khi xử lý câu hỏi của bạn.')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        device_profile, _ = self._get_user_profile_from_update(update)
        if not device_profile: return
        await update.message.reply_text(f"Để hỏi AI, vui lòng dùng lệnh /ask. Ví dụ: /ask {update.message.text}")

    def _is_allowed(self, chat_id: int) -> bool:
        if not self.allowed_chat_ids: return True
        return str(chat_id) in self.allowed_chat_ids

    async def run(self):
        logger.info(f"Bot cho thiết bị {self.device_id} đang chạy...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def stop(self):
        logger.info(f"Đang dừng bot cho {self.device_id}...")
        await self.application.updater.stop()
        await self.application.stop()

import asyncio
import io
from typing import AsyncIterator, Optional

import openai
from pydub import AudioSegment

from .llm_service import LLMService
from .stt_service import STTService
from .tts_service import TTSService


class OpenAI_STT(STTService):
    """Triển khai STTService sử dụng API Whisper của OpenAI."""

    def __init__(self, client: openai.AsyncOpenAI):
        self.client = client

    async def transcribe(self, audio_bytes: bytes, audio_format: str = 'opus') -> Optional[str]:
        try:
            # Whisper API hỗ trợ trực tiếp định dạng opus, không cần chuyển đổi.
            audio_file = io.BytesIO(audio_bytes)
            transcription = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=(f"audio.{audio_format}", audio_file)
            )
            return transcription.text
        except Exception as e:
            print(f"LỖI [OpenAI_STT]: {e}")
            return None


class OpenAI_LLM(LLMService):
    """Triển khai LLMService sử dụng API Chat Completions của OpenAI."""

    def __init__(self, client: openai.AsyncOpenAI, model: str = "gpt-3.5-turbo", system_prompt: str = "You are a helpful assistant."):
        self.client = client
        self.model = model
        self.system_prompt = system_prompt

    async def get_response(self, text: str) -> Optional[str]:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LỖI [OpenAI_LLM]: {e}")
            return None


class OpenAI_TTS(TTSService):
    """Triển khai TTSService sử dụng API TTS của OpenAI."""

    def __init__(self, client: openai.AsyncOpenAI):
        self.client = client

    async def stream_audio(self, text: str, voice: str = 'nova', output_format: str = 'opus') -> AsyncIterator[bytes]:
        try:
            # API của OpenAI hỗ trợ trực tiếp 'opus' cho TTS
            async with self.client.audio.speech.with_streaming_response(
                model="tts-1",
                voice=voice,
                input=text,
                response_format=output_format
            ) as response:
                async for chunk in response.iter_bytes(chunk_size=1024):
                    yield chunk
        except Exception as e:
            print(f"LỖI [OpenAI_TTS]: {e}")
            # Cần yield một giá trị rỗng để hàm vẫn là một async generator hợp lệ
            yield b''

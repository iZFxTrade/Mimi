#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module này chứa ProfileManager, chịu trách nhiệm quản lý việc lưu trữ và
truy xuất các Hồ sơ Thiết bị (DeviceProfile).
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional

# Chỉ cần import DeviceProfile, vì UserProfile là một phần của nó
from device_profile import DeviceProfile

logger = logging.getLogger(__name__)

class ProfileManager:
    """Quản lý tập hợp các Hồ sơ Thiết bị, lưu trữ trong một tệp JSON."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProfileManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, profiles_file: str = "device_profiles.json"):
        if not hasattr(self, 'initialized'):
            self.profiles_file = Path(profiles_file)
            self.profiles: Dict[str, DeviceProfile] = {}
            self.load_profiles()
            self.initialized = True
            logger.info(f"ProfileManager đã được khởi tạo với tệp '{profiles_file}'.")

    def load_profiles(self):
        """Tải tất cả hồ sơ từ tệp JSON vào bộ nhớ."""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for device_id, profile_data in data.items():
                        # Pydantic sẽ tự động xử lý việc parse các UserProfile lồng nhau
                        self.profiles[device_id] = DeviceProfile(**profile_data)
                logger.info(f"Đã tải {len(self.profiles)} hồ sơ từ {self.profiles_file}.")
            except (json.JSONDecodeError, TypeError) as e:
                logger.error(f"Lỗi khi đọc tệp hồ sơ {self.profiles_file}: {e}. Tạo tệp mới.")
                self.profiles = {}
        else:
            logger.warning(f"Tệp hồ sơ {self.profiles_file} không tồn tại. Sẽ tạo mới khi cần.")

    def save_profiles(self):
        """Lưu tất cả hồ sơ hiện tại vào tệp JSON."""
        try:
            serializable_profiles = {uid: p.dict() for uid, p in self.profiles.items()}
            with open(self.profiles_file, "w", encoding="utf-8") as f:
                json.dump(serializable_profiles, f, ensure_ascii=False, indent=2)
        except (TypeError, IOError) as e:
            logger.error(f"Không thể ghi vào tệp hồ sơ {self.profiles_file}: {e}")

    def get_profile(self, device_id: str) -> Optional[DeviceProfile]:
        """Lấy hồ sơ của một thiết bị."""
        return self.profiles.get(device_id)

    def get_or_create_profile(self, device_id: str) -> DeviceProfile:
        """Lấy hồ sơ của thiết bị, hoặc tạo mới nếu chưa tồn tại."""
        profile = self.get_profile(device_id)
        if profile is None:
            logger.info(f"Không tìm thấy hồ sơ cho {device_id}. Đang tạo hồ sơ mặc định.")
            profile = DeviceProfile(device_id=device_id)
            self.profiles[device_id] = profile
            self.save_profiles()
        return profile

    # Hàm update không cần thay đổi, vì Pydantic xử lý việc cập nhật dict lồng nhau
    def update_profile(self, device_id: str, updates: Dict) -> DeviceProfile:
        """Cập nhật một hồ sơ và lưu lại."""
        profile = self.get_or_create_profile(device_id)
        profile_data = profile.dict()
        updated_data = self._recursive_update(profile_data, updates)
        self.profiles[device_id] = DeviceProfile(**updated_data)
        self.save_profiles()
        logger.info(f"Đã cập nhật hồ sơ cho {device_id}.")
        return self.profiles[device_id]

    def _recursive_update(self, original_dict: Dict, new_dict: Dict) -> Dict:
        for key, value in new_dict.items():
            if isinstance(value, dict) and isinstance(original_dict.get(key), dict):
                original_dict[key] = self._recursive_update(original_dict[key], value)
            else:
                original_dict[key] = value
        return original_dict

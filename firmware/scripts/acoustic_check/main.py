#!/usr/bin/env python3
"""
Chương trình chính của hệ thống giám sát và vẽ đồ thị âm thanh thời gian thực
Dựa trên Qt GUI + Matplotlib + nhận UDP + giải mã chuỗi AFSK
"""

import sys
import asyncio
from graphic import main

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Chương trình bị người dùng ngắt")
    except Exception as e:
        print(f"Lỗi thực thi chương trình: {e}")
        sys.exit(1)

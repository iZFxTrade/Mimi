#!/usr/bin/env python3
import argparse
import json
import os

HEADER_TEMPLATE = """// Tệp cấu hình ngôn ngữ được tạo tự động
// Ngôn ngữ: {lang_code} với dự phòng en-US
#pragma once

#include <string_view>

#ifndef {lang_code_for_font}
    #define {lang_code_for_font}  // Ngôn ngữ mặc định
#endif

namespace Lang {{
    // Siêu dữ liệu ngôn ngữ
    constexpr const char* CODE = "{lang_code}";

    // Tài nguyên chuỗi (dự phòng en-US cho các khóa bị thiếu)
    namespace Strings {{
{strings}
    }}

    // Tài nguyên âm thanh (dự phòng en-US cho các tệp âm thanh bị thiếu)
    namespace Sounds {{
{sounds}
    }}
}}
"""

def load_base_language(assets_dir):
    """Tải dữ liệu ngôn ngữ cơ sở en-US"""
    base_lang_path = os.path.join(assets_dir, 'locales', 'en-US', 'language.json')
    if os.path.exists(base_lang_path):
        try:
            with open(base_lang_path, 'r', encoding='utf-8') as f:
                base_data = json.load(f)
                print(f"Đã tải ngôn ngữ cơ sở en-US với {len(base_data.get('strings', {}))} chuỗi")
                return base_data
        except json.JSONDecodeError as e:
            print(f"Cảnh báo: Không thể phân tích tệp ngôn ngữ en-US: {e}")
    else:
        print("Cảnh báo: Không tìm thấy tệp ngôn ngữ cơ sở en-US, cơ chế dự phòng đã bị vô hiệu hóa")
    return {{'strings': {{}}}}

def get_sound_files(directory):
    """Lấy danh sách tệp âm thanh trong thư mục"""
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if f.endswith('.ogg')]

def generate_header(lang_code, output_path):
    # Suy ra cấu trúc dự án từ đường dẫn đầu ra
    # output_path thường là main/assets/lang_config.h
    main_dir = os.path.dirname(output_path)  # main/assets
    if os.path.basename(main_dir) == 'assets':
        main_dir = os.path.dirname(main_dir)  # main
    project_dir = os.path.dirname(main_dir)  # Thư mục gốc của dự án
    assets_dir = os.path.join(main_dir, 'assets')
    
    # Xây dựng đường dẫn tệp JSON ngôn ngữ
    input_path = os.path.join(assets_dir, 'locales', lang_code, 'language.json')
    
    print(f"Đang xử lý ngôn ngữ: {lang_code}")
    print(f"Đường dẫn tệp đầu vào: {input_path}")
    print(f"Đường dẫn tệp đầu ra: {output_path}")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Không tìm thấy tệp ngôn ngữ: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Xác minh cấu trúc dữ liệu
    if 'language' not in data or 'strings' not in data:
        raise ValueError("Cấu trúc JSON không hợp lệ")

    # Tải dữ liệu ngôn ngữ cơ sở en-US
    base_data = load_base_language(assets_dir)
    
    # Hợp nhất chuỗi: lấy en-US làm cơ sở, ngôn ngữ người dùng sẽ ghi đè
    base_strings = base_data.get('strings', {{}})
    user_strings = data['strings']
    merged_strings = base_strings.copy()
    merged_strings.update(user_strings)
    
    # Thông tin thống kê
    base_count = len(base_strings)
    user_count = len(user_strings)
    total_count = len(merged_strings)
    fallback_count = total_count - user_count
    
    print(f"Thống kê chuỗi ngôn ngữ {lang_code}:")
    print(f"  - Ngôn ngữ cơ sở (en-US): {base_count} chuỗi")
    print(f"  - Ngôn ngữ người dùng: {user_count} chuỗi")
    print(f"  - Tổng cộng: {total_count} chuỗi")
    if fallback_count > 0:
        print(f"  - Dự phòng về en-US: {fallback_count} chuỗi")

    # Tạo hằng số chuỗi
    strings = []
    sounds = []
    for key, value in merged_strings.items():
        value = value.replace('"', '\\"')
        strings.append(f'        constexpr const char* {key.upper()} = "{value}";')

    # Thu thập tệp âm thanh: lấy en-US làm cơ sở, ngôn ngữ người dùng sẽ ghi đè
    current_lang_dir = os.path.join(assets_dir, 'locales', lang_code)
    base_lang_dir = os.path.join(assets_dir, 'locales', 'en-US')
    common_dir = os.path.join(assets_dir, 'common')
    
    # Lấy tất cả các tệp âm thanh có thể
    base_sounds = get_sound_files(base_lang_dir)
    current_sounds = get_sound_files(current_lang_dir)
    common_sounds = get_sound_files(common_dir)
    
    # Hợp nhất danh sách tệp âm thanh: ngôn ngữ người dùng ghi đè lên ngôn ngữ cơ sở
    all_sound_files = set(base_sounds)
    all_sound_files.update(current_sounds)
    
    # Thông tin thống kê âm thanh
    base_sound_count = len(base_sounds)
    user_sound_count = len(current_sounds)
    common_sound_count = len(common_sounds)
    sound_fallback_count = len(set(base_sounds) - set(current_sounds))
    
    print(f"Thống kê âm thanh ngôn ngữ {lang_code}:")
    print(f"  - Ngôn ngữ cơ sở (en-US): {base_sound_count} âm thanh")
    print(f"  - Ngôn ngữ người dùng: {user_sound_count} âm thanh")
    print(f"  - Âm thanh chung: {common_sound_count} âm thanh")
    if sound_fallback_count > 0:
        print(f"  - Dự phòng âm thanh về en-US: {sound_fallback_count} âm thanh")
    
    # Tạo hằng số âm thanh dành riêng cho ngôn ngữ
    for file in sorted(all_sound_files):
        base_name = os.path.splitext(file)[0]
        # Ưu tiên sử dụng âm thanh của ngôn ngữ hiện tại, nếu không tồn tại sẽ dự phòng về en-US
        if file in current_sounds:
            sound_lang = lang_code.replace('-', '_').lower()
        else:
            sound_lang = 'en_us'
            
        sounds.append(f''''
        extern const char ogg_{base_name}_start[] asm("_binary_{base_name}_ogg_start");
        extern const char ogg_{base_name}_end[] asm("_binary_{base_name}_ogg_end");
        static const std::string_view OGG_{base_name.upper()} {{{{
        static_cast<const char*>(ogg_{base_name}_start),
        static_cast<size_t>(ogg_{base_name}_end - ogg_{base_name}_start)
        }}}};'''')
    
    # Tạo hằng số âm thanh chung
    for file in sorted(common_sounds):
        base_name = os.path.splitext(file)[0]
        sounds.append(f''''
        extern const char ogg_{base_name}_start[] asm("_binary_{base_name}_ogg_start");
        extern const char ogg_{base_name}_end[] asm("_binary_{base_name}_ogg_end");
        static const std::string_view OGG_{base_name.upper()} {{{{
        static_cast<const char*>(ogg_{base_name}_start),
        static_cast<size_t>(ogg_{base_name}_end - ogg_{base_name}_start)
        }}}};'''')

    # Điền vào mẫu
    content = HEADER_TEMPLATE.format(
        lang_code=lang_code,
        lang_code_for_font=lang_code.replace('-', '_').lower(),
        strings="\n".join(sorted(strings)),
        sounds="\n".join(sorted(sounds))
    )

    # Ghi vào tệp
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo tệp tiêu đề cấu hình ngôn ngữ với dự phòng en-US")
    parser.add_argument("--language", required=True, help="Mã ngôn ngữ (ví dụ: zh-CN, en-US, ja-JP)")
    parser.add_argument("--output", required=True, help="Đường dẫn tệp tiêu đề đầu ra")
    args = parser.parse_args()

    try:
        generate_header(args.language, args.output)
        print(f"Đã tạo thành công tệp cấu hình ngôn ngữ: {args.output}")
    except Exception as e:
        print(f"Lỗi: {e}")
        exit(1)

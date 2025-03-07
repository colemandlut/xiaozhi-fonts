import os
import subprocess
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Font converter utility')
    parser.add_argument('type', choices=['lvgl', 'dump'], help='Output type: lvgl or dump')
    parser.add_argument('--font-size', type=int, default=14, help='Font size (default: 14)')
    parser.add_argument('--bpp', type=int, default=4, help='Bits per pixel (default: 4)')
    parser.add_argument('--language', choices=['zh_cn', 'zh_tw', 'ja_jp'], help='zh_cn/zh_tw/ja_jp')
    return parser.parse_args()

def load_symbols_zh_cn():
    symbols = ["•", "·", "÷", "×", "©", "¥", "®"]
    for line in open("GB2312.TXT"):
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        unicode = int(parts[1], 16)
        symbols.append(chr(unicode))
    return symbols

def load_symbols_zh_tw():
    symbols = ["•", "·", "÷", "×", "©", "¥", "®"]
    for line in open("BIG5.TXT"):
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        unicode = int(parts[1], 16)
        symbols.append(chr(unicode))
    return symbols

def load_symbols_ja_jp():
    symbols = ["•", "·", "÷", "×", "©", "¥", "®"]
    for line in open("SHIFTJIS.TXT"):
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        unicode = int(parts[1], 16)
        symbols.append(chr(unicode))
    return symbols


def main():
    args = parse_arguments()
    
    flags = "--force-fast-kern-format --no-compress --no-prefilter"
    
    if args.language == "zh_cn":
        font = "AlibabaPuHuiTi-3-55-Regular.ttf"
        symbols = load_symbols_zh_tw()
    elif args.language == "zh_tw":
        font = "NotoSansTC-Medium.ttf"
        symbols = load_symbols_zh_tw()
    elif args.language == "ja_jp":
        font = "NotoSansJP-Medium.ttf"
        symbols = load_symbols_ja_jp()
        
    
    if args.type == "lvgl":
        output = f"src/font_puhui_{args.font_size}_{args.bpp}_{args.language}.c"
        symbols_str = "".join(symbols)
    else:  # dump
        output = f"./dump"
        symbols_str = "欢迎使用小智聊天机器人，这是一个纯手工打造的人工智能硬件产品。"
        cmd = f"lv_font_conv {flags} --font {font} --format dump --bpp {args.bpp} -o {output} --size {args.font_size} -r 0x20-0x7F --symbols {symbols_str}"

    print("Total symbols:", len(symbols_str))
    print("Generating", output)

    # 有些特殊字符無法在shell處理，必須要改成subprocess
    ret = subprocess.call(["lv_font_conv", "--force-fast-kern-format", "--no-compress", "--no-prefilter", 
                    "--font", font, 
                    "--format", "lvgl",
                    "--lv-include", "lvgl.h",
                    "--bpp", str(args.bpp),
                    "-o", output,
                    "--size", str(args.font_size),
                    "-r", "0x20-0x7F",
                    "--symbols", symbols_str])
    if ret != 0:
        print(f"命令执行失败，返回码：{ret}")
    else:
        print("命令执行成功")

if __name__ == "__main__":
    main()


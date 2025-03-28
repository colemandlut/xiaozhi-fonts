import os
import subprocess
import sys
import argparse

font =  ""

def parse_arguments():
    parser = argparse.ArgumentParser(description='Font converter utility')
    parser.add_argument('type', choices=['lvgl', 'dump'], help='Output type: lvgl or dump')
    parser.add_argument('--font-size', type=int, default=14, help='Font size (default: 14)')
    parser.add_argument('--bpp', type=int, default=1, help='Bits per pixel (default: 1)')
    parser.add_argument('--language', choices=['zh_cn', 'zh_tw', 'ja_jp','all'], help='zh_cn/zh_tw/ja_jp/all')
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

def load_symbols_all():
    global font
    symbols_zh = load_symbols_zh_cn()
    font = "--font AlibabaPuHuiTi-3-55-Regular.ttf"
    symbols_ja = load_symbols_ja_jp()
    symbols_tw = load_symbols_zh_tw()

    symbols = symbols_zh + symbols_tw + symbols_ja
    unique_symbols = list(set(symbols))

    return unique_symbols

def main():
    global font
    args = parse_arguments()

    flags = "--force-fast-kern-format --no-compress --no-prefilter"

    # 有些特殊字符無法在shell處理，必須要改成subprocess
    if args.language == "zh_cn":
        font = "NotoSansSC-Regular.ttf"
        symbols = load_symbols_zh_cn()
        output = f"src/font_NatoSans_{args.font_size}_{args.bpp}_{args.language}.c"
    elif args.language == "zh_tw":
        font = "NotoSansTC-Regular.ttf"
        symbols = load_symbols_zh_tw()
        output = f"src/font_NatoSans_{args.font_size}_{args.bpp}_{args.language}.c"
    elif args.language == "ja_jp":
        font = "NotoSansJP-Regular.ttf"
        symbols = load_symbols_ja_jp()
        output = f"src/font_NatoSans_{args.font_size}_{args.bpp}_{args.language}.c"

    if args.language == "all":
        symbols_zh = load_symbols_zh_cn()
        symbols_str_zh = "".join(symbols_zh)
        symbols_tw = load_symbols_zh_tw()
        symbols_str_tw = "".join(symbols_tw)
        symbols_jp = load_symbols_ja_jp()
        symbols_str_jp = "".join(symbols_jp)
        output = f"src/font_NatoSans_{args.font_size}_{args.bpp}_{args.language}.c"

        print("Total symbols:", len(symbols_str_zh)+len(symbols_str_tw)+len(symbols_str_jp))
        print("Generating", output)

        ret = subprocess.call(["lv_font_conv", "--force-fast-kern-format", "--no-compress", "--no-prefilter",
                    "--format", "lvgl",
                    "--lv-include", "lvgl.h",
                    "--bpp", str(args.bpp),
                    "-o", output,
                    "--size", str(args.font_size),
                    "--font", "NotoSansSC-Regular.ttf",
                    "-r", "0x20-0x7F",
                    "--symbols", symbols_str_zh,
                    "--font", "NotoSansTC-Regular.ttf",
                    "-r", "0x20-0x7F",
                    "--symbols", symbols_str_tw,
                    "--font", "NotoSansJP-Regular.ttf",
                    "-r", "0x20-0x7F",
                    "--symbols", symbols_str_jp])
    else:
        if args.type == "lvgl":
            symbols_str = "".join(symbols)
        else:  # dump
            output = f"./dump"
            symbols_str = "欢迎使用小智聊天机器人，这是一个纯手工打造的人工智能硬件产品。"
            cmd = f"lv_font_conv {flags} --font {font} --format dump --bpp {args.bpp} -o {output} --size {args.font_size} -r 0x20-0x7F --symbols {symbols_str}"

        print("Total symbols:", len(symbols_str))
        print("Generating", output)

        ret = subprocess.call(["lv_font_conv", "--force-fast-kern-format", "--no-compress", "--no-prefilter",
            "--format", "lvgl",
            "--lv-include", "lvgl.h",
            "--bpp", str(args.bpp),
            "-o", output,
            "--size", str(args.font_size),
            "--font", font,
            "-r", "0x20-0x7F",
            "--symbols", symbols_str])


    if ret != 0:
        print(f"命令执行失败，返回码：{ret}")
    else:
        print("命令执行成功")

if __name__ == "__main__":
    main()


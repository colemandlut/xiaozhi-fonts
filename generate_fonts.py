import os
import subprocess

# 定义要生成的字体配置
font_configs = [
    (14, 1, "zh_cn"),  # 14号字体，1 bpp
    (16, 4, "zh_cn"),  # 16号字体，4 bpp
    (20, 4, "zh_cn"),  # 20号字体，4 bpp
    (30, 4, "zh_cn"),  # 30号字体，4 bpp
    (14, 1, "zh_tw"),  # 14号字体，1 bpp
    (16, 4, "zh_tw"),  # 16号字体，4 bpp
    (20, 4, "zh_tw"),  # 20号字体，4 bpp
    (30, 4, "zh_tw"),  # 30号字体，4 bpp
    (14, 1, "ja_jp"),  # 14号字体，1 bpp
    (16, 4, "ja_jp"),  # 16号字体，4 bpp
    (20, 4, "ja_jp"),  # 20号字体，4 bpp
    (30, 4, "ja_jp"),  # 30号字体，4 bpp
    (14, 1, "all"),  # 14号字体，1 bpp
    (16, 4, "all"),  # 16号字体，4 bpp
    (20, 4, "all"),  # 20号字体，4 bpp
    (30, 4, "all"),  # 30号字体，4 bpp


]

def main():
    # 遍历所有字体配置
    for size, bpp, language in font_configs:
        print(f"\n正在生成 {size}px 字体，{bpp} bpp...")
        
        # 构建命令并执行
        cmd = f"python3 font.py lvgl --language {language} --font-size {size} --bpp {bpp}"
        ret = os.system(cmd) 
        
        if ret != 0:
            print(f"生成 {size}px 字体失败")
        else:
            print(f"生成 {size}px 字体成功")

if __name__ == "__main__":
    main() 

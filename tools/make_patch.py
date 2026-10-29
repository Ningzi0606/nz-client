# -*- coding: utf-8 -*-
import os, zipfile, shutil

OUT = r"C:\大肥鱼\升级包"
SRC = r"C:\大肥鱼\build\凝紫客户端.exe"
URL = "https://raw.githubusercontent.com/Ningzi0606/nz-client/main/update.json"

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, "updater"))
shutil.copy2(SRC, os.path.join(OUT, "updater", "凝紫客户端.exe"))
with open(os.path.join(OUT, "updater", "updater.ini"), "w", encoding="utf-8") as f:
    f.write("url=" + URL + "\n")

bat = r"""@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist "凝紫客户端.exe" if not exist "凝紫客户端(主程序).exe" ren "凝紫客户端.exe" "凝紫客户端(主程序).exe"
if not exist "凝紫客户端(主程序).exe" (
  echo 没找到 凝紫客户端.exe，请把这个升级包解压到客户端文件夹里再运行。
  pause
  exit /b
)
copy /y "updater\凝紫客户端.exe" "凝紫客户端.exe" >nul
copy /y "updater\updater.ini" "updater.ini" >nul
echo.
echo 升级完成！以后直接双击 凝紫客户端.exe，就会自动检查并更新到最新版。
pause
"""
with open(os.path.join(OUT, "一键升级.bat"), "w", encoding="gbk") as f:
    f.write(bat)

readme = """凝紫客户端 · 自动更新升级包
================================
1. 把这个压缩包解压到客户端文件夹里（和 凝紫客户端.exe 同一个目录）
2. 双击「一键升级.bat」，看到"升级完成"即可
3. 以后直接双击 凝紫客户端.exe，客户端会自己检查更新并按需下载

说明：
- 原来的启动器会被改名成 凝紫客户端(主程序).exe，不会被删除
- 升级后想还原：删掉新的 凝紫客户端.exe，把 凝紫客户端(主程序).exe 改回 凝紫客户端.exe 即可
"""
with open(os.path.join(OUT, "说明.txt"), "w", encoding="utf-8") as f:
    f.write(readme)

zip_path = r"C:\大肥鱼\凝紫客户端-自动更新升级包.zip"
if os.path.exists(zip_path):
    os.remove(zip_path)
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for dirpath, _, filenames in os.walk(OUT):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, OUT)
            z.write(full, os.path.join("凝紫客户端-自动更新升级包", rel))
print("OK", zip_path, os.path.getsize(zip_path))

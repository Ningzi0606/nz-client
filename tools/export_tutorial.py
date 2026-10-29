import shutil, os

src = r"C:\大肥鱼\凝紫服-Mac玩家进服教程.md"
dst_md = r"C:\Users\Administrator\Desktop\凝紫服-Mac玩家进服教程.md"
dst_txt = r"C:\Users\Administrator\Desktop\凝紫服-Mac玩家进服教程.txt"

shutil.copy2(src, dst_md)
text = open(src, encoding="utf-8").read()
# 给记事本/微信用的纯文本版：去掉 markdown 记号
plain = text.replace("**", "").replace("`", "").replace("> ", "")
open(dst_txt, "w", encoding="utf-8").write(plain)
print(os.path.getsize(dst_md), os.path.getsize(dst_txt))

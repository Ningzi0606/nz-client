p = r"C:\大肥鱼\nz-client\README.md"
t = open(p, encoding="utf-8").read()
old = """凝紫客户端(主程序).exe, logo.png, app.ico, manifest.json,
使用说明.txt, 更新说明.txt,
game/config/CustomSkinLoader/CustomSkinLoader.json,
game/CustomSkinLoader/CustomSkinLoader.json
"""
new = """凝紫客户端(主程序).exe, logo.png, app.ico, manifest.json,
使用说明.txt, 更新说明.txt,
game/config/CustomSkinLoader/CustomSkinLoader.json,
game/CustomSkinLoader/CustomSkinLoader.json,
game/mods/Quick Skin - Fabric - 26.3-3.1.1.jar,
game/mods/architectury-fabric-22.0.5.jar
"""
if old in t:
    t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t)
    print("patched")
else:
    print("pattern not found")

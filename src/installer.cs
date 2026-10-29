using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

// 凝紫客户端 v5 升级器（给已经装了 v4 的玩家）
// 双击 → 自动找客户端目录 → 把旧启动器改名 → 装上新更新器
public static class Installer
{
    const string MAIN = "凝紫客户端.exe";
    const string CORE = "凝紫客户端(主程序).exe";
    const string INI = "updater.ini";
    const string URL = "https://raw.githubusercontent.com/Ningzi0606/nz-client/main/update.json";

    [STAThread]
    public static void Main()
    {
        try
        {
            string dir = FindClientDir();
            if (dir == null)
            {
                MessageBox.Show("没找到客户端文件夹。\n\n请把本程序放到客户端文件夹里（和 凝紫客户端.exe 同一个目录）再双击。",
                    "凝紫客户端 v5 升级", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            string main = Path.Combine(dir, MAIN);
            string core = Path.Combine(dir, CORE);

            if (!File.Exists(core) && !File.Exists(main))
            {
                MessageBox.Show("这个文件夹里没有 凝紫客户端.exe，不像客户端目录：\n" + dir,
                    "凝紫客户端 v5 升级", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (!File.Exists(core) && File.Exists(main))
            {
                try { File.Move(main, core); }
                catch (Exception ex)
                {
                    MessageBox.Show("改名字失败（可能客户端还开着）：\n" + ex.Message + "\n\n请先关掉客户端和游戏再试。",
                        "凝紫客户端 v5 升级", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
            }

            Extract("updater.bin", main);
            File.WriteAllText(Path.Combine(dir, INI), "url=" + URL + Environment.NewLine);

            MessageBox.Show("升级完成！\n\n以后直接双击 凝紫客户端.exe，会自动检查更新再启动游戏。\n\n目录：" + dir,
                "凝紫客户端 v5 升级", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            MessageBox.Show("升级出错：" + ex.Message, "凝紫客户端 v5 升级", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    static string FindClientDir()
    {
        string self = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        if (LooksLikeClient(self)) return self;

        // 桌面快捷方式
        foreach (var name in new[] { "凝紫客户端.lnk", "凝紫客户端 - 快捷方式.lnk" })
        {
            var lnk = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory), name);
            if (!File.Exists(lnk)) continue;
            try
            {
                var t = Type.GetTypeFromProgID("WScript.Shell");
                dynamic sh = Activator.CreateInstance(t);
                dynamic sc = sh.CreateShortcut(lnk);
                string target = (string)sc.TargetPath;
                string d = Path.GetDirectoryName(target);
                if (LooksLikeClient(d)) return d;
            }
            catch { }
        }

        using (var dlg = new FolderBrowserDialog())
        {
            dlg.Description = "请选择凝紫客户端文件夹（里面有 凝紫客户端.exe 和 game 文件夹）";
            if (dlg.ShowDialog() == DialogResult.OK && LooksLikeClient(dlg.SelectedPath)) return dlg.SelectedPath;
        }
        return null;
    }

    static bool LooksLikeClient(string dir)
    {
        if (string.IsNullOrEmpty(dir)) return false;
        return File.Exists(Path.Combine(dir, MAIN)) || File.Exists(Path.Combine(dir, CORE));
    }

    static void Extract(string resName, string target)
    {
        using (var s = Assembly.GetExecutingAssembly().GetManifestResourceStream(resName))
        {
            if (s == null) throw new Exception("缺少内置更新器资源");
            using (var f = File.Create(target))
                s.CopyTo(f);
        }
    }
}

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using System.Web.Script.Serialization;

// 凝紫客户端 更新引导器
// 1) 读 updater.ini 的 url= （指向 GitHub 上的 update.json）
// 2) 对比 .clientver 版本号，需要更新时按清单下载、校验 sha256、覆盖
// 3) 无论成功失败，最后都启动 凝紫客户端(主程序).exe
public static class Program
{
    const string CORE_NAME = "凝紫客户端(主程序).exe";
    const string VER_FILE = ".clientver";
    const string LOG_FILE = "updater.log";
    static string LastError = "";

    static Program()
    {
        try
        {
            ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072 | (SecurityProtocolType)12288;
            ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };
            ServicePointManager.CheckCertificateRevocationList = false;
            ServicePointManager.Expect100Continue = false;
        }
        catch { }
    }

    [STAThread]
    public static void Main(string[] args)
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\');
        string core = Path.Combine(dir, CORE_NAME);
        string log = Path.Combine(dir, LOG_FILE);

        try
        {
            RunUpdate(dir, log);
        }
        catch (Exception ex)
        {
            Log(log, "更新异常: " + ex.GetType().Name + " " + ex.Message);
        }

        if (File.Exists(core))
        {
            try
            {
                Process.Start(new ProcessStartInfo(core) { WorkingDirectory = dir, UseShellExecute = false });
            }
            catch (Exception ex)
            {
                MessageBox.Show("启动主程序失败：" + ex.Message, "凝紫客户端", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        else
        {
            MessageBox.Show("找不到 " + CORE_NAME + "\n请重新解压完整客户端。", "凝紫客户端", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    static void RunUpdate(string dir, string log)
    {
        string iniPath = Path.Combine(dir, "updater.ini");
        string url = ReadIni(iniPath, "url");
        if (string.IsNullOrEmpty(url))
        {
            Log(log, "updater.ini 没有 url=，跳过更新");
            return;
        }

        string json = HttpGet(url, 15000);
        if (json == null) { Log(log, "拉取清单失败，跳过" + (LastError == "" ? "" : "：" + LastError)); return; }

        var ser = new JavaScriptSerializer();
        var manifest = ser.Deserialize<Dictionary<string, object>>(json);
        if (manifest == null || !manifest.ContainsKey("version")) { Log(log, "清单格式不对，跳过"); return; }

        string version = Convert.ToString(manifest["version"]);
        string local = "";
        string verPath = Path.Combine(dir, VER_FILE);
        if (File.Exists(verPath)) local = File.ReadAllText(verPath).Trim();
        Log(log, "本地 " + (local == "" ? "未记录" : local) + " -> 远端 " + version);
        if (local == version) return;

        string baseUrl = manifest.ContainsKey("base") ? Convert.ToString(manifest["base"]) : "";
        var files = manifest.ContainsKey("files") ? manifest["files"] as Dictionary<string, object> : null;
        var remove = manifest.ContainsKey("remove") ? manifest["remove"] as System.Collections.IEnumerable : null;

        var todo = new List<KeyValuePair<string, Dictionary<string, object>>>();
        if (files != null)
        {
            foreach (var kv in files)
            {
                var info = kv.Value as Dictionary<string, object>;
                if (info == null) continue;
                string rel = kv.Key;
                string target = Path.Combine(dir, rel.Replace('/', Path.DirectorySeparatorChar));
                if (!File.Exists(target)) { todo.Add(new KeyValuePair<string, Dictionary<string, object>>(rel, info)); continue; }
                string want = info.ContainsKey("sha256") ? Convert.ToString(info["sha256"]) : "";
                if (want.Length == 0) continue;
                if (!string.Equals(Sha256File(target), want, StringComparison.OrdinalIgnoreCase))
                    todo.Add(new KeyValuePair<string, Dictionary<string, object>>(rel, info));
            }
        }

        if (remove != null)
        {
            foreach (var o in remove)
            {
                try
                {
                    string p = Path.Combine(dir, Convert.ToString(o).Replace('/', Path.DirectorySeparatorChar));
                    if (File.Exists(p)) { File.Delete(p); Log(log, "已删除 " + o); }
                }
                catch { }
            }
        }

        if (todo.Count == 0)
        {
            File.WriteAllText(verPath, version);
            Log(log, "没有需要下载的文件");
            return;
        }

        // 主程序放到最后：它最容易被占用，失败也不该拖累其它文件
        todo.Sort(delegate (KeyValuePair<string, Dictionary<string, object>> a, KeyValuePair<string, Dictionary<string, object>> b)
        {
            bool ca = string.Equals(a.Key, CORE_NAME, StringComparison.OrdinalIgnoreCase);
            bool cb = string.Equals(b.Key, CORE_NAME, StringComparison.OrdinalIgnoreCase);
            if (ca == cb) return 0;
            return ca ? 1 : -1;
        });

        int failed = 0;
        using (var form = new ProgressForm(todo.Count))
        {
            form.Show();
            Application.DoEvents();
            int done = 0;
            foreach (var item in todo)
            {
                done++;
                form.SetStatus("正在更新 " + done + "/" + todo.Count, done);
                Application.DoEvents();
                string tmp = null;
                try
                {
                    string relUrl = baseUrl + EscapePath(item.Key);
                    byte[] data = HttpGetBytes(relUrl, 30000);
                    if (data == null) throw new Exception("下载失败: " + item.Key);
                    string want = item.Value.ContainsKey("sha256") ? Convert.ToString(item.Value["sha256"]) : "";
                    if (want.Length > 0)
                    {
                        string got = Sha256Bytes(data);
                        if (!string.Equals(got, want, StringComparison.OrdinalIgnoreCase))
                            throw new Exception("校验失败: " + item.Key);
                    }
                    string target = Path.Combine(dir, item.Key.Replace('/', Path.DirectorySeparatorChar));
                    Directory.CreateDirectory(Path.GetDirectoryName(target));
                    tmp = target + ".download";
                    File.WriteAllBytes(tmp, data);
                    if (File.Exists(target)) File.Delete(target);
                    File.Move(tmp, target);
                    tmp = null;
                    Log(log, "已更新 " + item.Key + " (" + data.Length + " 字节)");
                }
                catch (Exception ex)
                {
                    failed++;
                    LastError = ex.Message;
                    Log(log, "跳过 " + item.Key + "：" + ex.Message);
                    if (tmp != null) { try { File.Delete(tmp); } catch { } }
                }
            }
            form.Close();
        }

        if (failed > 0)
        {
            Log(log, "更新未完成，失败 " + failed + " 项，下次启动会重试");
            return;
        }

        File.WriteAllText(verPath, version);
        Log(log, "更新完成，版本 " + version);
    }

    class ProgressForm : Form
    {
        Label label;
        ProgressBar bar;
        public ProgressForm(int total)
        {
            Text = "凝紫客户端 · 正在更新";
            FormBorderStyle = FormBorderStyle.FixedDialog;
            StartPosition = FormStartPosition.CenterScreen;
            MaximizeBox = false; MinimizeBox = false;
            ClientSize = new Size(380, 96);
            label = new Label { Left = 16, Top = 18, Width = 348, Text = "正在检查更新…" };
            bar = new ProgressBar { Left = 16, Top = 50, Width = 348, Maximum = Math.Max(total, 1) };
            Controls.Add(label); Controls.Add(bar);
        }
        public void SetStatus(string text, int value)
        {
            label.Text = text;
            if (value <= bar.Maximum) bar.Value = value;
        }
    }

    static string EscapePath(string rel)
    {
        var parts = rel.Split('/');
        for (int i = 0; i < parts.Length; i++) parts[i] = Uri.EscapeDataString(parts[i]);
        return string.Join("/", parts);
    }

    static string ReadIni(string path, string key)
    {
        if (!File.Exists(path)) return "";
        foreach (var line in File.ReadAllLines(path, Encoding.UTF8))
        {
            var t = line.Trim();
            if (t.StartsWith("#") || t.StartsWith(";")) continue;
            int i = t.IndexOf('=');
            if (i <= 0) continue;
            if (t.Substring(0, i).Trim().Equals(key, StringComparison.OrdinalIgnoreCase))
                return t.Substring(i + 1).Trim();
        }
        return "";
    }

    static string HttpGet(string url, int timeoutMs)
    {
        try
        {
            var req = (HttpWebRequest)WebRequest.Create(url);
            req.Proxy = null;
            req.UserAgent = "NZUpdater/1.0";
            req.Timeout = timeoutMs;
            req.ReadWriteTimeout = timeoutMs;
            ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12;
            using (var resp = (HttpWebResponse)req.GetResponse())
            using (var rs = resp.GetResponseStream())
            using (var sr = new StreamReader(rs, Encoding.UTF8))
                return sr.ReadToEnd();
        }
        catch (Exception ex) { LastError = ex.Message; return null; }
    }

    static byte[] HttpGetBytes(string url, int timeoutMs)
    {
        try
        {
            var req = (HttpWebRequest)WebRequest.Create(url);
            req.Proxy = null;
            req.UserAgent = "NZUpdater/1.0";
            req.Timeout = timeoutMs;
            req.ReadWriteTimeout = timeoutMs;
            ServicePointManager.SecurityProtocol |= SecurityProtocolType.Tls12;
            using (var resp = (HttpWebResponse)req.GetResponse())
            using (var ms = new MemoryStream())
            {
                resp.GetResponseStream().CopyTo(ms);
                return ms.ToArray();
            }
        }
        catch (Exception ex) { LastError = ex.Message; return null; }
    }

    static string Sha256File(string path)
    {
        using (var sha = SHA256.Create())
        using (var fs = File.OpenRead(path))
            return ToHex(sha.ComputeHash(fs));
    }

    static string Sha256Bytes(byte[] data)
    {
        using (var sha = SHA256.Create())
            return ToHex(sha.ComputeHash(data));
    }

    static string ToHex(byte[] hash)
    {
        var sb = new StringBuilder(hash.Length * 2);
        foreach (var b in hash) sb.Append(b.ToString("x2"));
        return sb.ToString();
    }

    static void Log(string path, string msg)
    {
        try
        {
            File.AppendAllText(path, DateTime.Now.ToString("HH:mm:ss ") + msg + Environment.NewLine, Encoding.UTF8);
        }
        catch { }
    }
}

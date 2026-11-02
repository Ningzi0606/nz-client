using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Net.Cache;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Web.Script.Serialization;
using System.Windows.Forms;

[assembly: RuntimeCompatibility(WrapNonExceptionThrows = true)]
[assembly: CompilationRelaxations(8)]
[assembly: AssemblyVersion("0.0.0.0")]
public class TimeoutWebClient : WebClient
{
	public int TimeoutMs = 12000;

	protected override WebRequest GetWebRequest(Uri address)
	{
		WebRequest webRequest = base.GetWebRequest(address);
		try
		{
			webRequest.Timeout = TimeoutMs;
			HttpWebRequest httpWebRequest = webRequest as HttpWebRequest;
			if (httpWebRequest == null)
			{
				return webRequest;
			}
			httpWebRequest.ReadWriteTimeout = TimeoutMs;
			httpWebRequest.AllowAutoRedirect = true;
			httpWebRequest.KeepAlive = false;
			return webRequest;
		}
		catch
		{
			return webRequest;
		}
	}
}
public class Launcher : Form
{
	private const string Server = "play.simpfun.cn:14039";

	private const string Title = "凝紫服务器 二周目";

	private static string BaseDir;

	private static string GameDir;

	private static string AssetsDir;

	private static string LibDir;

	private static string VerDir;

	private TextBox txtName;

	private TextBox txtPass;

	private Label lblStatus;

	private ProgressBar bar;

	private Button btnStart;

	private TextBox txtLog;
	private LinkLabel lnkHelp;

	private static readonly object fileLock = new object();

	[DllImport("user32.dll")]
	private static extern bool SetProcessDPIAware();

	public Launcher()
	{
		BaseDir = AppDomain.CurrentDomain.BaseDirectory;
		GameDir = Path.Combine(BaseDir, "game");
		AssetsDir = Path.Combine(GameDir, "assets");
		LibDir = Path.Combine(BaseDir, "libraries");
		VerDir = Path.Combine(GameDir, "versions", "26.3");
		if (!LooksLikeClientFolder())
		{
			MessageBox.Show("这里找不到客户端文件（runtime / game 目录）。\n\n多半是把「凝紫客户端.exe」单独复制出来了 —— 它必须和 runtime、game、游戏资源-assets.zip 放在同一个文件夹里。\n\n正确做法：复制整个「凝紫客户端」文件夹；想放到桌面就右键 exe →「发送到」→「桌面快捷方式」。\n\n当前目录：" + BaseDir, "凝紫服务器 二周目", MessageBoxButtons.OK, MessageBoxIcon.Hand);
			Environment.Exit(1);
		}
		EnsureDesktopShortcut("凝紫客户端");
		Text = "凝紫服务器 二周目 客户端";
		base.ClientSize = new Size(620, 480);
		base.FormBorderStyle = FormBorderStyle.FixedSingle;
		base.MaximizeBox = false;
		base.StartPosition = FormStartPosition.CenterScreen;
		BackColor = Color.FromArgb(26, 16, 48);
		ForeColor = Color.White;
		Font = new Font("微软雅黑", 9f);
		base.AutoScaleMode = AutoScaleMode.Dpi;
		base.AutoScaleDimensions = new SizeF(96f, 96f);
		DoubleBuffered = true;
		try
		{
			AutoScroll = false;
		}
		catch
		{
		}
		Label label = new Label();
		label.Text = "凝紫服务器 二周目";
		label.Font = new Font("微软雅黑", 17f, FontStyle.Bold);
		label.ForeColor = Color.FromArgb(201, 166, 255);
		label.SetBounds(24, 16, 460, 36);
		base.Controls.Add(label);
		Label label2 = new Label();
		label2.Text = "Minecraft 26.3  ·  Fabric  ·  自动更新";
		label2.ForeColor = Color.FromArgb(150, 130, 190);
		label2.SetBounds(26, 52, 500, 20);
		base.Controls.Add(label2);
		try
		{
			string text = Path.Combine(BaseDir, "logo.png");
			if (File.Exists(text))
			{
				PictureBox pictureBox = new PictureBox();
				Image image2 = pictureBox.Image = Image.FromFile(text);
				pictureBox.SizeMode = PictureBoxSizeMode.Zoom;
				pictureBox.SetBounds(524, 14, 76, 76);
				base.Controls.Add(pictureBox);
			}
		}
		catch
		{
		}
		Label label3 = new Label();
		label3.Text = "玩家名";
		label3.SetBounds(26, 86, 60, 22);
		base.Controls.Add(label3);
		txtName = new TextBox();
		txtName.SetBounds(96, 84, 380, 26);
		txtName.Text = LoadCfg("name");
		base.Controls.Add(txtName);
		Label label4 = new Label();
		label4.Text = "进服密码";
		label4.SetBounds(26, 118, 70, 22);
		base.Controls.Add(label4);
		txtPass = new TextBox();
		txtPass.SetBounds(96, 116, 380, 26);
		txtPass.UseSystemPasswordChar = true;
		txtPass.Text = LoadCfg("pass");
		base.Controls.Add(txtPass);
		Label label5 = new Label();
		label5.Text = "首次进服用自己的名字，进服后输入 /register 密码 ，再输入 /autologin set 密码（只需一次）";
		label5.ForeColor = Color.FromArgb(150, 130, 190);
		label5.Font = new Font("微软雅黑", 8.5f);
		label5.SetBounds(26, 150, 570, 44);
		base.Controls.Add(label5);
		lblStatus = new Label();
		lblStatus.Text = "就绪";
		lblStatus.ForeColor = Color.FromArgb(180, 220, 255);
		lblStatus.SetBounds(26, 198, 470, 20);
		base.Controls.Add(lblStatus);
		bar = new ProgressBar();
		bar.SetBounds(26, 222, 570, 16);
		bar.Style = ProgressBarStyle.Continuous;
		base.Controls.Add(bar);
		btnStart = new Button();
		btnStart.Text = "启 动 游 戏";
		btnStart.Font = new Font("微软雅黑", 11f, FontStyle.Bold);
		btnStart.SetBounds(26, 252, 570, 48);
		btnStart.BackColor = Color.FromArgb(124, 77, 255);
		btnStart.ForeColor = Color.White;
		btnStart.FlatStyle = FlatStyle.Flat;
		btnStart.FlatAppearance.BorderSize = 0;
		btnStart.Click += delegate
		{
			OnStart();
		};
		base.Controls.Add(btnStart);
		txtLog = new TextBox();
		txtLog.Multiline = true;
		txtLog.ReadOnly = true;
		txtLog.ScrollBars = ScrollBars.Vertical;
		txtLog.SetBounds(26, 312, 570, 120);
		txtLog.BackColor = Color.FromArgb(18, 10, 34);
		txtLog.ForeColor = Color.FromArgb(170, 170, 200);
		txtLog.BorderStyle = BorderStyle.None;
		base.Controls.Add(txtLog);
		lnkHelp = new LinkLabel();
		lnkHelp.Text = "使用说明 / 常见问题（皮肤 · 登录 · 更新）";
		lnkHelp.LinkColor = Color.FromArgb(160, 190, 255);
		lnkHelp.ActiveLinkColor = Color.White;
		lnkHelp.LinkBehavior = LinkBehavior.HoverUnderline;
		lnkHelp.SetBounds(26, 438, 460, 22);
		lnkHelp.Click += delegate
		{
			ShowHelp();
		};
		base.Controls.Add(lnkHelp);
		try
		{
			base.Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath);
		}
		catch
		{
		}
		base.Load += delegate
		{
			btnStart.Enabled = false;
			ThreadPool.QueueUserWorkItem(delegate
			{
				try
				{
					UpdateClient();
				}
				catch (Exception arg)
				{
					LogFile("UPDATE: " + arg);
				}
				finally
				{
					try
					{
						BeginInvoke((MethodInvoker)delegate
						{
							btnStart.Enabled = true;
						});
					}
					catch
					{
					}
				}
			});
		};
	}

	private void ShowHelp()
	{
		try
		{
			using (HelpForm helpForm = new HelpForm(BaseDir))
			{
				helpForm.ShowDialog(this);
			}
		}
		catch (Exception ex)
		{
			MessageBox.Show("打开说明失败：" + ex.Message, "凝紫服务器 二周目");
		}
	}

	private static bool LooksLikeClientFolder()
	{
		string path = Path.Combine(BaseDir, "runtime", "bin", "javaw.exe");
		string path2 = Path.Combine(BaseDir, "runtime", "bin", "java.exe");
		string path3 = Path.Combine(GameDir, "versions", "26.3", "26.3.json");
		if (File.Exists(path) || File.Exists(path2))
		{
			return File.Exists(path3);
		}
		return false;
	}

	private static void EnsureDesktopShortcut(string name)
	{
		try
		{
			string executablePath = Application.ExecutablePath;
			string folderPath = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
			if (!string.IsNullOrEmpty(folderPath) && Directory.Exists(folderPath))
			{
				Type typeFromProgID = Type.GetTypeFromProgID("WScript.Shell");
				if (!(typeFromProgID == (Type)null))
				{
					object obj = Activator.CreateInstance(typeFromProgID);
					if (obj != null)
					{
						object obj2 = typeFromProgID.InvokeMember("CreateShortcut", BindingFlags.InvokeMethod, null, obj, new object[1]
						{
							Path.Combine(folderPath, name + ".lnk")
						});
						if (obj2 != null)
						{
							Type type = obj2.GetType();
							type.InvokeMember("TargetPath", BindingFlags.SetProperty, null, obj2, new object[1]
							{
								executablePath
							});
							type.InvokeMember("WorkingDirectory", BindingFlags.SetProperty, null, obj2, new object[1]
							{
								BaseDir
							});
							type.InvokeMember("IconLocation", BindingFlags.SetProperty, null, obj2, new object[1]
							{
								executablePath + ",0"
							});
							type.InvokeMember("Description", BindingFlags.SetProperty, null, obj2, new object[1]
							{
								"凝紫服务器 二周目 客户端"
							});
							type.InvokeMember("Save", BindingFlags.InvokeMethod, null, obj2, null);
							Marshal.ReleaseComObject(obj2);
						}
						Marshal.ReleaseComObject(obj);
					}
				}
			}
		}
		catch
		{
		}
	}

	private static string CfgPath()
	{
		return Path.Combine(BaseDir, "config.ini");
	}

	private static string LoadCfg(string key)
	{
		try
		{
			string path = CfgPath();
			if (!File.Exists(path))
			{
				return "";
			}
			string[] array = File.ReadAllLines(path);
			foreach (string text in array)
			{
				int num = text.IndexOf('=');
				if (num > 0 && text.Substring(0, num).Trim() == key)
				{
					return text.Substring(num + 1).Trim();
				}
			}
		}
		catch
		{
		}
		return "";
	}

	private static void SaveCfg(string name, string pass)
	{
		try
		{
			File.WriteAllText(CfgPath(), "name=" + name + "\r\npass=" + pass + "\r\n", Encoding.UTF8);
		}
		catch
		{
		}
	}

	private void Log(string s)
	{
		if (base.InvokeRequired)
		{
			BeginInvoke((MethodInvoker)delegate
			{
				Log(s);
			});
		}
		else
		{
			txtLog.AppendText(s + "\r\n");
			try
			{
				string text = Path.Combine(BaseDir, "launcher.log");
				FileInfo fileInfo = new FileInfo(text);
				if (fileInfo.Exists && fileInfo.Length > 1048576)
				{
					File.Delete(text);
				}
				File.AppendAllText(text, DateTime.Now.ToString("HH:mm:ss ") + s + "\r\n", Encoding.UTF8);
			}
			catch
			{
			}
		}
	}

	private void Status(string s, int pct)
	{
		if (base.InvokeRequired)
		{
			BeginInvoke((MethodInvoker)delegate
			{
				Status(s, pct);
			});
		}
		else
		{
			lblStatus.Text = s;
			if (pct >= 0)
			{
				bar.Value = Math.Max(0, Math.Min(100, pct));
			}
		}
	}

	private void OnStart()
	{
		string name = txtName.Text.Trim();
		string text = txtPass.Text;
		if (name.Length < 3 || name.Length > 16 || !Regex.IsMatch(name, "^[A-Za-z0-9_]+$"))
		{
			MessageBox.Show("玩家名只能是 3-16 位字母、数字、下划线。", "凝紫服务器 二周目");
		}
		else
		{
			SaveCfg(name, text);
			btnStart.Enabled = false;
			txtLog.Clear();
			ThreadPool.QueueUserWorkItem(delegate
			{
				try
				{
					DoStart(name);
				}
				catch (Exception ex)
				{
					Log("ERROR: " + ex.Message);
					Status("启动失败", 0);
					MessageBox.Show("启动失败：\r\n\r\n" + ex.Message, "凝紫服务器 二周目");
				}
				finally
				{
					BeginInvoke((MethodInvoker)delegate
					{
						btnStart.Enabled = true;
					});
				}
			});
		}
	}

	private static string OfflineUuid(string name)
	{
		MD5 mD = MD5.Create();
		byte[] array = mD.ComputeHash(Encoding.UTF8.GetBytes("OfflinePlayer:" + name));
		array[6] = (byte)((array[6] & 0xF) | 0x30);
		array[8] = (byte)((array[8] & 0x3F) | 0x80);
		string text = BitConverter.ToString(array).Replace("-", "").ToLower();
		return text.Substring(0, 8) + "-" + text.Substring(8, 4) + "-" + text.Substring(12, 4) + "-" + text.Substring(16, 4) + "-" + text.Substring(20, 12);
	}

	private void DoStart(string name)
	{
		UpdateClient();
		Status("检查游戏文件…", 3);
		Log("客户端目录: " + BaseDir);
		Log("玩家名: " + name);
		if (!Directory.Exists(VerDir))
		{
			throw new Exception("找不到游戏版本目录: " + VerDir);
		}
		string path = Path.Combine(VerDir, "26.3.json");
		if (!File.Exists(path))
		{
			throw new Exception("缺少版本文件 26.3.json");
		}
		string text = File.ReadAllText(path, Encoding.UTF8);
		string text2 = Match(text, "\"mainClass\"\\s*:\\s*\"([^\"]+)\"");
		if (text2 == null)
		{
			throw new Exception("版本文件里没有 mainClass");
		}
		string text3 = "34";
		Match match = Regex.Match(text, "\"assetIndex\"\\s*:\\s*\\{[^}]*\"id\"\\s*:\\s*\"([^\"]+)\"");
		if (match.Success)
		{
			text3 = match.Groups[1].Value;
		}
		string indexUrl = null;
		Match match2 = Regex.Match(text, "\"assetIndex\"\\s*:\\s*\\{[^}]*\"url\"\\s*:\\s*\"([^\"]+)\"");
		if (match2.Success)
		{
			indexUrl = match2.Groups[1].Value;
		}
		try
		{
			UpdateMods();
		}
		catch (Exception ex)
		{
			Log("自动更新跳过: " + ex.Message);
		}
		try
		{
			ExtractLocalAssets();
		}
		catch (Exception ex2)
		{
			Log("解压资源失败: " + ex2.Message);
		}
		EnsureAssets(text3, indexUrl);
		Status("组装启动命令…", 80);
		string text4 = BuildClasspath();
		Log("classpath 条目: " + text4.Split(';').Length);
		string text5 = Path.Combine(GameDir, "natives");
		if (!Directory.Exists(text5))
		{
			Directory.CreateDirectory(text5);
		}
		string text6 = Path.Combine(GameDir, "temp");
		if (!Directory.Exists(text6))
		{
			Directory.CreateDirectory(text6);
		}
		string text7 = Path.Combine(BaseDir, "runtime", "bin", "javaw.exe");
		if (!File.Exists(text7))
		{
			text7 = Path.Combine(BaseDir, "runtime", "bin", "java.exe");
		}
		if (!File.Exists(text7))
		{
			throw new Exception("找不到 Java 运行时: " + text7);
		}
		string arguments = "-Xmx4G -Djava.library.path=\"" + text5 + "\" -Djava.io.tmpdir=\"" + text6 + "\" -Dminecraft.launcher.brand=NZClient -Dminecraft.launcher.version=1 -cp \"" + text4 + "\" " + text2 + " --username \"" + name + "\" --version 26.3 --gameDir \"" + GameDir + "\" --assetsDir \"" + AssetsDir + "\" --assetIndex " + text3 + " --uuid " + OfflineUuid(name) + " --accessToken 0 --quickPlayMultiplayer play.simpfun.cn:14039";
		Status("启动游戏…", 95);
		Log("正在启动 Minecraft…");
		Log("Java: " + text7);
		Log("classpath 长度: " + text4.Length);
		ProcessStartInfo processStartInfo = new ProcessStartInfo(text7, arguments);
		processStartInfo.WorkingDirectory = GameDir;
		processStartInfo.UseShellExecute = false;
		processStartInfo.RedirectStandardOutput = true;
		processStartInfo.RedirectStandardError = true;
		string jlog = Path.Combine(GameDir, "java-launcher.log");
		try
		{
			File.WriteAllText(jlog, "");
		}
		catch
		{
		}
		Process process = new Process();
		process.StartInfo = processStartInfo;
		process.OutputDataReceived += delegate(object s, DataReceivedEventArgs e)
		{
			if (e.Data != null)
			{
				AppendLine(jlog, e.Data);
			}
		};
		process.ErrorDataReceived += delegate(object s, DataReceivedEventArgs e)
		{
			if (e.Data != null)
			{
				AppendLine(jlog, "ERR " + e.Data);
			}
		};
		process.Start();
		process.BeginOutputReadLine();
		process.BeginErrorReadLine();
		Status("游戏已启动，进入后自动连接服务器", 100);
		Log("已启动，PID=" + process.Id);
		Log("服务器: play.simpfun.cn:14039");
		Log("Java 日志: " + jlog);
		Thread.Sleep(1500);
		BeginInvoke((MethodInvoker)delegate
		{
			Hide();
		});
	}

	private static bool IsZip(string path)
	{
		try
		{
			using (FileStream fileStream = File.OpenRead(path))
			{
				if (fileStream.Length >= 22)
				{
					byte[] array = new byte[4];
					fileStream.Read(array, 0, 4);
					if (array[0] == 80 && array[1] == 75)
					{
						fileStream.Seek(-22L, SeekOrigin.End);
						byte[] array2 = new byte[22];
						fileStream.Read(array2, 0, 22);
						for (int i = 0; i < 22; i++)
						{
							if (array2[i] == 80 && array2[i + 1] == 75 && array2[i + 2] == 5 && array2[i + 3] == 6)
							{
								return true;
							}
						}
						return false;
					}
					return false;
				}
				return false;
			}
		}
		catch
		{
			return false;
		}
	}

	private static string Match(string s, string pattern)
	{
		Match match = Regex.Match(s, pattern);
		if (!match.Success)
		{
			return null;
		}
		return match.Groups[1].Value;
	}

	private string BuildClasspath()
	{
		List<string> list = new List<string>();
		if (Directory.Exists(LibDir))
		{
			string[] files = Directory.GetFiles(LibDir, "*.jar", SearchOption.AllDirectories);
			foreach (string text in files)
			{
				string text2 = Path.GetFileName(text).ToLower();
				if (text2.IndexOf("-natives-linux") < 0 && text2.IndexOf("-natives-macos") < 0)
				{
					list.Add(text);
				}
			}
		}
		string text3 = Path.Combine(VerDir, "26.3.jar");
		if (File.Exists(text3))
		{
			list.Add(text3);
		}
		return string.Join(";", list.ToArray());
	}

	private static string Sha1Of(string path)
	{
		using (FileStream inputStream = File.OpenRead(path))
		{
			using (SHA1 sHA = SHA1.Create())
			{
				byte[] array = sHA.ComputeHash(inputStream);
				StringBuilder stringBuilder = new StringBuilder(array.Length * 2);
				byte[] array2 = array;
				for (int i = 0; i < array2.Length; i++)
				{
					byte b = array2[i];
					stringBuilder.Append(b.ToString("x2"));
				}
				return stringBuilder.ToString();
			}
		}
	}

	private static string JoinUrl(string baseUrl, string rel)
	{
		if (baseUrl.Length == 0)
		{
			return rel;
		}
		if (!baseUrl.EndsWith("/"))
		{
			baseUrl += "/";
		}
		string[] array = rel.Split('/');
		StringBuilder stringBuilder = new StringBuilder(baseUrl);
		for (int i = 0; i < array.Length; i++)
		{
			if (i > 0)
			{
				stringBuilder.Append('/');
			}
			stringBuilder.Append(Uri.EscapeDataString(array[i]));
		}
		return stringBuilder.ToString();
	}

	private void UpdateClient()
	{
		string text = LoadCfg("update");
		if (text.Length == 0)
		{
			Log("自更新: config.ini 里没配 update 地址，跳过");
		}
		else
		{
			Status("检查客户端更新…", 2);
			string input = default(string);
			try
			{
				using (TimeoutWebClient timeoutWebClient = new TimeoutWebClient())
				{
					timeoutWebClient.Headers.Add("User-Agent", "NZClient/1.0");
					timeoutWebClient.CachePolicy = new RequestCachePolicy(RequestCacheLevel.NoCacheNoStore);
					input = timeoutWebClient.DownloadString(text);
				}
			}
			catch (Exception ex)
			{
				Log("自更新: 拉取清单失败（" + ex.Message + "），跳过");
				return;
			}
			Dictionary<string, object> dictionary;
			try
			{
				JavaScriptSerializer javaScriptSerializer = new JavaScriptSerializer();
				javaScriptSerializer.MaxJsonLength = 2147483647;
				dictionary = javaScriptSerializer.Deserialize<Dictionary<string, object>>(input);
			}
			catch (Exception ex2)
			{
				Log("自更新: 清单解析失败：" + ex2.Message);
				return;
			}
			if (dictionary != null)
			{
				string text2 = dictionary.ContainsKey("version") ? Convert.ToString(dictionary["version"]) : "";
				string baseUrl = dictionary.ContainsKey("base") ? Convert.ToString(dictionary["base"]) : "";
				string path = Path.Combine(BaseDir, ".clientver");
				string text3 = File.Exists(path) ? File.ReadAllText(path).Trim() : "";
				if (text2.Length > 0 && text2 == text3)
				{
					Log("自更新: 已是最新（" + text2 + "）");
				}
				else
				{
					Log("自更新: 本地 " + ((text3.Length == 0) ? "未记录" : text3) + " → 远端 " + text2);
					IList list = dictionary.ContainsKey("files") ? (dictionary["files"] as IList) : null;
					string text4 = Path.Combine(BaseDir, ".nzupdate");
					int num = list?.Count ?? 0;
					int num2 = 0;
					int num3 = 0;
					bool flag = false;
					for (int i = 0; i < num; i++)
					{
						Dictionary<string, object> dictionary2 = list[i] as Dictionary<string, object>;
						if (dictionary2 != null && dictionary2.ContainsKey("path"))
						{
							num2++;
							string text5 = Convert.ToString(dictionary2["path"]).Replace('\\', '/');
							string text6 = Path.Combine(BaseDir, text5.Replace('/', Path.DirectorySeparatorChar));
							string text7 = dictionary2.ContainsKey("sha1") ? Convert.ToString(dictionary2["sha1"]).ToLowerInvariant() : "";
							Status("更新 " + num2 + "/" + num + "：" + Path.GetFileName(text5), 2 + 20 * num2 / Math.Max(1, num));
							string a = File.Exists(text6) ? Sha1Of(text6) : "";
							if (text7.Length <= 0 || !(a == text7))
							{
								string address = dictionary2.ContainsKey("url") ? Convert.ToString(dictionary2["url"]) : JoinUrl(baseUrl, text5);
								string text8 = Path.Combine(text4, Path.GetFileName(text5));
								try
								{
									if (Directory.Exists(text4))
									{
										Directory.Delete(text4, true);
									}
									Directory.CreateDirectory(text4);
									using (TimeoutWebClient timeoutWebClient2 = new TimeoutWebClient())
									{
										timeoutWebClient2.Headers.Add("User-Agent", "NZClient/1.0");
										timeoutWebClient2.DownloadFile(address, text8);
									}
									string text9 = Sha1Of(text8);
									if (text7.Length > 0 && text9 != text7)
									{
										Log("自更新: 校验失败 " + text5 + "（期望 " + text7.Substring(0, 7) + " 实得 " + text9.Substring(0, 7) + "）");
									}
									else
									{
										Directory.CreateDirectory(Path.GetDirectoryName(text6));
										try
										{
											if (File.Exists(text6))
											{
												File.Delete(text6);
											}
											File.Move(text8, text6);
										}
										catch
										{
											string text10 = text6 + ".old";
											if (File.Exists(text10))
											{
												File.Delete(text10);
											}
											File.Move(text6, text10);
											File.Move(text8, text6);
										}
										num3++;
										Log("自更新: 已更新 " + text5);
										if (text5.EndsWith(".exe", StringComparison.OrdinalIgnoreCase))
										{
											flag = true;
										}
									}
								}
								catch (Exception ex3)
								{
									Log("自更新: 下载失败 " + text5 + "：" + ex3.Message);
								}
							}
						}
					}
					IList list2 = dictionary.ContainsKey("remove") ? (dictionary["remove"] as IList) : null;
					if (list2 != null)
					{
						foreach (object item in list2)
						{
							try
							{
								string path2 = Path.Combine(BaseDir, Convert.ToString(item).Replace('/', Path.DirectorySeparatorChar));
								if (File.Exists(path2))
								{
									File.Delete(path2);
									num3++;
									Log("自更新: 已删除 " + item);
								}
							}
							catch
							{
							}
						}
					}
					try
					{
						if (Directory.Exists(text4))
						{
							Directory.Delete(text4, true);
						}
					}
					catch
					{
					}
					try
					{
						File.WriteAllText(path, text2, Encoding.UTF8);
					}
					catch
					{
					}
					if (num3 > 0)
					{
						Log("自更新: 完成，共处理 " + num3 + " 个文件");
					}
					if (flag)
					{
						Log("启动器已更新，正在自动重启…");
						Status("启动器已更新，正在重启", 100);
						try
						{
							Process.Start(Application.ExecutablePath);
						}
						catch
						{
						}
						Environment.Exit(0);
					}
				}
			}
		}
	}

	private void UpdateMods()
	{
		string text = LoadCfg("manifest");
		string text2 = null;
		if (text.Length == 0)
		{
			string path = Path.Combine(BaseDir, "manifest.json");
			if (File.Exists(path))
			{
				text2 = File.ReadAllText(path, Encoding.UTF8);
			}
		}
		else
		{
			using (TimeoutWebClient timeoutWebClient = new TimeoutWebClient())
			{
				timeoutWebClient.Headers.Add("User-Agent", "NZClient/1.0");
				text2 = timeoutWebClient.DownloadString(text);
			}
		}
		if (text2 == null)
		{
			Log("自动更新: 未配置清单，跳过");
		}
		else
		{
			Match match = Regex.Match(text2, "\"mods\"\\s*:\\s*\\[(.*?)\\]", RegexOptions.Singleline);
			if (!match.Success)
			{
				Log("自动更新: 清单里没有 mods 数组");
			}
			else
			{
				MatchCollection matchCollection = Regex.Matches(match.Groups[1].Value, "\"([a-z0-9][a-z0-9-]{1,64})\"");
				string text3 = Path.Combine(GameDir, "mods");
				if (!Directory.Exists(text3))
				{
					Directory.CreateDirectory(text3);
				}
				string[] files = Directory.GetFiles(text3, "*.jar");
				if (LoadCfg("modupdate") != "1" && files.Length >= matchCollection.Count)
				{
					Log("mod 已齐全（" + files.Length + " 个，清单 " + matchCollection.Count + " 个），跳过联网检查");
					Status("mod 已齐全，跳过联网检查", 45);
				}
				else
				{
					int num = 0;
					int num2 = 0;
					foreach (Match item in matchCollection)
					{
						string value = item.Groups[1].Value;
						num++;
						Status("检查 mod " + num + "/" + matchCollection.Count, 5 + num * 40 / Math.Max(1, matchCollection.Count));
						try
						{
							string address = "https://api.modrinth.com/v2/project/" + value + "/version?game_versions=%5B%2226.3%22%5D&loaders=%5B%22fabric%22%5D";
							string s = default(string);
							using (TimeoutWebClient timeoutWebClient2 = new TimeoutWebClient())
							{
								timeoutWebClient2.Headers.Add("User-Agent", "NZClient/1.0");
								s = timeoutWebClient2.DownloadString(address);
							}
							string text4 = Match(s, "\"url\"\\s*:\\s*\"(https://cdn\\.modrinth\\.com/[^\"]+)\"");
							string text5 = Match(s, "\"filename\"\\s*:\\s*\"([^\"]+)\"");
							string text6 = Match(s, "\"size\"\\s*:\\s*(\\d+)");
							long result = 0L;
							if (text6 != null)
							{
								long.TryParse(text6, out result);
							}
							if (text4 != null && text5 != null)
							{
								string text7 = Path.Combine(text3, text5);
								if (!File.Exists(text7) || (result != 0 && new FileInfo(text7).Length != result))
								{
									if (File.Exists(text7))
									{
										File.Delete(text7);
									}
									string text8 = text7 + ".part";
									try
									{
										using (TimeoutWebClient timeoutWebClient3 = new TimeoutWebClient())
										{
											timeoutWebClient3.Headers.Add("User-Agent", "NZClient/1.0");
											timeoutWebClient3.DownloadFile(text4, text8);
										}
										long length = new FileInfo(text8).Length;
										if (result > 0 && length != result)
										{
											throw new Exception("文件大小不符 " + length + "/" + result);
										}
										if (!IsZip(text8))
										{
											throw new Exception("下载内容不是有效的 jar");
										}
										if (File.Exists(text7))
										{
											File.Delete(text7);
										}
										File.Move(text8, text7);
										Log("自动安装: " + text5);
										num2++;
									}
									catch (Exception ex)
									{
										try
										{
											if (File.Exists(text8))
											{
												File.Delete(text8);
											}
										}
										catch
										{
										}
										Log("下载失败 " + value + ": " + ex.Message);
									}
								}
							}
						}
						catch (Exception ex2)
						{
							Log("跳过 " + value + ": " + ex2.Message);
						}
					}
					Log("自动更新完成，新增 " + num2 + " 个 mod（本地 " + files.Length + " 个）");
				}
			}
		}
	}

	private void ExtractLocalAssets()
	{
		string path = Path.Combine(AssetsDir, "indexes");
		if (!Directory.Exists(AssetsDir) || !Directory.Exists(path))
		{
			string[] array = new string[2]
			{
				"游戏资源-assets.zip",
				"assets.zip"
			};
			string[] array2 = array;
			int num = 0;
			string text;
			string text2;
			while (true)
			{
				if (num >= array2.Length)
				{
					return;
				}
				text = array2[num];
				text2 = Path.Combine(BaseDir, text);
				if (File.Exists(text2))
				{
					break;
				}
				num++;
			}
			Status("解压游戏资源…", 5);
			Log("发现资源包，开始解压: " + text);
			ZipFile.ExtractToDirectory(text2, BaseDir);
			Log("资源解压完成");
		}
	}

	private void EnsureAssets(string indexId, string indexUrl)
	{
		string text = Path.Combine(AssetsDir, "indexes");
		if (!Directory.Exists(text))
		{
			Directory.CreateDirectory(text);
		}
		string text2 = Path.Combine(text, indexId + ".json");
		if (!File.Exists(text2))
		{
			if (indexUrl == null)
			{
				throw new Exception("版本文件里没有资源索引地址");
			}
			Status("下载资源索引…", 8);
			Log("下载资源索引: " + indexUrl);
			using (TimeoutWebClient timeoutWebClient = new TimeoutWebClient())
			{
				timeoutWebClient.DownloadFile(indexUrl, text2);
			}
		}
		string input = File.ReadAllText(text2, Encoding.UTF8);
		MatchCollection matchCollection = Regex.Matches(input, "\"([^\"]+)\"\\s*:\\s*\\{\\s*\"hash\"\\s*:\\s*\"([0-9a-f]{40})\"\\s*,\\s*\"size\"\\s*:\\s*(\\d+)");
		int count = matchCollection.Count;
		int num = 0;
		int num2 = 0;
		Log("资源条目: " + count);
		if (count != 0)
		{
			Status("检查资源文件…", 10);
			using (TimeoutWebClient timeoutWebClient2 = new TimeoutWebClient())
			{
				timeoutWebClient2.Headers.Add("User-Agent", "NZClient/1.0");
				foreach (Match item in matchCollection)
				{
					string value = item.Groups[2].Value;
					long num3 = long.Parse(item.Groups[3].Value);
					string text3 = value.Substring(0, 2);
					string text4 = Path.Combine(AssetsDir, "objects", text3);
					string text5 = Path.Combine(text4, value);
					num++;
					if (File.Exists(text5))
					{
						try
						{
							if (new FileInfo(text5).Length == num3)
							{
								num2++;
								continue;
							}
						}
						catch
						{
						}
					}
					if (!Directory.Exists(text4))
					{
						Directory.CreateDirectory(text4);
					}
					string address = "https://resources.download.minecraft.net/" + text3 + "/" + value;
					try
					{
						timeoutWebClient2.DownloadFile(address, text5);
					}
					catch (Exception ex)
					{
						Log("资源下载失败 " + value + " : " + ex.Message);
					}
					if (num % 5 == 0 || num == count)
					{
						int pct = 10 + (int)(70.0 * (double)num / (double)count);
						Status("下载游戏资源 " + num + "/" + count, pct);
					}
				}
			}
			Log("资源检查完成：已有 " + num2 + " 个，共 " + count);
		}
	}

	private static void AppendLine(string path, string line)
	{
		lock (fileLock)
		{
			try
			{
				File.AppendAllText(path, line + "\r\n", Encoding.UTF8);
			}
			catch
			{
			}
		}
	}

	private static void LogFile(string s)
	{
		try
		{
			File.AppendAllText(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "error.log"), DateTime.Now.ToString("HH:mm:ss") + " " + s + "\r\n", Encoding.UTF8);
		}
		catch
		{
		}
	}

	[STAThread]
	public static void Main()
	{
		LogFile("=== start ===");
		try
		{
			ServicePointManager.SecurityProtocol = (SecurityProtocolType.Tls | SecurityProtocolType.Tls11 | SecurityProtocolType.Tls12);
			ServicePointManager.Expect100Continue = false;
			LogFile("tls ok");
		}
		catch (Exception ex)
		{
			LogFile("tls: " + ex.Message);
		}
		try
		{
			SetProcessDPIAware();
			LogFile("dpi ok");
		}
		catch (Exception ex2)
		{
			LogFile("dpi: " + ex2.Message);
		}
		Application.ThreadException += delegate(object s, ThreadExceptionEventArgs e)
		{
			LogFile("THREAD: " + e.Exception);
			MessageBox.Show(e.Exception.ToString(), "错误");
		};
		AppDomain.CurrentDomain.UnhandledException += delegate(object s, UnhandledExceptionEventArgs e)
		{
			LogFile("UNHANDLED: " + e.ExceptionObject);
		};
		try
		{
			Application.EnableVisualStyles();
			LogFile("styles ok, creating form");
			Launcher mainForm = new Launcher();
			LogFile("form created");
			Application.Run(mainForm);
			LogFile("exited normally");
		}
		catch (Exception ex3)
		{
			LogFile("MAIN: " + ex3);
			MessageBox.Show(ex3.ToString(), "启动失败");
		}
	}
}

public class HelpForm : Form
{
	private static readonly string Fallback =
		"凝紫服务器 二周目 · 使用说明" + Environment.NewLine +
		"====================================" + Environment.NewLine + Environment.NewLine +
		"一、怎么用" + Environment.NewLine +
		"1. 解压整个文件夹（不要只解压 exe）" + Environment.NewLine +
		"2. 双击 凝紫客户端.exe" + Environment.NewLine +
		"3. 填玩家名（3-16 位字母/数字/下划线，定了别改）" + Environment.NewLine +
		"4. 点「启动游戏」，首次会自动解压资源并直接进服" + Environment.NewLine + Environment.NewLine +
		"二、第一次进服（只需一次）" + Environment.NewLine +
		"   /register 你的密码 你的密码" + Environment.NewLine +
		"   /login 你的密码" + Environment.NewLine +
		"   /autologin set 你的密码   （以后自动登录）" + Environment.NewLine + Environment.NewLine +
		"三、进服不需要申请" + Environment.NewLine +
		"本服没有白名单，填好玩家名、注册登录就能玩。" + Environment.NewLine + Environment.NewLine +
		"四、皮肤" + Environment.NewLine +
		"littleskin.cn 注册 → 角色名 = 游戏名 → 上传 64x64 PNG → 回游戏重进。" + Environment.NewLine + Environment.NewLine +
		"五、怎么更新" + Environment.NewLine +
		"群里发新包后：退出游戏 → 把新包解压覆盖到客户端目录（选「全部替换」）。" + Environment.NewLine +
		"存档、地图缓存、皮肤配置都在 game 目录里，不会被覆盖。" + Environment.NewLine + Environment.NewLine +
		"六、进不去游戏？" + Environment.NewLine +
		"  - 一直提示要先登录 → 聊天栏 /login 你的密码" + Environment.NewLine +
		"  - 提示版本不符 → 别自己加模组，用群里最新的完整包" + Environment.NewLine +
		"  - 启动器报错 → 把客户端目录里的 launcher.log 发给管理员";

	private RichTextBox box;
	private string docPath;

	public HelpForm(string baseDir)
	{
		Text = "使用说明 · 凝紫服务器 二周目";
		base.ClientSize = new Size(760, 560);
		base.StartPosition = FormStartPosition.CenterParent;
		base.FormBorderStyle = FormBorderStyle.FixedSingle;
		base.MaximizeBox = false;
		base.MinimizeBox = false;
		BackColor = Color.FromArgb(26, 16, 48);
		ForeColor = Color.White;
		Font = new Font("微软雅黑", 9f);
		docPath = Path.Combine(baseDir, "使用说明.txt");
		string text = Fallback;
		try
		{
			if (File.Exists(docPath))
			{
				string text2 = File.ReadAllText(docPath, Encoding.UTF8);
				if (text2 != null && text2.Trim().Length > 20)
				{
					text = text2;
				}
			}
		}
		catch
		{
		}
		box = new RichTextBox();
		box.ReadOnly = true;
		box.BorderStyle = BorderStyle.None;
		box.BackColor = Color.FromArgb(18, 10, 34);
		box.ForeColor = Color.FromArgb(228, 228, 242);
		box.Font = new Font("微软雅黑", 10f);
		box.SetBounds(20, 20, 720, 468);
		box.Text = text;
		base.Controls.Add(box);
		Button button = new Button();
		button.Text = "打开说明文件";
		button.SetBounds(20, 504, 160, 36);
		button.FlatStyle = FlatStyle.Flat;
		button.BackColor = Color.FromArgb(46, 32, 78);
		button.ForeColor = Color.White;
		button.FlatAppearance.BorderColor = Color.FromArgb(124, 77, 255);
		button.Click += delegate
		{
			try
			{
				if (File.Exists(docPath))
				{
					Process.Start(new ProcessStartInfo(docPath)
					{
						UseShellExecute = true
					});
				}
				else
				{
					MessageBox.Show("找不到 使用说明.txt，请重新解压完整客户端。", "使用说明");
				}
			}
			catch (Exception ex)
			{
				MessageBox.Show("打不开：" + ex.Message, "使用说明");
			}
		};
		base.Controls.Add(button);
		Button button2 = new Button();
		button2.Text = "关闭";
		button2.SetBounds(580, 504, 160, 36);
		button2.FlatStyle = FlatStyle.Flat;
		button2.BackColor = Color.FromArgb(124, 77, 255);
		button2.ForeColor = Color.White;
		button2.FlatAppearance.BorderSize = 0;
		button2.Click += delegate
		{
			Close();
		};
		base.Controls.Add(button2);
		base.AcceptButton = button2;
		base.CancelButton = button2;
	}
}
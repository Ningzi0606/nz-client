using System;
using System.IO;

public static class DummyCore
{
    public static void Main()
    {
        File.AppendAllText(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "core_launched.txt"),
            DateTime.Now.ToString("HH:mm:ss") + " core started" + Environment.NewLine);
    }
}

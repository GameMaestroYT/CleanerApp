import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import time

# === SPLASH / AUTHORSHIP ===
splash = tk.Tk()
splash.overrideredirect(True)
splash.geometry("400x100+500+300")
splash_label = tk.Label(
    splash, 
    text="CleanApp V1\nOfficially by GameMaestroYT & ChatGPT",
    font=("Segoe UI", 14, "bold"), 
    fg="white", 
    bg="black"
)
splash_label.pack(expand=True, fill='both')
splash.update()
time.sleep(3)
splash.destroy()

# === CONFIG ===
DRIVE = "C:"
LOW_SPACE_GB = 5

def bytes_to_gb(bytes_val):
    return round(bytes_val / (1024 ** 3), 2)

def get_drive_stats():
    usage = shutil.disk_usage(DRIVE)
    total = bytes_to_gb(usage.total)
    used = bytes_to_gb(usage.used)
    free = bytes_to_gb(usage.free)
    return total, used, free

def get_suggestions(free_gb):
    if free_gb > LOW_SPACE_GB:
        return ["✅ Space is OK. No cleanup needed."]
    return [
        "⚠️ Low disk space detected. Suggestions:",
        "• Clear Windows Temp files",
        "• Clean Windows Update Cache",
        "• Disable Hibernation",
        "• Run Disk Cleanup (cleanmgr)",
        "• Shrink or disable pagefile",
        "• Enable CompactOS",
        "• Run DISM cleanup",
        "• Disable Reserved Storage",
    ]

def run_cleanup():
    try:
        # Run tasks if checked
        for name, var in cleanup_options.items():
            if var.get():
                progress_label.config(text=f"Running: {name}...")
                root.update()
                # Map the task commands here
                if name == "Disk Cleanup (silent)":
                    subprocess.run("cleanmgr /sagerun:1", shell=True)
                elif name == "Disable Hibernation":
                    subprocess.run("powercfg -h off", shell=True)
                elif name == "Clear Windows Update Cache":
                    cmds = [
                        "net stop wuauserv",
                        "net stop bits",
                        f'del /f /s /q "{os.path.join(os.environ["WINDIR"], "SoftwareDistribution", "Download")}\\*.*"',
                        "net start wuauserv",
                        "net start bits"
                    ]
                    for c in cmds:
                        subprocess.run(c, shell=True)
                elif name == "Disable Reserved Storage":
                    cmds = [
                        r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\ReserveManager" /v ShippedWithReserves /t REG_DWORD /d 0 /f',
                        "dism /Online /Set-ReservedStorageState /State:Disabled"
                    ]
                    for c in cmds:
                        subprocess.run(c, shell=True)
                elif name == "Shrink Pagefile":
                    cmds = [
                        'wmic computersystem where name="%computername%" set AutomaticManagedPagefile=False',
                        r'wmic pagefileset where name="C:\\pagefile.sys" set InitialSize=1024,MaximumSize=1950'
                    ]
                    for c in cmds:
                        subprocess.run(c, shell=True)
                elif name == "WinSxS Component Cleanup":
                    subprocess.run("Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase", shell=True)
                elif name == "Enable Compact OS":
                    subprocess.run("compact.exe /CompactOS:always", shell=True)
                elif name == "Delete TEMP files":
                    cmds = [
                        f'del /s /f /q "{os.environ["TEMP"]}\\*.*"',
                        r'del /s /f /q "C:\Windows\Temp\*.*"',
                        f'del /s /f /q "{os.path.join(os.environ["USERPROFILE"], "AppData\\Local\\Temp")}\\*.*"'
                    ]
                    for c in cmds:
                        subprocess.run(c, shell=True)

        messagebox.showinfo("Cleanup Finished", "✅ All selected cleanup tasks completed! Please reboot your PC.")
        refresh_data()

    except Exception as e:
        messagebox.showerror("Error", f"Cleanup failed:\n{e}")

def refresh_data():
    total, used, free = get_drive_stats()
    percent_used = round((used / total) * 100, 1)
    progress_bar['value'] = percent_used
    space_label.config(text=f"Used: {used} GB | Free: {free} GB of {total} GB")

    suggestions = get_suggestions(free)
    suggestions_text.config(state='normal')
    suggestions_text.delete(1.0, tk.END)
    for line in suggestions:
        suggestions_text.insert(tk.END, line + "\n")
    suggestions_text.config(state='disabled')

# === GUI SETUP (DARK MODE) ===
root = tk.Tk()
root.title("💾 CleanApp V1")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#2e2e2e")

title_label = tk.Label(
    root, text="💾 CleanApp V1", 
    font=("Segoe UI", 14, "bold"),
    fg="white", bg="#2e2e2e"
)
title_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=450, mode='determinate')
progress_bar.pack(pady=5)

progress_label = tk.Label(root, text="", font=("Segoe UI", 10), fg="white", bg="#2e2e2e")
progress_label.pack()

space_label = tk.Label(root, text="", font=("Segoe UI", 10), fg="white", bg="#2e2e2e")
space_label.pack()

suggestions_label = tk.Label(
    root, text="🧠 Suggestions:", font=("Segoe UI", 11, "bold"), fg="white", bg="#2e2e2e"
)
suggestions_label.pack(pady=(15,2))

suggestions_text = tk.Text(
    root, width=60, height=6, wrap='word', state='disabled', 
    font=("Segoe UI", 9), bg="#3e3e3e", fg="white", insertbackground="white"
)
suggestions_text.pack()

# --- Cleanup checkboxes in two columns ---
actions_frame = tk.Frame(root, bg="#2e2e2e")
actions_frame.pack(pady=5)

cleanup_options = {
    "Disk Cleanup (silent)": tk.BooleanVar(value=True),
    "Disable Hibernation": tk.BooleanVar(value=True),
    "Clear Windows Update Cache": tk.BooleanVar(value=True),
    "Disable Reserved Storage": tk.BooleanVar(value=True),
    "Shrink Pagefile": tk.BooleanVar(value=True),
    "WinSxS Component Cleanup": tk.BooleanVar(value=True),
    "Enable Compact OS": tk.BooleanVar(value=True),
    "Delete TEMP files": tk.BooleanVar(value=True)
}

for i, (name, var) in enumerate(cleanup_options.items()):
    row = i % 4
    col = i // 4
    cb = tk.Checkbutton(actions_frame, text=name, variable=var, bg="#2e2e2e", fg="white", selectcolor="#555555")
    cb.grid(row=row, column=col, sticky="w", padx=10, pady=2)

# --- Buttons ---
button_frame = tk.Frame(root, bg="#2e2e2e")
button_frame.pack(pady=10)

refresh_btn = tk.Button(button_frame, text="🔄 Refresh", width=15, command=refresh_data,
    bg="#555555", fg="white", activebackground="#777777")
refresh_btn.grid(row=0, column=0, padx=5)

cleanup_btn = tk.Button(button_frame, text="🧹 Run Deep Cleanup", width=20, command=run_cleanup,
    bg="#555555", fg="white", activebackground="#777777")
cleanup_btn.grid(row=0, column=1, padx=5)

# === AUTHORSHIP WATERMARK ===
watermark = tk.Label(root, text="© GameMaestroYT & ChatGPT", font=("Segoe UI", 8), fg="white", bg="#2e2e2e")
watermark.pack(side='bottom', pady=2)

refresh_data()
root.mainloop()

import os
import shutil
import psutil
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

# === SPLASH / AUTHORSHIP ===
import time
splash = tk.Tk()
splash.overrideredirect(True)
splash.geometry("400x100+500+300")  # adjust size/position if needed
splash_label = tk.Label(splash, text="CleanupApp\nOfficially by GameMaestroYT & ChatGPT",
                        font=("Segoe UI", 14, "bold"), fg="white", bg="black")
splash_label.pack(expand=True, fill='both')
splash.update()
time.sleep(3)  # shows 3 seconds
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
        # 1. Disk Cleanup (silent)
        subprocess.run("cleanmgr /sagerun:1", shell=True)

        # 2. Disable Hibernation
        subprocess.run("powercfg -h off", shell=True)

        # 3. Clear Windows Update Cache
        subprocess.run("net stop wuauserv", shell=True)
        subprocess.run("net stop bits", shell=True)
        update_cache = os.path.join(os.environ['WINDIR'], "SoftwareDistribution", "Download")
        subprocess.run(f'del /f /s /q "{update_cache}\\*.*"', shell=True)
        subprocess.run("net start wuauserv", shell=True)
        subprocess.run("net start bits", shell=True)

        # 4. Disable Reserved Storage
        subprocess.run(r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\ReserveManager" /v ShippedWithReserves /t REG_DWORD /d 0 /f', shell=True)
        subprocess.run("dism /Online /Set-ReservedStorageState /State:Disabled", shell=True)

        # 5. Shrink Pagefile
        subprocess.run(f'wmic computersystem where name="%computername%" set AutomaticManagedPagefile=False', shell=True)
        subprocess.run(r'wmic pagefileset where name="C:\\pagefile.sys" set InitialSize=1024,MaximumSize=1950', shell=True)

        # 6. WinSxS Component Cleanup
        subprocess.run("Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase", shell=True)

        # 7. Enable Compact OS
        subprocess.run("compact.exe /CompactOS:always", shell=True)

        # 8. Delete TEMP files
        temp_paths = [os.environ['TEMP'], r"C:\Windows\Temp", os.path.join(os.environ['USERPROFILE'], "AppData\\Local\\Temp")]
        for path in temp_paths:
            subprocess.run(f'del /s /f /q "{path}\\*.*"', shell=True)

        messagebox.showinfo("Cleanup Finished", "✅ All cleanup tasks completed! Please reboot your PC.")
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
root.title("💾 SpaceSaver - Deep Cleanup")
root.geometry("450x360")
root.resizable(False, False)
root.configure(bg="#2e2e2e")  # dark gray background

title_label = tk.Label(root, text="💾 SpaceSaver - Deep Windows Cleanup", font=("Segoe UI", 14, "bold"),
                       fg="white", bg="#2e2e2e")
title_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=380, mode='determinate')
progress_bar.pack(pady=5)

space_label = tk.Label(root, text="", font=("Segoe UI", 10), fg="white", bg="#2e2e2e")
space_label.pack()

suggestions_label = tk.Label(root, text="🧠 Suggestions:", font=("Segoe UI", 11, "bold"), fg="white", bg="#2e2e2e")
suggestions_label.pack(pady=(15,2))

suggestions_text = tk.Text(root, width=55, height=8, wrap='word', state='disabled', font=("Segoe UI", 9),
                           bg="#3e3e3e", fg="white", insertbackground="white")
suggestions_text.pack()

button_frame = tk.Frame(root, bg="#2e2e2e")
button_frame.pack(pady=10)

refresh_btn = tk.Button(button_frame, text="🔄 Refresh", width=15, command=refresh_data,
                        bg="#555555", fg="white", activebackground="#777777")
refresh_btn.grid(row=0, column=0, padx=5)

cleanup_btn = tk.Button(button_frame, text="🧹 Run Deep Cleanup", width=20, command=run_cleanup,
                        bg="#555555", fg="white", activebackground="#777777")
cleanup_btn.grid(row=0, column=1, padx=5)

refresh_data()
root.mainloop()

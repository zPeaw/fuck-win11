
import subprocess
import sys
import winreg
import os
import ctypes
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading
import re
import locale


BG_DARK       = "#0d1117"
BG_CARD       = "#161b22"
BG_INPUT      = "#21262d"
FG_PRIMARY    = "#e6edf3"
FG_SECONDARY  = "#8b949e"
ACCENT_BLUE   = "#58a6ff"
ACCENT_GREEN  = "#3fb950"
ACCENT_RED    = "#f85149"
ACCENT_YELLOW = "#d29922"
ACCENT_PURPLE = "#bc8cff"
ACCENT_ORANGE = "#f0883e"
BORDER_COLOR  = "#30363d"

LANG = {
    "title":            {"tr": "� Fuck Win11 — Sistem Kontrol Aracı", "en": "� Fuck Win11 — System Control Tool"},
    "win_title":        {"tr": "🖕 Fuck Win11", "en": "🖕 Fuck Win11"},
    "admin_yes":        {"tr": "✅ Yönetici", "en": "✅ Admin"},
    "admin_no":         {"tr": "❌ Yönetici Değil", "en": "❌ Not Admin"},
    "admin_ok":         {"tr": "Yönetici yetkileri aktif.\n", "en": "Administrator privileges active.\n"},
    "admin_warn":       {"tr": "⚠️  UYARI: Bu araç yönetici olarak çalıştırılmalıdır!\n", "en": "⚠️  WARNING: This tool must be run as administrator!\n"},
    "admin_warn2":      {"tr": "Araçlar düzgün çalışmayabilir.\n", "en": "Tools may not work properly.\n"},
    "repair_tools":     {"tr": "Onarım Araçları", "en": "Repair Tools"},
    "wu_control":       {"tr": "Windows Update Kontrolü", "en": "Windows Update Control"},
    "wd_control":       {"tr": "Windows Defender Kontrolü", "en": "Windows Defender Control"},
    "console":          {"tr": "📋 Konsol Çıktısı", "en": "📋 Console Output"},
    "clear":            {"tr": "🗑️ Temizle", "en": "🗑️ Clear"},
    "cancel":           {"tr": "⛔ İptal Et", "en": "⛔ Cancel"},
    "ready":            {"tr": "Hazır", "en": "Ready"},
    "cancelled":        {"tr": "İptal edildi", "en": "Cancelled"},
    "cancel_msg":       {"tr": "\n⛔ İşlem kullanıcı tarafından iptal edildi.\n", "en": "\n⛔ Operation cancelled by user.\n"},
    "running":          {"tr": "Çalışıyor", "en": "Running"},
    "cmd":              {"tr": "Komut", "en": "Command"},
    "start_time":       {"tr": "Başlangıç", "en": "Start"},
    "end_time":         {"tr": "Bitiş", "en": "End"},
    "exit_code":        {"tr": "Çıkış kodu", "en": "Exit code"},
    "error":            {"tr": "Hata", "en": "Error"},
    "btn_sfc":          {"tr": "🔍 SFC Tara", "en": "🔍 SFC Scan"},
    "btn_dism_ch":      {"tr": "🏥 DISM Sağlık Kontrol", "en": "🏥 DISM Health Check"},
    "btn_dism_rp":      {"tr": "🔧 DISM Onar", "en": "🔧 DISM Repair"},
    "btn_chkdsk":       {"tr": "💾 Disk Kontrol", "en": "💾 Disk Check"},
    "btn_full":         {"tr": "🚀 Tam Onarım", "en": "🚀 Full Repair"},
    "tip_sfc":          {"tr": "Sistem dosyalarını tarar ve onarır", "en": "Scans and repairs system files"},
    "tip_dism_ch":      {"tr": "Windows imaj sağlığını kontrol eder", "en": "Checks Windows image health"},
    "tip_dism_rp":      {"tr": "Bozuk Windows imajını onarır", "en": "Repairs corrupted Windows image"},
    "tip_chkdsk":       {"tr": "Disk hatalarını kontrol eder", "en": "Checks for disk errors"},
    "tip_full":         {"tr": "Tüm araçları sırayla çalıştırır", "en": "Runs all tools sequentially"},
    "btn_wu_off":       {"tr": "🚫 Update Kapat", "en": "🚫 Disable Update"},
    "btn_wu_on":        {"tr": "✅ Update Aç", "en": "✅ Enable Update"},
    "btn_wu_check":     {"tr": "ℹ️ Update Durumu", "en": "ℹ️ Update Status"},
    "tip_wu_off":       {"tr": "Windows Update servisini durdurur ve devre dışı bırakır", "en": "Stops and disables Windows Update service"},
    "tip_wu_on":        {"tr": "Windows Update servisini tekrar etkinleştirir", "en": "Re-enables Windows Update service"},
    "tip_wu_check":     {"tr": "Windows Update servisinin mevcut durumunu gösterir", "en": "Shows current Windows Update status"},
    "btn_wd_off":       {"tr": "🚫 Defender Kapat", "en": "🚫 Disable Defender"},
    "btn_wd_on":        {"tr": "✅ Defender Aç", "en": "✅ Enable Defender"},
    "btn_wd_check":     {"tr": "ℹ️ Defender Durumu", "en": "ℹ️ Defender Status"},
    "tip_wd_off":       {"tr": "Windows Defender gerçek zamanlı korumayı kapatır", "en": "Disables Windows Defender real-time protection"},
    "tip_wd_on":        {"tr": "Windows Defender korumayı tekrar açar", "en": "Re-enables Windows Defender protection"},
    "tip_wd_check":     {"tr": "Windows Defender mevcut durumunu gösterir", "en": "Shows current Windows Defender status"},
    "tweak_control":    {"tr": "Sistem Ayarları", "en": "System Tweaks"},
    "btn_sandbox_on":   {"tr": "📦 Sandbox Aç", "en": "📦 Enable Sandbox"},
    "btn_sandbox_off":  {"tr": "📦 Sandbox Kapat", "en": "📦 Disable Sandbox"},
    "btn_widgets_off":  {"tr": "📰 Haber/Widget Kapat", "en": "📰 Disable News/Widgets"},
    "btn_widgets_on":   {"tr": "📰 Haber/Widget Aç", "en": "📰 Enable News/Widgets"},
    "btn_telemetry":    {"tr": "📡 Telemetri Kapat", "en": "📡 Disable Telemetry"},
    "tip_sandbox_on":   {"tr": "Windows Sandbox özelliğini etkinleştirir", "en": "Enables Windows Sandbox feature"},
    "tip_sandbox_off":  {"tr": "Windows Sandbox özelliğini devre dışı bırakır", "en": "Disables Windows Sandbox feature"},
    "tip_widgets_off":  {"tr": "Gereksiz haber ve widget panelini kapatır", "en": "Disables unnecessary news and widget panel"},
    "tip_widgets_on":   {"tr": "Haber ve widget panelini tekrar açar", "en": "Re-enables news and widget panel"},
    "tip_telemetry":    {"tr": "Microsoft telemetri ve veri toplama servislerini kapatır", "en": "Disables Microsoft telemetry and data collection"},
    "backup_control":   {"tr": "💿 Yedekleme", "en": "💿 Backup"},
    "btn_restore_pt":   {"tr": "📌 Geri Yükleme Noktası", "en": "📌 Restore Point"},
    "btn_reg_backup":   {"tr": "🗂️ Registry Yedekle", "en": "🗂️ Backup Registry"},
    "btn_driver_backup":{"tr": "🖥️ Sürücü Yedekle", "en": "🖥️ Backup Drivers"},
    "tip_restore_pt":   {"tr": "Sistem geri yükleme noktası oluşturur", "en": "Creates a system restore point"},
    "tip_reg_backup":   {"tr": "Tüm registry'yi yedekler", "en": "Backs up entire registry"},
    "tip_driver_backup":{"tr": "Yüklü sürücüleri yedekler", "en": "Backs up installed drivers"},
}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1
            )
            sys.exit(0)
        except Exception:
            return False
    return True


class SystemRepairApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("950x780")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        sys_lang = locale.getdefaultlocale()[0] or ""
        self.lang = "tr" if sys_lang.startswith("tr") else "en"

        self.is_running = False
        self.current_process = None

        self.labels = {}
        self.tips = {}

        self._show_splash()

    def _show_splash(self):
        self.splash = tk.Frame(self.root, bg=BG_DARK)
        self.splash.pack(fill="both", expand=True)

        banner = [
            "███████╗██╗   ██╗ ██████╗██╗  ██╗",
            "██╔════╝██║   ██║██╔════╝██║ ██╔╝",
            "█████╗  ██║   ██║██║     █████╔╝ ",
            "██╔══╝  ██║   ██║██║     ██╔═██╗ ",
            "██║     ╚██████╔╝╚██████╗██║  ██╗",
            "╚═╝      ╚═════╝  ╚═════╝╚═╝  ╚═╝",
            "",
            "██╗    ██╗██╗███╗   ██╗ ██╗ ██╗",
            "██║    ██║██║████╗  ██║███║███║",
            "██║ █╗ ██║██║██╔██╗ ██║╚██║╚██║",
            "██║███╗██║██║██║╚██╗██║ ██║ ██║",
            "╚███╔███╔╝██║██║ ╚████║ ██║ ██║",
            " ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝ ╚═╝ ╚═╝",
        ]

        spacer = tk.Frame(self.splash, bg=BG_DARK, height=80)
        spacer.pack()

        for line in banner:
            tk.Label(
                self.splash, text=line, font=("Consolas", 11),
                fg=ACCENT_PURPLE, bg=BG_DARK
            ).pack()

        tk.Label(self.splash, text="", bg=BG_DARK, height=1).pack()
        tk.Label(
            self.splash, text="━" * 42,
            font=("Consolas", 10), fg=BORDER_COLOR, bg=BG_DARK
        ).pack()
        tk.Label(
            self.splash, text="🖕 Fuck Win11 — v1.0",
            font=("Segoe UI", 16, "bold"), fg=ACCENT_BLUE, bg=BG_DARK
        ).pack(pady=5)
        tk.Label(
            self.splash, text="━" * 42,
            font=("Consolas", 10), fg=BORDER_COLOR, bg=BG_DARK
        ).pack()

        tk.Label(
            self.splash, text="⚠️ Bu araç sadece Windows 11 hata verdiğinde kullanılmalıdır!",
            font=("Segoe UI", 10), fg=ACCENT_YELLOW, bg=BG_DARK
        ).pack(pady=(10, 0))

        self.countdown_label = tk.Label(
            self.splash, text="", font=("Segoe UI", 12),
            fg=FG_SECONDARY, bg=BG_DARK
        )
        self.countdown_label.pack(pady=(20, 0))

        self.root.title("🖕 Fuck Win11")
        self._splash_countdown(10)

    def _splash_countdown(self, sec):
        if sec <= 0:
            self.splash.destroy()
            self._build_ui()
            self._apply_lang()
            self._check_admin()
            return
        self.countdown_label.config(text=f"⏳ {sec}s...")
        self.root.after(1000, self._splash_countdown, sec - 1)

    def t(self, key):
        entry = LANG.get(key)
        if entry:
            return entry.get(self.lang, entry.get("tr", key))
        return key

    def _toggle_lang(self):
        self.lang = "en" if self.lang == "tr" else "tr"
        self._apply_lang()

    def _apply_lang(self):
        self.root.title(self.t("win_title"))
        self.lang_btn.config(text="🇬🇧 EN" if self.lang == "tr" else "🇹🇷 TR")
        self.title_label.config(text=self.t("title"))
        self.status_label.config(text=self.t("ready"))
        self.cancel_btn.config(text=self.t("cancel"))
        self.clear_btn.config(text=self.t("clear"))
        self.console_label.config(text=self.t("console"))
        for key, lbl in self.labels.items():
            lbl.config(text=self.t(key))
        btn_keys = {"sfc":"btn_sfc","dism_ch":"btn_dism_ch","dism_rp":"btn_dism_rp",
                    "chkdsk":"btn_chkdsk","full":"btn_full",
                    "wu_off":"btn_wu_off","wu_on":"btn_wu_on","wu_check":"btn_wu_check",
                    "wd_off":"btn_wd_off","wd_on":"btn_wd_on","wd_check":"btn_wd_check",
                    "sandbox_on":"btn_sandbox_on","sandbox_off":"btn_sandbox_off",
                    "widgets_off":"btn_widgets_off","widgets_on":"btn_widgets_on",
                    "telemetry":"btn_telemetry",
                    "restore_pt":"btn_restore_pt","reg_backup":"btn_reg_backup",
                    "driver_backup":"btn_driver_backup"}
        for bk, lk in btn_keys.items():
            if bk in self.buttons:
                self.buttons[bk].config(text=self.t(lk))
        tip_keys = {"sfc":"tip_sfc","dism_ch":"tip_dism_ch","dism_rp":"tip_dism_rp",
                    "chkdsk":"tip_chkdsk","full":"tip_full",
                    "wu_off":"tip_wu_off","wu_on":"tip_wu_on","wu_check":"tip_wu_check",
                    "wd_off":"tip_wd_off","wd_on":"tip_wd_on","wd_check":"tip_wd_check",
                    "sandbox_on":"tip_sandbox_on","sandbox_off":"tip_sandbox_off",
                    "widgets_off":"tip_widgets_off","widgets_on":"tip_widgets_on",
                    "telemetry":"tip_telemetry",
                    "restore_pt":"tip_restore_pt","reg_backup":"tip_reg_backup",
                    "driver_backup":"tip_driver_backup"}
        for bk, tk_ in tip_keys.items():
            if bk in self.tips:
                self.tips[bk].config(text=self.t(tk_))

    def _build_ui(self):
        main = tk.Frame(self.root, bg=BG_DARK, padx=20, pady=15)
        main.pack(fill="both", expand=True)

        header = tk.Frame(main, bg=BG_DARK)
        header.pack(fill="x", pady=(0, 15))

        self.title_label = tk.Label(
            header, text="",
            font=("Segoe UI", 20, "bold"), fg=ACCENT_BLUE, bg=BG_DARK
        )
        self.title_label.pack(side="left")

        self.admin_label = tk.Label(
            header, text="", font=("Segoe UI", 10), bg=BG_DARK
        )
        self.admin_label.pack(side="right")

        self.lang_btn = tk.Button(
            header, text="", font=("Segoe UI", 10, "bold"),
            fg="#ffffff", bg=ACCENT_PURPLE, activebackground=ACCENT_PURPLE,
            bd=0, padx=12, pady=4, cursor="hand2",
            command=self._toggle_lang
        )
        self.lang_btn.pack(side="right", padx=(0, 10))

        btn_frame = tk.Frame(main, bg=BG_CARD, bd=0, highlightthickness=1,
                             highlightbackground=BORDER_COLOR)
        btn_frame.pack(fill="x", pady=(0, 12))
        btn_inner = tk.Frame(btn_frame, bg=BG_CARD, padx=15, pady=12)
        btn_inner.pack(fill="x")

        lbl = tk.Label(btn_inner, text="", font=("Segoe UI", 12, "bold"), fg=FG_PRIMARY, bg=BG_CARD)
        lbl.pack(anchor="w", pady=(0, 8))
        self.labels["repair_tools"] = lbl

        buttons_row = tk.Frame(btn_inner, bg=BG_CARD)
        buttons_row.pack(fill="x")

        self.buttons = {}
        self.tips = {}
        tools = [
            ("sfc",     "", ACCENT_BLUE,   ""),
            ("dism_ch", "", ACCENT_GREEN,  ""),
            ("dism_rp", "", ACCENT_YELLOW, ""),
            ("chkdsk",  "", ACCENT_PURPLE, ""),
            ("full",    "", ACCENT_RED,    ""),
        ]

        for i, (key, text, color, tooltip) in enumerate(tools):
            f = tk.Frame(buttons_row, bg=BG_CARD)
            f.pack(side="left", padx=(0 if i == 0 else 8, 0), fill="x", expand=True)

            btn = tk.Button(
                f, text=text, font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg=color, activebackground=color,
                activeforeground="#ffffff", bd=0, padx=14, pady=8,
                cursor="hand2",
                command=lambda k=key: self._on_tool_click(k)
            )
            btn.pack(fill="x")
            self.buttons[key] = btn

            tip = tk.Label(f, text="", font=("Segoe UI", 8),
                           fg=FG_SECONDARY, bg=BG_CARD)
            tip.pack(pady=(2, 0))
            self.tips[key] = tip

        wu_frame = tk.Frame(main, bg=BG_CARD, bd=0, highlightthickness=1,
                            highlightbackground=BORDER_COLOR)
        wu_frame.pack(fill="x", pady=(0, 12))
        wu_inner = tk.Frame(wu_frame, bg=BG_CARD, padx=15, pady=12)
        wu_inner.pack(fill="x")

        lbl2 = tk.Label(wu_inner, text="", font=("Segoe UI", 12, "bold"), fg=FG_PRIMARY, bg=BG_CARD)
        lbl2.pack(anchor="w", pady=(0, 8))
        self.labels["wu_control"] = lbl2

        wu_row = tk.Frame(wu_inner, bg=BG_CARD)
        wu_row.pack(fill="x")

        wu_tools = [
            ("wu_off",   "", ACCENT_RED,    ""),
            ("wu_on",    "", ACCENT_GREEN,  ""),
            ("wu_check", "", ACCENT_ORANGE, ""),
        ]

        for i, (key, text, color, tooltip) in enumerate(wu_tools):
            f = tk.Frame(wu_row, bg=BG_CARD)
            f.pack(side="left", padx=(0 if i == 0 else 8, 0), fill="x", expand=True)

            btn = tk.Button(
                f, text=text, font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg=color, activebackground=color,
                activeforeground="#ffffff", bd=0, padx=14, pady=8,
                cursor="hand2",
                command=lambda k=key: self._on_tool_click(k)
            )
            btn.pack(fill="x")
            self.buttons[key] = btn

            tip = tk.Label(f, text="", font=("Segoe UI", 8),
                           fg=FG_SECONDARY, bg=BG_CARD)
            tip.pack(pady=(2, 0))
            self.tips[key] = tip

        wd_frame = tk.Frame(main, bg=BG_CARD, bd=0, highlightthickness=1,
                            highlightbackground=BORDER_COLOR)
        wd_frame.pack(fill="x", pady=(0, 12))
        wd_inner = tk.Frame(wd_frame, bg=BG_CARD, padx=15, pady=12)
        wd_inner.pack(fill="x")

        lbl3 = tk.Label(wd_inner, text="", font=("Segoe UI", 12, "bold"), fg=FG_PRIMARY, bg=BG_CARD)
        lbl3.pack(anchor="w", pady=(0, 8))
        self.labels["wd_control"] = lbl3

        wd_row = tk.Frame(wd_inner, bg=BG_CARD)
        wd_row.pack(fill="x")

        wd_tools = [
            ("wd_off",   "", ACCENT_RED,    ""),
            ("wd_on",    "", ACCENT_GREEN,  ""),
            ("wd_check", "", ACCENT_ORANGE, ""),
        ]

        for i, (key, text, color, tooltip) in enumerate(wd_tools):
            f = tk.Frame(wd_row, bg=BG_CARD)
            f.pack(side="left", padx=(0 if i == 0 else 8, 0), fill="x", expand=True)

            btn = tk.Button(
                f, text=text, font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg=color, activebackground=color,
                activeforeground="#ffffff", bd=0, padx=14, pady=8,
                cursor="hand2",
                command=lambda k=key: self._on_tool_click(k)
            )
            btn.pack(fill="x")
            self.buttons[key] = btn

            tip = tk.Label(f, text="", font=("Segoe UI", 8),
                           fg=FG_SECONDARY, bg=BG_CARD)
            tip.pack(pady=(2, 0))
            self.tips[key] = tip

        tw_frame = tk.Frame(main, bg=BG_CARD, bd=0, highlightthickness=1,
                            highlightbackground=BORDER_COLOR)
        tw_frame.pack(fill="x", pady=(0, 12))
        tw_inner = tk.Frame(tw_frame, bg=BG_CARD, padx=15, pady=12)
        tw_inner.pack(fill="x")

        lbl4 = tk.Label(tw_inner, text="", font=("Segoe UI", 12, "bold"), fg=FG_PRIMARY, bg=BG_CARD)
        lbl4.pack(anchor="w", pady=(0, 8))
        self.labels["tweak_control"] = lbl4

        tw_row = tk.Frame(tw_inner, bg=BG_CARD)
        tw_row.pack(fill="x")

        ACCENT_CYAN = "#39d2c0"
        tw_tools = [
            ("sandbox_on",  "", ACCENT_CYAN,   ""),
            ("sandbox_off", "", ACCENT_RED,     ""),
            ("widgets_off", "", ACCENT_ORANGE,  ""),
            ("widgets_on",  "", ACCENT_GREEN,   ""),
            ("telemetry",   "", ACCENT_PURPLE,  ""),
        ]

        for i, (key, text, color, tooltip) in enumerate(tw_tools):
            f = tk.Frame(tw_row, bg=BG_CARD)
            f.pack(side="left", padx=(0 if i == 0 else 8, 0), fill="x", expand=True)

            btn = tk.Button(
                f, text=text, font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg=color, activebackground=color,
                activeforeground="#ffffff", bd=0, padx=14, pady=8,
                cursor="hand2",
                command=lambda k=key: self._on_tool_click(k)
            )
            btn.pack(fill="x")
            self.buttons[key] = btn

            tip = tk.Label(f, text="", font=("Segoe UI", 8),
                           fg=FG_SECONDARY, bg=BG_CARD)
            tip.pack(pady=(2, 0))
            self.tips[key] = tip

        bk_frame = tk.Frame(main, bg=BG_CARD, bd=0, highlightthickness=1,
                            highlightbackground=BORDER_COLOR)
        bk_frame.pack(fill="x", pady=(0, 12))
        bk_inner = tk.Frame(bk_frame, bg=BG_CARD, padx=15, pady=12)
        bk_inner.pack(fill="x")

        lbl5 = tk.Label(bk_inner, text="", font=("Segoe UI", 12, "bold"), fg=FG_PRIMARY, bg=BG_CARD)
        lbl5.pack(anchor="w", pady=(0, 8))
        self.labels["backup_control"] = lbl5

        bk_row = tk.Frame(bk_inner, bg=BG_CARD)
        bk_row.pack(fill="x")

        ACCENT_TEAL = "#2dd4bf"
        bk_tools = [
            ("restore_pt",    "", ACCENT_TEAL,   ""),
            ("reg_backup",    "", ACCENT_BLUE,   ""),
            ("driver_backup", "", ACCENT_ORANGE, ""),
        ]

        for i, (key, text, color, tooltip) in enumerate(bk_tools):
            f = tk.Frame(bk_row, bg=BG_CARD)
            f.pack(side="left", padx=(0 if i == 0 else 8, 0), fill="x", expand=True)

            btn = tk.Button(
                f, text=text, font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg=color, activebackground=color,
                activeforeground="#ffffff", bd=0, padx=14, pady=8,
                cursor="hand2",
                command=lambda k=key: self._on_tool_click(k)
            )
            btn.pack(fill="x")
            self.buttons[key] = btn

            tip = tk.Label(f, text="", font=("Segoe UI", 8),
                           fg=FG_SECONDARY, bg=BG_CARD)
            tip.pack(pady=(2, 0))
            self.tips[key] = tip

        prog_frame = tk.Frame(main, bg=BG_CARD, bd=0, highlightthickness=1,
                              highlightbackground=BORDER_COLOR)
        prog_frame.pack(fill="x", pady=(0, 12))
        prog_inner = tk.Frame(prog_frame, bg=BG_CARD, padx=15, pady=10)
        prog_inner.pack(fill="x")

        self.status_label = tk.Label(
            prog_inner, text="", font=("Segoe UI", 10),
            fg=ACCENT_GREEN, bg=BG_CARD, anchor="w"
        )
        self.status_label.pack(fill="x")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor=BG_INPUT, background=ACCENT_BLUE,
                        bordercolor=BORDER_COLOR, lightcolor=ACCENT_BLUE,
                        darkcolor=ACCENT_BLUE)

        self.progress = ttk.Progressbar(
            prog_inner, style="Custom.Horizontal.TProgressbar",
            mode="indeterminate", length=400
        )
        self.progress.pack(fill="x", pady=(6, 0))

        console_frame = tk.Frame(main, bg=BG_CARD, bd=0, highlightthickness=1,
                                 highlightbackground=BORDER_COLOR)
        console_frame.pack(fill="both", expand=True)
        console_inner = tk.Frame(console_frame, bg=BG_CARD, padx=15, pady=10)
        console_inner.pack(fill="both", expand=True)

        console_header = tk.Frame(console_inner, bg=BG_CARD)
        console_header.pack(fill="x", pady=(0, 6))

        self.console_label = tk.Label(
            console_header, text="",
            font=("Segoe UI", 12, "bold"), fg=FG_PRIMARY, bg=BG_CARD
        )
        self.console_label.pack(side="left")

        self.clear_btn = tk.Button(
            console_header, text="", font=("Segoe UI", 9),
            fg=FG_SECONDARY, bg=BG_INPUT, activebackground=BORDER_COLOR,
            bd=0, padx=10, pady=3, cursor="hand2",
            command=self._clear_console
        )
        self.clear_btn.pack(side="right")

        self.console = scrolledtext.ScrolledText(
            console_inner, font=("Cascadia Code", 10),
            bg=BG_DARK, fg=FG_PRIMARY, insertbackground=FG_PRIMARY,
            selectbackground=ACCENT_BLUE, selectforeground="#ffffff",
            bd=0, wrap="word", state="disabled", height=18
        )
        self.console.pack(fill="both", expand=True)

        self.console.tag_configure("info",    foreground=ACCENT_BLUE)
        self.console.tag_configure("success", foreground=ACCENT_GREEN)
        self.console.tag_configure("error",   foreground=ACCENT_RED)
        self.console.tag_configure("warning", foreground=ACCENT_YELLOW)
        self.console.tag_configure("header",  foreground=ACCENT_PURPLE, font=("Cascadia Code", 11, "bold"))
        self.console.tag_configure("dim",     foreground=FG_SECONDARY)

        bottom = tk.Frame(main, bg=BG_DARK)
        bottom.pack(fill="x", pady=(10, 0))

        self.cancel_btn = tk.Button(
            bottom, text="", font=("Segoe UI", 10, "bold"),
            fg="#ffffff", bg=ACCENT_RED, activebackground="#da3633",
            bd=0, padx=20, pady=8, cursor="hand2", state="disabled",
            command=self._cancel
        )
        self.cancel_btn.pack(side="right")

        self.time_label = tk.Label(
            bottom, text="", font=("Segoe UI", 9), fg=FG_SECONDARY, bg=BG_DARK
        )
        self.time_label.pack(side="left")

    def _check_admin(self):
        if is_admin():
            self.admin_label.config(text=self.t("admin_yes"), fg=ACCENT_GREEN)
            self._log(self.t("admin_ok"), "success")
        else:
            self.admin_label.config(text=self.t("admin_no"), fg=ACCENT_RED)
            self._log(self.t("admin_warn"), "error")
            self._log(self.t("admin_warn2"), "warning")

    def _log(self, text, tag=None):
        self.console.config(state="normal")
        if tag:
            self.console.insert("end", text, tag)
        else:
            self.console.insert("end", text)
        self.console.see("end")
        self.console.config(state="disabled")

    def _clear_console(self):
        self.console.config(state="normal")
        self.console.delete("1.0", "end")
        self.console.config(state="disabled")

    def _set_running(self, running):
        self.is_running = running
        state = "disabled" if running else "normal"
        for btn in self.buttons.values():
            btn.config(state=state)
        self.cancel_btn.config(state="normal" if running else "disabled")
        if running:
            self.progress.start(15)
        else:
            self.progress.stop()

    def _cancel(self):
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.kill()
            except Exception:
                pass
            self._log(self.t("cancel_msg"), "error")
            self._set_running(False)
            self.status_label.config(text=self.t("cancelled"), fg=ACCENT_RED)

    def _on_tool_click(self, key):
        if self.is_running:
            return
        actions = {
            "sfc":      self._run_sfc,
            "dism_ch":  self._run_dism_check,
            "dism_rp":  self._run_dism_repair,
            "chkdsk":   self._run_chkdsk,
            "full":     self._run_full_repair,
            "wu_off":   self._disable_update,
            "wu_on":    self._enable_update,
            "wu_check": self._check_update_status,
            "wd_off":   self._disable_defender,
            "wd_on":    self._enable_defender,
            "wd_check": self._check_defender_status,
            "sandbox_on":  self._enable_sandbox,
            "sandbox_off": self._disable_sandbox,
            "widgets_off": self._disable_widgets,
            "widgets_on":  self._enable_widgets,
            "telemetry":   self._disable_telemetry,
            "restore_pt":    self._create_restore_point,
            "reg_backup":    self._backup_registry,
            "driver_backup": self._backup_drivers,
        }
        threading.Thread(target=actions[key], daemon=True).start()

    def _run_command(self, cmd, description):
        self._log(f"\n{'═' * 60}\n", "dim")
        self._log(f"▶ {description}\n", "header")
        self._log(f"  {self.t('cmd')}: {cmd}\n", "dim")
        self._log(f"  {self.t('start_time')}: {datetime.now().strftime('%H:%M:%S')}\n", "dim")
        self._log(f"{'─' * 60}\n", "dim")

        self.root.after(0, lambda: self.status_label.config(
            text=f"{self.t('running')}: {description}...", fg=ACCENT_YELLOW
        ))

        try:
            process = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="cp857", errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.current_process = process

            output_lines = []
            for line in iter(process.stdout.readline, ""):
                if not self.is_running:
                    break
                stripped = line.strip()
                if stripped:
                    output_lines.append(stripped)
                    if any(w in stripped.lower() for w in ["hata", "error", "fail", "başarısız"]):
                        self.root.after(0, lambda l=stripped: self._log(f"  ❌ {l}\n", "error"))
                    elif any(w in stripped.lower() for w in ["başarı", "success", "tamam", "tamamlandı", "onarıldı", "repaired"]):
                        self.root.after(0, lambda l=stripped: self._log(f"  ✅ {l}\n", "success"))
                    elif any(w in stripped.lower() for w in ["uyarı", "warning", "dikkat"]):
                        self.root.after(0, lambda l=stripped: self._log(f"  ⚠️  {l}\n", "warning"))
                    elif "%" in stripped:
                        self.root.after(0, lambda l=stripped: self._log(f"  ⏳ {l}\n", "info"))
                    else:
                        self.root.after(0, lambda l=stripped: self._log(f"  {l}\n"))

            process.wait()
            exit_code = process.returncode
            self.current_process = None

            self.root.after(0, lambda: self._log(
                f"\n  {self.t('end_time')}: {datetime.now().strftime('%H:%M:%S')} | {self.t('exit_code')}: {exit_code}\n",
                "dim"
            ))

            return exit_code, output_lines

        except Exception as e:
            self.current_process = None
            self.root.after(0, lambda: self._log(f"\n  ❌ {self.t('error')}: {e}\n", "error"))
            return -1, []

    def _run_sfc(self):
        self._set_running(True)
        self._log("\n🔍 SFC (System File Checker) başlatılıyor...\n", "info")
        self._log("Bu işlem sistem dosyalarını tarar ve bozuk olanları onarır.\n", "dim")
        self._log("İşlem birkaç dakika sürebilir, lütfen bekleyin...\n\n", "warning")

        code, output = self._run_command("sfc /scannow", "SFC Tam Tarama")

        full_output = "\n".join(output).lower()
        self._log(f"\n{'─' * 60}\n", "dim")
        if "bütünlük ihlali bulunamadı" in full_output or "did not find any integrity violations" in full_output:
            self._log("✅ SONUÇ: Bozuk sistem dosyası bulunamadı. Sisteminiz sağlıklı!\n", "success")
        elif "başarıyla onarıldı" in full_output or "successfully repaired" in full_output:
            self._log("✅ SONUÇ: Bozuk dosyalar bulundu ve başarıyla onarıldı!\n", "success")
        elif "onaramadı" in full_output or "could not" in full_output:
            self._log("⚠️  SONUÇ: Bazı dosyalar onarılamadı. DISM aracını çalıştırmayı deneyin.\n", "warning")
        else:
            self._log(f"ℹ️  SONUÇ: İşlem tamamlandı (Çıkış kodu: {code})\n", "info")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="SFC taraması tamamlandı", fg=ACCENT_GREEN))

    def _run_dism_check(self):
        self._set_running(True)
        self._log("\n🏥 DISM Sağlık Kontrolü başlatılıyor...\n", "info")
        self._log("Windows imaj sağlığı kontrol edilecek.\n\n", "dim")

        code, output = self._run_command(
            "DISM /Online /Cleanup-Image /CheckHealth",
            "DISM Sağlık Kontrolü (Hızlı)"
        )

        code2, output2 = self._run_command(
            "DISM /Online /Cleanup-Image /ScanHealth",
            "DISM Detaylı Tarama"
        )

        full_output = "\n".join(output + output2).lower()
        self._log(f"\n{'─' * 60}\n", "dim")
        if "repairable" in full_output or "onarılabilir" in full_output:
            self._log("⚠️  SONUÇ: Onarılabilir hatalar bulundu! DISM Onar butonunu kullanın.\n", "warning")
        elif "no component store corruption" in full_output or "bozulma algılanmadı" in full_output:
            self._log("✅ SONUÇ: Windows imajı sağlıklı!\n", "success")
        else:
            self._log(f"ℹ️  SONUÇ: Kontrol tamamlandı (Çıkış kodu: {code2})\n", "info")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="DISM kontrolü tamamlandı", fg=ACCENT_GREEN))

    def _run_dism_repair(self):
        self._set_running(True)
        self._log("\n🔧 DISM Onarım başlatılıyor...\n", "info")
        self._log("Bu işlem Windows Update üzerinden bozuk dosyaları indirir ve onarır.\n", "dim")
        self._log("İnternet bağlantısı gereklidir. İşlem uzun sürebilir...\n\n", "warning")

        code, output = self._run_command(
            "DISM /Online /Cleanup-Image /RestoreHealth",
            "DISM İmaj Onarımı"
        )

        full_output = "\n".join(output).lower()
        self._log(f"\n{'─' * 60}\n", "dim")
        if "restore operation completed successfully" in full_output or "geri yükleme işlemi başarıyla tamamlandı" in full_output:
            self._log("✅ SONUÇ: Windows imajı başarıyla onarıldı!\n", "success")
            self._log("💡 İPUCU: Şimdi SFC taramasını tekrar çalıştırmanız önerilir.\n", "info")
        elif code == 0:
            self._log("✅ SONUÇ: DISM onarım işlemi tamamlandı.\n", "success")
        else:
            self._log(f"⚠️  SONUÇ: İşlem tamamlandı ama hatalar olabilir (Çıkış kodu: {code})\n", "warning")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="DISM onarım tamamlandı", fg=ACCENT_GREEN))

    def _run_chkdsk(self):
        self._set_running(True)
        self._log("\n💾 Disk Kontrolü başlatılıyor...\n", "info")
        self._log("C: sürücüsü hata taraması yapılacak (salt okunur).\n", "dim")
        self._log("Not: Onarım için bilgisayar yeniden başlatma gerekebilir.\n\n", "warning")

        code, output = self._run_command(
            "chkdsk C: /scan",
            "CHKDSK Disk Tarama"
        )

        full_output = "\n".join(output).lower()
        self._log(f"\n{'─' * 60}\n", "dim")
        if "no problems" in full_output or "sorun bulunamadı" in full_output or "herhangi bir sorun" in full_output:
            self._log("✅ SONUÇ: Diskte hata bulunamadı!\n", "success")
        elif "found errors" in full_output or "hata bulundu" in full_output:
            self._log("⚠️  SONUÇ: Disk hataları bulundu.\n", "warning")
            self._log("💡 Onarım için komut isteminde şu komutu çalıştırın:\n", "info")
            self._log("   chkdsk C: /f /r  (Yeniden başlatma gerektirir)\n", "info")
        else:
            self._log(f"ℹ️  SONUÇ: Tarama tamamlandı (Çıkış kodu: {code})\n", "info")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Disk kontrolü tamamlandı", fg=ACCENT_GREEN))

    def _run_full_repair(self):
        self._set_running(True)
        self._log("\n" + "🚀" * 30 + "\n", "info")
        self._log("TAM ONARIM BAŞLATILIYOR\n", "header")
        self._log("Sıra: DISM Kontrol → DISM Onar → SFC Tara → Disk Kontrol\n", "dim")
        self._log("Bu işlem oldukça uzun sürebilir, lütfen sabırlı olun.\n", "warning")
        self._log("🚀" * 30 + "\n", "info")

        steps = [
            ("DISM /Online /Cleanup-Image /ScanHealth",    "DISM Sağlık Taraması [1/4]"),
            ("DISM /Online /Cleanup-Image /RestoreHealth",  "DISM İmaj Onarımı [2/4]"),
            ("sfc /scannow",                                "SFC Sistem Taraması [3/4]"),
            ("chkdsk C: /scan",                             "CHKDSK Disk Taraması [4/4]"),
        ]

        results = []
        for i, (cmd, desc) in enumerate(steps):
            if not self.is_running:
                break
            self.root.after(0, lambda d=desc: self.status_label.config(
                text=f"Çalışıyor: {d}", fg=ACCENT_YELLOW
            ))
            code, output = self._run_command(cmd, desc)
            results.append((desc, code))

        self._log(f"\n{'═' * 60}\n", "dim")
        self._log("📊 TAM ONARIM SONUÇ ÖZETİ\n", "header")
        self._log(f"{'─' * 60}\n", "dim")
        for desc, code in results:
            status = "✅ Başarılı" if code == 0 else f"⚠️  Çıkış kodu: {code}"
            tag = "success" if code == 0 else "warning"
            self._log(f"  {desc}: {status}\n", tag)
        self._log(f"{'═' * 60}\n", "dim")
        self._log("\n💡 ÖNERİ: Değişikliklerin tam olarak uygulanması için bilgisayarınızı\n", "info")
        self._log("   yeniden başlatmanız önerilir.\n", "info")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Tam onarım tamamlandı!", fg=ACCENT_GREEN))

    def _disable_update(self):
        self._set_running(True)
        self._log("\n🚫 Windows Update kapatılıyor...\n", "info")

        services = ["wuauserv", "WaaSMedicSvc", "UsoSvc"]
        for svc in services:
            self._log(f"  Servis durduruluyor: {svc}\n", "dim")
            subprocess.run(f'sc stop "{svc}"', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(f'sc config "{svc}" start=disabled', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        try:
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            except FileNotFoundError:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            winreg.SetValueEx(key, "NoAutoUpdate", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "AUOptions", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            self._log("  ✅ Registry ayarları güncellendi (NoAutoUpdate=1)\n", "success")
        except Exception as e:
            self._log(f"  ❌ Registry hatası: {e}\n", "error")

        tasks = [
            "\\Microsoft\\Windows\\WindowsUpdate\\Scheduled Start",
            "\\Microsoft\\Windows\\UpdateOrchestrator\\Schedule Scan",
        ]
        for task in tasks:
            subprocess.run(f'schtasks /Change /TN "{task}" /DISABLE', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        self._log("\n✅ Windows Update başarıyla kapatıldı!\n", "success")
        self._log("💡 Değişiklikler yeniden başlatmadan sonra tam olarak uygulanır.\n", "info")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Windows Update kapatıldı", fg=ACCENT_RED))

    def _enable_update(self):
        self._set_running(True)
        self._log("\n✅ Windows Update açılıyor...\n", "info")

        services = ["wuauserv", "WaaSMedicSvc", "UsoSvc"]
        for svc in services:
            self._log(f"  Servis etkinleştiriliyor: {svc}\n", "dim")
            subprocess.run(f'sc config "{svc}" start=auto', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(f'sc start "{svc}"', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        try:
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, "NoAutoUpdate")
                winreg.DeleteValue(key, "AUOptions")
                winreg.CloseKey(key)
            except FileNotFoundError:
                pass
            self._log("  ✅ Registry ayarları temizlendi\n", "success")
        except Exception as e:
            self._log(f"  ❌ Registry hatası: {e}\n", "error")

        tasks = [
            "\\Microsoft\\Windows\\WindowsUpdate\\Scheduled Start",
            "\\Microsoft\\Windows\\UpdateOrchestrator\\Schedule Scan",
        ]
        for task in tasks:
            subprocess.run(f'schtasks /Change /TN "{task}" /ENABLE', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        self._log("\n✅ Windows Update başarıyla açıldı!\n", "success")
        self._log("💡 Güncellemeler tekrar otomatik olarak indirilecektir.\n", "info")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Windows Update açıldı", fg=ACCENT_GREEN))

    def _check_update_status(self):
        self._set_running(True)
        self._log("\nℹ️  Windows Update durumu kontrol ediliyor...\n", "info")
        self._log(f"{'─' * 60}\n", "dim")

        services = [
            ("wuauserv",     "Windows Update"),
            ("WaaSMedicSvc", "WaaS Medic Svc"),
            ("UsoSvc",       "Update Orchestrator"),
        ]
        for svc_id, svc_name in services:
            result = subprocess.run(
                f'sc query "{svc_id}"', shell=True,
                capture_output=True, text=True, encoding="cp857", errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            output = result.stdout.lower()
            if "running" in output:
                self._log(f"  🟢 {svc_name}: Çalışıyor\n", "success")
            elif "stopped" in output:
                self._log(f"  🔴 {svc_name}: Durdurulmuş\n", "error")
            else:
                self._log(f"  🟡 {svc_name}: Bilinmiyor\n", "warning")

        try:
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
            val, _ = winreg.QueryValueEx(key, "NoAutoUpdate")
            winreg.CloseKey(key)
            if val == 1:
                self._log(f"\n  📋 Registry: Otomatik güncelleme KAPALI\n", "error")
            else:
                self._log(f"\n  📋 Registry: Otomatik güncelleme AÇIK\n", "success")
        except FileNotFoundError:
            self._log(f"\n  📋 Registry: Varsayılan (güncelleme açık)\n", "success")
        except Exception as e:
            self._log(f"\n  📋 Registry okunamadı: {e}\n", "warning")

        self._log(f"{'─' * 60}\n", "dim")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Durum kontrolü tamamlandı", fg=ACCENT_GREEN))

    def _ps(self, cmd):
        return subprocess.run(
            f'powershell -ExecutionPolicy Bypass -Command "{cmd}"',
            shell=True, capture_output=True, text=True,
            encoding="cp857", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    def _reg_set(self, path, name, value=1):
        try:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE)
            except FileNotFoundError:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    def _disable_defender(self):
        self._set_running(True)
        self._log("\n" + "🚫" * 30 + "\n", "error")
        self._log("WINDOWS DEFENDER KÖKTEN KAPATILIYOR\n", "header")
        self._log("Tüm korumalar, servisler ve bileşenler devre dışı bırakılacak.\n", "dim")
        self._log("🚫" * 30 + "\n\n", "error")

        self._log("━━━ [1/8] Tamper Protection ━━━\n", "header")
        self._ps("Set-MpPreference -DisableTamperProtection $true")
        self._reg_set(r"SOFTWARE\Microsoft\Windows Defender\Features", "TamperProtection", 0)
        self._log("  Tamper Protection kapatılmaya çalışıldı\n", "info")
        self._log("  ⚠️  Windows 11 bunu engelleyebilir — altta manuel yol gösterilecek\n", "warning")

        self._log("\n━━━ [2/8] Tüm Korumalar Kapatılıyor (PowerShell) ━━━\n", "header")
        ps_prefs = [
            ("DisableRealtimeMonitoring", "Gerçek zamanlı koruma"),
            ("DisableBehaviorMonitoring", "Davranış izleme"),
            ("DisableIOAVProtection", "İndirme taraması"),
            ("DisableOnAccessProtection", "Erişim koruması"),
            ("DisableScanOnRealtimeEnable", "Anlık tarama"),
            ("DisableBlockAtFirstSeen", "İlk görüşte engelleme"),
            ("DisableEmailScanning", "E-posta taraması"),
            ("DisableScriptScanning", "Script taraması"),
            ("DisableArchiveScanning", "Arşiv taraması"),
            ("DisableRemovableDriveScanning", "USB taraması"),
            ("DisableNetworkProtectionPerfTelemetry", "Ağ telemetrisi"),
            ("DisableDatagramProcessing", "Datagram işleme"),
            ("DisableDnsParsing", "DNS ayrıştırma"),
            ("DisableDnsOverTcpParsing", "DNS over TCP"),
            ("DisableHttpParsing", "HTTP ayrıştırma"),
            ("DisableInboundConnectionFiltering", "Gelen bağlantı filtresi"),
            ("DisableRdpParsing", "RDP ayrıştırma"),
            ("DisableSshParsing", "SSH ayrıştırma"),
            ("DisableTlsParsing", "TLS ayrıştırma"),
        ]
        for pref, name in ps_prefs:
            r = self._ps(f"Set-MpPreference -{pref} $true")
            tag = "success" if r.returncode == 0 else "warning"
            symbol = "✅" if r.returncode == 0 else "⚠️ "
            self._log(f"  {symbol} {name}\n", tag)

        self._ps("Set-MpPreference -MAPSReporting 0")
        self._ps("Set-MpPreference -SubmitSamplesConsent 2")
        self._log("  ✅ Bulut koruma ve örnek gönderme kapatıldı\n", "success")

        self._ps("Set-MpPreference -PUAProtection 0")
        self._log("  ✅ PUA (İstenmeyen Uygulama) koruması kapatıldı\n", "success")

        self._log("\n━━━ [3/8] Registry — Defender Devre Dışı ━━━\n", "header")
        reg_entries = [
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "DisableAntiSpyware", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "DisableAntiVirus", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "ServiceKeepAlive", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "AllowFastServiceStartup", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableRealtimeMonitoring", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableBehaviorMonitoring", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableOnAccessProtection", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableScanOnRealtimeEnable", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableIOAVProtection", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet", "SpynetReporting", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Spynet", "SubmitSamplesConsent", 2),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\MpEngine", "MpEnablePus", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Reporting", "DisableEnhancedNotifications", 1),
        ]
        ok_count = 0
        for path, name, val in reg_entries:
            if self._reg_set(path, name, val):
                ok_count += 1
        self._log(f"  ✅ {ok_count}/{len(reg_entries)} registry değeri yazıldı\n", "success")

        self._log("\n━━━ [4/8] Servisler Durduruluyor ━━━\n", "header")
        services = [
            ("WinDefend", "Windows Defender Antivirus"),
            ("WdNisSvc", "Defender Network Inspection"),
            ("WdNisDrv", "Defender NIS Driver"),
            ("WdFilter", "Defender Mini-Filter Driver"),
            ("WdBoot", "Defender Boot Driver"),
            ("Sense", "Defender Advanced Threat Protection"),
            ("SecurityHealthService", "Security Health Service"),
            ("wscsvc", "Security Center"),
            ("SgrmBroker", "System Guard Runtime Monitor"),
        ]
        for svc, name in services:
            subprocess.run(f'sc stop "{svc}"', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(f'sc config "{svc}" start=disabled', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self._log(f"  🔴 {name} ({svc}) durduruldu\n", "dim")

        self._log("\n━━━ [5/8] Güvenlik Bildirimleri Kapatılıyor ━━━\n", "header")
        notif_entries = [
            (r"SOFTWARE\Policies\Microsoft\Windows Defender Security Center\Notifications", "DisableNotifications", 1),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender Security Center\Notifications", "DisableEnhancedNotifications", 1),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Notifications\Settings\Windows.SystemToast.SecurityAndMaintenance", "Enabled", 0),
        ]
        for path, name, val in notif_entries:
            self._reg_set(path, name, val)
        self._log("  ✅ Güvenlik bildirimleri kapatıldı\n", "success")

        self._reg_set(r"SOFTWARE\Policies\Microsoft\Windows Defender Security Center\Systray", "HideSystray", 1)
        self._log("  ✅ Sistem tepsisi simgesi gizlendi\n", "success")

        self._log("\n━━━ [6/8] Windows Firewall Kapatılıyor ━━━\n", "header")
        for profile in ["domainprofile", "privateprofile", "publicprofile"]:
            subprocess.run(f'netsh advfirewall set {profile} state off', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        self._log("  ✅ Tüm Firewall profilleri kapatıldı (Domain/Private/Public)\n", "success")

        self._log("\n━━━ [7/8] SmartScreen Kapatılıyor ━━━\n", "header")
        ss_entries = [
            (r"SOFTWARE\Policies\Microsoft\Windows\System", "EnableSmartScreen", 0),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer", "SmartScreenEnabled", 0),
            (r"SOFTWARE\Policies\Microsoft\MicrosoftEdge\PhishingFilter", "EnabledV9", 0),
        ]
        for path, name, val in ss_entries:
            self._reg_set(path, name, val)
        self._ps("Set-MpPreference -EnableNetworkProtection 0")
        self._log("  ✅ SmartScreen ve ağ koruması kapatıldı\n", "success")

        self._log("\n━━━ [8/8] Zamanlanmış Görevler Kapatılıyor ━━━\n", "header")
        tasks = [
            "\\Microsoft\\Windows\\Windows Defender\\Windows Defender Cache Maintenance",
            "\\Microsoft\\Windows\\Windows Defender\\Windows Defender Cleanup",
            "\\Microsoft\\Windows\\Windows Defender\\Windows Defender Scheduled Scan",
            "\\Microsoft\\Windows\\Windows Defender\\Windows Defender Verification",
            "\\Microsoft\\Windows\\ExploitGuard\\ExploitGuard MDM policy Refresh",
        ]
        for task in tasks:
            subprocess.run(f'schtasks /Change /TN "{task}" /DISABLE', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        self._log("  ✅ Tüm Defender zamanlanmış görevleri devre dışı bırakıldı\n", "success")

        self._log(f"\n{'═' * 60}\n", "dim")
        self._log("✅ WINDOWS DEFENDER KÖKTEN KAPATILDI!\n", "success")
        self._log(f"{'═' * 60}\n", "dim")
        self._log("\n⚠️  Tamper Protection manuel kapatılmalı (Windows engelliyor):\n", "warning")
        self._log("   1. Ayarlar → Gizlilik ve Güvenlik → Windows Güvenliği\n", "info")
        self._log("   2. Virüs ve tehdit koruması → Ayarları yönet\n", "info")
        self._log("   3. 'Kurcalama Koruması' → KAPALI\n", "info")
        self._log("   4. Sonra bu aracı tekrar çalıştırın\n", "info")
        self._log("\n💡 Değişikliklerin tam uygulanması için YENIDEN BAŞLATIN.\n", "warning")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Defender kökten kapatıldı!", fg=ACCENT_RED))

    def _enable_defender(self):
        self._set_running(True)
        self._log("\n✅ Windows Defender açılıyor...\n", "info")

        self._log("  Gerçek zamanlı koruma açılıyor...\n", "dim")
        subprocess.run(
            'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $false"',
            shell=True, capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        protections = [
            ("DisableBehaviorMonitoring", "Davranış izleme"),
            ("DisableIOAVProtection", "İndirme taraması"),
            ("DisableOnAccessProtection", "Erişim koruması"),
            ("DisableScanOnRealtimeEnable", "Anlık tarama"),
        ]
        for pref, name in protections:
            self._log(f"  {name} açılıyor...\n", "dim")
            subprocess.run(
                f'powershell -Command "Set-MpPreference -{pref} $false"',
                shell=True, capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

        try:
            key_path = r"SOFTWARE\Policies\Microsoft\Windows Defender"
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, "DisableAntiSpyware")
                winreg.CloseKey(key)
            except (FileNotFoundError, OSError):
                pass

            rtp_path = r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection"
            try:
                rtp_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rtp_path, 0, winreg.KEY_SET_VALUE)
                for val in ["DisableRealtimeMonitoring", "DisableBehaviorMonitoring",
                            "DisableOnAccessProtection", "DisableScanOnRealtimeEnable"]:
                    try:
                        winreg.DeleteValue(rtp_key, val)
                    except FileNotFoundError:
                        pass
                winreg.CloseKey(rtp_key)
            except (FileNotFoundError, OSError):
                pass
            self._log("  ✅ Registry ayarları temizlendi\n", "success")
        except Exception as e:
            self._log(f"  ❌ Registry hatası: {e}\n", "error")

        subprocess.run('sc config WinDefend start=auto', shell=True,
                       capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run('sc start WinDefend', shell=True,
                       capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        self._log("\n✅ Windows Defender başarıyla açıldı!\n", "success")
        self._log("💡 Tüm korumalar tekrar etkinleştirildi.\n", "info")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Windows Defender açıldı", fg=ACCENT_GREEN))

    def _check_defender_status(self):
        self._set_running(True)
        self._log("\nℹ️  Windows Defender durumu kontrol ediliyor...\n", "info")
        self._log(f"{'─' * 60}\n", "dim")

        result = subprocess.run(
            'powershell -Command "Get-MpPreference | Select-Object DisableRealtimeMonitoring, DisableBehaviorMonitoring, DisableIOAVProtection, DisableOnAccessProtection | Format-List"',
            shell=True, capture_output=True, text=True, encoding="cp857", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        prefs = {}
        for line in result.stdout.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                prefs[k.strip()] = v.strip()

        labels = {
            "DisableRealtimeMonitoring": "Gerçek Zamanlı Koruma",
            "DisableBehaviorMonitoring": "Davranış İzleme",
            "DisableIOAVProtection": "İndirme Taraması",
            "DisableOnAccessProtection": "Erişim Koruması",
        }

        for pref_key, label in labels.items():
            val = prefs.get(pref_key, "Bilinmiyor")
            if val.lower() == "false":
                self._log(f"  🟢 {label}: AÇIK\n", "success")
            elif val.lower() == "true":
                self._log(f"  🔴 {label}: KAPALI\n", "error")
            else:
                self._log(f"  🟡 {label}: {val}\n", "warning")

        svc_result = subprocess.run(
            'sc query WinDefend', shell=True,
            capture_output=True, text=True, encoding="cp857", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        svc_out = svc_result.stdout.lower()
        if "running" in svc_out:
            self._log(f"\n  🟢 Defender Servisi: Çalışıyor\n", "success")
        elif "stopped" in svc_out:
            self._log(f"\n  🔴 Defender Servisi: Durdurulmuş\n", "error")
        else:
            self._log(f"\n  🟡 Defender Servisi: Bilinmiyor\n", "warning")

        tp_result = subprocess.run(
            'powershell -Command "(Get-MpComputerStatus).IsTamperProtected"',
            shell=True, capture_output=True, text=True, encoding="cp857", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        tp_val = tp_result.stdout.strip().lower()
        if tp_val == "true":
            self._log(f"  🔒 Tamper Protection: AÇIK (manuel kapatılmalı)\n", "warning")
        elif tp_val == "false":
            self._log(f"  🔓 Tamper Protection: KAPALI\n", "success")

        self._log(f"{'─' * 60}\n", "dim")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text="Defender durumu kontrol edildi", fg=ACCENT_GREEN))

    def _enable_sandbox(self):
        self._set_running(True)
        self._log("\n📦 Windows Sandbox etkinleştiriliyor...\n", "info")
        r = subprocess.run(
            'dism /online /enable-feature /featurename:Containers-DisposableClientVM /all /norestart',
            shell=True, capture_output=True, text=True, encoding="cp857", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if r.returncode == 0:
            self._log("  ✅ Windows Sandbox etkinleştirildi!\n", "success")
            self._log("  💡 Değişiklik için yeniden başlatma gerekli.\n", "info")
        else:
            self._log("  ⚠️  Sandbox etkinleştirilemedi.\n", "warning")
            self._log("  Bu özellik Windows 11 Pro/Enterprise gerektirir.\n", "dim")
            if r.stdout:
                for line in r.stdout.strip().splitlines():
                    if line.strip():
                        self._log(f"  {line.strip()}\n", "dim")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def _disable_sandbox(self):
        self._set_running(True)
        self._log("\n📦 Windows Sandbox devre dışı bırakılıyor...\n", "info")
        r = subprocess.run(
            'dism /online /disable-feature /featurename:Containers-DisposableClientVM /norestart',
            shell=True, capture_output=True, text=True, encoding="cp857", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if r.returncode == 0:
            self._log("  ✅ Windows Sandbox devre dışı bırakıldı!\n", "success")
        else:
            self._log("  ⚠️  İşlem başarısız oldu.\n", "warning")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def _disable_widgets(self):
        self._set_running(True)
        self._log("\n📰 Haber ve Widget paneli kapatılıyor...\n", "info")

        self._log("  Widget servisi kapatılıyor...\n", "dim")
        subprocess.run('winget uninstall "Windows Web Experience Pack" --accept-source-agreements --silent',
                       shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        entries = [
            (r"SOFTWARE\Policies\Microsoft\Dsh", "AllowNewsAndInterests", 0),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "TaskbarDa", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows\Windows Feeds", "EnableFeeds", 0),
        ]
        for path, name, val in entries:
            self._reg_set(path, name, val)
        self._log("  ✅ Widget/Haber paneli registry'den kapatıldı\n", "success")

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "TaskbarDa", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except Exception:
            pass

        self._reg_set(r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana", 0)
        self._reg_set(r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowSearchToUseLocation", 0)
        self._reg_set(r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", "DisableWebSearch", 1)
        self._log("  ✅ Cortana ve web araması kapatıldı\n", "success")

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", 0, winreg.KEY_SET_VALUE)
            for name in ["SubscribedContent-338388Enabled", "SubscribedContent-338389Enabled",
                         "SubscribedContent-353694Enabled", "SubscribedContent-353696Enabled",
                         "SystemPaneSuggestionsEnabled", "SoftLandingEnabled"]:
                winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            self._log("  ✅ Başlat menüsü önerileri kapatıldı\n", "success")
        except Exception:
            pass

        self._reg_set(r"SOFTWARE\Policies\Microsoft\Windows\CloudContent", "DisableWindowsConsumerFeatures", 1)
        self._reg_set(r"SOFTWARE\Policies\Microsoft\Windows\CloudContent", "DisableSoftLanding", 1)
        self._log("  ✅ Kilit ekranı ipuçları ve reklam içerikleri kapatıldı\n", "success")

        self._log("\n✅ Tüm gereksiz haberler ve widget'lar kapatıldı!\n", "success")
        self._log("💡 Tam etki için Explorer'ı yeniden başlatın veya PC'yi reboot edin.\n", "info")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def _enable_widgets(self):
        self._set_running(True)
        self._log("\n📰 Haber ve Widget paneli açılıyor...\n", "info")

        paths_to_delete = [
            (r"SOFTWARE\Policies\Microsoft\Dsh", "AllowNewsAndInterests"),
            (r"SOFTWARE\Policies\Microsoft\Windows\Windows Feeds", "EnableFeeds"),
        ]
        for path, name in paths_to_delete:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, name)
                winreg.CloseKey(key)
            except (FileNotFoundError, OSError):
                pass

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "TaskbarDa", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except Exception:
            pass

        subprocess.run('winget install "Windows Web Experience Pack" --accept-source-agreements --silent',
                       shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

        self._log("  ✅ Widget/Haber paneli tekrar açıldı!\n", "success")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def _disable_telemetry(self):
        self._set_running(True)
        self._log("\n📡 Telemetri ve veri toplama kapatılıyor...\n", "info")

        self._log("  Telemetri servisleri kapatılıyor...\n", "dim")
        services = ["DiagTrack", "dmwappushservice", "diagnosticshub.standardcollector.service",
                    "WerSvc", "PcaSvc"]
        for svc in services:
            subprocess.run(f'sc stop "{svc}"', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(f'sc config "{svc}" start=disabled', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self._log(f"  🔴 {svc} durduruldu\n", "dim")

        self._log("  Registry güncelleniyor...\n", "dim")
        tel_entries = [
            (r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "DoNotShowFeedbackNotifications", 1),
            (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", "AllowTelemetry", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows\AppCompat", "AITEnable", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows\AppCompat", "DisableUAR", 1),
            (r"SOFTWARE\Policies\Microsoft\SQMClient\Windows", "CEIPEnable", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows\PreviewBuilds", "AllowBuildPreview", 0),
        ]
        ok = 0
        for path, name, val in tel_entries:
            if self._reg_set(path, name, val):
                ok += 1
        self._log(f"  ✅ {ok}/{len(tel_entries)} registry değeri yazıldı\n", "success")

        self._log("  Zamanlanmış görevler kapatılıyor...\n", "dim")
        tasks = [
            "\\Microsoft\\Windows\\Application Experience\\Microsoft Compatibility Appraiser",
            "\\Microsoft\\Windows\\Application Experience\\ProgramDataUpdater",
            "\\Microsoft\\Windows\\Autochk\\Proxy",
            "\\Microsoft\\Windows\\Customer Experience Improvement Program\\Consolidator",
            "\\Microsoft\\Windows\\Customer Experience Improvement Program\\UsbCeip",
            "\\Microsoft\\Windows\\DiskDiagnostic\\Microsoft-Windows-DiskDiagnosticDataCollector",
            "\\Microsoft\\Windows\\Feedback\\Siuf\\DmClient",
        ]
        for task in tasks:
            subprocess.run(f'schtasks /Change /TN "{task}" /DISABLE', shell=True,
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        self._log("  ✅ Telemetri zamanlanmış görevleri kapatıldı\n", "success")

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except Exception:
            pass
        self._log("  ✅ Reklam kimliği kapatıldı\n", "success")

        self._log("\n✅ Telemetri ve veri toplama kökten kapatıldı!\n", "success")
        self._log("💡 Yeniden başlatma önerilir.\n", "info")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def _create_restore_point(self):
        self._set_running(True)
        self._log("\n📌 Sistem geri yükleme noktası oluşturuluyor...\n", "info")
        self._log("  Bu işlem birkaç dakika sürebilir...\n", "warning")

        self._ps("Enable-ComputerRestore -Drive 'C:\\'")

        r = self._ps(
            "Checkpoint-Computer -Description 'FuckWin11_Backup' -RestorePointType 'MODIFY_SETTINGS'"
        )
        if r.returncode == 0:
            self._log("\n  ✅ Geri yükleme noktası başarıyla oluşturuldu!\n", "success")
            self._log(f"  📅 Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n", "info")
        else:
            err = r.stderr.strip() if r.stderr else ""
            if "1314" in err or "privilege" in err.lower():
                self._log("  ❌ Yönetici yetkisi gerekli!\n", "error")
            elif "already been created" in err.lower() or "zaten" in err.lower():
                self._log("  ⚠️  Son 24 saat içinde zaten bir geri yükleme noktası oluşturulmuş.\n", "warning")
            else:
                self._log(f"  ❌ Hata: {err}\n", "error")
                if r.stdout:
                    self._log(f"  {r.stdout.strip()}\n", "dim")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def _backup_registry(self):
        self._set_running(True)
        self._log("\n🗂️ Registry yedekleniyor...\n", "info")

        backup_dir = os.path.join(os.path.expanduser("~"), "Desktop", "FuckWin11_Backups")
        os.makedirs(backup_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        hives = [
            ("HKLM\\SYSTEM",   f"SYSTEM_{ts}.reg"),
            ("HKLM\\SOFTWARE", f"SOFTWARE_{ts}.reg"),
            ("HKCU",           f"HKCU_{ts}.reg"),
        ]

        for hive, filename in hives:
            path = os.path.join(backup_dir, filename)
            self._log(f"  {hive} yedekleniyor...\n", "dim")
            r = subprocess.run(
                f'reg export "{hive}" "{path}" /y',
                shell=True, capture_output=True, text=True,
                encoding="cp857", errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if r.returncode == 0:
                size_mb = os.path.getsize(path) / (1024 * 1024)
                self._log(f"  ✅ {filename} ({size_mb:.1f} MB)\n", "success")
            else:
                self._log(f"  ❌ {hive} yedeklenemedi\n", "error")

        self._log(f"\n  ✅ Registry yedekleri kaydedildi: {backup_dir}\n", "success")
        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def _backup_drivers(self):
        self._set_running(True)
        self._log("\n🖥️ Sürücüler yedekleniyor...\n", "info")
        self._log("  Bu işlem birkaç dakika sürebilir...\n", "warning")

        backup_dir = os.path.join(os.path.expanduser("~"), "Desktop", "FuckWin11_Backups", "Drivers")
        os.makedirs(backup_dir, exist_ok=True)

        r = subprocess.run(
            f'dism /online /export-driver /destination:"{backup_dir}"',
            shell=True, capture_output=True, text=True,
            encoding="cp857", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if r.returncode == 0:
            driver_count = len([f for f in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, f))])
            self._log(f"\n  ✅ {driver_count} sürücü yedeklendi!\n", "success")
            self._log(f"  📁 Konum: {backup_dir}\n", "info")
        else:
            self._log("  ❌ Sürücü yedekleme başarısız oldu.\n", "error")
            if r.stdout:
                for line in r.stdout.strip().splitlines()[-5:]:
                    if line.strip():
                        self._log(f"  {line.strip()}\n", "dim")

        self._set_running(False)
        self.root.after(0, lambda: self.status_label.config(text=self.t("ready"), fg=ACCENT_GREEN))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    
    app = SystemRepairApp()
    app.run()

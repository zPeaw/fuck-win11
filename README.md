# 🖕 Fuck Win11 — Windows 11 System Control Tool

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Language-TR%20%7C%20EN-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Admin-Required-red?style=for-the-badge&logo=windows-terminal" />
</p>

---

> 🇹🇷 **[Türkçe](#-türkçe-dokümantasyon)** | 🇬🇧 **[English](#-english-documentation)**

---

## 🇬🇧 English Documentation

### What is this?

**Fuck Win11** is an advanced Windows 11 system control and repair utility built with Python and Tkinter. It provides a dark-themed GUI that allows you to repair broken system files, control Windows Update & Defender, tweak privacy settings, and create full system backups — all from a single interface, without touching the command line.

> ⚠️ **This tool is intended for use when Windows 11 is misbehaving, causing problems, or when you need full control over system services.**

---

### 🖥️ Interface Overview

On startup, a **10-second splash screen** is displayed with the ASCII art logo and a countdown timer. After the countdown, the main interface loads automatically.

The main window (950×780, resizable) contains:
- **Header** — Title, admin status badge, and a language toggle button (TR ↔ EN)
- **Section panels** — One panel per feature category, each with action buttons and tooltip labels
- **Progress bar** — Animated indeterminate bar that activates during any running operation
- **Console output** — A scrollable, color-coded log area showing real-time command output
- **Cancel button** — Terminates the currently running process immediately
- **Status bar** — Shows the current state (Ready / Running / Cancelled)

The UI automatically detects your system language on startup and switches between **Turkish** and **English** accordingly. You can also toggle it manually at any time.

---

### ✨ Features

#### 🔧 System Repair

| Button | Command | Description |
|---|---|---|
| 🔍 SFC Scan | `sfc /scannow` | Scans all protected Windows system files and automatically repairs corrupted ones |
| 🏥 DISM Health Check | `DISM /CheckHealth` + `DISM /ScanHealth` | Performs a quick check and a deep scan of the Windows component store |
| 🔧 DISM Repair | `DISM /RestoreHealth` | Downloads healthy files from Windows Update and repairs the system image (requires internet) |
| 💾 Disk Check | `chkdsk C: /scan` | Scans the C: drive for file system errors in read-only mode |
| 🚀 Full Repair | All of the above, sequentially | Runs DISM Scan → DISM Repair → SFC → CHKDSK in order and shows a summary at the end |

**Smart output parsing:** The console automatically color-codes output lines:
- 🔴 **Error** lines (containing "error", "fail", "hata") → red
- 🟢 **Success** lines (containing "success", "repaired", "tamamlandı") → green
- 🟡 **Warning** lines (containing "warning", "uyarı") → yellow
- ⏳ **Progress** lines (containing `%`) → blue

---

#### 🚫 Windows Update Control

Stops and prevents Windows Update from running automatically.

**Disable Update** performs:
1. Stops services: `wuauserv`, `WaaSMedicSvc`, `UsoSvc`
2. Sets all three services to `start=disabled`
3. Writes registry key `NoAutoUpdate=1` and `AUOptions=1` under `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU`
4. Disables scheduled tasks: `Scheduled Start` and `Schedule Scan`

**Enable Update** reverses all of the above — re-enables services, deletes the registry keys, and re-enables scheduled tasks.

**Check Status** shows the live running state of each service and reads the registry to show whether auto-update is currently blocked.

---

#### �️ Windows Defender Control

The Defender disable function runs **8 sequential steps** for a deep, thorough shutdown:

| Step | What it does |
|---|---|
| [1/8] Tamper Protection | Attempts to disable via PowerShell and registry (may require manual disable first) |
| [2/8] All Protections (PowerShell) | Disables **19 protection modules** via `Set-MpPreference` — real-time monitoring, behavior monitoring, download scanning, email scanning, script scanning, archive scanning, USB scanning, network parsers (DNS, HTTP, RDP, SSH, TLS), cloud reporting, PUA protection, etc. |
| [3/8] Registry (13 keys) | Writes 13 registry values across 5 paths to force-disable antispyware, antivirus, real-time protection, cloud reporting, and enhanced notifications |
| [4/8] Services (9 services) | Stops and disables: `WinDefend`, `WdNisSvc`, `WdNisDrv`, `WdFilter`, `WdBoot`, `Sense`, `SecurityHealthService`, `wscsvc`, `SgrmBroker` |
| [5/8] Notifications | Hides Defender notifications and the system tray icon |
| [6/8] Windows Firewall | Disables firewall on all 3 profiles: Domain, Private, Public |
| [7/8] SmartScreen | Disables SmartScreen for Explorer, Edge, and network protection |
| [8/8] Scheduled Tasks | Disables all 5 Defender scheduled tasks (cache, cleanup, scheduled scan, verification, ExploitGuard) |

> ⚠️ **Tamper Protection** cannot be disabled programmatically on Windows 11 — it must be turned off manually:
> `Settings → Privacy & Security → Windows Security → Virus & threat protection → Manage settings → Tamper Protection → OFF`

**Enable Defender** re-enables real-time monitoring, clears registry overrides, and restarts the `WinDefend` service.

**Check Status** uses `Get-MpPreference` to show the live state of 4 key protection modules plus the service state and Tamper Protection status.

---

#### ⚙️ System Tweaks

**📰 Disable News/Widgets:**
- Uninstalls "Windows Web Experience Pack" via winget
- Disables news & interests via registry (`AllowNewsAndInterests=0`, `TaskbarDa=0`, `EnableFeeds=0`)
- Disables Cortana and web search in Start menu
- Disables Start menu app suggestions (6 ContentDeliveryManager keys)
- Disables lock screen tips and ad content (`DisableWindowsConsumerFeatures`, `DisableSoftLanding`)

**📦 Windows Sandbox:**
- Enable: `dism /online /enable-feature /featurename:Containers-DisposableClientVM /all /norestart`
- Disable: `dism /online /disable-feature /featurename:Containers-DisposableClientVM /norestart`
- Requires Windows 11 Pro or Enterprise

**📡 Disable Telemetry:**
- Stops and disables 5 telemetry services: `DiagTrack`, `dmwappushservice`, `diagnosticshub.standardcollector.service`, `WerSvc`, `PcaSvc`
- Writes 7 registry values: sets `AllowTelemetry=0`, disables CEIP, feedback notifications, AI telemetry, and Windows Insider previews
- Disables 7 scheduled tasks related to compatibility appraiser, CEIP, disk diagnostics, and feedback
- Disables Advertising ID in current user registry

---

#### 💿 Backup

**📌 Create Restore Point:**
- Ensures System Restore is enabled on C:
- Creates a labeled restore point: `FuckWin11_Backup` (type: `MODIFY_SETTINGS`)
- Note: Windows limits restore point creation to once per 24 hours

**🗂️ Backup Registry:**
- Saves `HKLM\SYSTEM`, `HKLM\SOFTWARE`, and `HKCU` as `.reg` files
- Files are timestamped: e.g., `SYSTEM_20250226_014355.reg`
- Saved to `Desktop\FuckWin11_Backups\`
- Reports the size of each exported file

**🖥️ Backup Drivers:**
- Uses `dism /online /export-driver` to export all installed drivers
- Saved to `Desktop\FuckWin11_Backups\Drivers\`
- Reports the count of backed up drivers

---

### 🚀 Installation & Usage

#### Requirements
- Windows 11
- Python 3.8 or higher
- Administrator privileges (automatically requested on launch)

> ✅ **No `pip install` needed.** This tool uses only Python's standard library (`tkinter`, `subprocess`, `winreg`, `os`, `ctypes`, `threading`, etc.) — all included with Python by default.

#### Quick Check (install.bat)

Double-click `install.bat` to verify your environment is ready:

```
install.bat
```

It will:
1. Check that Python 3.8+ is installed and on PATH
2. Check that `tkinter` is available
3. Tell you everything is ready — no downloads required

#### Running the script
```bash
python win11_system_repair.py
```

The script checks for admin rights on startup. If not running as admin, it will automatically re-launch itself with a UAC elevation prompt. After the 10-second splash screen, the main interface loads.

> 💡 Right-click `win11_system_repair.py` → **Run as administrator** for best results.

---

### ⚠️ Important Warnings

- **Administrator rights are mandatory.** The tool will warn you if not running as admin and many features will not work.
- **Disabling Windows Defender reduces system security.** Only do this if you know what you're doing.
- **Tamper Protection** must be disabled manually before the full Defender shutdown takes effect.
- **Most changes take full effect after a system restart.** A restart is recommended after any operation.
- **Backup files** are saved to `Desktop\FuckWin11_Backups\` — do not delete them until you're sure everything works correctly.
- The **CHKDSK** scan runs in read-only `/scan` mode. To actually repair disk errors, run `chkdsk C: /f /r` from an elevated command prompt (requires restart).
- **Windows Sandbox** requires Windows 11 Pro or Enterprise. It will not work on Home edition.

---

### 📁 File Structure

```
fuck win11 update/
├── win11_system_repair.py   # Main application (single-file, ~1500 lines)
├── README.md                # This documentation
├── LICENSE                  # MIT License
└── .gitignore
```

---

### 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---
---

## 🇹🇷 Türkçe Dokümantasyon

### Bu nedir?

**Fuck Win11**, Python ve Tkinter ile yazılmış gelişmiş bir Windows 11 sistem kontrol ve onarım aracıdır. Bozuk sistem dosyalarını onarmak, Windows Update ve Defender'ı kontrol etmek, gizlilik ayarlarını düzenlemek ve sistem yedeği almak gibi işlemleri komut satırına dokunmadan tek bir arayüzden yapmanızı sağlar.

> ⚠️ **Bu araç, Windows 11 sorun çıkardığında, hata verdiğinde veya sistem servisleri üzerinde tam kontrol istediğinizde kullanılmak üzere tasarlanmıştır.**

---

### 🖥️ Arayüz Genel Bakış

Uygulama açıldığında, **10 saniyelik bir splash ekranı** gösterilir. Bu ekranda ASCII logo ve geri sayım sayacı yer alır. Sayaç sıfırlandığında ana arayüz otomatik olarak yüklenir.

Ana pencere (950×780, yeniden boyutlandırılabilir) şu bölümleri içerir:
- **Başlık** — Uygulama adı, yönetici durumu rozeti ve dil değiştirme butonu (TR ↔ EN)
- **Bölüm panelleri** — Her özellik kategorisi için ayrı panel; butonlar ve açıklama etiketleri içerir
- **İlerleme çubuğu** — Herhangi bir işlem çalışırken aktifleşen animasyonlu çubuk
- **Konsol çıktısı** — Gerçek zamanlı komut çıktısını renk kodlamasıyla gösteren kaydırılabilir log alanı
- **İptal butonu** — Çalışan işlemi anında sonlandırır
- **Durum çubuğu** — Mevcut durumu gösterir (Hazır / Çalışıyor / İptal Edildi)

Arayüz, sistem dilinizi otomatik olarak algılar ve Türkçe ya da İngilizce olarak başlar. İstediğiniz zaman manuel olarak dil değiştirebilirsiniz.

---

### ✨ Özellikler

#### 🔧 Sistem Onarımı

| Buton | Komut | Açıklama |
|---|---|---|
| � SFC Tara | `sfc /scannow` | Tüm korumalı Windows sistem dosyalarını tarar ve bozuk olanları otomatik onarır |
| 🏥 DISM Sağlık Kontrol | `DISM /CheckHealth` + `DISM /ScanHealth` | Windows bileşen deposunu hızlı kontrol ve derin tarama yapar |
| 🔧 DISM Onar | `DISM /RestoreHealth` | Windows Update üzerinden sağlıklı dosyaları indirip sistem imajını onarır (internet gerekli) |
| 💾 Disk Kontrol | `chkdsk C: /scan` | C: sürücüsünü salt okunur modda dosya sistemi hatalarına karşı tarar |
| 🚀 Tam Onarım | Yukarıdakilerin tamamı, sırayla | DISM Tarama → DISM Onar → SFC → CHKDSK sırasıyla çalışır, sonda özet gösterilir |

**Akıllı çıktı ayrıştırma:** Konsol, komut çıktısı satırlarını otomatik olarak renklendirir:
- 🔴 **Hata** satırları (içinde "error", "fail", "hata" geçen) → kırmızı
- 🟢 **Başarılı** satırlar (içinde "success", "repaired", "tamamlandı" geçen) → yeşil
- 🟡 **Uyarı** satırları (içinde "warning", "uyarı" geçen) → sarı
- ⏳ **İlerleme** satırları (`%` içeren) → mavi

---

#### 🚫 Windows Update Kontrolü

Windows Update'in otomatik çalışmasını tamamen durdurur ve engeller.

**Update Kapat** şu adımları uygular:
1. Servisleri durdurur: `wuauserv`, `WaaSMedicSvc`, `UsoSvc`
2. Üç servisin başlangıç tipini `start=disabled` olarak ayarlar
3. `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU` altına `NoAutoUpdate=1` ve `AUOptions=1` yazar
4. Zamanlanmış görevleri devre dışı bırakır: `Scheduled Start` ve `Schedule Scan`

**Update Aç**, yukarıdakilerin tamamını geri alır — servisleri yeniden etkinleştirir, registry anahtarlarını siler ve zamanlanmış görevleri açar.

**Update Durumu**, her servisin anlık çalışma durumunu ve registry'de otomatik güncellemenin engellenip engellenmediğini gösterir.

---

#### 🛡️ Windows Defender Kontrolü

Defender kapatma işlevi **8 ardışık adım** uygulayarak tam ve kapsamlı bir kapatma gerçekleştirir:

| Adım | Ne yapar |
|---|---|
| [1/8] Tamper Protection | PowerShell ve registry ile kapatmaya çalışır (önce manuel kapatma gerekebilir) |
| [2/8] Tüm Korumalar (PowerShell) | `Set-MpPreference` ile **19 koruma modülünü** devre dışı bırakır — gerçek zamanlı izleme, davranış izleme, indirme taraması, e-posta taraması, script taraması, arşiv taraması, USB taraması, ağ ayrıştırıcıları (DNS, HTTP, RDP, SSH, TLS), bulut raporlama, PUA koruması vb. |
| [3/8] Registry (13 anahtar) | 5 farklı yolda 13 registry değeri yazar: antispyware, antivirus, gerçek zamanlı koruma, bulut raporlama ve gelişmiş bildirimler devre dışı bırakılır |
| [4/8] Servisler (9 servis) | Şu servisleri durdurur ve devre dışı bırakır: `WinDefend`, `WdNisSvc`, `WdNisDrv`, `WdFilter`, `WdBoot`, `Sense`, `SecurityHealthService`, `wscsvc`, `SgrmBroker` |
| [5/8] Bildirimler | Defender bildirimlerini ve sistem tepsisi simgesini gizler |
| [6/8] Windows Firewall | 3 profilin tamamında (Domain, Private, Public) güvenlik duvarını kapatır |
| [7/8] SmartScreen | Explorer, Edge için SmartScreen'i ve ağ korumasını devre dışı bırakır |
| [8/8] Zamanlanmış Görevler | 5 Defender zamanlanmış görevini devre dışı bırakır (önbellek, temizleme, tarama, doğrulama, ExploitGuard) |

> ⚠️ **Tamper Protection**, Windows 11'de programatik olarak kapatılamaz — manuel olarak kapatılmalıdır:
> `Ayarlar → Gizlilik ve Güvenlik → Windows Güvenliği → Virüs ve tehdit koruması → Ayarları yönet → Kurcalama Koruması → KAPALI`

**Defender Aç**, gerçek zamanlı izlemeyi yeniden açar, registry geçersiz kılmalarını temizler ve `WinDefend` servisini yeniden başlatır.

**Defender Durumu**, `Get-MpPreference` kullanarak 4 temel koruma modülünün anlık durumunu, servis durumunu ve Tamper Protection'ın açık/kapalı olduğunu gösterir.

---

#### ⚙️ Sistem Ayarları

**� Haber/Widget Kapat:**
- Winget ile "Windows Web Experience Pack" kaldırır
- Registry üzerinden haber ve ilgi alanlarını devre dışı bırakır (`AllowNewsAndInterests=0`, `TaskbarDa=0`, `EnableFeeds=0`)
- Başlat menüsünde Cortana ve web aramasını kapatır
- Başlat menüsü uygulama önerilerini kapatır (6 ContentDeliveryManager anahtarı)
- Kilit ekranı ipuçlarını ve reklam içeriklerini kapatır (`DisableWindowsConsumerFeatures`, `DisableSoftLanding`)

**📦 Windows Sandbox:**
- Aç: `dism /online /enable-feature /featurename:Containers-DisposableClientVM /all /norestart`
- Kapat: `dism /online /disable-feature /featurename:Containers-DisposableClientVM /norestart`
- Windows 11 Pro veya Enterprise gerektirir

**📡 Telemetri Kapat:**
- 5 telemetri servisini durdurur ve devre dışı bırakır: `DiagTrack`, `dmwappushservice`, `diagnosticshub.standardcollector.service`, `WerSvc`, `PcaSvc`
- 7 registry değeri yazar: `AllowTelemetry=0`, CEIP, geri bildirim bildirimleri, AI telemetrisi ve Windows Insider önizlemesi devre dışı bırakılır
- Uyumluluk değerlendiricisi, CEIP, disk tanılama ve geri bildirimle ilgili 7 zamanlanmış görevi devre dışı bırakır
- Mevcut kullanıcıda Reklam kimliğini devre dışı bırakır

---

#### 💿 Yedekleme

**📌 Geri Yükleme Noktası:**
- C: sürücüsünde Sistem Geri Yükleme'nin etkin olduğundan emin olur
- `FuckWin11_Backup` etiketiyle bir geri yükleme noktası oluşturur (tür: `MODIFY_SETTINGS`)
- Not: Windows, 24 saat içinde yalnızca bir geri yükleme noktası oluşturulmasına izin verir

**🗂️ Registry Yedekle:**
- `HKLM\SYSTEM`, `HKLM\SOFTWARE` ve `HKCU`'yu `.reg` dosyası olarak kaydeder
- Dosyalar zaman damgalıdır: örn. `SYSTEM_20250226_014355.reg`
- `Masaüstü\FuckWin11_Backups\` klasörüne kaydedilir
- Her dışa aktarılan dosyanın boyutunu raporlar

**🖥️ Sürücü Yedekle:**
- `dism /online /export-driver` komutuyla tüm yüklü sürücüleri dışa aktarır
- `Masaüstü\FuckWin11_Backups\Drivers\` klasörüne kaydedilir
- Yedeklenen sürücü sayısını raporlar

---

### 🚀 Kurulum ve Kullanım

#### Gereksinimler
- Windows 11
- Python 3.8 veya üzeri
- Yönetici yetkisi (başlatılırken otomatik olarak istenir)

> ✅ **`pip install` gerekmez.** Bu araç yalnızca Python'un standart kütüphanesini kullanır (`tkinter`, `subprocess`, `winreg`, `os`, `ctypes`, `threading` vb.) — hepsi Python ile birlikte gelir.

#### Hızlı Kontrol (install.bat)

`install.bat` dosyasına çift tıklayarak ortamınızın hazır olup olmadığını kontrol edin:

```
install.bat
```

Şunları kontrol eder:
1. Python 3.8+ kurulu ve PATH'te mi?
2. `tkinter` mevcut mu?
3. Her şey hazır — indirme gerekmez

#### Scripti Çalıştırma
```bash
python win11_system_repair.py
```

Script, başlarken yönetici yetkilerini kontrol eder. Yönetici olarak çalışmıyorsa, otomatik olarak kendini UAC yetki yükseltme istemiyle yeniden başlatır. 10 saniyelik splash ekranının ardından ana arayüz yüklenir.

> 💡 `win11_system_repair.py` dosyasına sağ tık → **Yönetici olarak çalıştır** yapmanız önerilir.

---

### ⚠️ Önemli Uyarılar

- **Yönetici yetkisi zorunludur.** Yönetici olarak çalıştırılmadığında araç sizi uyarır ve birçok özellik çalışmaz.
- **Windows Defender'ı kapatmak sistem güvenliğini düşürür.** Bunu yalnızca ne yaptığınızı biliyorsanız yapın.
- **Tamper Protection**, Defender tam kapatması etkili olmadan önce manuel olarak kapatılmalıdır.
- **Değişikliklerin büyük çoğunluğu sistem yeniden başlatılmasından sonra tam olarak uygulanır.** Herhangi bir işlem sonrasında yeniden başlatma önerilir.
- **Yedek dosyaları** `Masaüstü\FuckWin11_Backups\` klasörüne kaydedilir — her şeyin doğru çalıştığından emin olana kadar silmeyiniz.
- **CHKDSK** taraması salt okunur `/scan` modunda çalışır. Disk hatalarını gerçekten onarmak için yükseltilmiş komut isteminde `chkdsk C: /f /r` komutunu çalıştırın (yeniden başlatma gerektirir).
- **Windows Sandbox**, Windows 11 Pro veya Enterprise gerektirir. Home sürümünde çalışmaz.


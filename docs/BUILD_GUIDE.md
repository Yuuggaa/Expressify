# 🏗️ Expressify - Build Guide

Panduan lengkap untuk membuild Expressify menjadi executable (.exe) yang dapat dijalankan tanpa instalasi Python.

## 📋 Daftar Isi

- [Metode Build](#metode-build)
- [Persiapan](#persiapan)
- [Build dengan Script Otomatis](#build-dengan-script-otomatis)
- [Build Manual](#build-manual)
- [Troubleshooting](#troubleshooting)
- [Distribusi](#distribusi)

---

## 🎯 Metode Build

Ada 2 metode build yang tersedia:

### 1. **One-File Mode** (Recommended untuk distribusi)
- ✅ Satu file .exe tunggal
- ✅ Mudah didistribusikan
- ⚠️ Startup lebih lambat (~5-10 detik)
- ⚠️ Ukuran file besar (~150-200 MB)

### 2. **One-Directory Mode** (Recommended untuk performa)
- ✅ Startup lebih cepat
- ✅ Ukuran total lebih kecil
- ⚠️ Banyak file dalam folder (harus didistribusikan bersama)

---

## 🛠️ Persiapan

### 1. Install Dependencies Build

```bash
# Aktifkan virtual environment
venv\Scripts\activate

# Install PyInstaller
pip install pyinstaller

# (Optional) Install auto-py-to-exe untuk GUI
pip install auto-py-to-exe
```

### 2. Buat Icon (Optional)

Jika belum ada `assets/images/icon.ico`, buat dari gambar PNG:

```bash
pip install pillow
```

```python
from PIL import Image

img = Image.open('assets/photo/Senang.png')
img.save('assets/images/icon.ico', format='ICO', sizes=[(256, 256)])
```

---

## 🚀 Build dengan Script Otomatis

### Metode 1: One-File Mode

```bash
# Jalankan script build
build_exe.bat
```

Output: `dist\Expressify.exe` (single file)

### Metode 2: One-Directory Mode

```bash
# Jalankan script build directory
build_exe_dir.bat
```

Output: `dist\Expressify\` folder dengan `Expressify.exe` di dalamnya

---

## 🔧 Build Manual

### PyInstaller Command (One-File)

```bash
pyinstaller ^
    --name="Expressify" ^
    --onefile ^
    --windowed ^
    --icon="assets/images/icon.ico" ^
    --add-data="assets;assets" ^
    --add-data="src/ui;src/ui" ^
    --hidden-import="mediapipe" ^
    --hidden-import="cv2" ^
    --hidden-import="pygame" ^
    --hidden-import="numpy" ^
    --hidden-import="PIL" ^
    --collect-data="mediapipe" ^
    --noconsole ^
    src/main.py
```

### PyInstaller Command (One-Directory)

```bash
pyinstaller ^
    --name="Expressify" ^
    --onedir ^
    --windowed ^
    --icon="assets/images/icon.ico" ^
    --add-data="assets;assets" ^
    --add-data="src/ui;src/ui" ^
    --hidden-import="mediapipe" ^
    --hidden-import="cv2" ^
    --hidden-import="pygame" ^
    --hidden-import="numpy" ^
    --hidden-import="PIL" ^
    --collect-data="mediapipe" ^
    --noconsole ^
    src/main.py
```

### Penjelasan Parameter

| Parameter | Fungsi |
|-----------|--------|
| `--name` | Nama executable |
| `--onefile` | Build menjadi satu file tunggal |
| `--onedir` | Build menjadi folder dengan dependencies |
| `--windowed` | Tanpa console window (GUI only) |
| `--icon` | Icon aplikasi (.ico) |
| `--add-data` | Include file/folder ke build |
| `--hidden-import` | Import module yang tidak terdeteksi |
| `--collect-data` | Collect data files dari package |
| `--noconsole` | Sama dengan --windowed |

---

## 🎨 Build dengan GUI (auto-py-to-exe)

Untuk yang lebih suka interface grafis:

```bash
# Install
pip install auto-py-to-exe

# Jalankan GUI
auto-py-to-exe
```

### Pengaturan di GUI:

1. **Script Location**: `src/main.py`
2. **Onefile**: One Directory (recommended)
3. **Console Window**: Window Based (hide the console)
4. **Icon**: `assets/images/icon.ico`
5. **Additional Files**:
   - Add Folder: `assets` → `assets`
   - Add Folder: `src/ui` → `src/ui`
6. **Hidden Imports**: mediapipe, cv2, pygame, numpy, PIL
7. **Advanced**: `--collect-data mediapipe`

---

## ⚠️ Troubleshooting

### Problem: "Module not found" error

**Solusi**: Tambahkan hidden import

```bash
--hidden-import=module_name
```

### Problem: Assets tidak ditemukan

**Solusi**: Pastikan add-data benar

```bash
--add-data="assets;assets"
```

### Problem: MediaPipe error

**Solusi**: Collect MediaPipe data

```bash
--collect-data="mediapipe"
```

### Problem: Executable terlalu besar

**Solusi**: 
1. Gunakan `--onedir` mode
2. Exclude module tidak terpakai:
```bash
--exclude-module=matplotlib
--exclude-module=scipy
```

### Problem: Antivirus mendeteksi sebagai virus

**Solusi**: 
1. False positive umum pada PyInstaller
2. Submit ke VirusTotal untuk verifikasi
3. Sign executable dengan code signing certificate (optional, berbayar)

### Problem: Startup sangat lambat (onefile mode)

**Solusi**:
1. Gunakan `--onedir` mode
2. Atau tambahkan `--splash` untuk splash screen saat loading:
```bash
--splash="assets/images/splash.png"
```

---

## 📦 Distribusi

### One-File Mode

Distribusikan file tunggal:
```
Expressify.exe (150-200 MB)
```

User tinggal double-click untuk main!

### One-Directory Mode

Distribusikan folder lengkap:
```
Expressify/
├── Expressify.exe
├── _internal/  (dependencies)
├── assets/     (game assets)
└── ...
```

**Cara distribusi:**
1. Zip folder `dist\Expressify`
2. Upload ke Google Drive / GitHub Releases
3. User extract dan jalankan `Expressify.exe`

---

## 📤 Upload ke GitHub Releases

```bash
# 1. Create release di GitHub
# 2. Zip executable
cd dist
7z a Expressify-v1.0-Windows.zip Expressify.exe

# 3. Upload zip ke GitHub Releases
```

---

## 🔒 Code Signing (Optional, untuk produksi)

Untuk menghindari warning Windows SmartScreen:

1. Beli code signing certificate (~$100-300/tahun)
2. Sign executable:
```bash
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com Expressify.exe
```

---

## 📊 Perbandingan Metode

| Aspek | One-File | One-Directory |
|-------|----------|---------------|
| **Ukuran** | ~150-200 MB | ~200-250 MB (total) |
| **File Count** | 1 file | 100+ files |
| **Startup Time** | 5-10 detik | 1-2 detik |
| **Distribusi** | Sangat mudah | Perlu zip folder |
| **Update** | Ganti 1 file | Update folder |
| **Recommended** | Casual users | Performance-focused |

---

## 🎮 Testing Executable

Setelah build, test executable:

1. ✅ Jalankan tanpa Python installed
2. ✅ Test di Windows PC lain (fresh install)
3. ✅ Test semua fitur game
4. ✅ Test dengan webcam berbeda
5. ✅ Cek sound berfungsi
6. ✅ Cek leaderboard tersimpan

---

## 📝 Checklist Pre-Release

- [ ] Build executable berhasil
- [ ] Test di PC clean (tanpa Python)
- [ ] Semua assets terinclude
- [ ] Webcam detection working
- [ ] Sound system working
- [ ] Leaderboard save/load working
- [ ] Tidak ada error/crash
- [ ] Ukuran file reasonable
- [ ] Buat README untuk user
- [ ] Zip untuk distribusi
- [ ] Upload ke GitHub Releases

---

## 🆘 Support & Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [auto-py-to-exe GitHub](https://github.com/brentvollebregt/auto-py-to-exe)
- [Expressify Issues](https://github.com/Yuuggaa/Expressify/issues)

---

**Happy Building! 🚀**

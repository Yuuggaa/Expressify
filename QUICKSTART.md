# Quick Start Guide

## 🚀 Instalasi Cepat (5 Menit)

### Windows Users

1. **Buka PowerShell di folder project**
2. **Jalankan:**
   ```powershell
   .\setup.bat
   ```
3. **Tunggu sampai selesai install**
4. **Jalankan game:**
   ```powershell
   venv\Scripts\activate
   python src\main.py
   ```

### Linux/Mac Users

1. **Buka Terminal di folder project**
2. **Jalankan:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. **Tunggu sampai selesai install**
4. **Jalankan game:**
   ```bash
   source venv/bin/activate
   python src/main.py
   ```

## ⚠️ Troubleshooting Cepat

### "Python tidak ditemukan"

**Solusi:** Install Python dari [python.org](https://www.python.org/downloads/)

- Pastikan check "Add Python to PATH" saat install

### "pip tidak ditemukan"

**Solusi:**

```bash
python -m ensurepip --upgrade
```

### "Kamera tidak berfungsi"

**Solusi:**

- Close aplikasi lain yang menggunakan kamera
- Check permission kamera di system settings
- Restart computer

### Error saat install dependencies

**Solusi:**

```bash
# Upgrade pip dulu
python -m pip install --upgrade pip

# Install satu-satu jika ada yang gagal
pip install mediapipe
pip install opencv-python
pip install pygame
pip install numpy
pip install Pillow
```

## ✅ Checklist Sebelum Mulai

- [ ] Python 3.8+ terinstall
- [ ] Git terinstall (untuk clone repo)
- [ ] Webcam tersedia dan berfungsi
- [ ] Internet connection (untuk download dependencies)
- [ ] Minimal 500MB free space

## 🎮 Controls

| Key     | Action                  |
| ------- | ----------------------- |
| `SPACE` | Start game / Play again |
| `ESC`   | Exit game               |

---

**Happy Gaming! 🎉**

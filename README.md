# 🎮 Expressify - Face Expression Game

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10.0-red.svg)

## 📝 Deskripsi Project

**Expressify** adalah permainan interaktif berbasis deteksi ekspresi wajah yang menantang pemain untuk menunjukkan berbagai ekspresi dengan cepat dan akurat! Dalam 20 detik, kamu akan diberi instruksi acak seperti **senyum lebar**, **cemberut sedih**, atau **kaget maksimal**! Setiap ekspresi yang benar akan menambah skor kamu.

Game ini dikembangkan sebagai Tugas Besar untuk mata kuliah **Sistem Teknologi Multimedia** menggunakan **MediaPipe Face Mesh** untuk deteksi landmark wajah tanpa deep learning.

## ✨ Fitur

- 🎯 **Real-time Face Detection** menggunakan MediaPipe Face Mesh
- 😊 **4 Ekspresi Berbeda**: Happy, Sad, Surprised, Neutral
- ⏱️ **20 Detik Gameplay** yang intens dan seru
- 🎨 **UI Interaktif** dengan Pygame
- 📊 **Sistem Scoring** dengan feedback performa
- 🎵 **Support untuk Audio** (dapat dikembangkan lebih lanjut)

## 🧑‍🤝‍🧑 Tim Pengembang

| Nama                    | Role      |
| ----------------------- | --------- |
| **Hamka Putra Andiyan** | Developer |
| **Bayu Ega Ferdana**    | Developer |
| **Falih Dzakwan Zuhdi** | Developer |

## 🔧 Teknologi yang Digunakan

- **Python 3.8+**
- **MediaPipe** - Face Mesh untuk deteksi landmark wajah
- **OpenCV** - Pengolahan video dan gambar
- **Pygame** - User interface dan game rendering
- **NumPy** - Komputasi numerik

## 📋 Requirements

Semua dependencies sudah terdaftar di `requirements.txt`:

```
mediapipe==0.10.14
opencv-python==4.10.0.84
numpy==1.26.4
pygame==2.6.0
Pillow==10.4.0
```

## 🚀 Instalasi

### Untuk Windows (PowerShell/CMD):

1. Clone repository ini:

```bash
git clone https://github.com/Yuuggaa/Expressify.git
cd Expressify
```

2. Jalankan script setup:

```bash
setup.bat
```

Script akan otomatis:

- Membuat virtual environment
- Menginstall semua dependencies
- Menyiapkan environment

### Untuk Linux/Mac:

1. Clone repository ini:

```bash
git clone https://github.com/Yuuggaa/Expressify.git
cd Expressify
```

2. Jalankan script setup:

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Installation (Semua Platform):

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Cara Menjalankan Game

1. **Aktifkan virtual environment** (jika belum aktif):

   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

2. **Jalankan game**:

```bash
python src/main.py
```

3. **Kontrol Game**:
   - `SPASI` - Mulai game / Main lagi
   - `ESC` - Keluar dari game

## 🎯 Cara Bermain

1. **Menu Utama**: Tekan SPASI untuk memulai game
2. **Gameplay**:
   - Perhatikan instruksi ekspresi di layar atas
   - Tunjukkan ekspresi yang diminta ke kamera
   - Setiap ekspresi benar menambah 1 poin
   - Kamu punya 20 detik untuk mendapat skor tertinggi!
3. **Hasil**: Lihat skor akhir dan performa kamu
4. **Ulangi**: Tekan SPASI untuk main lagi

## 📁 Struktur Project

```
Expressify/
├── src/
│   ├── main.py              # Entry point game
│   ├── face_detector.py     # Module deteksi wajah
│   ├── game_logic.py        # Logic permainan
│   └── ui_manager.py        # User interface
├── assets/
│   ├── sounds/              # Audio files (optional)
│   └── images/              # Image assets (optional)
├── docs/                    # Dokumentasi tambahan
├── requirements.txt         # Python dependencies
├── setup.bat               # Setup script Windows
├── setup.sh                # Setup script Linux/Mac
├── .gitignore              # Git ignore file
└── README.md               # Dokumentasi project
```

## 🔍 Cara Kerja Deteksi Ekspresi

Game ini menggunakan **MediaPipe Face Mesh** yang mendeteksi 478 landmark pada wajah. Algoritma deteksi ekspresi bekerja dengan:

1. **Deteksi Landmark**: Mengidentifikasi posisi mata, alis, mulut, dll.
2. **Analisis Geometri**: Menghitung jarak dan sudut antar landmark
3. **Klasifikasi Ekspresi**:
   - **Happy**: Sudut mulut naik ke atas
   - **Sad**: Sudut mulut turun ke bawah
   - **Surprised**: Mulut terbuka lebar, alis naik
   - **Neutral**: Posisi rileks/default

## 🐛 Troubleshooting

### Kamera tidak terdeteksi

- Pastikan webcam terpasang dan tidak digunakan aplikasi lain
- Coba restart aplikasi
- Check permission kamera di sistem operasi

### Dependencies error

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Virtual environment issues

```bash
# Hapus dan buat ulang venv
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
python -m venv venv
```

## 📚 Referensi

- [MediaPipe Face Mesh](https://github.com/google-ai-edge/mediapipe/wiki/MediaPipe-Face-Mesh)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Pygame Documentation](https://www.pygame.org/docs/)

## 📄 Lisensi

Project ini dibuat untuk keperluan akademik (Tugas Besar Sistem Teknologi Multimedia).

## 🎓 Mata Kuliah

**Sistem Teknologi Multimedia**  
Tugas Besar - Face Expression Game

---

**Dibuat dengan ❤️ oleh Tim Expressify**

_Hamka Putra Andiyan • Bayu Ega Ferdana • Falih Dzakwan Zuhdi_

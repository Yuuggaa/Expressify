# 🎮 Fitur Baru - Difficulty & Leaderboard

## ✨ Yang Baru Ditambahkan:

### 1. **Difficulty Selection** 🎚️

Game sekarang punya 3 tingkat kesulitan:

#### 🟢 MUDAH (Easy)

- **Durasi**: 30 detik
- **Ekspresi**: 2 ekspresi (Happy & Sad)
- **Cooldown**: 1.5 detik
- **Cocok untuk**: Pemula yang baru mencoba

#### 🟡 SEDANG (Medium)

- **Durasi**: 20 detik
- **Ekspresi**: 4 ekspresi (Happy, Sad, Surprised, Neutral)
- **Cooldown**: 1.0 detik
- **Cocok untuk**: Player biasa

#### 🔴 SULIT (Hard)

- **Durasi**: 15 detik
- **Ekspresi**: 4 ekspresi (Happy, Sad, Surprised, Neutral)
- **Cooldown**: 0.5 detik (super cepat!)
- **Cocok untuk**: Expert yang ingin challenge!

### 2. **Leaderboard System** 🏆

- **Top 10** high scores per difficulty
- **Auto-save** ke file `leaderboard.json`
- Tampilkan:
  - Rank (#1, #2, #3 dengan warna khusus!)
  - Nama player
  - Score
  - Tanggal & waktu

## 🎮 Cara Main:

### Di Menu Difficulty:

- **↑↓**: Pilih kesulitan
- **SPASI**: Mulai game
- **L**: Lihat leaderboard
- **ESC**: Keluar

### Di Leaderboard:

- **1**: Lihat leaderboard Easy
- **2**: Lihat leaderboard Medium
- **3**: Lihat leaderboard Hard
- **ESC**: Kembali ke menu

### Di Results:

- **SPASI**: Main lagi
- **ESC**: Keluar

## 📁 File Structure:

```
Expressify/
├── src/
│   ├── leaderboard_manager.py   # ← NEW! Manage leaderboard
│   ├── game_logic.py            # ← UPDATED! Support difficulty
│   ├── ui_manager.py            # ← UPDATED! New screens
│   └── main.py                  # ← UPDATED! Game flow
└── leaderboard.json             # ← AUTO-GENERATED! Score data
```

## 🔧 Technical Details:

### Difficulty Settings

```python
"easy": {
    "duration": 30,
    "expressions": ["happy", "sad"],
    "cooldown": 1.5
}
```

### Leaderboard Data Format

```json
{
  "easy": [
    {
      "name": "Player",
      "score": 15,
      "date": "2025-11-12 14:30"
    }
  ],
  "medium": [...],
  "hard": [...]
}
```

## 💡 Future Improvements:

- [ ] Input nama player (sekarang default "Player")
- [ ] Online leaderboard (sync dengan server)
- [ ] Achievement badges
- [ ] Challenge mode (specific expression sequences)
- [ ] Multiplayer leaderboard
- [ ] Export/share scores

## 🐛 Known Issues:

- Player name belum bisa custom (default "Player")
- Leaderboard file di root project (bisa pindah ke data folder)

## 📊 How Scoring Works:

Score = Jumlah ekspresi benar yang berhasil ditampilkan

**Example:**

- Easy (30s): Max ~20 poin
- Medium (20s): Max ~20 poin
- Hard (15s): Max ~30 poin (karena cooldown lebih cepat!)

---

**Selamat Bermain! 🎉**

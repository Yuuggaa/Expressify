#!/bin/bash

echo "========================================"
echo "   EXPRESSIFY - Setup Environment"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 tidak ditemukan! Silakan install Python3 terlebih dahulu."
    exit 1
fi

echo "[1/4] Membuat virtual environment..."
python3 -m venv venv

echo "[2/4] Mengaktifkan virtual environment..."
source venv/bin/activate

echo "[3/4] Mengupgrade pip..."
python -m pip install --upgrade pip

echo "[4/4] Menginstall dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "   Setup Berhasil! 🎉"
echo "========================================"
echo ""
echo "Untuk menjalankan game:"
echo "1. Aktifkan environment: source venv/bin/activate"
echo "2. Jalankan game: python src/main.py"
echo ""

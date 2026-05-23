#!/bin/bash

ROOT="$(pwd)"
OUT="$ROOT/dist"
SRC="$ROOT"

echo "============================================================"
echo "              ARDUINOWAVEHANDLER BUILD TOOL                 "
echo "============================================================"

echo "[INFO] Checking Python..."
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 not found"
    exit 1
fi

mkdir -p "$OUT"

echo "[INFO] Cleaning old build..."
rm -rf "$OUT"/*
mkdir -p "$OUT"

echo "[INFO] Running syntax check..."

find "$SRC" -name "*.py" | while read file
do
    python3 -m py_compile "$file"
    if [ $? -ne 0 ]; then
        echo "[FAIL] Syntax error in $file"
        exit 1
    fi
done

echo "[INFO] Generating file index..."
INDEX="$OUT/index.txt"

echo "NORTHBRIDGE SYSTEMS PACKAGE" > "$INDEX"
echo "BUILD TIME: $(date)" >> "$INDEX"
echo "==============================" >> "$INDEX"

find "$SRC" -name "*.py" | while read file
do
    clean="${file#$SRC/}"
    echo "$clean" >> "$INDEX"
done

echo "[INFO] Copying files..."
find "$SRC" -name "*.py" -exec cp --parents {} "$OUT" \;

echo "[INFO] Build complete"
echo "Output: $OUT"

echo "============================================================"
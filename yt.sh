#!/usr/bin/env bash
# Скачивает YouTube URLs из файла, конвертирует в MP3 и объединяет в один файл.
# Использование: ./yt_merge.sh urls.txt [output_dir] [output.mp3]

set -euo pipefail

URLS_FILE="${1:-urls.txt}"
OUT_DIR="${2:-downloads}"
FINAL_OUT="${3:-merged.mp3}"
PROXY="socks5://127.0.0.1:10808/"

if [[ ! -f "$URLS_FILE" ]]; then
    echo "Файл с URL не найден: $URLS_FILE"
    exit 1
fi

mkdir -p "$OUT_DIR"

echo "==> Скачивание и конвертация в MP3..."
yt-dlp \
    --proxy "$PROXY" \
    --extract-audio \
    --audio-format mp3 \
    --audio-quality 0 \
    --output "$OUT_DIR/%(autonumber)s - %(title)s.%(ext)s" \
    --no-playlist \
    --batch-file "$URLS_FILE"

echo "==> Создание списка файлов для ffmpeg..."
CONCAT_LIST=$(mktemp /tmp/ffmpeg_list.XXXXXX.txt)
while IFS= read -r -d '' f; do
    echo "file '$(realpath "$f")'" >> "$CONCAT_LIST"
done < <(find "$OUT_DIR" -maxdepth 1 -name "*.mp3" -print0 | sort -z)

COUNT=$(grep -c "^file" "$CONCAT_LIST" || true)
echo "==> Объединение $COUNT файлов в $FINAL_OUT..."
ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$FINAL_OUT"

rm -f "$CONCAT_LIST"
echo "==> Готово: $FINAL_OUT"

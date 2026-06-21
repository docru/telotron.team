#!/usr/bin/env bash
# Звук/ → Текст/ (только .txt; vtt/srt/json/tsv с тем же именем удаляются). Модель: small.
# ./transcribe.sh <файл_в_Звук> [модель]
# Первый раз: docker compose build

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

NAME="${1:?Укажи имя файла в папке Звук, например: test.mp3}"
MODEL="${2:-small}"

if [[ ! -f "Звук/$NAME" ]]; then
  echo "Файл не найден: Звук/$NAME" >&2
  exit 1
fi

docker compose run --rm transcribe \
  "/in/$NAME" \
  --language ru \
  --model "$MODEL" \
  --output_dir /out

echo "Готово. Смотри папку Текст/ (базовое имя совпадает с файлом в Звук)."

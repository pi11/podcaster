#!/bin/bash

SCRIPT_NAME=$(basename "$0")

# Функция помощи
print_help() {
  echo "Использование: $SCRIPT_NAME <url> <channel_id>"
  echo
  echo "Скачивает видео как подкаст и публикует в указанный Telegram-канал."
  echo
  echo "Аргументы:"
  echo "  <url>         Ссылка на видео (например, https://www.youtube.com/watch?v=...)"
  echo "  <channel_id>  ID Telegram-канала (например, 4)"
  echo
  echo "Пример:"
  echo "  $SCRIPT_NAME https://www.youtube.com/watch?v=rShyYcdWeK0 4"
}

# Проверка аргументов
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  print_help
  exit 0
fi

if [[ $# -ne 2 ]]; then
  echo "Ошибка: требуется 2 аргумента."
  print_help
  exit 1
fi

URL="$1"
CHANNEL_ID="$2"

# Выполнение команды
poetry run podcast download --url="$URL" --tg-channel "$CHANNEL_ID"


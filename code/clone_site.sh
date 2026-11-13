#!/bin/bash
# Безопасный клон сайта для правок html (без 860 МБ видео в рабочей папке).
set -e; D=${1:-/home/claude/ortho-guide}
git clone -q --no-checkout https://github.com/pravopomosh-rf/ortho-guide "$D"; cd "$D"
git sparse-checkout set --no-cone '/*.html' '/*.css' '/*.js' '/ops/' '/qr/' '/*.json' '/*.txt' '/.github/'
git checkout -q main
curl -fsSL https://raw.githubusercontent.com/pravopomosh-rf/ortho-guide/tts-data/code/pre-push -o .git/hooks/pre-push && chmod +x .git/hooks/pre-push
echo "ok: файлов в индексе $(git ls-files | wc -l), hook установлен"

#!/bin/bash
# Запуск плеера: Django (waitress) + nginx + туннель Cloudflare

NGINX_DIR="/c/nginx-1.31.6"

cd "$(dirname "$0")" || exit 1
source ../.venv/Scripts/activate || { echo "Не найдено окружение ../.venv"; exit 1; }

STARTED_NGINX=0
WAITRESS_PID=""

cleanup() {
    echo
    echo "Останавливаю всё..."
    [ -n "$WAITRESS_PID" ] && kill "$WAITRESS_PID" 2>/dev/null
    if [ "$STARTED_NGINX" = 1 ]; then
        (cd "$NGINX_DIR" && ./nginx.exe -s stop)
    fi
    exit 0
}
trap cleanup INT TERM

echo "1/3 Запускаю Django (waitress)..."
waitress-serve --threads=8 --listen=127.0.0.1:8000 music_player.wsgi:application &
WAITRESS_PID=$!
sleep 2

echo "2/3 Запускаю nginx..."
if tasklist | grep -qi nginx.exe; then
    echo "nginx уже запущен, пропускаю."
else
    (cd "$NGINX_DIR" && ./nginx.exe &)
    STARTED_NGINX=1
fi
sleep 1


CLOUDFLARED="/c/Program Files (x86)/cloudflared/cloudflared.exe"

echo "3/3 Запускаю туннель. Ссылку ищите в рамке ниже (https://...trycloudflare.com)"
"$CLOUDFLARED" tunnel --protocol http2 --url http://localhost:8888 --http-host-header music.localhost

cleanup
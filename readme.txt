docker build -t imap_tg_bot .
docker run --rm -e TZ=Europe/Moscow imap_tg_bot

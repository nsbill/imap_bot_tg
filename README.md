# Пересылка почты по протоколу IMAP на Python в Telegram
Aleksandr Kirilyuk alx@nsbill.ru

https://eax.me/python-imap/ - ориг статья 

1. cp config.ini.git config.ini и правим файл под себя
```
[DEFAULT]
SERVER = imap.yandex.ru -- Server IMAP в данном случае yandex  
LOGIN = login@yandex.ru -- email
PWHASH = f9s35d718c4dbse81acc5f80s93fae1011635e07 -- pwhash
```
Как получить PWHASH

```
# >>> import hashlib        
# >>> hashlib.sha1(b"qwerty").hexdigest()
```
```
PASSWORD = password123 -- пароль от почтового ящика
PAUSE_TIME = 240 -- время с какой переодичностью проверять почту
FOLDER = INFO -- папка откуда забирать почту

[BOT]
TOKEN = 123449:AAFBGbWkO313Oh-5SCHHSRo4Ycn8sWZcilM -- токен бота TG
UserID = ['1111111','2222222'] -- ID пользователей кому будут приходить сообщения
```
2. Сборка и запуск
```
docker-compose build
docker-compose up -d
```
3. Письма удаляются с указанной папки на сервере и сохр. в /script/arhive/date 


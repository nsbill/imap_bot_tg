import imaplib
import hashlib
import getpass
import email
import email.message
import time
import os.path
import subprocess
import re
import sys
import base64
import telebot
import datetime
import configparser

config = configparser.ConfigParser()
conf = config.read("config.ini")
print(conf)

server = (config["DEFAULT"]["SERVER"])
login = (config["DEFAULT"]["LOGIN"])
pause_time = int((config["DEFAULT"]["PAUSE_TIME"]))
# >>> import hashlib
# >>> hashlib.sha1(b"qwerty").hexdigest()
pwhash = (config["DEFAULT"]["PWHASH"])
#password = getpass.getpass("IMAP Password: ")
password = (config["DEFAULT"]["PASSWORD"])

if hashlib.sha1(bytearray(password, 'utf-8')).hexdigest() != pwhash:
  print("Invalid password", file = sys.stderr)
  sys.exit(1)

def main_loop_proc():
    print("Connecting to {}...".format(server))
    imap = imaplib.IMAP4_SSL(server)
    print("Connected! Logging in as {}...".format(login));
    imap.login(login, password)
    print("Logged in! Listing messages...");
    status, select_data = imap.select((config["DEFAULT"]["FOLDER"]))
    nmessages = select_data[0].decode('utf-8')
    status, search_data = imap.search(None, 'ALL')
    if search_data == [b'']:
        imap.expunge()
        imap.logout()
        return search_data

    for msg_id in search_data[0].split():
        msg_id_str = msg_id.decode('utf-8')
        print("Fetching message {} of {}".format(msg_id_str,nmessages))
        status, msg_data = imap.fetch(msg_id, '(RFC822)')
        msg_raw = msg_data[0][1]
        status, msg_data = imap.fetch(select_data[0],'(UID BODY[TEXT])')

        msg = email.message_from_bytes(msg_raw,_class = email.message.EmailMessage)
        msg_subject = msg.get('Subject')
        if '=?utf-8?B?' == msg_subject[0:10]:
            msg_subject = msg_subject[10:-2]
            msg_subject_bs64 = base64.b64decode(msg_subject+'=')
            msg_subject = str(msg_subject_bs64, 'utf-8')

# парсим body от tags
        s = str(msg_data[0][1], 'utf-8')
        s = s.replace('<br />', '\n')
        p = re.compile(r'<.*?>')
        msg_body = p.sub('', s)

#        with open('asdzxc', 'w') as f:
#            f.write(message_send)

        # mailing_list = msg.get('X-Mailing-List', 'undefined')
        mailing_list = msg.get('List-Id', 'undefined')
        mailing_list = re.sub('^(?s).*?<([^>]+?)(?:\\..*?)>.*$',
                              '\\1', mailing_list)
        timestamp = email.utils.parsedate_tz(msg['Date'])
        year, month, day, hour, minute, second = timestamp[:6]
        msg_hash = hashlib.sha256(msg_raw).hexdigest()[:16]
        fname = ("./archive/{7}/{0:04}/{0:04}-{1:02}-{2:02}/" +
                 "{0:04}-{1:02}-{2:02}-{3:02}-{4:02}-{5:02}" +
                 "-{6}.txt").format(
            year, month, day, hour, minute, second,
            msg_hash, mailing_list)
        dirname = os.path.dirname(fname)
        print("Saving message {} to file {}".format(msg_id_str, fname))
        subprocess.call('mkdir -p {}'.format(dirname), shell=True)
        with open(fname, 'wb') as f:
            f.write(msg_raw)
        imap.store(msg_id, '+FLAGS', '\\Deleted')
        msg_send = '<b>'+ str(msg_subject) +'</b>\n\n' + msg_body
    imap.expunge()
    imap.logout()
    return msg_send

def tel_bot(msg_send):
    if msg_send != [b'']:
        print(msg_send)
        bot = telebot.TeleBot(config["BOT"]["TOKEN"])
        UserID=[(config["BOT"]["UserID"])]
        for uid in UserID:
            bot.send_message(str(uid), parse_mode='HTML', text=msg_send)
    return print('Done')

while True:
    try:
        now = datetime.datetime.now()
        print('Date: ' + str(now))
        msg_send = main_loop_proc()
        tel_bot(msg_send)
    except Exception as e:
        print("ERROR:" + str(e))
    print("Sleeping {} seconds...".format(pause_time))
    time.sleep(pause_time)

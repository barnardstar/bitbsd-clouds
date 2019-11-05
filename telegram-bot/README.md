### How to spin up your own Telegram bot ###

You can control Telegram in two ways:

[Using bots], so you can interract with users and build apps inside messenger 

[Using API] and controlling whole account (control contacts, numbers and do everything you can do on your mobile app)

[Using bots]:https://github.com/bitcoin-software/Telethon
[Using API]:https://github.com/bitcoin-software/python-telegram-bot


![bf](https://i.imgur.com/3OYZZGN.png "@BotFather")

After we have a token, let's create a jail where bot will live

`$ curl https://bitclouds.sh/create/rootshell`

`$ curl https://bitclouds.sh/status/praecipua-1`
```
{
  "app_port": 52113, 
  "hours_left": 4, 
  "ip": "bitbsd.org", 
  "ssh_port": 62742, 
  "ssh_pwd": "9a09b27f355cb297", 
  "ssh_usr": "satoshi", 
  "status": "subscribed"
}
```

`$ ssh satoshi@bitbsd.org -p62742`

`[root@praecipua-1]$ python3.7 -m pip install python-telegram-bot`

Here's [examples], but to demonstrate a minimum app create a file

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep


update_id = None


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('1069585330:AAGKZX_xH6NXFgDcErsDTGsx92nK0nUoHpQ')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)


if __name__ == '__main__':
    main()
```

[examples]:https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples

Finally, launch it

`$ python3.7 bot.py`

![bot](https://i.imgur.com/NBJiFJl.png "@CloudBot")

To control your Telegram account, [use Telethon]

[use Telethon]:https://docs.telethon.dev/en/latest/

`[root@praecipua-1]$ python3.7 -m pip install telethon`

```python
from telethon.sync import TelegramClient, events

with TelegramClient('name', API_ID, API_HASH) as client:
   client.send_message('me', 'Hello, myself!')
   print(client.download_profile_photo('me'))

   @client.on(events.NewMessage(pattern='(?i).*Hello'))
   async def handler(event):
      await event.reply('Hey!')

   client.run_until_disconnected()

```

`[root@praecipua-1]$ python3.7 telegram_api.py`

Code above will reply to your contacts with message

**Attention! For security purposes this jail has no normal internet connection, while you still can access internet via proxy socks5://192.168.0.199:9050 or http://192.168.0.199:8123**

Or you can also simply execute any command with torsocks prefix

`torsocks ssh user@someserver.com`

`[satoshi@praecipua-1]$ torsocks ssh rmtusr@myserver.domain.com`

However, some programs will work as usual, because proxy enviroment variable is set in ~/.cshrc to use HTTP TORed proxy
This means that your bot is completely anonymous and communicates over TOR with Telegram servers ;)

import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
"""Merhaba,
Ben gruplarınız için geliştirilmiş özel tag botuyum! 
*𝐇𝐄𝐘! ,*
┏━━━━━━━━━━━━━━━━
┣ ₪ *BENİ BİR GRUBA EKLE* `
┣ ₪ GEREKLİ YETKİLERİ VERİP /RELOAD KOMUTUNU KULLAN
┗━━━━━━━━━━━━━━━━━
 
  Burdan /help **DESTEK ALABİLİRSİNİZ**
 [❤](https://telegra.ph/file/2fa3a833f3ccc1d98dba1.jpg),
""",
    link_preview=False,
    buttons=(
       [
        Button.url(' Grup', 'https://t.me/SamataSohbet'),
        Button.url('Sahip', 'https://t.me/Dnztrmn')
    ],
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "COMMANDS:/mentionall,/cancel. excample /mentionall hi add me your groups iam best tagger pro bot"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url(' Grup', 'https://t.me/SamataSohbet'),
        Button.url('Sahip', 'https://t.me/Dnztrmn')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/etiketle ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__Bu komut gruplarda ve kanallarda kullanılabilir!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Yalnızca yöneticiler etiketleme işlemi başlatabilir!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Bana lütfen hangi konuda etiketleme islemi başlatıcağımı belirle!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__Eski mesajlar için üyelerden bahsedemem (Gruba eklenmeden önce gönderilen mesajlar)__")
  else:
    return await event.respond("__Bir mesajı yanıtlayın yada bana tüm kullanıcıları etiketlemem için bir metin belirtin!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/iptal$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__Devam eden islem yok...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__İşlem başarıyla bitirildi.__')

print(">> Bot başlatıldı <<")
client.run_until_disconnected()

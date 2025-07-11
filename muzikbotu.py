from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputStream, AudioPiped
import yt_dlp
import asyncio
import os

API_ID = 22021596  # Buraya kendi API_ID
API_HASH = "cc93223b2aac85fabd09ab224d75afb9"
BOT_TOKEN = "7639669501:AAHIOXLLIUpPwKo1Sr91Wob1QhCt4eC9VZc"

app = Client("muzikbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
vc = PyTgCalls(app)

# YouTube'dan ses indir
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir():
        if file.startswith("music") and file.endswith(".webm") or file.endswith(".m4a") or file.endswith(".mp3"):
            return file

@app.on_message(filters.command("play"))
async def play(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("🎵 Lütfen bir şarkı linki gönderin.\nÖrnek: /play [YouTube URL]")
    url = msg.command[1]
    await msg.reply("🔎 Müzik indiriliyor...")
    audio_file = download_audio(url)
    await vc.join_group_call(
        msg.chat.id,
        AudioPiped(audio_file),
        stream_type=InputStream().local_stream
    )
    await msg.reply("✅ Müzik çalmaya başladı!")

@app.on_message(filters.command("stop"))
async def stop(_, msg):
    await vc.leave_group_call(msg.chat.id)
    await msg.reply("🛑 Müzik durduruldu.")

@vc.on_stream_end()
async def on_stream_end(_, update):
    try:
        os.remove("music.webm")
    except: pass

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("🎧 Müzik Botu aktif!\n/play [link] yazarak şarkı çalabilirsiniz.")

# Botu başlat
vc.start()
app.start()
print("Bot çalışıyor...")
idle()
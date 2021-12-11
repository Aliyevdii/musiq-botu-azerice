# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Menu", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Sil", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("siz __Anonim Adminsiniz__ !\n\n» admin hüquqlarından istifadəçi hesabına geri qayıdın.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Məndən istifadə etmək üçün aşağıdakı **icazələrə** malik **İnzibatçı** olmalıyam:\n\n» ❌ __Mesajları sil__\n» ❌ __İstifadəçi əlavə et__\n» ❌ __Video söhbəti idarə et__\n\nMəlumatlar * avtomatik olaraq sizdən sonra *yenilənilir**
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "tələb olunan icazə çatışmır:" + "\n\n» ❌ __Video söhbəti idarə et__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "lazımi icazə yoxdur:" + "\n\n» ❌ __Mesajları silin__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("tələb olunan icazə çatışmır:" + "\n\n» ❌ __İstifadəçilər əlavə edin__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **qrupda qadağa qoyulub** {m.chat.title}\n\n» **bu botdan istifadə etmək istəyirsinizsə, əvvəlcə istifadəçi robotunun qadağanını ləğv edin.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot qoşula bilmədi**\n\n**reason**: `{e}`")
                return
        else:
            try:
                user_id = (await user.get_me()).id
                link = await c.export_chat_invite_link(chat_id)
                if "+" in link:
                    link_hash = (link.replace("+", "")).split("t.me/")[1]
                    await ubot.join_chat(link_hash)
                await c.promote_member(chat_id, user_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot qoşula bilmədi**\n\n**səbəb**: `{e}`"
                )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **video yüklənir...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __only 720, 480, 360 allowed__ \n💡 **indi 720p-də video yayımlanır**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Trek növbəyə əlavə edildi »** `{pos}`\n\n🏷 **Ad:** [{mahnı adı}]({link})\n💭 **Çat:** `{chat_id}`\n🎧 **Müraciət edən:** {requester}",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit("🔄 **Səsliyə qoşulur...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"💡 **Video yayımı başladı.**\n\n🏷 **Ad:** [{mahnı adı}]({link})\n💭 **Çat:** `{chat_id}`\n💡 **Status:** `Oynanır`\n🎧 **Sorğu ilə:** {requester}",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» **video faylına** cavab verin və ya **axtarmaq üçün nəsə verin.**"
                )
            else:
                loser = await c.send_message(chat_id, "🔎 **Axtarılır...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **Heç bir nəticə tapılmadı.**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ youtube-dl problemləri aşkarlandı\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"💡 **Trek növbəyə əlavə edildi »** `{pos}`\n\n🏷 **Ad:** [{mahnı adı}]({url})\n💭 **Çat:** `{chat_id}`\n🎧 ** Müraciət edən:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await loser.edit("🔄 **Səsliyə qoşulur..**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💡 **Video yayımı başladı.**\n\n🏷 **Ad:** [{mahnı adı}]({url})\n💭 **Çat:** `{chat_id}`\n💡 **Status:** `Oynanır`\n🎧 **Sorğu ilə:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 xəta: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» **video faylına** cavab verin və ya **axtarmaq üçün nəsə verin.**"
            )
        else:
            loser = await c.send_message(chat_id, "🔎 **Axtarılır...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **Heç bir nəticə tapılmadı.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ youtube-dl problemləri aşkarlandı\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"💡 **Trek növbəyə əlavə edildi »** `{pos}`\n\n🏷 **Ad:** [{mahnı adı}]({url})\n💭 **Çat:** `{chat_id}`\n🎧 **Tərəfindən sorğu:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await loser.edit("🔄 **Səsliyə qoşulur...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"💡 **Video yayımı başladı.**\n\n🏷 **Ad:** [{mahnı adı}]({url})\n💭 **Çat:** `{chat_id}`\n💡 **Status:** `Oynanır`\n🎧 **Sorğu ilə:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 xəta: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Menu", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Sil", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("siz __Anonim Adminsiniz__ !\n\n» admin hüquqlarından istifadəçi hesabına geri qayıdın.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için, bei'ye ihtiyacım var**Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Add users__\n» ❌ __Manage video chat__\n\nData is **updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __Video söhbəti idarə edin__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "missing required permission:" + "\n\n» ❌ __Mesajları silin__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("missing required permission:" + "\n\n» ❌ __İstifadəçilər əlavə edin__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **qrupda qadağa qoyulub** {m.chat.title}\n\n» **bu botdan istifadə etmək istəyirsinizsə, əvvəlcə istifadəçi robotunun qadağanını ləğv edin.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot failed to join**\n\n**reason**: `{e}`")
                return
        else:
            try:
                user_id = (await user.get_me()).id
                link = await c.export_chat_invite_link(chat_id)
                if "+" in link:
                    link_hash = (link.replace("+", "")).split("t.me/")[1]
                    await ubot.join_chat(link_hash)
                await c.promote_member(chat_id, user_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» axın etmək üçün mənə canlı link/m3u8 url/youtube linki verin.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **emal axını...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **indi 720p-də video yayımlanır**"
                )
            loser = await c.send_message(chat_id, "🔄 **emal axını...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ youtube-dl problemləri aşkarlandı\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Trek növbəyə əlavə edildi »** `{pos}`\n\n💭 **Söhbət:** `{chat_id}`\n🎧 **Soruş::** {requester}",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **Səsliyə qoşulur...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[Canlı video]({link}) yayımı başladı.**\n\n💭 **Çat:** `{chat_id}`\n💡 **Status:** `Oynanır`\n🎧 **Soruş edən::** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 xəta: `{ep}`")

# Copyright (C) 2021 By VeezMusicProject

from driver.queues import QUEUE
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""👻 **Xoş gəldiniz [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Telegramda səsli söhbətdə musiqi ifa etmək və video yayımı üçün kodlaşdırılmışam!**

💡 **»Mənim həddindən çox əmrim var. Əmrlərə baxmaq üçün 📚 Əmrlər 📚 düyməsinə vur!**

🔖 **Əgər botu qrupuna qoşmaq istəyirsənsə'sə Quraşdırılma ❓ baxa bilərsən**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Məni Qrupunuza əlavə edin ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❔ Queaşdırma ❔", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 Əmirlər", callback_data="cbcmds"),
                    InlineKeyboardButton("❤ 𝙾𝚠𝚖𝚎𝚛", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 Rəsmi Qrup", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Rəsmi Kanal", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 𝚂𝚞𝚙𝚙𝚘𝚛𝚝 ", url="https://t.me/NEXUS_MMC"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **Necə Quraşdırılır:**

1.) **Əvvəlcə məni qrupunuza əlavə edin.**
2.) **Sonra məni administrator kimi yüksəldin və Anonim Admindən başqa bütün icazələri verin.**
3.) **Məni təbliğ etdikdən sonra admin məlumatlarını yeniləmək üçün qrupa /reload yazın.**
3.) **Əlavə et @{ASSISTANT_NAME} qrupunuza daxil olun və ya onu dəvət etmək üçün /userbotjoin yazın.**
4.) **Video/musiqi oxutmağa başlamazdan əvvəl video çatı yandırın.**
5.) **Bəzən /reload əmrindən istifadə edərək botun yenidən yüklənməsi sizə kömək edə bilər.
📌 **Assistant səsli söhbətə qoşulmayıbsa, səsli söhbətin aktiv olub olmadığına əmin olun və ya /leave yazın, sonra yenidən /add yazın.**
💡 **Bu bot haqqında əlavə suallarınız varsa, onu buradakı dəstək söhbətimdə deyə bilərsiniz: @{GROUP_SUPPORT}**

⚡ __𝙽𝚎𝚡𝚞𝚜 𝚋𝚘𝚝 {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Qeri qayıt", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Salam [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**

» **Mənim əmrlərimin siyahısına baxmaq və izahlarını oxumaq üçün aşağıdakı butona basın !**

⚡ __𝙽𝚎𝚡𝚞𝚜 𝚋𝚘𝚝 {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 Admin əmirləri", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 Sudo əmirləri", callback_data="cbsudo"),
                ],[
                    InlineKeyboardButton("📚 Sadə əmirlər", callback_data="cbbasic")
                ],[
                    InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbstart")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 Sadə əmrlər bunlardır::

» /mplay (musiqi adı) - Səsli söhbətdə musiqi oxudur
» /stream (link) - Səslidə canlı açılır
» /vplay (video adı) - Səslidə video açır
» /vstream - Səslidə canlı radio açır
» /playlist - Playlisti göstərir
» /video (ad) - Videonu youtubedən yükləyir
» /song (ad) - Musiqini youtubedən yükləyir
» /lyric (musiqi adı) - Musiqi sözlərini tapır
» /search (ad) - Axtaris edir

» /ping - Ping statusu göstərir
» /uptime - İşləmə vaxtını göstərir
» /alive - Botun aktiv olduğunu yoxlayın

⚡️ __𝙽𝚎𝚡𝚞𝚜 𝚋𝚘𝚝 {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 Admin əmrləri::

» /pause - Pause verir
» /resume - Davam edir
» /skip - Növbəti musiqiyə keçir
» /stop - Musiqini bitirir
» /vmute - Asistanı səssizə alır
» /vunmute - Asistanın səsini açır
» /volume 1-200 - Səs səviyyəsi qeyd edin
» /reload - Admin listi yeniləyin
» /userbotjoin - Asistanı qrupa dəvət edin
» /userbotleave - Asistanı qrupdan çıxarın

⚡️ __𝙽𝚎𝚡𝚞𝚜 𝚋𝚘𝚝 {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )

@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 Sudo əmrləri:

» /rmw - Raw faylları silin
» /rmd - Datanı təmizləyin
» /sysinfo - Sistemə baxın
» /restart - Botu yenidən başladın
» /leaveall - Asistantı bütün qruplardan çıxarın

⚡ __𝙽𝚎𝚡𝚞𝚜 𝚋𝚘𝚝 {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("siz Anonim Adminsiniz !\n\n» admin hüquqlarından istifadəçi hesabına qayıdın.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 yalnız səsli söhbətləri idarə etmək icazəsi olan admin bu düyməyə toxuna bilər!", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **settings of** {query.message.chat.title}\n\n⏸ : yayımı dayandırın\n▶️ : yayımı davam etdirin\n🔇 : istifadəçi robotunu susdurun\n🔊 : istifadəçi robotunun səsini söndürün\n⏹ : yayımı dayandırın",
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("⏹", callback_data="cbstop"),
                      InlineKeyboardButton("⏸", callback_data="cbpause"),
                      InlineKeyboardButton("▶️", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton("🔇", callback_data="cbmute"),
                      InlineKeyboardButton("🔊", callback_data="cbunmute"),
                  ],[
                      InlineKeyboardButton("🗑 Sil", callback_data="cls")],
                  ]
             ),
         )
    else:
        await query.answer("❌ hazırda heç nə yayımlanmır", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 yalnız bu düyməyə toxuna bilən səsli söhbətləri idarə etmək icazəsi olan admin !", show_alert=True)
    await query.message.delete()

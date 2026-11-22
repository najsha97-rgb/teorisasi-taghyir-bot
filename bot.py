# -*- coding: utf-8 -*-
"""
BOT TELEGRAM TANẒĪR AL-TAGHYĪR (تنظير التغيير)
Membina Teori Integrasi Perubahan Politik Islam
Karya: Asy-Syeikh Muhammad Ahmad ar-Rasyid (رحمه الله)
Siri Rujukan Gerakan & Fiqh Siyasah Perubahan
Versi: 1.1 (208 Topik Kanonikal, 120 Mutiara Kata, 131 Nota Kaki & Carian Pintar)
"""

import os
import sys
import json
import time
import re
import html
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Bot Tanẓīr al-Taghyīr Telegram beroperasi 24/7.".encode("utf-8"))

    def log_message(self, format, *args):
        return

def start_health_server():
    port = int(os.environ.get("PORT", 0))
    if port:
        server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        print(f"Health-check HTTP Server aktif pada port {port}.")

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DATA_PATH = os.path.join(BASE_DIR, "tanzir_data.json")
QUOTES_PATH = os.path.join(BASE_DIR, "tanzir_quotes.json")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN_TANZIR", "")

if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f)
            if not BOT_TOKEN and cfg.get("bot_token"):
                BOT_TOKEN = cfg.get("bot_token").strip()
    except Exception as e:
        print(f"Ralat membaca config.json: {e}")

if not os.path.exists(DATA_PATH):
    print(f"Ralat kritikal: Fail data {DATA_PATH} tidak wujud!")
    sys.exit(1)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    RAW_DATA = json.load(f)

CHAPTERS = RAW_DATA.get("chapters", [])
METADATA = RAW_DATA.get("metadata", {})

HIKMAH_DATA = []
if os.path.exists(QUOTES_PATH):
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        HIKMAH_DATA = json.load(f)
elif "quotes" in RAW_DATA:
    HIKMAH_DATA = RAW_DATA["quotes"]

TOTAL_SUBTOPICS = sum(len(c.get("subtopics", [])) for c in CHAPTERS)
TOTAL_QUOTES = len(HIKMAH_DATA) if HIKMAH_DATA else 120
PWA_PRIMARY_URL = "https://najsha97-rgb.github.io/teorisasi-taghyir/"
PWA_BACKUP_URL = "https://teorisasi-taghyir.pages.dev/"

print(f"Berjaya memuatkan {len(CHAPTERS)} Bahagian ({TOTAL_SUBTOPICS} Topik) & {TOTAL_QUOTES} Mutiara Kata Tanẓīr al-Taghyīr.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def to_tg_html(text):
    """Pastikan simbol ampersand (&) yang tidak berformat die-escape kepada &amp; untuk Telegram."""
    if not text:
        return ""
    return re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+);)', '&amp;', text)

def call_telegram_api(method, payload):
    if not BOT_TOKEN or "MASUKKAN" in BOT_TOKEN:
        return None
    url = f"{TELEGRAM_API_URL}/{method}"
    try:
        r = requests.post(url, json=payload, timeout=25)
        return r.json()
    except Exception as e:
        print(f"Ralat sambungan API ({method}): {e}")
        return None

def edit_or_send(chat_id, message_id, text, reply_markup=None):
    safe_text = to_tg_html(text)
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": safe_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    res = call_telegram_api("editMessageText", payload)
    if not res or not res.get("ok"):
        payload_send = {
            "chat_id": chat_id,
            "text": safe_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        if reply_markup:
            payload_send["reply_markup"] = reply_markup
        return call_telegram_api("sendMessage", payload_send)
    return res

def send_msg(chat_id, text, reply_markup=None):
    safe_text = to_tg_html(text)
    payload = {
        "chat_id": chat_id,
        "text": safe_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return call_telegram_api("sendMessage", payload)

def get_main_menu_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "🎨 Epigraf & Kulit Buku", "callback_data": "ch_0"},
                {"text": "📌 Mukadimah: 9 Faktor Perubahan", "callback_data": "ch_1"}
            ],
            [
                {"text": "📖 Baca Ikut Bab (6 Bab Lengkap)", "callback_data": "menu_chapters"},
                {"text": "🔍 Carian Kata Kunci", "callback_data": "menu_search_info"}
            ],
            [
                {"text": f"💎 {TOTAL_QUOTES} Mutiara Fiqh Siyasah", "callback_data": "hikmah_random"}
            ],
            [
                {"text": "🌍 Ummah Fadhilah & Kuasa Nasional", "callback_data": "menu_peradaban"}
            ],
            [
                {"text": "🧭 Buka Web PWA Tanẓīr al-Taghyīr 🌐", "url": PWA_PRIMARY_URL}
            ],
            [
                {"text": "🔄 Refresh Menu Utama", "callback_data": "menu_main"}
            ]
        ]
    }

def handle_start(chat_id, message_id=None):
    welcome_text = (
        "<b>🌿 Selamat Datang ke Bot Tanẓīr al-Taghyīr (تنظير التغيير)</b>\n"
        "<i>Membina Teori Integrasi Perubahan Politik Islam</i>\n"
        "<b>Karya:</b> Asy-Syeikh Muhammad Ahmad ar-Rasyid <i>rahimahullah</i>\n\n"
        "Aplikasi bot pintar ini menyediakan capaian komprehensif kepada:\n"
        f"• <b>11 Bahagian Kanonikal</b> (Epigraf, Mukadimah, 6 Bab Utama, Khatimah, Epilog &amp; Sumbangan Peradaban)\n"
        f"• <b>{TOTAL_SUBTOPICS} Topik Lengkap</b> semuka demi muka naskhah Arab\n"
        f"• <b>{TOTAL_QUOTES} Mutiara Hikmah &amp; Fiqh Siyasah Syar'iyyah</b>\n"
        "• <b>Rujukan Nota Kaki Ilmiah</b> &amp; Rujukan Silang Kitab Siasah\n"
        "• Enjin carian pintar teks penuh &amp; ringkasan eksekutif\n\n"
        "Sila pilih menu navigasi di bawah atau taip apa-apa kata kunci untuk carian pantas:"
    )
    kb = get_main_menu_keyboard()
    if message_id:
        edit_or_send(chat_id, message_id, welcome_text, kb)
    else:
        send_msg(chat_id, welcome_text, kb)

def handle_help(chat_id, message_id=None):
    help_text = (
        "<b>🧭 PANDUAN PENGGUNAAN BOT TANẒĪR AL-TAGHYĪR</b>\n\n"
        "Anda boleh berinteraksi dengan bot ini melalui butang menu atau arahan teks berikut:\n\n"
        "<b>📌 Arahan Pintas:</b>\n"
        "• <code>/start</code> atau <code>/menu</code> — Paparkan Menu Utama\n"
        "• <code>/bab</code> — Senarai 6 Bab Utama &amp; Bahagian Khas\n"
        "• <code>/hikmah</code> — Paparan Mutiara Hikmah Fiqh Siyasah secara rawak\n"
        "• <code>/peradaban</code> — Ringkasan Doktrin Ummah Fadhilah &amp; Kuasa Nasional\n"
        "• <code>/cari &lt;kata kunci&gt;</code> — Cari topik atau mutiara hikmah\n"
        "• <code>/help</code> — Bantuan penggunaan bot\n\n"
        "<b>🔍 Carian Terus:</b>\n"
        "Anda boleh menaip apa-apa perkataan terus ke dalam ruang bual ini (contoh: <code>sunnatullah</code>, <code>pemuda</code>, <code>Turki</code>, <code>Gaza</code>, dll) dan bot akan menyenaraikan padanan topik yang relevan secara automatik."
    )
    kb = {"inline_keyboard": [[{"text": "« Kembali ke Menu Utama", "callback_data": "menu_main"}]]}
    if message_id:
        edit_or_send(chat_id, message_id, help_text, kb)
    else:
        send_msg(chat_id, help_text, kb)

def handle_chapters_menu(chat_id, message_id):
    keyboard = [
        [
            {"text": "Bab 1: Logik Fiqh Perubahan", "callback_data": "ch_2"},
            {"text": "Bab 2: Pemuda Penekan", "callback_data": "ch_3"}
        ],
        [
            {"text": "Bab 3: Syarat Empirikal", "callback_data": "ch_4"},
            {"text": "Bab 4: Pergerakan Hidup", "callback_data": "ch_5"}
        ],
        [
            {"text": "Bab 5: Mukjizat Pemuda", "callback_data": "ch_6"},
            {"text": "Bab 6: Rumusan Teori", "callback_data": "ch_7"}
        ],
        [
            {"text": "Khatimah (Wasiat Penutup)", "callback_data": "ch_8"},
            {"text": "Epilog Penterjemah", "callback_data": "ch_9"}
        ],
        [
            {"text": "« Kembali ke Menu Utama", "callback_data": "menu_main"}
        ]
    ]
    
    text = (
        "<b>📖 SENARAI BAB TANẒĪR AL-TAGHYĪR</b>\n\n"
        "Pilih bab yang ingin anda telaah untuk paparan intisari ilmiah dan pecahan topik terperinci:"
    )
    if message_id:
        edit_or_send(chat_id, message_id, text, {"inline_keyboard": keyboard})
    else:
        send_msg(chat_id, text, {"inline_keyboard": keyboard})

def handle_chapter_view(chat_id, message_id, ch_idx):
    if ch_idx < 0 or ch_idx >= len(CHAPTERS):
        handle_start(chat_id, message_id)
        return
    ch = CHAPTERS[ch_idx]
    
    title_ar_str = f"\n<i>{html.escape(ch.get('title_ar', ''))}</i>" if ch.get('title_ar') else ""
    summary_preview = ""
    if ch.get("summary"):
        clean_sum = re.sub(r'#+\s*', '', ch["summary"])
        clean_sum = re.sub(r'\*+', '', clean_sum)
        clean_sum = re.sub(r'<[^>]+>', '', clean_sum)
        summary_preview = f"\n\n<b>📝 Intisari Bab:</b>\n{html.escape(clean_sum[:450])}..."
    
    text = (
        f"<b>📌 {html.escape(ch['number'])}: {html.escape(ch['title'])}</b>{title_ar_str}\n\n"
        f"• <b>Jumlah Subtajuk:</b> {ch.get('total_subtopics', len(ch.get('subtopics', [])))} Topik\n"
        f"• <b>Jumlah Perenggan:</b> {ch.get('total_paragraphs', 0)} Perenggan\n"
        f"• <b>Nota Kaki:</b> {len(ch.get('footnotes', []))} Rujukan"
        f"{summary_preview}"
    )
    
    kb = [
        [
            {"text": f"📑 Senarai {len(ch.get('subtopics', []))} Subtajuk", "callback_data": f"ch_subs_{ch_idx}_0"},
            {"text": "📖 Baca Dari Awal", "callback_data": f"read_full_{ch_idx}_0"}
        ],
        [
            {"text": "« Kembali ke Senarai Bab", "callback_data": "menu_chapters"},
            {"text": "🏠 Menu Utama", "callback_data": "menu_main"}
        ]
    ]
    edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})

def handle_subtopics_list(chat_id, message_id, ch_idx, page=0):
    ch = CHAPTERS[ch_idx]
    subs = ch.get("subtopics", [])
    per_page = 6
    total_pages = max(1, (len(subs) + per_page - 1) // per_page)
    page = max(0, min(page, total_pages - 1))
    start = page * per_page
    end = min(start + per_page, len(subs))
    
    text = (
        f"<b>📑 SUBTAJUK {html.escape(ch['number'])}</b> (Halaman {page+1}/{total_pages})\n\n"
        f"Pilih tajuk untuk membaca terjemahan ilmiah:"
    )
    
    kb = []
    for s_i in range(start, end):
        st = subs[s_i]
        st_title = st.get("title", f"Subtajuk {s_i+1}")
        st_title = re.sub(r'^#+\s*', '', st_title)
        st_title = re.sub(r'[*_`]', '', st_title)
        if len(st_title) > 35:
            st_title = st_title[:32] + "..."
        kb.append([{"text": f"🔹 {st_title}", "callback_data": f"view_sub_{ch_idx}_{s_i}"}])
    
    nav_row = []
    if page > 0:
        nav_row.append({"text": "⬅️ Sebelumnya", "callback_data": f"ch_subs_{ch_idx}_{page-1}"})
    if page < total_pages - 1:
        nav_row.append({"text": "Seterusnya ➡️", "callback_data": f"ch_subs_{ch_idx}_{page+1}"})
    if nav_row:
        kb.append(nav_row)
    
    kb.append([
        {"text": f"« Kembali ke {ch['number']}", "callback_data": f"ch_{ch_idx}"},
        {"text": "🏠 Menu Utama", "callback_data": "menu_main"}
    ])
    edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})

def handle_subtopic_view(chat_id, message_id, ch_idx, sub_idx):
    ch = CHAPTERS[ch_idx]
    subs = ch.get("subtopics", [])
    if sub_idx < 0 or sub_idx >= len(subs):
        handle_subtopics_list(chat_id, message_id, ch_idx, 0)
        return
    st = subs[sub_idx]
    
    paras = st.get("paragraphs", [])
    clean_paras = []
    for p in paras:
        p_clean = re.sub(r'<span[^>]*class=["\']fn-ref["\'][^>]*>(.*?)</span>', r'\1', p)
        p_clean = re.sub(r'<[^>]+>', '', p_clean)
        clean_paras.append(p_clean)
    
    para_text = "\n\n".join(clean_paras)
    if len(para_text) > 2800:
        para_text = para_text[:2750] + "...\n\n<i>[Teks dipendekkan untuk Telegram. Sila buka Web PWA untuk teks penuh].</i>"
    
    fn_text = ""
    if st.get("footnotes"):
        fn_items = []
        for fn in st["footnotes"][:5]:
            if isinstance(fn, dict):
                txt = fn.get("text", "")
                txt_clean = re.sub(r'<[^>]+>', '', txt)
                fn_id = fn.get("id", "")
                fn_items.append(f"[{fn_id}] {html.escape(txt_clean)}")
            else:
                txt_clean = re.sub(r'<[^>]+>', '', str(fn))
                fn_items.append(html.escape(txt_clean))
        fn_text = "\n\n<b>📌 Nota Kaki:</b>\n" + "\n".join(fn_items)
    
    raw_title = re.sub(r'^#+\s*', '', st.get('title', ''))
    raw_title = re.sub(r'[*_`]', '', raw_title)
    
    text = (
        f"<b>📌 {html.escape(ch['number'])}: {html.escape(raw_title)}</b>\n\n"
        f"{html.escape(para_text)}"
        f"{fn_text}"
    )
    
    prev_sub = max(0, sub_idx - 1)
    next_sub = min(len(subs) - 1, sub_idx + 1)
    nav_buttons = []
    if sub_idx > 0:
        nav_buttons.append({"text": "« Sebelumnya", "callback_data": f"view_sub_{ch_idx}_{prev_sub}"})
    if sub_idx < len(subs) - 1:
        nav_buttons.append({"text": "Seterusnya »", "callback_data": f"view_sub_{ch_idx}_{next_sub}"})
    
    kb = []
    if nav_buttons:
        kb.append(nav_buttons)
    
    kb.append([
        {"text": f"📑 Senarai Topik {ch['number']}", "callback_data": f"ch_subs_{ch_idx}_{sub_idx//6}"},
        {"text": "🏠 Menu Utama", "callback_data": "menu_main"}
    ])
    edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})

def handle_hikmah(chat_id, message_id, q_id=None):
    if not HIKMAH_DATA:
        edit_or_send(chat_id, message_id, "Tiada mutiara kata dijumpai.", get_main_menu_keyboard())
        return
    
    if q_id is None:
        q = random.choice(HIKMAH_DATA)
    else:
        q = next((item for item in HIKMAH_DATA if item.get("id") == q_id), HIKMAH_DATA[0])
    
    cur_id = q.get("id", 1)
    prev_id = cur_id - 1 if cur_id > 1 else len(HIKMAH_DATA)
    next_id = cur_id + 1 if cur_id < len(HIKMAH_DATA) else 1
    
    arabic_part = f"<b>«{html.escape(q.get('arabic', ''))}»</b>\n\n" if q.get("arabic") else ""
    trans_part = f"<i>“{html.escape(q.get('translation', ''))}”</i>\n\n" if q.get("translation") else ""
    dimensi_part = f"<b>⚔️ Fiqh Siyasah &amp; Pengajaran:</b>\n{html.escape(q.get('dimensi', ''))}\n\n" if q.get("dimensi") else ""
    
    text = (
        f"<b>💎 MUTIARA HIKMAH FIQH SIYASAH #{cur_id} / {len(HIKMAH_DATA)}</b>\n"
        f"<b>Tokoh / Sumber:</b> {html.escape(q.get('speaker', 'Syeikh al-Rasyid'))}\n\n"
        f"{arabic_part}"
        f"{trans_part}"
        f"{dimensi_part}"
        f"<b>Kitab:</b> Tanẓīr al-Taghyīr (تنظير التغيير)"
    )
    
    kb = [
        [
            {"text": "⬅️ Mutiara Lalu", "callback_data": f"hikmah_{prev_id}"},
            {"text": "🎲 Rawak", "callback_data": "hikmah_random"},
            {"text": "Mutiara Depan ➡️", "callback_data": f"hikmah_{next_id}"}
        ],
        [
            {"text": f"🧭 Buka Web PWA ({len(HIKMAH_DATA)} Mutiara Emas) 🌐", "url": PWA_PRIMARY_URL}
        ],
        [
            {"text": "🏠 Kembali ke Menu Utama", "callback_data": "menu_main"}
        ]
    ]
    if message_id:
        edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})
    else:
        send_msg(chat_id, text, {"inline_keyboard": kb})

def handle_peradaban(chat_id, message_id):
    text = (
        "<b>🌍 SUMBANGAN TANẒĪR AL-TAGHYĪR DALAM STRATEGI PERADABAN</b>\n\n"
        "Kitab <i>Tanẓīr al-Taghyīr</i> bukan sekadar ulasan sejarah kebangkitan massa 2011, "
        "sebaliknya ia adalah <b>Enjin Operasi Peralihan Kuasa &amp; Sains Kuantum Siasah</b> "
        "dalam kerangka membina <b>Ummah Fadhilah, Kuasa Nasional &amp; Peradaban Baru Islam (PBI)</b>.\n\n"
        "<b>📌 5 Teras Operasi Siasah Syeikh al-Rasyid:</b>\n"
        "1. <b>Hukum Jisim Kritikal (Critical Mass)</b>: Menggerakkan perubahan tanpa perlu menanti kesempurnaan utopia seluruh masyarakat.\n"
        "2. <b>Sinergi Akal &amp; Kesungguhan (Ḥilf al-'Uqūl)</b>: Menggabungkan teknokrat pakar dengan komitmen haraki.\n"
        "3. <b>Kebebasan Didahulukan (Al-Ḥurriyyah Awwalan)</b>: Membuka ruang sivil dan meruntuhkan tirani sebagai prasyarat dakwah terbuka.\n"
        "4. <b>Potensi Mukjizat Angkatan Muda</b>: Membimbing kepimpinan digital anak muda menembusi sekatan autokrasi.\n"
        "5. <b>Pengajaran Realiti Lapangan Turki &amp; Iraq</b>: Mengelakkan kesilapan strategi kudeta dan perangkap sektarianisme."
    )
    kb = [
        [
            {"text": "📖 Baca Dokumen Sumbangan Penuh", "callback_data": "ch_10"}
        ],
        [
            {"text": "🏠 Kembali ke Menu Utama", "callback_data": "menu_main"}
        ]
    ]
    if message_id:
        edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})
    else:
        send_msg(chat_id, text, {"inline_keyboard": kb})

def handle_search_info(chat_id, message_id):
    text = (
        "<b>🔍 ENJIN CARIAN PINTAR TANẒĪR AL-TAGHYĪR</b>\n\n"
        "Sila taip perkataan atau frasa carian yang anda inginkan di dalam chat ini "
        "(contohnya: <code>sunnatullah</code>, <code>pemuda</code>, <code>Turki</code>, "
        "<code>revolusi</code>, <code>Gaza</code>, <code>Musa</code>, dll).\n\n"
        f"Bot akan mencari secara automatik pada {TOTAL_SUBTOPICS} topik dan {TOTAL_QUOTES} mutiara hikmah."
    )
    kb = [[{"text": "« Kembali ke Menu Utama", "callback_data": "menu_main"}]]
    if message_id:
        edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})
    else:
        send_msg(chat_id, text, {"inline_keyboard": kb})

def perform_search(chat_id, query):
    q_lower = query.lower().strip()
    if len(q_lower) < 2:
        send_msg(chat_id, "Sila masukkan sekurang-kurangnya 2 aksara untuk carian.")
        return
        
    results = []
    
    # 1. Cari dalam Mutiara Kata
    for m in HIKMAH_DATA:
        m_txt = (m.get("translation", "") + " " + m.get("dimensi", "") + " " + m.get("arabic", "")).lower()
        if q_lower in m_txt:
            results.append({
                "type": "mutiara",
                "id": m.get("id"),
                "title": f"Mutiara #{m.get('id')}: {m.get('speaker', '')}",
                "snippet": m.get("translation", "")[:120] + "..."
            })
            if len(results) >= 4:
                break
    
    # 2. Cari dalam Bab & Subtajuk
    if len(results) < 8:
        for c_idx, ch in enumerate(CHAPTERS):
            for s_idx, st in enumerate(ch.get("subtopics", [])):
                paras_clean = [re.sub(r'<[^>]+>', '', p) for p in st.get("paragraphs", [])]
                st_text = (st.get("title", "") + " " + " ".join(paras_clean)).lower()
                if q_lower in st_text:
                    raw_title = re.sub(r'^#+\s*', '', st.get("title", ""))
                    raw_title = re.sub(r'[*_`]', '', raw_title)
                    snippet = (paras_clean[0] if paras_clean else "")[:120] + "..."
                    results.append({
                        "type": "subtopic",
                        "ch_idx": c_idx,
                        "sub_idx": s_idx,
                        "title": f"{ch['number']}: {raw_title}",
                        "snippet": snippet
                    })
                    if len(results) >= 8:
                        break
            if len(results) >= 8:
                break
    
    if not results:
        text = f"<b>🔍 Hasil Carian:</b> <i>\"{html.escape(query)}\"</i>\n\nMaaf, tiada padanan dijumpai. Sila cuba kata kunci lain."
        kb = [
            [{"text": "🔍 Cuba Carian Lain", "callback_data": "menu_search_info"}],
            [{"text": "🏠 Menu Utama", "callback_data": "menu_main"}]
        ]
        send_msg(chat_id, text, {"inline_keyboard": kb})
        return

    text = f"<b>🔍 Hasil Carian untuk:</b> <i>\"{html.escape(query)}\"</i>\nDijumpai {len(results)} padanan terpilih:\n\n"
    kb = []
    for idx, r in enumerate(results):
        t_short = r["title"]
        if len(t_short) > 36:
            t_short = t_short[:33] + "..."
        if r["type"] == "mutiara":
            kb.append([{"text": f"💎 {t_short}", "callback_data": f"hikmah_{r['id']}"}])
        else:
            kb.append([{"text": f"📖 {t_short}", "callback_data": f"view_sub_{r['ch_idx']}_{r['sub_idx']}"}])
    
    kb.append([{"text": "🏠 Menu Utama", "callback_data": "menu_main"}])
    send_msg(chat_id, text, {"inline_keyboard": kb})

def main_polling():
    if not BOT_TOKEN or "MASUKKAN" in BOT_TOKEN:
        print("PERINGATAN: TELEGRAM_BOT_TOKEN_TANZIR belum ditetapkan dalam environment atau config.json.", flush=True)
        print("Sila masukkan token rasmi ke dalam config.json untuk mengaktifkan bot secara langsung.", flush=True)
        return

    print("Bot Tanẓīr al-Taghyīr bersedia dan memulakan polling...", flush=True)
    offset = None
    while True:
        try:
            payload = {"timeout": 30}
            if offset:
                payload["offset"] = offset
            
            res = call_telegram_api("getUpdates", payload)
            if res and res.get("ok"):
                for upd in res.get("result", []):
                    offset = upd["update_id"] + 1
                    
                    if "message" in upd:
                        msg = upd["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg.get("text", "").strip()
                        
                        if not text:
                            continue
                        
                        print(f"[Mesej] Dari {chat_id}: {text}", flush=True)
                            
                        if text.startswith("/"):
                            cmd = text.split()[0].lower()
                            arg = text[len(cmd):].strip()
                            
                            if cmd in ["/start", "/mula", "/menu"]:
                                handle_start(chat_id)
                            elif cmd in ["/help", "/bantuan"]:
                                handle_help(chat_id)
                            elif cmd in ["/bab", "/chapters", "/senarai"]:
                                handle_chapters_menu(chat_id, None)
                            elif cmd in ["/hikmah", "/quote", "/mutiara"]:
                                handle_hikmah(chat_id, None)
                            elif cmd in ["/peradaban", "/sumbangan"]:
                                handle_peradaban(chat_id, None)
                            elif cmd in ["/cari", "/search"]:
                                if arg:
                                    perform_search(chat_id, arg)
                                else:
                                    handle_search_info(chat_id, None)
                            else:
                                perform_search(chat_id, text)
                        else:
                            perform_search(chat_id, text)
                    
                    elif "callback_query" in upd:
                        cb = upd["callback_query"]
                        chat_id = cb["message"]["chat"]["id"]
                        msg_id = cb["message"]["message_id"]
                        data = cb.get("data", "")
                        
                        print(f"[Callback] Dari {chat_id}: {data}", flush=True)
                        call_telegram_api("answerCallbackQuery", {"callback_query_id": cb["id"]})
                        
                        if data == "menu_main":
                            handle_start(chat_id, msg_id)
                        elif data == "menu_chapters":
                            handle_chapters_menu(chat_id, msg_id)
                        elif data == "menu_peradaban":
                            handle_peradaban(chat_id, msg_id)
                        elif data == "menu_search_info":
                            handle_search_info(chat_id, msg_id)
                        elif data == "hikmah_random":
                            handle_hikmah(chat_id, msg_id)
                        elif data.startswith("hikmah_"):
                            q_id = int(data.split("_")[1])
                            handle_hikmah(chat_id, msg_id, q_id)
                        elif data.startswith("ch_subs_"):
                            parts = data.split("_")
                            handle_subtopics_list(chat_id, msg_id, int(parts[2]), int(parts[3]))
                        elif data.startswith("view_sub_"):
                            parts = data.split("_")
                            handle_subtopic_view(chat_id, msg_id, int(parts[2]), int(parts[3]))
                        elif data.startswith("read_full_"):
                            parts = data.split("_")
                            handle_subtopic_view(chat_id, msg_id, int(parts[2]), int(parts[3]))
                        elif data.startswith("ch_"):
                            ch_idx = int(data.split("_")[1])
                            handle_chapter_view(chat_id, msg_id, ch_idx)

        except Exception as e:
            print(f"Ralat gelung polling: {e}")
            time.sleep(3)

if __name__ == "__main__":
    start_health_server()
    main_polling()

# -*- coding: utf-8 -*-
"""
BOT TELEGRAM TANẒĪR AL-TAGHYĪR (تنظير التغيير)
Membina Teori Integrasi Perubahan Politik Islam
Karya: Asy-Syeikh Muhammad Ahmad ar-Rasyid (رحمه الله)
Siri Rujukan Gerakan & Fiqh Siyasah Perubahan
Versi: 1.3 (Infografik Khas Telegram, Multi-Page Pagination, Penyingkiran Ralat Epilog)
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
from bs4 import BeautifulSoup
import requests

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        response = '{"status":"ok","bot":"Tanzir al-Taghyir","uptime":"24/7"}'
        self.wfile.write(response.encode("utf-8"))

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
# Mulakan health server SEGERA sebelum sebarang proses lain
_early_port = int(os.environ.get("PORT", 0))
if _early_port:
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler as _BH
    class _EarlyHandler(_BH):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type","application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        def log_message(self, *a): return
    threading.Thread(target=HTTPServer(("0.0.0.0",_early_port),_EarlyHandler).serve_forever, 
daemon=True).start()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DATA_PATH = os.path.join(BASE_DIR, "tanzir_data.json")
QUOTES_PATH = os.path.join(BASE_DIR, "tanzir_quotes.json")

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN_TANZIR", "").strip()

if not BOT_TOKEN and os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f)
            if cfg.get("bot_token"):
                BOT_TOKEN = cfg.get("bot_token").strip()
    except Exception as e:
        print(f"Ralat membaca config.json: {e}", flush=True)

# Token Sandaran Rasmi Tanẓīr al-Taghyīr
if not BOT_TOKEN or "MASUKKAN" in BOT_TOKEN:
    BOT_TOKEN = "9276024407:AAGk2pu0mae6kGOK24J-loMznOP_gQRjVv4"

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
PWA_PRIMARY_URL = "https://teorisasi-taghyir.pages.dev/"
PWA_BACKUP_URL = "https://najsha97-rgb.github.io/teorisasi-taghyir/"
IMG_FRONT_COVER = "https://najsha97-rgb.github.io/teorisasi-taghyir/images/cover_revitalized_vibrant_tanzir.jpg"
IMG_BACK_COVER = "https://najsha97-rgb.github.io/teorisasi-taghyir/images/kulit_belakang_tanzir.jpg"

print(f"Berjaya memuatkan {len(CHAPTERS)} Bahagian ({TOTAL_SUBTOPICS} Topik) & {TOTAL_QUOTES} Mutiara Kata Tanẓīr al-Taghyīr.")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

SESSION = requests.Session()

def tg_escape(text):
    """Escape khusus untuk mod HTML Telegram tanpa meng-escape tanda petik tunggal."""
    if text is None:
        return ""
    s = str(text)
    s = s.replace(r"\'", "'").replace(r'\"', '"')
    s = s.replace(r"\&#x27;", "'").replace("&#x27;", "'").replace("&apos;", "'")
    return html.escape(s, quote=False)

# ==========================================
# ENJIN PENUKAR INFOGRAFIK KHAS TELEGRAM
# ==========================================

def clean_html_markup(s):
    if not s:
        return ""
    # Buang ulasan HTML seperti <!-- RUKUN 1 -->
    s = re.sub(r'<!--.*?-->', '', s, flags=re.DOTALL)
    return s

def parse_rukun_infographic(html_str):
    """Menukar Rukun Model 2026 dalam Epilog menjadi infografik kad Telegram yang lengkap."""
    soup = BeautifulSoup(clean_html_markup(html_str), "html.parser")
    badge = soup.find(class_="rukun-badge")
    ar_title = soup.find(class_="rukun-ar-title")
    main_title = soup.find(class_="rukun-main-title")
    subtitle = soup.find(class_="rukun-subtitle")
    
    lines = []
    if badge:
        lines.append(f"<b>{badge.get_text(strip=True)}</b>")
    if ar_title:
        lines.append(f"<i>{ar_title.get_text(strip=True)}</i>")
    if main_title:
        lines.append(f"<b>{main_title.get_text(strip=True).upper()}</b>")
    if subtitle:
        lines.append(f"<i>{subtitle.get_text(strip=True)}</i>")
        
    lines.append("────────────────────")
    
    cards = soup.find_all(class_="rukun-card")
    for c in cards:
        icon_elem = c.find(class_="rukun-card-icon")
        icon = icon_elem.get_text(strip=True) if icon_elem else "🔹"
        
        tag_elem = c.find(class_="rukun-tag")
        tag = tag_elem.get_text(strip=True) if tag_elem else ""
        
        title_elem = c.find(class_="rukun-card-title")
        title = title_elem.get_text(strip=True) if title_elem else ""
        
        desc_elem = c.find(class_="rukun-card-desc")
        desc = desc_elem.get_text(" ", strip=True) if desc_elem else ""
        desc = re.sub(r'\s+', ' ', desc)
        
        m_t = re.match(r'^(\d+\.)\s*(.*?)(?:\s*\((.*?)\))?$', title)
        if m_t:
            num = m_t.group(1)
            t_main = m_t.group(2).strip()
            t_sub = m_t.group(3).strip() if m_t.group(3) else ""
            t_formatted = f"<b>{num} {t_main}</b>" + (f" <i>({t_sub})</i>" if t_sub else "")
        else:
            t_formatted = f"<b>{title}</b>"
            
        header_card = f"{icon} <b>[{tag}]</b>\n{t_formatted}" if tag else f"{icon} {t_formatted}"
        lines.append(f"{header_card}\n• {desc}")
        
    note_elem = soup.find(class_="rukun-footer-note")
    if note_elem:
        note_txt = note_elem.get_text(" ", strip=True)
        note_txt = re.sub(r'\s+', ' ', note_txt)
        lines.append(f"────────────────────\n💡 <i>{note_txt}</i>")
        
    return "\n\n".join(lines)

def parse_pentalogi_infographic(html_str):
    """Menukar Pentalogi Peradaban menjadi kad infografik Telegram."""
    soup = BeautifulSoup(clean_html_markup(html_str), "html.parser")
    badge = soup.find(class_="pentalogi-badge")
    ar_title = soup.find(class_="pentalogi-ar-title")
    main_title = soup.find(class_="pentalogi-main-title")
    subtitle = soup.find(class_="pentalogi-subtitle")
    
    lines = []
    if badge: lines.append(f"<b>{badge.get_text(strip=True)}</b>")
    if ar_title: lines.append(f"<i>{ar_title.get_text(strip=True)}</i>")
    if main_title: lines.append(f"<b>{main_title.get_text(strip=True).upper()}</b>")
    if subtitle: lines.append(f"<i>{subtitle.get_text(strip=True)}</i>")
    lines.append("────────────────────")
    
    cards = soup.find_all(class_="pentalogi-card")
    for c in cards:
        step = c.find(class_="pentalogi-step")
        step_txt = step.get_text(strip=True) if step else ""
        icon = c.find(class_="pentalogi-icon")
        icon_txt = icon.get_text(strip=True) if icon else "📖"
        t_ms = c.find(class_="pentalogi-title-ms")
        ms_txt = t_ms.get_text(strip=True) if t_ms else ""
        t_ar = c.find(class_="pentalogi-title-ar")
        ar_txt = t_ar.get_text(strip=True) if t_ar else ""
        role = c.find(class_="pentalogi-role")
        role_txt = role.get_text(" ", strip=True) if role else ""
        desc = c.find(class_="pentalogi-desc")
        desc_txt = desc.get_text(" ", strip=True) if desc else ""
        
        card_str = f"{icon_txt} <b>{step_txt}: {ms_txt}</b> <i>({ar_txt})</i>"
        if role_txt: card_str += f"\n• <b>Fungsi:</b> {role_txt}"
        if desc_txt: card_str += f"\n• {desc_txt}"
        lines.append(card_str)
        
    return "\n\n".join(lines)

def parse_tonggak_infographic(html_str):
    """Menukar 8 Tonggak Kuasa Nasional menjadi kad infografik Telegram."""
    soup = BeautifulSoup(clean_html_markup(html_str), "html.parser")
    badge = soup.find(class_="tonggak-badge")
    ar_title = soup.find(class_="tonggak-ar-title")
    main_title = soup.find(class_="tonggak-main-title")
    subtitle = soup.find(class_="tonggak-subtitle")
    
    lines = []
    if badge: lines.append(f"<b>{badge.get_text(strip=True)}</b>")
    if ar_title: lines.append(f"<i>{ar_title.get_text(strip=True)}</i>")
    if main_title: lines.append(f"<b>{main_title.get_text(strip=True).upper()}</b>")
    if subtitle: lines.append(f"<i>{subtitle.get_text(strip=True)}</i>")
    lines.append("────────────────────")
    
    cards = soup.find_all(class_="tonggak-card")
    for c in cards:
        title = c.find(class_="tonggak-card-title")
        t_txt = title.get_text(strip=True) if title else ""
        core = c.find(class_="tonggak-core")
        core_txt = core.get_text(" ", strip=True) if core else ""
        fokus = c.find(class_="tonggak-fokus")
        fokus_txt = fokus.get_text(" ", strip=True) if fokus else ""
        
        card_str = f"🏛️ <b>{t_txt}</b>"
        if core_txt: card_str += f"\n• <b>Teras:</b> {core_txt}"
        if fokus_txt: card_str += f"\n• {fokus_txt}"
        lines.append(card_str)
        
    return "\n\n".join(lines)

def parse_epigraf_infographic(html_str):
    """Menukar seni epigraf kulit belakang menjadi paparan Telegram."""
    soup = BeautifulSoup(clean_html_markup(html_str), "html.parser")
    badge = soup.find(class_="epigraf-badge-gold")
    title = soup.find(class_="epigraf-title")
    title_ar = soup.find(class_="epigraf-title-ar")
    blurb_quote = soup.find(class_="epigraf-blurb-quote")
    
    lines = []
    if badge: lines.append(f"<b>{badge.get_text(strip=True)}</b>")
    if title: lines.append(f"<b>{title.get_text(strip=True)}</b>")
    if title_ar: lines.append(f"<i>{title_ar.get_text(strip=True)}</i>")
    lines.append("────────────────────")
    
    if blurb_quote:
        lines.append(f"<blockquote>{blurb_quote.get_text(strip=True)}</blockquote>")
        
    points = soup.find_all(class_="epigraf-point")
    for pt in points:
        t = pt.find(class_="epigraf-point-title")
        t_txt = t.get_text(strip=True) if t else ""
        d = pt.find(class_="epigraf-point-desc")
        d_txt = d.get_text(" ", strip=True) if d else ""
        lines.append(f"• <b>{t_txt}:</b> {d_txt}")
        
    return "\n\n".join(lines)

def convert_any_infographic(text):
    if not text:
        return ""
    if "rukun-infographic-container" in text:
        return parse_rukun_infographic(text)
    elif "pentalogi-infographic-container" in text:
        return parse_pentalogi_infographic(text)
    elif "tonggak-infographic-container" in text:
        return parse_tonggak_infographic(text)
    elif "epigraf-hero-layout" in text:
        return parse_epigraf_infographic(text)
    return text

def clean_raw_text(text):
    """Membersihkan mojibake tanda petik dan tag HTML web yang tidak disokong oleh Telegram."""
    if not text:
        return ""
    s = str(text)
    # Buang ulasan HTML
    s = re.sub(r'<!--.*?-->', '', s, flags=re.DOTALL)
    # Tukar infografik jika ada
    s = convert_any_infographic(s)
    
    s = s.replace(r"\&#x27;", "'").replace("&#x27;", "'").replace("&apos;", "'")
    s = s.replace(r"\'", "'").replace(r'\"', '"')
    # Tukar rujukan nota kaki web <span class="fn-ref">...</span> -> [1]
    s = re.sub(r'<span[^>]*class=["\']fn-ref["\'][^>]*>\[?(.*?)\]?</span>', r'[\1]', s)
    # Tukar tajuk HTML web jika ada kepada heading markdown
    s = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n### \1\n', s, flags=re.IGNORECASE)
    # Tukar tag gaya web kepada markdown
    s = re.sub(r'<(?:\/)?(?:strong|b)(?:\s+[^>]*)?>', '**', s, flags=re.IGNORECASE)
    s = re.sub(r'<(?:\/)?(?:em|i)(?:\s+[^>]*)?>', '*', s, flags=re.IGNORECASE)
    # Buang tag HTML web luar (div, span, p dsb)
    s = re.sub(r'</?(?:div|span|p|section|header|article|table|tr|td|th|tbody)[^>]*>', '\n', s, flags=re.IGNORECASE)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

def format_inline_markdown(s):
    """Menukar sintaks bold & italic Markdown kepada tag HTML Telegram yang sah."""
    if not s:
        return ""
    s = re.sub(r'\*\*([^\*\n]+?)\*([^\*\n]+?)\*\*\*', r'<b>\1<i>\2</i></b>', s)
    s = re.sub(r'\*\*\*([^\*\n]+?)\*([^\*\n]+?)\*\*', r'<b><i>\1</i>\2</b>', s)
    s = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^\*\n]+?)\*(?!\*)', r'<i>\1</i>', s)
    s = s.replace("*", "")
    return s

def balance_telegram_tags(s):
    """Memastikan semua tag HTML Telegram bersarang sempurna tanpa unclosed/mismatched tag."""
    valid_tags = {'b', 'i', 'u', 's', 'code', 'pre', 'blockquote', 'a'}
    tag_pattern = re.compile(r'(</?([a-z]+)(?:\s+[^>]*)?>)', re.IGNORECASE)
    
    stack = []
    output = []
    last_idx = 0
    
    for m in tag_pattern.finditer(s):
        full_tag = m.group(1)
        tag_name = m.group(2).lower()
        is_closing = full_tag.startswith('</')
        
        output.append(s[last_idx:m.start()])
        last_idx = m.end()
        
        if tag_name not in valid_tags:
            output.append(full_tag.replace('<', '&lt;').replace('>', '&gt;'))
            continue
            
        if not is_closing:
            stack.append(tag_name)
            output.append(full_tag)
        else:
            if not stack:
                continue
            if stack[-1] == tag_name:
                stack.pop()
                output.append(full_tag)
            else:
                if tag_name in stack:
                    while stack and stack[-1] != tag_name:
                        top = stack.pop()
                        output.append(f"</{top}>")
                    if stack and stack[-1] == tag_name:
                        stack.pop()
                        output.append(full_tag)
                else:
                    continue

    output.append(s[last_idx:])
    while stack:
        top = stack.pop()
        output.append(f"</{top}>")
        
    return "".join(output)

def md_to_telegram_html(text):
    """
    Penukar penuh format teks & Markdown Tanẓīr al-Taghyīr kepada Telegram HTML rasmi.
    """
    if not text:
        return ""
    
    text = clean_raw_text(text)
    lines = text.split("\n")
    out_lines = []
    
    in_quote = False
    quote_buf = []
    
    def flush_quote():
        nonlocal in_quote, quote_buf, out_lines
        if in_quote and quote_buf:
            while quote_buf and not quote_buf[0].strip():
                quote_buf.pop(0)
            while quote_buf and not quote_buf[-1].strip():
                quote_buf.pop()
            if quote_buf:
                q_text = "\n".join(quote_buf)
                q_text = re.sub(r'^\s*["“]+|["”]+\s*$', '', q_text).strip()
                safe_q = html.escape(q_text, quote=False)
                safe_q = format_inline_markdown(safe_q)
                out_lines.append(f"<blockquote>{safe_q}</blockquote>")
            quote_buf = []
            in_quote = False

    for line in lines:
        l_strip = line.strip()
        
        m_quote = re.match(r'^(?:>|&gt;)\s*(.*)$', l_strip)
        if m_quote:
            in_quote = True
            quote_buf.append(m_quote.group(1))
            continue
        elif in_quote and not l_strip:
            quote_buf.append("")
            continue
        else:
            flush_quote()
            
        if re.match(r'^(?:-{3,}|\*{3,}|_{3,})$', l_strip):
            out_lines.append("────────────────────")
            continue
            
        m_head = re.match(r'^(#{1,6})\s+(.*)$', l_strip)
        if m_head:
            head_txt = m_head.group(2).strip()
            head_txt = re.sub(r'^\(\*(.*?)\*\)$', r'\1', head_txt)
            head_txt = re.sub(r'[*_`]', '', head_txt).strip()
            safe_h = html.escape(head_txt, quote=False)
            out_lines.append(f"<b>{safe_h}</b>")
            continue
            
        m_bullet = re.match(r'^[-*•]\s+(.*)$', l_strip)
        if m_bullet:
            b_txt = m_bullet.group(1).strip()
            safe_b = html.escape(b_txt, quote=False)
            safe_b = format_inline_markdown(safe_b)
            out_lines.append(f"• {safe_b}")
            continue
            
        if not l_strip:
            out_lines.append("")
            continue
            
        safe_line = html.escape(line, quote=False)
        safe_line = format_inline_markdown(safe_line)
        out_lines.append(safe_line)
        
    flush_quote()
    res = "\n".join(out_lines)
    res = res.replace("&#x27;", "'").replace("&apos;", "'")
    res = balance_telegram_tags(res)
    return res

def to_tg_html(text):
    """Pastikan simbol ampersand (&) yang tidak berformat die-escape kepada &amp; untuk Telegram."""
    if not text:
        return ""
    text = text.replace(r"\&#x27;", "'").replace(r"&#x27;", "'").replace(r"&apos;", "'")
    text = text.replace(r"\'", "'").replace(r'\"', '"')
    return re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+);)', '&amp;', text)

def split_summary_pages(summary_text, max_len=2200):
    if not summary_text:
        return []
    paras = summary_text.split("\n\n")
    pages = []
    cur = []
    cur_len = 0
    for p in paras:
        p_str = p.strip()
        if not p_str:
            continue
        if cur_len + len(p_str) > max_len and cur:
            pages.append("\n\n".join(cur))
            cur = [p_str]
            cur_len = len(p_str)
        else:
            cur.append(p_str)
            cur_len += len(p_str) + 2
    if cur:
        pages.append("\n\n".join(cur))
    return pages

def split_subtopic_pages(paragraphs, max_len=2600):
    """Memecahkan teks subtajuk kepada beberapa halaman yang mudah dibaca tanpa terputus."""
    if not paragraphs:
        return [""]
    pages = []
    cur_paras = []
    cur_len = 0
    
    for p in paragraphs:
        p_str = p.strip()
        if not p_str:
            continue
        p_len = len(p_str)
        
        if p_len > max_len:
            if cur_paras:
                pages.append("\n\n".join(cur_paras))
                cur_paras = []
                cur_len = 0
            # Pecahkan perenggan sangat panjang ikut ayat
            sentences = re.split(r'(?<=[.!?\n])\s+', p_str)
            sub_cur = []
            sub_len = 0
            for s in sentences:
                if sub_len + len(s) > max_len and sub_cur:
                    pages.append(" ".join(sub_cur))
                    sub_cur = [s]
                    sub_len = len(s)
                else:
                    sub_cur.append(s)
                    sub_len += len(s) + 1
            if sub_cur:
                pages.append(" ".join(sub_cur))
        elif cur_len + p_len > max_len and cur_paras:
            pages.append("\n\n".join(cur_paras))
            cur_paras = [p_str]
            cur_len = p_len
        else:
            cur_paras.append(p_str)
            cur_len += p_len + 2
            
    if cur_paras:
        pages.append("\n\n".join(cur_paras))
    return pages if pages else [""]

def call_telegram_api(method, payload, timeout=8):
    if not BOT_TOKEN or "MASUKKAN" in BOT_TOKEN:
        return None
    url = f"{TELEGRAM_API_URL}/{method}"
    try:
        r = SESSION.post(url, json=payload, timeout=timeout)
        return r.json()
    except Exception as e:
        if "getUpdates" not in method:
            print(f"Ralat sambungan API ({method}): {e}", flush=True)
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
    
    res = call_telegram_api("editMessageText", payload, timeout=8)
    if not res or not res.get("ok"):
        err_desc = (res.get("description", "") if res else "").lower()
        if "message is not modified" in err_desc:
            return res
        payload_send = {
            "chat_id": chat_id,
            "text": safe_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        if reply_markup:
            payload_send["reply_markup"] = reply_markup
        return call_telegram_api("sendMessage", payload_send, timeout=8)
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

def send_photo(chat_id, photo_url, caption="", reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": to_tg_html(caption),
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return call_telegram_api("sendPhoto", payload, timeout=12)

def get_main_menu_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "🎨 Epigraf & Kulit", "callback_data": "ch_0"},
                {"text": "🖼️ Ilustrasi HD", "callback_data": "view_cover_front"}
            ],
            [
                {"text": "📖 Baca Ikut Bab", "callback_data": "menu_chapters"},
                {"text": "📌 Ringkasan Eksekutif", "callback_data": "menu_summaries"}
            ],
            [
                {"text": "📌 Mukadimah: 9 Faktor", "callback_data": "ch_1"},
                {"text": "🌐 Ummah Fadhilah (PBI)", "callback_data": "menu_peradaban"}
            ],
            [
                {"text": f"💎 {TOTAL_QUOTES} Mutiara Kata", "callback_data": "hikmah_random"},
                {"text": "🔍 Carian Pintar", "callback_data": "menu_search_info"}
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
        "• <code>/ringkasan</code> — Mod Ringkasan Eksekutif &amp; Intisari Bab\n"
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
    
    title_ar_str = f"\n<i>{tg_escape(ch.get('title_ar', ''))}</i>" if ch.get('title_ar') else ""
    summary_preview = ""
    if ch.get("summary"):
        clean_sum = clean_raw_text(ch["summary"])
        clean_sum = re.sub(r'#+\s*', '', clean_sum)
        clean_sum = re.sub(r'[*_`>]', '', clean_sum)
        clean_sum = re.sub(r'-{3,}', '', clean_sum).strip()
        summary_preview = f"\n\n<b>📌 Intisari Bab:</b>\n{tg_escape(clean_sum[:400])}..."
    
    text = (
        f"<b>📖 {tg_escape(ch['number'])}: {tg_escape(ch['title'])}</b>{title_ar_str}\n\n"
        f"• <b>Jumlah Subtajuk:</b> {ch.get('total_subtopics', len(ch.get('subtopics', [])))} Topik\n"
        f"• <b>Jumlah Perenggan:</b> {ch.get('total_paragraphs', 0)} Perenggan\n"
        f"• <b>Nota Kaki:</b> {len(ch.get('footnotes', []))} Rujukan"
        f"{summary_preview}"
    )
    
    kb = []
    if ch_idx == 0:
        kb.append([
            {"text": "🎨 Lihat Kulit Depan", "callback_data": "view_cover_front"},
            {"text": "📜 Lihat Kulit Belakang", "callback_data": "view_cover_back"}
        ])
    kb.extend([
        [
            {"text": f"📑 Senarai {len(ch.get('subtopics', []))} Subtajuk", "callback_data": f"ch_subs_{ch_idx}_0"},
            {"text": "📌 Ringkasan Bab", "callback_data": f"ch_sum_{ch_idx}_0"}
        ],
        [
            {"text": "📖 Baca Teks Penuh Dari Awal", "callback_data": f"view_sub_{ch_idx}_0_0"}
        ],
        [
            {"text": "« Kembali ke Senarai Bab", "callback_data": "menu_chapters"},
            {"text": "🏠 Menu Utama", "callback_data": "menu_main"}
        ]
    ])
    edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})

def handle_cover_view(chat_id, cover_type="front"):
    if cover_type == "front":
        caption = (
            "<b>🎨 ILUSTRASI KULIT HADAPAN TANẒĪR AL-TAGHYĪR</b>\n"
            "<i>(Naskhah Kanonikal Edisi Bahasa Melayu Terselaras)</i>\n\n"
            "Lukisan kanvas abstrak karya <b>Asy-Syeikh Muhammad Ahmad ar-Rasyid</b> <i>rahimahullah</i>:\n\n"
            "• <b>Al-Qā' al-Dākin (Kegelapan Rejim):</b> Menolak kepasifan di bawah tirani.\n"
            "• <b>Bahjat al-Ghad al-Akhḍar (Fajar Hijau):</b> Matlamat akhir kemerdekaan umat dan daulah adil.\n"
            "• <b>Al-Thaman al-Aḥmar (Darah Pengorbanan):</b> Harga kebebasan yang ditebus di jalan Allah.\n"
            "• <b>Al-Farāsyāt al-Silmiyyah (Rama-rama Damai):</b> Gelombang pemuda berarak tanpa senjata menumbangkan thaghut."
        )
        kb = [
            [{"text": "📜 Lihat Kulit Belakang (Blurb)", "callback_data": "view_cover_back"}],
            [{"text": "📖 Baca Falsafah Epigraf Lengkap", "callback_data": "ch_0"}],
            [{"text": "🏠 Menu Utama", "callback_data": "menu_main"}]
        ]
        send_photo(chat_id, IMG_FRONT_COVER, caption, {"inline_keyboard": kb})
    else:
        caption = (
            "<b>📜 ILUSTRASI KULIT BELAKANG TANẒĪR AL-TAGHYĪR</b>\n"
            "<i>(Blurb, Falsafah Ketamadunan & Wasiat Haraki)</i>\n\n"
            "Memuatkan wasiat pemikiran strategik Syeikh Muhammad Ahmad ar-Rasyid:\n\n"
            "<blockquote>“Kemenangan politik bukanlah sekadar kejayaan meruntuhkan takhta kezaliman di jalanan, "
            "sebaliknya bermula apabila angkatan dakwah berupaya membina Super Inteligensi, "
            "menyatukan kepakaran teknokrat melalui Ḥilf al-'Uqūl, dan menegakkan Peradaban Baru Islam (PBI).”</blockquote>"
        )
        kb = [
            [{"text": "🎨 Lihat Kulit Hadapan", "callback_data": "view_cover_front"}],
            [{"text": "📖 Baca Falsafah Epigraf Lengkap", "callback_data": "ch_0"}],
            [{"text": "🏠 Menu Utama", "callback_data": "menu_main"}]
        ]
        send_photo(chat_id, IMG_BACK_COVER, caption, {"inline_keyboard": kb})

def handle_summaries_menu(chat_id, message_id):
    keyboard = [
        [
            {"text": "📌 Ringkasan Mukadimah (9 Faktor)", "callback_data": "ch_sum_1_0"},
            {"text": "Bab 1: Logik Fiqh Perubahan", "callback_data": "ch_sum_2_0"}
        ],
        [
            {"text": "Bab 2: Pemuda Penekan", "callback_data": "ch_sum_3_0"},
            {"text": "Bab 3: Syarat Empirikal", "callback_data": "ch_sum_4_0"}
        ],
        [
            {"text": "Bab 4: Pergerakan Hidup", "callback_data": "ch_sum_5_0"},
            {"text": "Bab 5: Mukjizat Pemuda", "callback_data": "ch_sum_6_0"}
        ],
        [
            {"text": "Bab 6: Rumusan Teori", "callback_data": "ch_sum_7_0"},
            {"text": "Khatimah (Wasiat Penutup)", "callback_data": "ch_sum_8_0"}
        ],
        [
            {"text": "⚖️ Epilog Penterjemah", "callback_data": "ch_sum_9_0"},
            {"text": "🌐 Sumbangan Peradaban (PBI)", "callback_data": "ch_sum_10_0"}
        ],
        [
            {"text": "« Kembali ke Menu Utama", "callback_data": "menu_main"}
        ]
    ]
    text = (
        "<b>📌 MOD RINGKASAN EKSEKUTIF TANẒĪR AL-TAGHYĪR</b>\n\n"
        "Mod ini menyediakan intisari ilmiah padat bagi setiap bab naskhah:\n"
        "• Peta minda &amp; navigasi pemikiran haraki\n"
        "• 5 Doktrin Siasah &amp; Rumusan Fiqh Sunnatullah\n"
        "• Unjuran realiti lapangan pasca-2011 menuju model 2026\n\n"
        "Sila pilih bahagian yang ingin anda baca ringkasannya:"
    )
    if message_id:
        edit_or_send(chat_id, message_id, text, {"inline_keyboard": keyboard})
    else:
        send_msg(chat_id, text, {"inline_keyboard": keyboard})

def handle_chapter_summary_view(chat_id, message_id, ch_idx, page=0):
    if ch_idx < 0 or ch_idx >= len(CHAPTERS):
        handle_summaries_menu(chat_id, message_id)
        return
    ch = CHAPTERS[ch_idx]
    raw_sum = ch.get("summary", "")
    if not raw_sum and "summary" in RAW_DATA:
        root_map = {0: "EPILOG / EPIGRAF", 1: "MUKADIMAH", 2: "BAB 1", 3: "BAB 2", 4: "BAB 3", 5: "BAB 4", 6: "BAB 5", 7: "BAB 6", 8: "KHATIMAH", 9: "EPILOG PENTERJEMAH", 10: "SUMBANGAN PERADABAN"}
        raw_sum = RAW_DATA["summary"].get(root_map.get(ch_idx, ""), "")
    
    pages = split_summary_pages(raw_sum)
    if not pages:
        pages = ["Tiada ringkasan khusus bagi bahagian ini."]
    
    total_pages = len(pages)
    page = max(0, min(page, total_pages - 1))
    cur_text = pages[page]
    
    clean_body = md_to_telegram_html(cur_text)
    
    text = (
        f"<b>📌 RINGKASAN EKSEKUTIF: {tg_escape(ch['number'])}</b> (Hlm {page+1}/{total_pages})\n"
        f"<i>{tg_escape(ch['title'])}</i>\n\n"
        f"{clean_body}"
    )
    
    nav_row = []
    if page > 0:
        nav_row.append({"text": "⬅️ Muka Surat Lalu", "callback_data": f"ch_sum_{ch_idx}_{page-1}"})
    if page < total_pages - 1:
        nav_row.append({"text": "Muka Surat Seterusnya ➡️", "callback_data": f"ch_sum_{ch_idx}_{page+1}"})
    
    kb = []
    if nav_row:
        kb.append(nav_row)
    
    kb.append([
        {"text": f"📖 Baca Terjemahan Penuh {ch['number']}", "callback_data": f"ch_subs_{ch_idx}_0"}
    ])
    kb.append([
        {"text": "« Senarai Ringkasan Bab", "callback_data": "menu_summaries"},
        {"text": "🏠 Menu Utama", "callback_data": "menu_main"}
    ])
    edit_or_send(chat_id, message_id, text, {"inline_keyboard": kb})

def handle_subtopic_summary_view(chat_id, message_id, ch_idx, sub_idx):
    ch = CHAPTERS[ch_idx]
    subs = ch.get("subtopics", [])
    if sub_idx < 0 or sub_idx >= len(subs):
        handle_subtopics_list(chat_id, message_id, ch_idx, 0)
        return
    st = subs[sub_idx]
    
    raw_title = re.sub(r'^#+\s*', '', st.get('title', ''))
    raw_title = re.sub(r'[*_`]', '', raw_title).strip()
    
    sum_text = st.get("summary", "")
    if not sum_text:
        sum_text = "Tiada ringkasan khusus untuk subtajuk ini. Sila baca terjemahan penuh di bawah."
    
    clean_body = md_to_telegram_html(sum_text)
    
    text = (
        f"<b>📌 INTISARI HARAKI (RINGKASAN SUBTAJUK)</b>\n"
        f"<b>📖 {tg_escape(ch['number'])}: {tg_escape(raw_title)}</b>\n\n"
        f"{clean_body}"
    )
    
    prev_sub = max(0, sub_idx - 1)
    next_sub = min(len(subs) - 1, sub_idx + 1)
    nav_buttons = []
    if sub_idx > 0:
        nav_buttons.append({"text": "« Subtajuk Lalu", "callback_data": f"sub_sum_{ch_idx}_{prev_sub}"})
    if sub_idx < len(subs) - 1:
        nav_buttons.append({"text": "Subtajuk Seterusnya »", "callback_data": f"sub_sum_{ch_idx}_{next_sub}"})
    
    kb = []
    if nav_buttons:
        kb.append(nav_buttons)
    
    kb.append([
        {"text": "📖 Baca Terjemahan Teks Penuh", "callback_data": f"view_sub_{ch_idx}_{sub_idx}_0"}
    ])
    kb.append([
        {"text": f"📑 Senarai Topik {ch['number']}", "callback_data": f"ch_subs_{ch_idx}_{sub_idx//6}"},
        {"text": "🏠 Menu Utama", "callback_data": "menu_main"}
    ])
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
        f"<b>📑 SUBTAJUK {tg_escape(ch['number'])}</b> (Halaman {page+1}/{total_pages})\n\n"
        f"Pilih tajuk untuk membaca terjemahan ilmiah:"
    )
    
    kb = []
    for s_i in range(start, end):
        st = subs[s_i]
        st_title = st.get("title", f"Subtajuk {s_i+1}")
        st_title = re.sub(r'^#+\s*', '', st_title)
        st_title = re.sub(r'[*_`]', '', st_title).strip()
        if len(st_title) > 35:
            st_title = st_title[:32] + "..."
        kb.append([{"text": f"🔹 {st_title}", "callback_data": f"view_sub_{ch_idx}_{s_i}_0"}])
    
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

def handle_subtopic_view(chat_id, message_id, ch_idx, sub_idx, page=0):
    """
    Paparan Subtajuk Lengkap (Versi Penuh) dengan sokongan multi-page dan infografik pintar.
    Tiada lagi pemotongan teks atau simbol mentah.
    """
    ch = CHAPTERS[ch_idx]
    subs = ch.get("subtopics", [])
    if sub_idx < 0 or sub_idx >= len(subs):
        handle_subtopics_list(chat_id, message_id, ch_idx, 0)
        return
    st = subs[sub_idx]
    
    # Tukar semua perenggan & infografik
    converted_paras = []
    for p in st.get("paragraphs", []):
        p_clean = clean_html_markup(p)
        if any(k in p_clean for k in ["rukun-infographic-container", "pentalogi-infographic-container", "tonggak-infographic-container", "epigraf-hero-layout"]):
            p_clean = convert_any_infographic(p_clean)
        converted_paras.append(p_clean)
        
    pages = split_subtopic_pages(converted_paras, max_len=2600)
    total_pages = len(pages)
    page = max(0, min(page, total_pages - 1))
    
    cur_text = pages[page]
    clean_body = md_to_telegram_html(cur_text)
    
    fn_text = ""
    # Paparkan nota kaki pada halaman terakhir jika ada
    if page == total_pages - 1 and st.get("footnotes"):
        fn_items = []
        for fn in st["footnotes"][:4]:
            if isinstance(fn, dict):
                txt = fn.get("text", "")
                txt_clean = re.sub(r'<[^>]+>', '', txt)
                fn_id = fn.get("id", "")
                fn_items.append(f"[{fn_id}] {tg_escape(txt_clean)}")
            else:
                txt_clean = re.sub(r'<[^>]+>', '', str(fn))
                fn_items.append(tg_escape(txt_clean))
        fn_text = "\n\n<b>📚 Nota Kaki:</b>\n" + "\n".join(fn_items)
    
    raw_title = re.sub(r'^#+\s*', '', st.get('title', ''))
    raw_title = re.sub(r'[*_`]', '', raw_title).strip()
    
    page_indicator = f" (Halaman {page+1}/{total_pages})" if total_pages > 1 else ""
    text = (
        f"<b>📖 {tg_escape(ch['number'])}: {tg_escape(raw_title)}</b>{page_indicator}\n\n"
        f"{clean_body}"
        f"{fn_text}"
    )
    
    # Butang navigasi antara halaman
    nav_page_row = []
    if page > 0:
        nav_page_row.append({"text": "⬅️ Halaman Lalu", "callback_data": f"view_sub_{ch_idx}_{sub_idx}_{page-1}"})
    if page < total_pages - 1:
        nav_page_row.append({"text": "Halaman Seterusnya ➡️", "callback_data": f"view_sub_{ch_idx}_{sub_idx}_{page+1}"})
    
    # Butang navigasi antara subtajuk
    prev_sub = max(0, sub_idx - 1)
    next_sub = min(len(subs) - 1, sub_idx + 1)
    nav_buttons = []
    if sub_idx > 0:
        nav_buttons.append({"text": "« Subtajuk Lalu", "callback_data": f"view_sub_{ch_idx}_{prev_sub}_0"})
    if sub_idx < len(subs) - 1:
        nav_buttons.append({"text": "Subtajuk Seterusnya »", "callback_data": f"view_sub_{ch_idx}_{next_sub}_0"})
    
    kb = []
    if nav_page_row:
        kb.append(nav_page_row)
    if nav_buttons:
        kb.append(nav_buttons)
    
    if st.get("summary"):
        kb.append([
            {"text": "📌 Baca Intisari Haraki (Ringkasan)", "callback_data": f"sub_sum_{ch_idx}_{sub_idx}"}
        ])
    
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
    
    arabic_part = f"<b>«{tg_escape(q.get('arabic', ''))}»</b>\n\n" if q.get("arabic") else ""
    
    trans_clean = md_to_telegram_html(q.get('translation', ''))
    dimensi_clean = md_to_telegram_html(q.get('dimensi', ''))
    
    trans_part = f"<blockquote>{trans_clean}</blockquote>\n\n" if trans_clean else ""
    dimensi_part = f"<b>⚔️ Fiqh Siyasah &amp; Pengajaran:</b>\n{dimensi_clean}\n\n" if dimensi_clean else ""
    
    text = (
        f"<b>💎 MUTIARA HIKMAH FIQH SIYASAH #{cur_id} / {len(HIKMAH_DATA)}</b>\n"
        f"<b>Tokoh / Sumber:</b> {tg_escape(q.get('speaker', 'Syeikh al-Rasyid'))}\n\n"
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
        "<b>🌐 SUMBANGAN TANẒĪR AL-TAGHYĪR DALAM STRATEGI PERADABAN</b>\n\n"
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
            snippet = clean_raw_text(m.get("translation", ""))
            snippet = re.sub(r'[*_`>]', '', snippet).strip()
            results.append({
                "type": "mutiara",
                "id": m.get("id"),
                "title": f"Mutiara #{m.get('id')}: {m.get('speaker', '')}",
                "snippet": (snippet[:120] + "...") if len(snippet) > 120 else snippet
            })
            if len(results) >= 4:
                break
    
    # 2. Cari dalam Bab & Subtajuk
    if len(results) < 8:
        for c_idx, ch in enumerate(CHAPTERS):
            for s_idx, st in enumerate(ch.get("subtopics", [])):
                paras_clean = [clean_raw_text(p) for p in st.get("paragraphs", [])]
                st_text = (st.get("title", "") + " " + " ".join(paras_clean)).lower()
                if q_lower in st_text:
                    raw_title = re.sub(r'^#+\s*', '', st.get("title", ""))
                    raw_title = re.sub(r'[*_`]', '', raw_title).strip()
                    snip_raw = paras_clean[0] if paras_clean else ""
                    snip_clean = re.sub(r'#+\s*', '', snip_raw)
                    snip_clean = re.sub(r'[*_`>]', '', snip_clean).strip()
                    snippet = (snip_clean[:120] + "...") if len(snip_clean) > 120 else snip_clean
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
        text = f"<b>🔍 Hasil Carian:</b> <i>\"{tg_escape(query)}\"</i>\n\nMaaf, tiada padanan dijumpai. Sila cuba kata kunci lain."
        kb = [
            [{"text": "🔍 Cuba Carian Lain", "callback_data": "menu_search_info"}],
            [{"text": "🏠 Menu Utama", "callback_data": "menu_main"}]
        ]
        send_msg(chat_id, text, {"inline_keyboard": kb})
        return

    text = f"<b>🔍 Hasil Carian untuk:</b> <i>\"{tg_escape(query)}\"</i>\nDijumpai {len(results)} padanan terpilih:\n\n"
    kb = []
    for idx, r in enumerate(results):
        t_short = r["title"]
        if len(t_short) > 36:
            t_short = t_short[:33] + "..."
        if r["type"] == "mutiara":
            kb.append([{"text": f"💎 {t_short}", "callback_data": f"hikmah_{r['id']}"}])
        else:
            kb.append([{"text": f"📖 {t_short}", "callback_data": f"view_sub_{r['ch_idx']}_{r['sub_idx']}_0"}])
        text += f"• <b>{tg_escape(r['title'])}</b>\n<i>{tg_escape(r['snippet'])}</i>\n\n"

    kb.append([{"text": "🏠 Menu Utama", "callback_data": "menu_main"}])
    send_msg(chat_id, text, {"inline_keyboard": kb})

def main_polling():
    if not BOT_TOKEN or "MASUKKAN" in BOT_TOKEN:
        print("PERINGATAN: TELEGRAM_BOT_TOKEN_TANZIR belum ditetapkan dalam environment atau config.json.", flush=True)
        print("Sila masukkan token rasmi ke dalam config.json untuk mengaktifkan bot secara langsung.", flush=True)
        return

    print("Bot Tanẓīr al-Taghyīr bersedia dan memulakan polling pantas (Fast-Polling)...", flush=True)
    offset = None
    while True:
        try:
            payload = {"timeout": 5}
            if offset:
                payload["offset"] = offset
            
            res = call_telegram_api("getUpdates", payload, timeout=12)
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
                            elif cmd in ["/kulit", "/cover", "/gambar"]:
                                handle_cover_view(chat_id, "front")
                            elif cmd in ["/help", "/bantuan"]:
                                handle_help(chat_id)
                            elif cmd in ["/bab", "/chapters", "/senarai"]:
                                handle_chapters_menu(chat_id, None)
                            elif cmd in ["/ringkasan", "/summary", "/intisari"]:
                                handle_summaries_menu(chat_id, None)
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
                        elif data == "menu_summaries":
                            handle_summaries_menu(chat_id, msg_id)
                        elif data.startswith("ch_sum_"):
                            parts = data.split("_")
                            handle_chapter_summary_view(chat_id, msg_id, int(parts[2]), int(parts[3]))
                        elif data.startswith("sub_sum_"):
                            parts = data.split("_")
                            handle_subtopic_summary_view(chat_id, msg_id, int(parts[2]), int(parts[3]))
                        elif data == "view_cover_front":
                            handle_cover_view(chat_id, "front")
                        elif data == "view_cover_back":
                            handle_cover_view(chat_id, "back")
                        elif data == "menu_chapters":
                            handle_chapters_menu(chat_id, msg_id)
                        elif data == "menu_peradaban":
                            handle_peradaban(chat_id, msg_id)
                        elif data == "menu_search_info":
                            handle_search_info(chat_id, msg_id)
                        elif data == "hikmah_random":
                            handle_hikmah(chat_id, msg_id, None)
                        elif data.startswith("hikmah_"):
                            parts = data.split("_")
                            q_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
                            handle_hikmah(chat_id, msg_id, q_id)
                        elif data.startswith("ch_subs_"):
                            parts = data.split("_")
                            ch_i = int(parts[2])
                            page = int(parts[3])
                            handle_subtopics_list(chat_id, msg_id, ch_i, page)
                        elif data.startswith("ch_"):
                            ch_i = int(data.split("_")[1])
                            handle_chapter_view(chat_id, msg_id, ch_i)
                        elif data.startswith("view_sub_"):
                            parts = data.split("_")
                            ch_i = int(parts[2])
                            sub_i = int(parts[3])
                            page_i = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 0
                            handle_subtopic_view(chat_id, msg_id, ch_i, sub_i, page_i)
                        elif data.startswith("read_full_"):
                            parts = data.split("_")
                            ch_i = int(parts[2])
                            handle_subtopic_view(chat_id, msg_id, ch_i, 0, 0)
                            
        except requests.exceptions.RequestException as e:
            time.sleep(0.5)
        except Exception as e:
            print(f"Ralat gelung utama polling: {e}", flush=True)
            time.sleep(1)

if __name__ == "__main__":
    start_health_server()
    main_polling()

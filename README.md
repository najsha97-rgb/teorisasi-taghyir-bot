# 🌿 Tanẓīr al-Taghyīr (تنظير التغيير) — Telegram Bot

Bot Telegram pintar rasmi bagi karya hebat Asy-Syeikh Muhammad Ahmad ar-Rasyid (*rahimahullah*):
**"Tanẓīr al-Taghyīr: Membina Teori Integrasi Perubahan Politik Islam"** (*Membina Teori Integrasi Fiqh Siyasah Syar'iyyah Menuju Ummah Fadhilah & Peradaban Baru Islam*).

---

## 🚀 Keupayaan & Ciri-Ciri Utama

1. **Navigasi Penuh 11 Bahagian Korpus Kanonikal:**
   - 🎨 **Epigraf & Kulit Buku:** Falsafah seni lukisan kanvas abstrak & puisi epigraf fajar kebebasan.
   - 📌 **Mukadimah:** 9 Faktor Pencetus Kebangkitan Ummah & Fiqh Sunnatullah.
   - 📖 **Bab 1 hingga Bab 6:** Kupasan lengkap teks ilmiah mantiq fiqh perubahan, revolusi rakyat vs kudeta tentera, syarat empirikal, pergerakan hidup, mukjizat pemuda, dan unjuran realiti lapangan Turki & Iraq.
   - 📜 **Khatimah:** Wasiat penutup & keberanian mengisytiharkan kebenaran.
   - ⚖️ **Epilog Penterjemah:** Bedah karya kritis, 6 analisis kelompongan (2012 vs 2026), dan 5 rukun baharu teori perubahan kontemporari.
   - 🌍 **Sumbangan Peradaban:** Pemetaan 8 Tonggak Kuasa Nasional, Ummah Fadhilah & Peradaban Baru Islam (PBI).

2. **208 Topik Ilmiah Terperinci:**
   - Pembahagian teks Arab asli dan terjemahan Bahasa Melayu akademik terselaras.
   - Paparan nota kaki ilmiah bersepadu secara terus dalam mesej topik.

3. **120 Mutiara Hikmah & Fiqh Siyasah (120 Mutiara Emas):**
   - Matan Arab bertanda baris lengkap berserta terjemahan puitis dan dimensi amal siyasah.
   - Butang rawak (dice) dan navigasi mutiara berturutan.

4. **Enjin Carian Pintar Berbilang Lapisan:**
   - Taip apa-apa kata kunci (contoh: `sunnatullah`, `pemuda`, `Turki`, `Gaza`, `kudeta`) untuk capaian pantas terus ke topik atau mutiara hikmah berkaitan.

5. **Penyepaduan Web PWA Rasmi:**
   - Akses terus ke Web PWA Tanẓīr al-Taghyīr:
     - 🌐 **Cloudflare Pages (Pantas & CDN Rasmi):** [teorisasi-taghyir.pages.dev](https://teorisasi-taghyir.pages.dev/)
     - 🌐 **GitHub Pages (Sandaran / Backup):** [najsha97-rgb.github.io/teorisasi-taghyir](https://najsha97-rgb.github.io/teorisasi-taghyir/)

---

## 🛠️ Arahan Telegram Bot (Commands)

| Arahan | Fungsi |
| :--- | :--- |
| `/start` atau `/menu` | Memaparkan Menu Utama bot secara interaktif |
| `/bab` | Memaparkan senarai 6 Bab Utama & Bahagian Khas |
| `/hikmah` | Menjana mutiara kata Fiqh Siyasah secara rawak |
| `/peradaban` | Ringkasan 5 Doktrin & 8 Tonggak Kuasa Nasional PBI |
| `/cari <kata kunci>` | Carian pantas teks penuh topik & mutiara |
| `/help` | Panduan lengkap penggunaan bot |

---

## 💻 Panduan Menjalankan Bot Secara Tempatan (Local)

### 1. Keperluan Sistem:
- Python 3.9 atau ke atas
- Pakej `requests`

### 2. Pemasangan Kebergantungan:
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Token:
Salin templat `config.json.example` kepada `config.json`:
```json
{
  "bot_token": "MASUKKAN_TOKEN_TELEGRAM_DARI_BOTFATHER",
  "bot_name": "TanzirTaghyir_bot",
  "description": "Bot Rasmi Teori Integrasi Perubahan Politik Islam Tanẓīr al-Taghyīr"
}
```
*Atau tetapkan environment variable:*
```bash
export TELEGRAM_BOT_TOKEN_TANZIR="token_telegram_anda"
```

### 4. Menjalankan Bot:
```bash
python bot.py
```

---

## ☁️ Panduan Deployment Percuma 24/7 (Serverless / PaaS)

Bot ini telah dilengkapi dengan **Health-check HTTP Server** dalaman (membaca `PORT`), menjadikannya serasi untuk di-deploy terus ke:
- **Render.com** (Web Service percuma)
- **Railway.app**
- **Koyeb**
- **VPS / Docker**

Tetapkan environment variable `TELEGRAM_BOT_TOKEN_TANZIR` pada papan pemuka perkhidmatan awan pilihan anda.

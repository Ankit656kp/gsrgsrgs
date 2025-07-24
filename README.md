# 👁️‍🗨️ Devil OSINT Bot

A powerful Telegram bot that provides Indian OSINT data search (Mobile, Aadhaar, Ration, Email, etc.) with a premium system, referral, redeem, force join, credits & more — fully Heroku-deployable and Pydroid/VPS compatible.

---

## 🚀 Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME)

> Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME` with your GitHub repo path after uploading this bot.

---

## 🔐 Environment Variables (Heroku Config Vars)

Set these variables in Heroku ➜ **Settings > Config Vars**:

| Variable       | Description                                              |
|----------------|----------------------------------------------------------|
| `API_ID`       | Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH`     | Telegram API HASH from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN`    | Bot token from [@BotFather](https://t.me/BotFather)      |
| `OWNER_ID`     | Your Telegram User ID (as admin)                         |
| `MONGO_URL`    | MongoDB URI (from [MongoDB Atlas](https://cloud.mongodb.com)) |
| `LOG_CHANNEL`  | Log group/channel ID (with bot added as admin)          |
| `FORCE_JOIN`   | Force join channel username (with @ prefix)             |
| `START_CREDITS`| Default coins new users get                              |
| `REFER_CREDITS`| Coins rewarded for each referral                         |

---

## 🧩 Features

- ✅ Force join channel before access
- ✅ Mobile, Aadhaar, Ration & Email Lookup
- ✅ Redeem code system for credits
- ✅ Referral system with unique invite links
- ✅ Admin panel for coin control
- ✅ Payout logs to proof channel
- ✅ Multilingual support (English/Hindi)
- ✅ Pydroid + VPS + Heroku support

---

## 📝 Notes

- `config.py` automatically loads values from environment
- `.env` is ignored for security; use Heroku config vars instead
- For local test, you can create a `.env` file with the same keys

---

## 💬 Support

For queries or help, contact [@YOUR_SUPPORT_HANDLE](https://t.me/YOUR_SUPPORT_HANDLE)

---
---
**Made with ❤️ by Ankit**

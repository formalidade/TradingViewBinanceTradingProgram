Thanks for the clarification! Here's a professional and clear `README.md` for your **GitHub repository**, written to inform and guide developers while showcasing your work responsibly:

---

# 📈 Binance Webhook Trading Bot

This project is a **Flask-based crypto trading bot** that executes **real-time trades** on **Binance.US** using webhook alerts from **TradingView**.

It automatically calculates the position size based on available capital, handles buy/sell logic, and ensures trade compliance with Binance’s rules (e.g., min quantity, price filters).

---

## 🚀 Features

* Accepts **secure POST webhooks** for automated trading.
* Integrates with **Binance.US API** via `python-binance`.
* Manages trading capital with environment-based configuration.
* Validates order quantities against **Binance's minQty & minPrice**.
* Supports **market buy/sell orders** on `BTC/USDT`.
* Logs trade details and dynamically updates capital in `.env`.

---

## 📦 Requirements

* Python 3.7+
* Flask
* `python-binance`
* `python-dotenv`

Install with:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with:

```ini
API_KEY=your_binance_api_key
API_SECRET=your_binance_api_secret
PASSPHRASE=secure_custom_passphrase
CAPITAL=1000.0  # initial trading capital in USDT
```

---

## ⚙️ Usage

### Start the Flask app:

```bash
python bot.py
```

### Webhook Endpoint:

* `/webhook` — accepts **TradingView alerts** formatted like:

```json
{
  "passphrase": "your_passphrase",
  "strategy": {
    "order_action": "buy",
    "order_price": 27000
  }
}
```

* `/initialCapital` — optionally reset capital (admin use only):

```json
{
  "passphrase": "your_passphrase",
  "capital": 500
}
```

---

## 🧠 Notes

* This bot is **configured for BTC/USDT** only.
* All orders are **market orders** (can be changed if needed).
* **Real orders are disabled by default**. Uncomment `order(...)` calls to activate live trading.
* Ensure your system clock is synced — time differences can affect API behavior.

---

## 📄 License

MIT License — feel free to use and modify with attribution.

---

Let me know if you'd like to include example TradingView alert templates or a [deployment guide](f).

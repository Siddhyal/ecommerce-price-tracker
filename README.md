# 🛒 E-Commerce Price Tracker

An automated e-commerce price monitoring system built with Python.

The application tracks product prices, stores historical price data, compares prices against user-defined targets, and sends email alerts when a target price is reached.

---

## 🚀 Features

- 🔗 Add products using their URLs
- 🕷️ Automatically scrape product information
- 💰 Track current product prices
- 🎯 Set custom target prices
- 💾 Store products and price history in SQLite
- 📈 Visualize price history
- 🔄 Manually check prices
- ⏰ Automatically check prices every hour
- 📧 Send email alerts when target prices are reached
- 🔔 Prevent duplicate price alerts
- 📊 Dashboard with product and price statistics

---

## 🧠 How It Works

```text
                Product URL
                     │
                     ▼
              ┌─────────────┐
              │ Web Scraper │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   SQLite    │
              │  Database   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │Price Checker│
              └──────┬──────┘
                     │
             ┌───────┴────────┐
             ▼                ▼
       Target reached?     Above target
             │
             ▼
       📧 Email Alert
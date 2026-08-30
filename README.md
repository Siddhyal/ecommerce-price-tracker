# 🛒 E-Commerce Price Tracker

A Python-based web application that automatically tracks e-commerce product prices, stores price history, and sends email notifications when a product reaches the user's target price.

## 📸 Dashboard Preview

![E-Commerce Price Tracker Dashboard]

## 📌 Overview

The E-Commerce Price Tracker helps users monitor product prices without repeatedly checking websites manually.

Users can add a product URL and set a target price. The application fetches the current product price, stores historical price data, and compares the latest price with the target price.

When the target price is reached, the system can send an email notification.

---

## ✨ Features

- 🔗 Track products using their URL
- 🕷️ Extract product information using web scraping
- 💰 Monitor current product prices
- 🎯 Set a custom target price
- 💾 Store products and price history using SQLite
- 📈 View price history through interactive charts
- 🔄 Manually check product prices
- ⏰ Automatically check prices using a scheduler
- 📧 Send email alerts when the target price is reached
- 🔔 Prevent duplicate email notifications
- 📊 Dashboard with product and price statistics

---

## 🖥️ Dashboard

The Streamlit dashboard provides:

- Number of tracked products
- Number of price records
- Current product prices
- Target prices
- Target-price status
- Alert status
- Product links
- Historical price charts
- Manual price checking

---

## ⚙️ How It Works

```text
                Product URL
                     │
                     ▼
             ┌──────────────┐
             │ Web Scraper  │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │    SQLite    │
             │   Database   │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ Price Checker│
             └──────┬───────┘
                    │
             ┌──────┴───────┐
             │              │
             ▼              ▼
       Target reached?   Above target
             │
             ▼
        📧 Email Alert

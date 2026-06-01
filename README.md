# FinTech Expense Tracker with Automated Budget Alerts

A backend-driven personal finance application designed to handle multiple user accounts, track multi-category expenses, and trigger real-time system alerts when a user approaches their monthly budget threshold.

## 🚀 Key Features
* **Multi-Account & Category Management:** Tracks unique user accounts with custom categories like Food, Rent, and Travel.
* **Data Types Integrity:** Flawlessly handles financial precision using strict database data types (`DECIMAL` for currency and `DATE` for timestamps).
* **"Wow" Backend Logic:** Utilizes SQL aggregate functions (`SUM`, `GROUP BY`) to generate instant monthly financial breakdowns.
* **Automated Live Listener:** A background trigger function that throws a system alert the exact moment a user's spending in any category crosses **90%** of their manually defined budget.

## 🛠️ Tech Stack
* **Database:** MySQL
* **Backend Language:** Python (or Node.js)
* **Database Connector:** `mysql-connector-python`

## 📊 Database Schema

The project relies on three relational tables designed for optimal integrity:
1.  **`users`**: Stores core user accounts information.
2.  **`budgets`**: Holds user-defined monthly limits for individual categories.
3.  **`expenses`**: Tracks every financial transaction with accurate dates and amounts.

## 💻 How to Setup and Run

### 1. Prerequisites
Make sure you have MySQL and Python installed on your local machine.

### 2. Database Setup
Log into your MySQL instance and run the queries provided in the `schema.sql` file to build the architecture.

### 3. Install Dependencies
```bash
pip install mysql-connector-python
-- Create the project database framework safely if it doesn't exist
CREATE DATABASE IF NOT EXISTS fintech_tracker;
USE fintech_tracker;

-- 1. Create Users Table (Stores separate individual account profiles)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- 2. Create Budgets Table (Where monthly limits are defined per category per user)
CREATE TABLE IF NOT EXISTS budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category VARCHAR(50) NOT NULL,
    monthly_limit DECIMAL(10, 2) NOT NULL, -- DECIMAL keeps currency numbers 100% exact without rounding bugs
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. Create Expenses Table (Tracks transactional amounts with absolute dates)
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2) NOT NULL, -- Matches budget decimal structure for seamless math evaluations
    category VARCHAR(50) NOT NULL,
    expense_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 4. Clean up any leftover test data rows to keep execution safe
DELETE FROM budgets;
DELETE FROM expenses;
DELETE FROM users;

-- 5. Inject complete testing records to simulate features instantly
-- Create a test profile user named Alex (User ID: 1)
INSERT INTO users (user_id, username, email) 
VALUES (1, 'Alex', 'alex@test.com');

-- Set explicit manual budget caps for our testing user profile
INSERT INTO budgets (user_id, category, monthly_limit) VALUES (1, 'Food', 1000.00);
INSERT INTO budgets (user_id, category, monthly_limit) VALUES (1, 'Travel', 500.00);
INSERT INTO budgets (user_id, category, monthly_limit) VALUES (1, 'Rent', 2000.00);
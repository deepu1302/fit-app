-- FitLife Tracker Database Schema for MySQL
-- Run this script to create the database and tables

-- Create database
CREATE DATABASE IF NOT EXISTS fitlife_tracker;
USE fitlife_tracker;

-- Users table (stores user profiles)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    age INT NOT NULL,
    height INT NOT NULL,
    weight DECIMAL(5,1) NOT NULL,
    goal ENUM('lose', 'gain', 'maintain') NOT NULL,
    diet_type ENUM('vegetarian', 'non-vegetarian', 'both') NOT NULL,
    health_conditions VARCHAR(255) DEFAULT 'none',
    allergies VARCHAR(255) DEFAULT 'none',
    period ENUM('week', 'month', '3months') NOT NULL,
    language ENUM('english', 'hindi', 'telugu') DEFAULT 'english',
    badge_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Weight logs table
CREATE TABLE IF NOT EXISTS weight_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    weight DECIMAL(5,1) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- Badges table (stores earned badges)
CREATE TABLE IF NOT EXISTS badges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    badge_name VARCHAR(100) NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- Insert sample data (optional - for testing)
-- INSERT INTO users (name, age, height, weight, goal, diet_type, period) 
-- VALUES ('TestUser', 25, 170, 70.0, 'lose', 'both', 'month');

# 🌌 AstronoInsightDaily

## 🚀 Overview
AstroInsightDaily is a Flask-based web application that provides the latest space-related news from multiple sources using the **Spaceflight News API**. It also features **user authentication** (**signup/login**) and a **NASA Astronomy Picture of the Day** (**APOD**) section.

## ✨ Features
+ 📰 **Latest Astronomy News** – Aggregates space-related articles from Spaceflight News API (No API key required)
+ 🔍 **Save for Later** – Users can save articles for future reading
+ 📷 **NASA APOD Integration** – Displays NASA’s daily astronomy image with descriptions
+ 👤 **User Authentication** – Signup/Login system with user data stored in MongoDB
+ ⚡ **AJAX for Smooth User Experience** – Reduces page reloads by dynamically fetching content
+ 🗄️ **MongoDB Storage** – Saves user accounts and selected articles

## 🛠️ Tech Stack
+ **Backend**: Python, Flask
+ **Frontend**: HTML, CSS, Bootstrap, JavaScript
+ **Database**: MongoDB
+ **APIs Used**: Spaceflight News API (No API Key Required), NASA APOD API

## 📌 How to Run

1. Clone the repository:
   `git clone https://github.com/yourusername/AstroInsightDaily.git`

2. Install dependencies:
   `pip install -r requirements.txt`
   
3. Set up MongoDB or any other database of your choosing for user authentication and saved articles
4. Get a NASA API key for APOD integration.
5. Run the Flask app:
   `flask run`
6. Open in browser: `http://127.0.0.1:5000/`

🚀 **Live Demo:** [Visit the Website](https://astroinsightdaily.onrender.com)




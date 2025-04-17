# 🏋️‍♀️ FitGo: Integrated Fitness and Wellness Platform

## 🚀 Overview
**FitGo** is a comprehensive **fitness and wellness tracking platform** that unifies workout planning, nutrition tracking, health monitoring, and professional guidance into one streamlined app.

Unlike traditional fitness apps focused on isolated features, FitGo brings everything together in a cohesive dashboard for a smarter health journey.

### 👥 Who It's For
- **Fitness Enthusiasts** – Track performance metrics and optimize workouts
- **Personal Trainers** – Manage client programs and monitor progress
- **Nutritionists** – Create and update meal plans tailored to client needs
- **Gym Owners** – Monitor facility usage and member engagement

---

## ✨ Key Features
- 🏋️‍♂️ **Personalized Workout Tracking**: Log exercises, sets, reps, and weights
- 🍎 **Nutrition Management**: Track meals, calories, and macronutrients
- 📊 **Health Metrics Dashboard**: Monitor vitals like heart rate and sleep
- 🏆 **Leaderboards**: Join challenges and stay motivated with community rankings
- 👩‍⚕️ **Professional Integration**: Collaborate with trainers and nutritionists

---

## 🏗️ Technical Architecture

FitGo is built using a modern **microservices architecture**:

- **Frontend**: [Streamlit](https://streamlit.io/) for interactive UI (port `8501`)
- **Backend**: [Flask RESTful API](https://flask.palletsprojects.com/) (port `4000`)
- **Database**: [MySQL](https://www.mysql.com/) for persistent storage (port `3200`)
- **Containerization**: [Docker](https://www.docker.com/) and Docker Compose for portability and isolation

---

## ⚙️ Getting Started

### ✅ Prerequisites
- Docker & Docker Compose
- Git

### 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fitgo.git
   cd fitgo

2. **Start all containers**
   ```bash
   docker compose up

3. **Access the application***
   Frontend: HTTP://localhost:8501

---

## 🛢️ Database Management

**Start only the database**
```bash
docker compose up db -d
```

**Stop the database**
```bash
docker compose down db
```

---

## 📦 Container Overview
app ------ Streamlit frontend ------ port: 8501
api ------ Flask backend API ------- port: 4000
db ------- MySQL Database ---------- port: 3200

---

## 🧪 Development Notes
### 📁 Database Initialization
The MySQL database is automatically initialized using .sql scripts located in the database-files/ directory. These scripts create necessary tables and insert sample data so you can test features without manual setup.

---

## 📚 API Documentation
The REST API is organized by user roles:
🧍 Client operations: /c/...
🧑‍🏫 Trainer operations: /t/...
🥗 Nutritionist operations: /n/...
🏢 Gym owner operations: /go/...

You can interact with endpoints using:
GET to retrieve data
POST to add new data
PUT to update data

🧠 All API calls return JSON and follow RESTful conventions.

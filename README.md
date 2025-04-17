# FitGo: Integrated Fitness and Wellness Platform

## Overview
FitGo is a comprehensive fitness and wellness tracking platform that combines workout planning, nutrition tracking, health monitoring, and professional guidance into one streamlined app. Our goal is to resolve the issue of utilizing different apps for these tasks by bringing it all together in a cohesive dashboard that enables users to identify key trends/patterns and make informed lifestyle choices based on reliable data. 

### Who It's For
- **Fitness Enthusiasts** – Track performance metrics, log workouts, participate in competitions
- **Personal Trainers** – Manage client workout plans and monitor progress
- **Nutritionists** – Create and update meal plans tailored to client dietary needs/restrictions
- **Gym Owners** – Manage community-wide events, employee/client rosters, and gym equipment

## Key Features
- **Personalized Workout Tracking**: Log exercises, sets, reps, and weights
- **Nutrition Management**: Track meals, calories, and macronutrients
- **Health Metrics Dashboard**: Monitor vitals like heart rate and sleep
- **Leaderboards**: Join challenges and stay motivated with community rankings

## Demo Links
- Google Drive: https://drive.google.com/file/d/1Q7rfANnfl-85hw9fbAiiyqqyN6OVF93U/view?usp=sharing
- YouTube: https://www.youtube.com/watch?v=g4hzAG4t0kw

## Tech Stack

- **Frontend**: Streamlit 
- **Backend**: Flask REST API
- **Database**: MySQL
- **Containerization**: Docker


## Getting Started

### Installation & Setup

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/fitgo.git
   cd fitgo

2. Start all containers
   ```bash
   docker compose up

3. Access the application
   Frontend: HTTP://localhost:8501


## Database Management

Start only the database
```bash
docker compose up db -d
```

Stop the database
```bash
docker compose down db
```

## Docker Container Overview
- app -> Streamlit (Frontend) -> port: 8501  
- api -> Flask API (Backend) ->  port: 4000  
- db -> MySQL Database -> port: 3200


## API Structure
The REST API is organized by creating blueprints for each of our four user personas with the following prefixes:
- Client: /c/...
- Trainer operations: /t/...
- Nutritionist operations: /n/...
- Gym owner operations: /go/...

All blueprints contain GET, POST, PUT, and DELETE routes to retrieve, add, update, and delete data based on the given persona's needs. 

### By CS 3200 Course Project team members: Sebastian Cheung, Saachi Bhatia, Tarun Anbarasu, Naisha Mistry, and Andrei Zubek

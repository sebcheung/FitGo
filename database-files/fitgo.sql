-- Creating the FitGo Database
DROP DATABASE IF EXISTS FitGo;
CREATE DATABASE IF NOT EXISTS FitGo;

-- Using the newly created FitGo Database
USE FitGo;

-- Creating the CLIENT table, a central part of our application
CREATE TABLE Client (
    Client_ID int AUTO_INCREMENT NOT NULL,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    Email varchar(50) NOT NULL,
    Join_Date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Sex varchar(10) NOT NULL,
    Age int NOT NULL,
    Weight int NOT NULL, #in pounds (LB)
    Height decimal(5,2) NOT NULL,
    Phone_Number varchar(15),
    PRIMARY KEY (Client_ID)
);

-- Creating the EVENT
CREATE TABLE Event (
    Event_ID int AUTO_INCREMENT NOT NULL,
    Event_Location varchar(50) NOT NULL,
    Event_Description text,
    Host_Name varchar(100),
    Sponsor varchar(100),
    Start_Time datetime NOT NULL,
    Event_Name varchar(50) NOT NULL,
    Event_Date date NOT NULL,
    PRIMARY KEY (Event_ID)
);

-- Bridge Table for EVENT_ATTENDEES
CREATE TABLE Event_Attendee (
    Client_ID int NOT NULL,
    Event_ID int NOT NULL,
    PRIMARY KEY (Client_ID, Event_ID),
    CONSTRAINT fk_00 FOREIGN KEY (Client_ID) REFERENCES Client (Client_ID),
    CONSTRAINT fk_01 FOREIGN KEY (Event_ID) REFERENCES Event (Event_ID)
);

-- Table for GYM OWNER
CREATE TABLE Gym_Owner (
    Owner_ID int AUTO_INCREMENT NOT NULL,
    GymName varchar(100) NOT NULL,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    Age int,
    PRIMARY KEY (Owner_ID)
);

-- Table for EMPLOYEE
CREATE TABLE Employee (
    Employee_ID int AUTO_INCREMENT NOT NULL,
    Boss_ID int NOT NULL,
    Manager_ID int NULL,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    Hire_Date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Age int,
    SSN varchar(15) NOT NULL,
    Address varchar(100),
    PRIMARY KEY (Employee_ID),
    CONSTRAINT fk_02 FOREIGN KEY (Manager_ID) REFERENCES Employee (Employee_ID),
    CONSTRAINT fk_03 FOREIGN KEY (Boss_ID) REFERENCES Gym_Owner (Owner_ID)
);

-- Bridge table for Employees working an Event
CREATE TABLE Event_Worker (
    Event_ID int NOT NULL,
    Employee_ID int NOT NULL,
    PRIMARY KEY (Event_ID, Employee_ID),
    CONSTRAINT fk_04 FOREIGN KEY (Event_ID) REFERENCES Event (Event_ID),
    CONSTRAINT fk_05 FOREIGN KEY (Employee_ID) REFERENCES Employee (Employee_ID)
);

-- Table for GYM
CREATE TABLE Gym (
    Gym_ID int AUTO_INCREMENT NOT NULL,
    Owner_ID int NOT NULL,
    Name varchar(100),
    Location varchar(100),
    PRIMARY KEY (Gym_ID),
    CONSTRAINT fk_06 FOREIGN KEY (Owner_ID) REFERENCES Gym_Owner (Owner_ID)
);

-- Table for EQUIPMENT
CREATE TABLE Equipment (
    Equipment_ID int AUTO_INCREMENT NOT NULL,
    Gym_ID int NOT NULL,
    Type varchar(100),
    Purchase_Date date,
    Name varchar(100) NOT NULL,
    Status tinyint(1) DEFAULT 1, -- 1 for active, 0 for inactive, default active
    Brand varchar(100),
    PRIMARY KEY (Equipment_ID),
    CONSTRAINT fk_07 FOREIGN KEY (Gym_ID) REFERENCES Gym (Gym_ID)
);

-- Table for Health Metrics (added a date column to be able to collect different days of health metrics for users, changed PK to Record ID)
CREATE TABLE Health_Metrics (
    Record_ID int AUTO_INCREMENT NOT NULL,
    User_ID int NOT NULL,
    Date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Heart_Rate int,
    Calories_Burned int,
    Sleep_Duration int, -- in minutes
    Blood_Pressure_Level varchar(200),
    Water_Intake decimal(4, 2),
    Caloric_Intake int,
    Body_Fat_Percentage decimal(4, 2),
    PRIMARY KEY (Record_ID),
    CONSTRAINT fk_08 FOREIGN KEY (User_ID) REFERENCES Client (Client_ID)
);

-- Table for Progress Visuals
CREATE TABLE Progress_Visuals (
    Visual_ID int AUTO_INCREMENT NOT NULL,
    Bar_Graph varchar(255),
    Pie_Chart varchar(255),
    Scatter_Plot varchar(255),
    PRIMARY KEY (Visual_ID)
);

-- Bridge Table for Health Metrics and Progress Visuals
CREATE TABLE Metrics_Visuals (
    Visual_ID int AUTO_INCREMENT NOT NULL,
    Record_ID int NOT NULL,
    PRIMARY KEY (Visual_ID, Record_ID),
    CONSTRAINT fk_09 FOREIGN KEY (Visual_ID) REFERENCES Progress_Visuals (Visual_ID),
    CONSTRAINT fk_10 FOREIGN KEY (Record_ID) REFERENCES Health_Metrics (Record_ID)
);

-- Table for Visual Colors
CREATE TABLE Progress_Colors (
    Visual_ID int NOT NULL,
    Color varchar(100) NOT NULL,
    PRIMARY KEY (Visual_ID, Color),
    CONSTRAINT fk_11 FOREIGN KEY (Visual_ID) REFERENCES Progress_Visuals (Visual_ID)
);

-- Table for Visual Labels
CREATE TABLE Progress_Labels (
    Visual_ID int NOT NULL,
    Label varchar(200) NOT NULL,
    PRIMARY KEY (Visual_ID, Label),
    CONSTRAINT fk_12 FOREIGN KEY (Visual_ID) REFERENCES Progress_Visuals (Visual_ID)
);

-- Table for Meal Plans
CREATE TABLE Meal_Plans (
    Plan_ID int AUTO_INCREMENT NOT NULL,
    User_ID int NOT NULL,
    Fiber_Goal int DEFAULT 0,
    Fat_Goal int DEFAULT 0,
    Carb_Goal int DEFAULT 0,
    Protein_Goal int DEFAULT 0,
    Calories int DEFAULT 0,
    Start_Date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    End_Date date NOT NULL,
    PRIMARY KEY (Plan_ID),
    CONSTRAINT fk_13 FOREIGN KEY (User_ID) REFERENCES Client (Client_Id)
        ON DELETE CASCADE
);

-- Table for Meals
CREATE TABLE Meals (
    Meal_ID int AUTO_INCREMENT NOT NULL,
    Plan_ID int NOT NULL,
    Name varchar(200) NOT NULL,
    Type varchar(200) NOT NULL,
    Recipe text,
    Ingredients text,
    Fiber_Intake int DEFAULT 0,
    Carb_Intake int DEFAULT 0,
    Calories int DEFAULT 0,
    Fat_Intake int DEFAULT 0,
    Protein_Intake int DEFAULT 0,
    PRIMARY KEY (Meal_ID),
    CONSTRAINT fk_14 FOREIGN KEY (Plan_ID) REFERENCES Meal_Plans (Plan_ID)
        ON DELETE CASCADE
);

-- Table for Meal Logs
CREATE TABLE Meal_Logs (
    Log_ID int AUTO_INCREMENT NOT NULL,
    User_ID int NOT NULL,
    Meal_ID int NOT NULL,
    Time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Fiber_Intake int DEFAULT 0,
    Carb_Intake int DEFAULT 0,
    Calories int DEFAULT 0,
    Fat_Intake int DEFAULT 0,
    Protein_Intake int DEFAULT 0,
    PRIMARY KEY (Log_ID),
    CONSTRAINT fk_15 FOREIGN KEY (User_ID) REFERENCES Client (Client_Id)
        ON DELETE CASCADE,
    CONSTRAINT fk_16 FOREIGN KEY (Meal_ID) REFERENCES Meals (Meal_ID)
        ON DELETE CASCADE
);

-- Table for Workout Logs
CREATE TABLE Workout_Logs (
    WorkoutLog_ID int AUTO_INCREMENT NOT NULL,
    User_ID int NOT NULL,
    Total_Weight int DEFAULT 0,
    Total_Time decimal(4,2) DEFAULT 0,
    PRIMARY KEY (WorkoutLog_ID),
    CONSTRAINT fk_17 FOREIGN KEY (User_ID) REFERENCES Client (Client_Id)
        ON DELETE CASCADE
);

-- Table for Workout Days
CREATE TABLE Workout_Day (
    Day_ID int AUTO_INCREMENT NOT NULL,
    Day_of_Week text NOT NULL,
    User_ID int NOT NULL,
    PRIMARY KEY (Day_ID),
    CONSTRAINT fk_18 FOREIGN KEY (User_ID) REFERENCES Client (Client_Id)
        ON DELETE CASCADE
);

-- Table for Exercises
CREATE TABLE Exercises (
    Exercise_ID int AUTO_INCREMENT NOT NULL,
    Name varchar(200) NOT NULL,
    Num_Sets int DEFAULT 0,
    Num_Reps int DEFAULT 0,
    PRIMARY KEY (Exercise_ID)
);

-- Bridge Table for Workout Day and Workout Log
CREATE TABLE Log_Exercises (
    WorkoutLog_ID int NOT NULL,
    Day_ID int NOT NULL,
    PRIMARY KEY (WorkoutLog_ID, Day_ID),
    CONSTRAINT fk_19 FOREIGN KEY (WorkoutLog_ID) REFERENCES Workout_Logs (WorkoutLog_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_20 FOREIGN KEY (Day_ID) REFERENCES Workout_Day (Day_ID)
        ON DELETE CASCADE
);

-- Bridge Table for Days and Exercises
CREATE TABLE Day_Exercises (
    Exercise_ID int NOT NULL,
    Day_ID int NOT NULL,
    PRIMARY KEY (Exercise_ID, Day_ID),
    CONSTRAINT fk_21 FOREIGN KEY (Exercise_ID) REFERENCES Exercises (Exercise_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_22 FOREIGN KEY (Day_ID) REFERENCES Workout_Day (Day_ID)
        ON DELETE CASCADE
);

CREATE TABLE Trainer (
    Trainer_ID int AUTO_INCREMENT,
    Name varchar(255) NOT NULL,
    Age int CHECK (Age >= 18), -- trainers must be adults
    Degree varchar(255),
    Years_experience int CHECK (Years_experience >= 0),
    Certification varchar(255),
    PRIMARY KEY (Trainer_ID)
);

CREATE TABLE Message (
    Message_ID int AUTO_INCREMENT NOT NULL,
    Content text NOT NULL,
    Sent_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    Client_ID int NOT NULL,
    Trainer_ID int NOT NULL,
    CONSTRAINT fk_23 FOREIGN KEY (Client_ID) REFERENCES Client (Client_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_24 FOREIGN KEY (Trainer_ID) REFERENCES Trainer (Trainer_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_25 PRIMARY KEY (Message_ID)
);

CREATE TABLE Resources (
    Resources_ID int AUTO_INCREMENT NOT NULL,
    Title varchar(255) NOT NULL,
    URL text NOT NULL,
    Type varchar(100), -- ex: "video", "article", "pdf"
    Trainer_ID int, -- optional: who originally uploaded/shared the resource
    CONSTRAINT fk_26 FOREIGN KEY (Trainer_ID) REFERENCES Trainer (Trainer_ID)
        ON DELETE SET NULL,
    CONSTRAINT fk_27 PRIMARY KEY (Resources_ID)
);

CREATE TABLE Trainer_Resources (
    Resources_ID int NOT NULL,
    Trainer_ID int NOT NULL,
    PRIMARY KEY (Resources_ID, Trainer_ID),
    CONSTRAINT fk_28 FOREIGN KEY (Resources_ID) REFERENCES Resources (Resources_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_29 FOREIGN KEY (Trainer_ID) REFERENCES Trainer (Trainer_ID)
        ON DELETE CASCADE
);

CREATE TABLE Client_Resources (
    Resources_ID int NOT NULL,
    Client_ID int NOT NULL,
    PRIMARY KEY (Resources_ID, Client_ID),
    CONSTRAINT fk_30 FOREIGN KEY (Resources_ID) REFERENCES Resources (Resources_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_31 FOREIGN KEY (Client_ID) REFERENCES Client (Client_ID)
        ON DELETE CASCADE
);

CREATE TABLE Reminders (
    Reminder_ID int AUTO_INCREMENT NOT NULL,
    Creator_ID int NOT NULL, -- could be a client, trainer, or general user
    Duration int, -- duration in minutes
    Date date NOT NULL,
    Time time NOT NULL,
    PRIMARY KEY (Reminder_ID),
    CONSTRAINT fk_32 FOREIGN KEY (Creator_ID) REFERENCES Client (Client_ID)
        ON DELETE CASCADE
);

CREATE TABLE Training_Session (
    Session_ID int AUTO_INCREMENT NOT NULL,
    Client_ID int NOT NULL,
    Trainer_ID int NOT NULL,
    Status text,
    Date_time datetime NOT NULL,
    Class_description text,
    Max_participants  int DEFAULT 15,
    PRIMARY KEY (Session_ID),
    CONSTRAINT fk_33 FOREIGN KEY (Client_ID) REFERENCES Client (Client_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_34 FOREIGN KEY (Trainer_ID) REFERENCES Trainer (Trainer_ID)
        ON DELETE CASCADE
);

CREATE TABLE Leaderboard (
    Leaderboard_ID int AUTO_INCREMENT NOT NULL,
    User_ID int NOT NULL,
    Username varchar(255) NOT NULL,
    Ranks varchar(100),
    Total_Points int DEFAULT 0,
    Region varchar(255) DEFAULT 'UNKNOWN',
    Profile_Pic varchar(255),
    PRIMARY KEY (Leaderboard_ID),
    CONSTRAINT fk_35 FOREIGN KEY (User_ID) REFERENCES Client (Client_ID)
        ON DELETE CASCADE
);

CREATE TABLE Workout_Plans (
    Plan_ID int AUTO_INCREMENT NOT NULL,
    Client_ID int,
    Trainer_ID int NOT NULL,
    Goal varchar(255),
    Exercise_List varchar(255),
    Duration int, -- in minutes
    PRIMARY KEY (Plan_ID),
    CONSTRAINT fk_36 FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
        ON DELETE CASCADE,
    CONSTRAINT fk_37 FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)
        ON DELETE CASCADE
);

CREATE TABLE Nutritionist (
    Nutritionist_ID int AUTO_INCREMENT NOT NULL,
    Client_ID int,
    Years_of_Experience int,
    Degree varchar(255),
    License varchar(255),
    Name varchar(255),
    PRIMARY KEY (Nutritionist_ID),
    CONSTRAINT fk_38 FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID)
        ON DELETE CASCADE
);

-- Table for Medical Record
CREATE TABLE Medical_Record (
    MedicalRecord_ID INT AUTO_INCREMENT,
    Client_ID INT NOT NULL,
    User_ID INT,
    Nutritionist_ID  INT NOT NULL,
    Date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    DateLast_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Dietary_pref TEXT,
    PRIMARY KEY (MedicalRecord_ID),
    FOREIGN KEY (Client_ID) REFERENCES Client (Client_ID)
);

-- Table for Allergies
CREATE TABLE Medical_Allergy (
    Allergy_ID INT AUTO_INCREMENT,
    MedicalRecord_ID INT NOT NULL,
    Allergy VARCHAR(255) NOT NULL,
    PRIMARY KEY (Allergy_ID),
    FOREIGN KEY (MedicalRecord_ID) REFERENCES Medical_Record (MedicalRecord_ID)
        ON DELETE CASCADE
);

-- Table for Intolerances
CREATE TABLE Medical_Intolerance (
    Intolerance_ID INT AUTO_INCREMENT,
    MedicalRecord_ID INT NOT NULL,
    Intolerance VARCHAR(255) NOT NULL,
    PRIMARY KEY (Intolerance_ID),
    FOREIGN KEY (MedicalRecord_ID) REFERENCES Medical_Record (MedicalRecord_ID)
        ON DELETE CASCADE
);

-- Table for Dietary/Medical Restrictions
CREATE TABLE Medical_Restriction (
    Restriction_ID INT AUTO_INCREMENT,
    MedicalRecord_ID INT NOT NULL,
    Restriction VARCHAR(255) NOT NULL,
    PRIMARY KEY (Restriction_ID),
    FOREIGN KEY (MedicalRecord_ID) REFERENCES Medical_Record (MedicalRecord_ID)
        ON DELETE CASCADE
);

-- Table for Conditions
CREATE TABLE Medical_Condition (
    Condition_ID INT AUTO_INCREMENT,
    MedicalRecord_ID INT NOT NULL,
    Med_Condition VARCHAR(255) NOT NULL,
    PRIMARY KEY (Condition_ID),
    FOREIGN KEY (MedicalRecord_ID) REFERENCES Medical_Record (MedicalRecord_ID)
        ON DELETE CASCADE
);

-- Table for Medications
CREATE TABLE Medical_Medication (
    Medication_ID INT AUTO_INCREMENT,
    MedicalRecord_ID INT NOT NULL,
    Medication VARCHAR(255) NOT NULL,
    PRIMARY KEY (Medication_ID),
    FOREIGN KEY (MedicalRecord_ID) REFERENCES Medical_Record (MedicalRecord_ID)
        ON DELETE CASCADE
);

-- Table for Fitness Record
CREATE TABLE Fitness_Record (
    FitnessRecord_ID INT AUTO_INCREMENT,
    Focus_topics TEXT,
    Fitness_level ENUM ('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    Goals TEXT,
    Workout_freq VARCHAR(50),
    User_ID INT NOT NULL,
    PRIMARY KEY (FitnessRecord_ID),
    FOREIGN KEY (User_ID) REFERENCES Client (Client_ID)
        ON DELETE CASCADE
);

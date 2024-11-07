# TimeLens

What is TimeLens:
  TimeLens aims to be a productivity/activity tracker for your Windows PC. I aim to provide insights and meaningful metrics using the WindowsAPI, such as total time on programs, and how often you switch tasks. A more specific breakdown of the inspiration is provided below, but overall I started this app to try and find out my own computer habits. While there are other tools, I wanted to delve into the WindowsAPI for a long time and finally got to doing it.


Problem: 
- While there are many activity/time trackers and logs, the main concern is where this data is going.
Solution:
- A product that is open-source, so the user knows where everything is going (their own control).
- Ease of use with simple gui.
- Gives insightful data on what the user is actually doing on their computer.

Inspiration: Most people nowadays are aware of dangers of social media and "doomscrolling", short-form content e.t.c. I found that while I didn't engage as much with the traditional apps like Instagram, Tik-tok and others, I would use Youtube a lot on my phone. Now cutting that down, I found out about Youtube tracking how much time you use it across your account. My usage shocked me, so that inspired me to make this application and learn more about myself and my computer habits.

Market and Audience:
- People interested in tracking their computer habits.

Value Proposition:
- What is the unique value proposition of my product?
  - The application is focused on tracking personal data, but with no external snooping or any privacy concerns as it is run locally. The user will have the choice on how to export their data, whether they want it to be in simple text documents, or even onto specific spreadsheets that can provide user-specific insight.
 

Feasibility:
- Key Features:
  - Simple GUI that is easy to start.
  - Very low utilization rate (doesnt cause any sort of lag)
  - Data Tracking:
    - Application Name
    - Time Started
    - Time Ended
    - RAW DATA (Why do we want Raw data? This is unfiltered and the most basic so that if the user wants to do specific analysis, they can do so with the most barebones and interpret how they want to)

  Tech Stack:
  - Python (Initial data formatting and gathering)
  - SQLite (db)
  - React + ReCharts for Frontend Dashboard
  - Java Spring (Backend)
  - Electron ?


Database Format: 3 Tables
    - focus_logs (raw data)
    - program_insights (per program insights)
    - day_insights (per day insights)
    - month_insights (per month insights)
    - general_insights (general insights)

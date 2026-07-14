Student AI Advisor

A lightweight, interactive Streamlit application designed for students to track their weekly academic performance, log habits, and receive instant, automated AI-driven feedback. The application maintains a local data history, allowing you to easily view trends or correct past entry mistakes.

---

Features

- **Weekly Progress Tracking:** Log your attendance, self-study hours, and weekly performance across quizzes, assignments, and internal exams.
- **Persistent Memory:** All data is saved automatically to a local JSON database (`student_records.json`). If you make a mistake, simply re-select the week, update the info, and save it to overwrite.
- **Smart Form Auto-Population:** Switching between weeks automatically pre-fills the form fields with previously saved data for that specific week.
- **Instant AI Insights:** Receives immediate rule-based recommendations concerning:
  - Low attendance warnings (under 75%).
  - Study hour deficits or praise for exceptional focus.
  - Academic performance deep dives based on total aggregate scores.
  - Qualitative keyword parsing (flags mentions of difficult subjects like *OS* or *Maths* to give specific study advice).
- **Historical Dashboard:** View a complete, tabular breakdown of your semester's progress directly at the bottom of the page.

---
Tech Stack

- **Python 3.8+**
- **Streamlit** (For the web interface)
- **Pandas** (For historical data rendering)

---

Installation & Setup

Follow these simple steps to get the application up and running locally.

1. Clone or Create the Project Folder
Create a folder on your local machine and ensure you have saved the `app.py` file inside it.

2. Install Dependencies
Open your terminal or command prompt inside the project folder and install the required packages using `pip`:

```bash
pip install streamlit pandas

# **Job Application Tracker (Backend)**

A powerful backend engine to track your job applications by analyzing email data (MBOX files) with automated processing and analytics.

# **Features**

- Layered Architecture: Clean separation of API, Service, and Repository layers for maintainable code.
- Asynchronous Processing: FastAPI BackgroundTasks handle large MBOX files without blocking requests.
- State Machine Logic: Enforces valid application status transitions (e.g., cannot move from ‘Interview’ back to ‘Applied’).
- Data Integrity: Idempotent ingestion ensures no duplicate records.
- Real-time Analytics: MongoDB aggregation pipelines for quick insights on applications and progress.

# **Tech Stack**

- Backend Framework: FastAPI
- Database: MongoDB (Motor for async operations)
- Validation: Pydantic
- Language: Python 3.11+

# **Getting Started**

1. Clone the repo:

git clone https://github.com/yourusername/job-application-tracker.git

1. 
2. Install dependencies:

pip install -r requirements.txt

1. 
2. Run the FastAPI server:

uvicorn app.main:app --reload

# **Key Use Case**

Automates tracking of job applications and provides real-time analytics to help job seekers stay organized and informed.

# **Why This Project?**

- Demonstrates backend design skills, asynchronous processing, and database management.
- Showcases ability to process and analyze real-world data efficiently.
- Highlights experience with Python, FastAPI, MongoDB, and Pydantic.
# Job Application Tracker (Backend)
A professional MBOX-ingestion engine that tracks job search progress via email forensics.

## Technical Highlights
- **Layered Architecture:** Separated into API, Service, and Repository layers for maintainability.
- **Asynchronous Processing:** Utilizes FastAPI BackgroundTasks to process large MBOX files without blocking.
- **State Machine Logic:** Enforces valid status transitions (e.g., cannot move from 'Interview' back to 'Applied').
- **Data Integrity:** Idempotent ingestion logic prevents duplicate application records.
- **Aggregation Pipeline:** Real-time analytics using MongoDB aggregation.

## Tech Stack
- FastAPI, Motor (Async MongoDB), Pydantic, Python 3.11+
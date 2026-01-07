# **Software Requirements Specification (SRS)**

Project Title: Job Application Tracker (Automated MBOX Forensic Engine)

Author: NabilaEln48

Status: Version 1.0 – Baseline Architecture

# **1. Introduction**

**1.1 Purpose**

The Job Application Tracker is a specialized data engineering tool designed to automate the job search lifecycle. By leveraging email forensics, the system extracts structured data from high-volume email archives (MBOX), eliminating manual entry and providing real-time career analytics.

**1.2 Scope**

The system includes:

- Backend: Asynchronous FastAPI service handling ingestion, processing, and state management.
- Database: MongoDB document store for flexible job schemas.
- Analytics: Streamlit-based dashboard for visualizing search progress and trends.

This tool replaces traditional spreadsheets with a database-driven, automated tracking solution.

# **2. Overall Description**

**2.1 Product Perspective**

A standalone productivity suite for job seekers. It allows tracking applications from “Applied” to “Offer” while supporting complex state logic and analytics.

**2.2 User Classes and Characteristics**

- Active Job Seekers: Want to visualize applications and response rates.
- Data Analysts: Interested in email “forensics” and deriving insights from job application data.

# **3. Use Case Diagram & Scenarios**

**3.1 Use Case List**

| **ID** | **Use Case** | **Description** |
| --- | --- | --- |
| UC-1 | Ingest MBOX Data | User uploads an email archive; system parses and saves new records. |
| UC-2 | Manage Application State | User updates job status (e.g., “Applied” → “Interview”). |
| UC-3 | Visualize Analytics | User views a high-level summary of job search progress. |

**3.2 Use Case Scenario: MBOX Ingestion**

Actor: User

Preconditions: Backend connected to MongoDB.

Main Flow:

1. User selects .mbox file via the dashboard.
2. Backend receives file using FastAPI UploadFile.
3. Parser extracts company, position, and timestamp.
4. System performs duplicate check (idempotency).
5. Success message displays total new records added.

# **4. Functional Requirements (FR)**

| **ID** | **Requirement** | **Priority** | **Description** |
| --- | --- | --- | --- |
| FR-01 | Automated Parsing | High | Extract company_name and job_title using regex from email subjects. |
| FR-02 | Duplicate Detection | High | Prevent duplicates using message-id or content hash in MongoDB. |
| FR-03 | Status State Machine | Medium | Enforce valid transitions (e.g., “Rejected” cannot move to “Interview”). |
| FR-04 | Async Ingestion | Medium | Process large MBOX files with background tasks to prevent UI blocking. |
| FR-05 | Export Function | Low | Allow users to download tracking data as CSV or Excel. |

# **5. Non-Functional Requirements (NFR)**

**5.1 Performance**

- Latency: API analytics responses < 200ms.
- Throughput: Parser handles 500+ emails in under 5 seconds.

**5.2 Security & Privacy**

- Data Isolation: All processing occurs locally.
- Environment Safety: Store sensitive credentials in .env files; never hardcode.

**5.3 Reliability**

- Database Connectivity: Retry MongoDB connection 3 times before failing.

# **6. System Models**

**6.1 Data Schema (MongoDB Document)**

{

"application_id": "UUID",

"company": "string",

"position": "string",

"status": "applied | interview | rejected | offer",

"applied_date": "ISO-8601 Timestamp",

"metadata": {

"source_file": "filename.mbox",

"extracted_via": "regex_v1"

}

}
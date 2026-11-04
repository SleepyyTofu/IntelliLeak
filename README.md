# IntelliLeak
### AI-Assisted Incident Response for Data Leakage Detection and Attribution Using Metadata and DLP Analysis

IntelliLeak is a prototype hybrid data leakage detection and attribution system developed as part of my Final Year Project.

The project explores how rule-based Data Loss Prevention (DLP), semantic similarity analysis, and document metadata extraction can work together to identify potentially sensitive information and investigate its possible source.

It provides a web-based platform for document and text analysis, alongside a Chrome browser extension that checks prompts before they are submitted to supported AI web interfaces.

## Project Overview

Traditional rule-based DLP solutions can identify predefined sensitive patterns, but may have difficulty recognising information that has been paraphrased or modified.

IntelliLeak addresses this limitation by combining:

- **Rule-Based DLP:** Identifies predefined sensitive information, including personally identifiable information (PII), credentials, API keys, and other sensitive patterns.
- **Semantic Similarity Analysis:** Uses a Sentence Transformer model to compare submitted content against reference documents and identify potentially similar content.
- **Metadata Extraction:** Extracts available document metadata to support source attribution.
- **Risk Scoring:** Assigns risk scores and severity classifications based on detected findings.
- **Source Attribution:** Uses similarity results and available metadata to identify potential source documents.

## Key Features

### 1. Document and Text Analysis
- Supports text input and document uploads.
- Supports TXT, PDF, and DOCX file formats.
- Detects predefined sensitive information.
- Highlights detected sensitive content.
- Generates risk scores and severity classifications.

### 2. Semantic Similarity Analysis
- Uses the `all-MiniLM-L6-v2` Sentence Transformer model.
- Compares submitted content against synthetic reference documents.
- Helps identify potentially leaked content even when wording has been modified.

### 3. Metadata Extraction and Attribution
- Extracts available metadata from supported PDF and DOCX documents.
- Uses metadata alongside similarity analysis to support source attribution.
- Ranks potential reference documents based on similarity results.

### 4. Browser Extension
- Built using Chrome Manifest V3.
- Monitors prompt input on supported AI web interfaces, including ChatGPT and Gemini.
- Analyses prompt content before submission.
- Displays warnings when potentially sensitive information is detected.

### 5. Risk Assessment
- Applies a weighted risk-scoring mechanism.
- Classifies findings into severity levels: SAFE, LOW, MEDIUM, HIGH, and CRITICAL.

## System Architecture

IntelliLeak consists of two main components:

**Web Application**
- Flask-based backend.
- Document upload and text analysis.
- Sensitive information detection.
- Semantic similarity analysis.
- Metadata extraction.
- Risk scoring and source attribution.
- MySQL-based analysis logging.

**Browser Extension**
- Chrome Manifest V3.
- Prompt monitoring on supported AI web interfaces.
- Pre-submission sensitive information checking.
- Warning notifications.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming Languages | Python, JavaScript |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Machine Learning | Sentence Transformers, all-MiniLM-L6-v2 |
| Data Processing | scikit-learn, NumPy |
| Database | MySQL |
| Document Processing | PyPDF2, python-docx |
| Browser Extension | Chrome Manifest V3 |
| Version Control | Git, GitHub |

## Project Structure

```text
IntelliLeak/
│
├── extension/             # Chrome browser extension
│
├── models/                # Detection, extraction, scoring,
│                          # similarity and attribution modules
│
├── reference_docs/        # Synthetic reference documents
│
├── static/                # Static assets and upload directory
│   └── uploads/
│
├── templates/             # Flask HTML templates
│   └── index.html
│
├── app.py                 # Main Flask application
├── risk_panel.js          # Risk panel functionality
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- MySQL Server
- Google Chrome
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/SleepyyTofu/IntelliLeak.git
cd IntelliLeak
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

Ensure MySQL Server is running and create the database:

```sql
CREATE DATABASE fyp_leakage_system;
```

Review `models/database.py` and configure the database connection using your local MySQL credentials before running the application.

Do not publish database passwords or other credentials in this repository. The current database configuration is intended for local development and should be secured before any production deployment.

### 5. Run the Application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

### 6. Install the Chrome Extension

1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode**.
4. Select **Load unpacked**.
5. Select the `extension` directory from the cloned repository.
6. Ensure the Flask application is running before testing functionality that communicates with the local backend.

## Reference Dataset

The project uses synthetic reference documents to evaluate semantic similarity and source attribution under controlled conditions.

The dataset includes examples of:
- Financial reports
- Employee records and handbooks
- HR policies
- Network inventory
- Project roadmaps
- Research proposals
- Credential registers

All reference documents are fictional and created for testing purposes.

## Evaluation Approach

The system is designed to be evaluated using controlled data leakage scenarios:

- **Exact Copy:** Direct reproduction of reference content.
- **Partial Excerpt:** Reuse of selected portions of a document.
- **Paraphrased:** Content rewritten while retaining its original meaning.
- **Obfuscated:** Content modified to make direct pattern matching more difficult.

The planned evaluation metrics include:

- Precision
- Recall
- F1-score
- Top-1 and Top-3 attribution accuracy

These metrics support comparison between rule-based detection and the hybrid detection approach.

## Limitations

IntelliLeak is an academic prototype and has several limitations:

### Detection and Analysis
- Detection focuses on textual information rather than images, audio, or other non-textual content.
- Browser monitoring is limited to supported AI web interfaces.
- The browser extension focuses on prompt monitoring and does not provide document upload or metadata extraction.
- Metadata extraction depends on the document format and available metadata fields. TXT files do not provide the same document metadata as PDF and DOCX files.
- Source attribution provides potential matches rather than definitive forensic proof.

### Database
- Requires a locally configured MySQL database to support analysis logging.
- Database connectivity depends on the availability and correct configuration of the local MySQL server.
- Analysis records may not be saved when database connectivity fails.
- Database credentials are currently configured in the backend source code rather than managed through a fully implemented secure configuration system.
- The prototype does not implement enterprise-level database management capabilities such as advanced access control, automated backups, or high availability.

### Deployment
- The system is designed as an academic prototype rather than a production-ready deployment.
- It is not intended to replace enterprise-grade DLP or digital forensic solutions.

## Disclaimer

This project was developed for academic and educational purposes. It uses synthetic reference documents and controlled testing scenarios.

It is a prototype and should not be considered a production-ready enterprise security solution.

## Author

**Darlene Rei Kurniadi**

Dual Degree Computer Science Graduate, specialising in Cybersecurity

Developed as part of my Final Year Project.

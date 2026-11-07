# AI Writing Assistant Pro

An AI-powered writing assistant built with Python, Streamlit, and Google's Gemini API. It helps users generate different types of written content, evaluate AI-generated responses, and track their writing activity.

## Features

- **Blog Writer** – Generate structured blog content.
- **Email Drafter** – Create professional email drafts.
- **Code Explainer** – Understand code through AI-generated explanations.
- **Social Media Writer** – Generate engaging social media content.
- **Customizable Temperature** – Adjust the creativity of AI-generated responses.
- **AI Quality Evaluation** – Evaluate generated content using multiple quality dimensions.
- **Generation History** – Store and review previous generations using SQLite.
- **Usage Analytics** – View writing activity and evaluation scores.
- **Export Options** – Download generated content as TXT or PDF.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | User interface |
| Google Gemini API | AI content generation |
| SQLite | Generation history and storage |
| ReportLab | PDF generation |
| python-dotenv | Environment variable management |

## Project Structure

```text
skillnexis-ai-writing-assistant/
│
├── app.py
├── prompts/
│   ├── __init__.py
│   └── templates.py
│
├── services/
│   ├── __init__.py
│   ├── gemini_service.py
│   ├── prompt_service.py
│   └── evaluation_service.py
│
├── database/
│   ├── __init__.py
│   └── db_manager.py
│
├── utils/
│   └── export.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/skillnexis-ai-writing-assistant.git
cd skillnexis-ai-writing-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own Gemini API key.

**Important:** Never upload your `.env` file or API key to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Application Modules

- Content Generator
- AI Evaluation
- Generation History
- Analytics
- About Project

## Learning Outcomes

- Working with Large Language Model APIs.
- Designing reusable prompt templates.
- Building interactive applications using Streamlit.
- Integrating SQLite for persistent storage.
- Evaluating AI-generated content.
- Implementing TXT and PDF export functionality.

## Developed As

**Skill Nexis – Generative AI & LLMs Internship**


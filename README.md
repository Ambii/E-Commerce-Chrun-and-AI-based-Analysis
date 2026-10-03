# Customer Retention & Churn Intelligence Hub

An AI-powered customer intelligence application that transforms buried, unorganized support reviews into actionable churn risk metrics, complaint categorizations, and automated retention outreach.

---

Problem Statement & Business Value

E-commerce businesses suffer significant customer churn because negative feedback remains hidden inside unstructured support reviews and unresolved tickets. 

* "The Problem:" Manual triage of customer support logs is slow, causing frustrated customers to abandon the brand before support teams can intervene.
* "The Solution:" This application ingests customer transaction and review datasets, automatically identifies high-churn-risk profiles using Pandas analytics, and leverages **Google Gemini 1.5 Flash** to categorize complaints and draft personalized retention offers in real time.

---

# System Architecture & Workflow

┌─────────────────────────┐
│ Raw CSV / Excel Dataset │
└────────────┬────────────┘
│
▼
┌─────────────────────────┐
│ Pandas Analytics Engine │ ──► Computes Churn Risk, Inactivity, Ticket Counts
└────────────┬────────────┘
│
▼
┌─────────────────────────┐
│ Gemini 1.5 Flash Engine │ ──► Sentiment Triage & Complaint Bucket Extraction
└────────────┬────────────┘
│
▼
┌─────────────────────────┐
│ Streamlit Interactive UI│ ──► Renders KPI Dashboard, Filtering & Email Drafts
└─────────────────────────┘

Key Features

- Automated Churn KPI Dashboard:** Instantly flags high-risk customers based on inactivity (`Days_Since_Last_Order > 60`) and support ticket thresholds.
- AI Sentiment & Complaint Triage:** Passes raw review text to Google Gemini to identify root causes (e.g., Shipping Delays, Defective Products, Return Hassles).
- One-Click Retention Email Generator:** Generates tailored, empathetic apology emails with custom promo codes tailored to the customer's specific grievance.
- Dynamic Dataset Support:** Includes a built-in sample dataset generator and allows custom CSV file uploads for live testing.

---

Tech Stack

- Frontend & UI: [Streamlit](https://streamlit.io/) (Python 3.10+)
- Data Processing: [Pandas](https://pandas.pydata.org/)
- AI / LLM Engine: [Google Generative AI SDK](https://ai.google.dev/) (`gemini-1.5-flash`)
- **Environment Management:** `python-dotenv`

---

AI Integration & Prompt Strategy

The application uses targeted zero-shot system prompts sent to `gemini-1.5-flash` to guarantee concise, structured business outputs:

1. Complaint Categorization: Isolates sentiment severity, root causes, and primary complaint buckets from raw feedback.
2. Context-Aware Outreach Generation: Ingests customer order history, inactivity days, and exact complaint text to construct personalized win-back emails under 150 words.

---

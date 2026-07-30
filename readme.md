# Lead Generation AI

> **AI-powered Company Intelligence & Lead Generation Platform using SearXNG, LLMs, Web Scraping, and Financial Data Extraction**

LeadIntel AI is an AI-powered lead generation and company intelligence system that automatically discovers companies within a specific industry and location, searches reliable financial sources, extracts company revenue for a given financial year, validates the extracted information, and exports structured business intelligence.

The goal of this project is to automate the manual process of researching companies and collecting financial information using modern AI and web technologies.

---

## Features

* Industry-based company discovery
* Location-based company search
* AI-powered company extraction
* Financial source discovery
* Annual report detection
* PDF financial report parsing
* Web scraping using BeautifulSoup
* Dynamic website scraping using Playwright
* Revenue extraction using LLMs
* Financial year validation
* Structured JSON output
* CSV export
* Modular pipeline architecture
* Dockerized SearXNG integration

---

## Project Workflow

```text
User Input
    │
    ▼
Industry + Location + Financial Year
    │
    ▼
Query Generator
    │
    ▼
SearXNG Search
    │
    ▼
Company Discovery
    │
    ▼
LLM Company Extraction
    │
    ▼
Financial Search
    │
    ▼
Source Ranking
    │
    ▼
Web Scraper
   ├── BeautifulSoup
   ├── Playwright
   └── PDF Parser
    │
    ▼
Relevant Financial Text
    │
    ▼
LLM Revenue Extraction
    │
    ▼
Validation
    │
    ▼
CSV Export
```

---

## Project Structure

```text
Leadgen-project/

├── main.py
├── requirements.txt
├── README.md
├── .env.example

├── search/
│   ├── searx_client.py
│   └── query_generator.py
│
├── discovery/
│   └── company_finder.py
│
├── scraping/
│   ├── web_scraper.py
│   ├── playwright_scraper.py
│   └── pdf_scraper.py
│
├── financials/
│   ├── company_financials.py
│   ├── revenue_search.py
│   ├── revenue_extractor.py
│   └── validator.py
│
├── llm/
│   └── client.py
│
├── output/
│   └── exporter.py
│
├── data/
│
└── searxng/
```

---

## Tech Stack

### Programming

* Python

### AI / LLM

* Groq API
* Llama 3.3 70B Versatile

### Search

* SearXNG
* Docker

### Scraping

* Requests
* BeautifulSoup
* Playwright
* PyPDF

### Data Processing

* Pandas

### Environment

* Python Virtual Environment
* Docker Compose

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/leadintel-ai.git

cd leadintel-ai
```

---

### Create Virtual Environment

```bash
python -m venv LeadGen
```

Activate

Windows

```bash
LeadGen\Scripts\activate
```

Linux / macOS

```bash
source LeadGen/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

---

### Start SearXNG

```bash
docker compose up -d
```

Verify:

```
http://localhost:8080
```

---

### Run Project

```bash
python main.py
```

---

## Example Input

```
Industry : Steel

Location : India

Financial Year : 2024-25
```

---

## Example Output

| Company      | Revenue           | FY      | Source            |
| ------------ | ----------------- | ------- | ----------------- |
| Tata Steel   | ₹218,542.51 Crore | 2024-25 | Annual Report     |
| JSW Steel    | Revenue Found     | 2024-25 | Financial Results |
| Jindal Steel | Revenue Found     | 2024-25 | Annual Report     |

Results are exported as CSV.

---

## Current Capabilities

* Discover companies using SearXNG
* Extract companies using LLM
* Rank financial sources
* Parse financial PDFs
* Scrape web pages
* Extract revenue information
* Validate financial year
* Export structured CSV

---

## Current Limitations

* Public search engines may temporarily rate-limit automated queries through SearXNG.
* Some private companies do not publicly disclose annual revenue.
* Revenue extraction quality depends on the availability of reliable public financial sources.
* Currently optimized for annual reports and official financial documents.

---

## Planned Improvements

* Search result caching
* LLM response caching
* Retry & exponential backoff
* Adaptive search strategy
* Confidence scoring
* Multi-source verification
* Additional search provider support
* Local LLM support (Ollama)
* Streamlit / FastAPI web interface
* PostgreSQL database
* REST API
* Dockerized deployment
* Authentication
* Interactive dashboard

---

## Why LeadIntel AI?

Traditional company research requires manually:

* Searching companies
* Finding annual reports
* Reading financial documents
* Identifying revenue
* Verifying financial year
* Creating reports

LeadIntel AI automates this workflow into a single intelligent pipeline, reducing manual effort while maintaining evidence-backed financial extraction.

---

## Future Vision

The long-term vision is to transform LeadIntel AI into a production-ready Company Intelligence Platform capable of:

* Discovering companies globally
* Extracting structured business intelligence
* Supporting multiple industries
* Providing AI-assisted company research
* Delivering downloadable reports through a web application

---

## Author

**Shivam Singh**

AI Engineer | Data Science & Machine Learning

GitHub: https://github.com/shivamsingh-itds

LinkedIn: https://www.linkedin.com/in/shivamsingh-itds/

---

## License

This project is licensed under the MIT License.

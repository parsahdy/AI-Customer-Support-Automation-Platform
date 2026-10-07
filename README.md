# AI Customer Support Automation Platform

An AI-powered customer support automation platform designed to automate the processing, routing, knowledge retrieval, and response generation of customer support requests.

The project combines a data-processing pipeline, rule-based workflow engine, Retrieval-Augmented Generation (RAG), local LLM inference, and a FastAPI interface into a modular foundation for an intelligent customer support system.

> **Project Status:** 🚧 In active development

---

## Overview

Customer support teams deal with a large volume of repetitive requests such as technical issues, product questions, shipping problems, payment questions, account issues, and refund requests.

The goal of this project is to build an automation platform that can understand incoming support requests, determine the appropriate workflow, retrieve relevant knowledge when necessary, and generate a contextual response.

The project is designed around the following principle:

```text
Customer Request
       ↓
      API
       ↓
Workflow / Routing
       ↓
Intent & Decision
       ↓
 ┌─────┴─────┐
 ↓           ↓
Workflow     RAG
 ↓           ↓
Action    Knowledge Base
      \     /
       \   /
     Response
```

The architecture is intentionally modular so that individual components can evolve independently as the project moves toward a more agentic customer-support system.

---

## Key Objectives

The main objectives of the project are:

- Automate repetitive customer-support workflows.
- Classify and route incoming support requests.
- Separate deterministic business decisions from LLM-based generation.
- Use RAG when the answer depends on organizational knowledge.
- Generate context-aware support responses.
- Prepare the system for integration with CRM and customer data.
- Build a reproducible data-processing pipeline.
- Evaluate data quality and identify automation opportunities.
- Provide a foundation for future AI-agent capabilities.

---

## Current Capabilities

The current implementation includes several core components:

### Data Pipeline

A reproducible data-processing pipeline is implemented for transforming raw support datasets into standardized, cleaned, and feature-enriched datasets.

The pipeline consists of:

```text
Raw Data
   ↓
Standardization
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Processed / Feature Data
```

The main scripts are:

- `scripts/standardize_data.py`
- `scripts/process_utility.py`
- `scripts/feature_engineering.py`
- `scripts/pipeline.py`

The pipeline can be executed as a single workflow rather than running every processing stage manually.

---

### Knowledge Base and RAG

The project contains a local knowledge-base pipeline for e-commerce support information.

The current knowledge base is built from cleaned FAQ data and consists of:

- Document loading
- Embedding generation
- FAISS vector indexing
- Document persistence
- Semantic retrieval
- Context construction
- LLM response generation

The RAG flow is approximately:

```text
User Question
      ↓
Query Embedding
      ↓
FAISS Search
      ↓
Relevant Documents
      ↓
Prompt Construction
      ↓
LLM
      ↓
Generated Answer
```

The knowledge base artifacts are stored under:

```text
data/knowledge_base/
├── documents.json
└── vector_index.faiss
```

The implementation is located primarily in:

```text
knowledge_base/
├── build_kb.py
├── document_loader.py
├── embedding_model.py
├── retriever.py
└── vector_store.py
```

---

### Workflow Engine

The workflow layer provides deterministic routing and business decision logic.

Supported workflow concepts currently include:

- Refund
- Payment
- Shipping
- Tracking
- Technical support
- Account
- Ordering
- CRM
- Human review

The workflow layer contains separate components for:

- Intent detection
- Intent-to-workflow routing
- Decision rules
- Action selection

This separation allows business rules to remain explicit instead of embedding every decision inside an LLM prompt.

---

### LLM Layer

The project uses an abstraction layer around LLM providers.

The current implementation supports a provider-based factory pattern with:

- Local Ollama models
- OpenAI provider interface
- Hugging Face provider interface

The local implementation uses `OllamaLLM` through LangChain.

The LLM layer is organized as:

```text
llm/
├── config.py
├── llm_factory.py
├── prompt_builder.py
├── prompt_templates.py
└── rag_generator.py
```

The factory pattern allows the model provider to be changed without coupling the rest of the application directly to a specific LLM implementation.

---

### FastAPI Interface

A FastAPI application provides the current API layer.

The API is responsible for exposing the support-question functionality and storing question/answer records through the database layer.

The current API structure includes:

```text
api/
├── app.py
├── database.py
├── models.py
├── routes.py
└── schemas.py
```

The application is designed to become the entry point for the larger customer-support automation workflow.

---

## Architecture

The project is organized into several logical layers:

```text
                    ┌──────────────────────┐
                    │      Customer        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │        API           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Workflow Engine    │
                    │ Intent + Routing     │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ Decision Engine  │   │   Knowledge Base │
          │ Business Rules   │   │      + RAG       │
          └────────┬─────────┘   └────────┬─────────┘
                   │                      │
                   └──────────┬───────────┘
                              ▼
                    ┌──────────────────────┐
                    │         LLM          │
                    │ Response Generation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Support Response   │
                    └──────────────────────┘
```

The architecture is intentionally designed to distinguish between:

- deterministic business logic,
- information retrieval,
- language generation,
- API responsibilities,
- and data processing.

This makes the system easier to test, debug, and extend.

---

## Data Pipeline

The project uses multiple public datasets to model different aspects of customer-support and business automation.

The raw datasets are stored under:

```text
data/raw/
```

The processing pipeline produces:

```text
data/processed/
```

and feature-engineered datasets are stored under:

```text
data/features/
```

### Pipeline Stages

#### 1. Dataset Standardization

Different datasets have different schemas and naming conventions.

The standardization stage converts heterogeneous source datasets into a more consistent internal representation.

#### 2. Data Cleaning

The cleaning stage handles issues such as:

- missing values,
- inconsistent text,
- duplicate or unusable records,
- normalization of categorical values,
- and preparation of textual fields.

#### 3. Feature Engineering

The feature-engineering stage creates additional features that can later be used for:

- analysis,
- classification,
- prioritization,
- routing,
- and automation decisions.

---

## Datasets

The project currently works with several datasets covering customer support, FAQ knowledge, and CRM/sales information.

### Customer IT Support Tickets

Source:

Kaggle — Multilingual Customer Support Tickets

Purpose:

- ticket classification,
- priority analysis,
- support routing,
- analysis of recurring support issues.

---

### Customer Support Ticket Dataset

Source:

Kaggle — Customer Support Ticket Dataset

Purpose:

- multi-class support-ticket categorization,
- customer-support analytics,
- experimentation with support automation.

---

### E-commerce FAQ Dataset

Source:

Kaggle — E-commerce FAQ Chatbot Dataset

Purpose:

- FAQ knowledge base,
- semantic retrieval,
- RAG-based question answering.

The cleaned FAQ data is also used to build the current FAISS knowledge base.

---

### CRM Sales Opportunities

Source:

Kaggle — CRM Sales Opportunities

The dataset contains CRM sales-pipeline records and is intended to support future business-automation capabilities such as:

- opportunity tracking,
- deal analysis,
- sales workflow automation,
- predictive scoring,
- CRM integration.

---

## Business Insights

Exploratory analysis of the support-ticket data identified several useful patterns.

Support demand is concentrated in a relatively small number of categories. Technical Support represents approximately 29.25% of tickets, followed by Product Support at 18.37%, Customer Service at 14.93%, and IT Support at 12.01%.

This concentration indicates that a significant portion of support activity is associated with recurring request types, making these categories strong candidates for automation.

Priority is also associated with ticket category. A chi-square test found a statistically significant relationship between category and priority, with:

```text
χ²(18) = 4667.36
p < 0.05
Cramer's V = 0.29
```

This suggests a moderate association between the type of support request and its priority.

For example, Service Outages and Maintenance contains a particularly high proportion of high-priority tickets, followed by Technical Support and IT Support.

From an automation perspective, this supports a workflow in which ticket classification and priority assessment influence downstream routing and escalation decisions.

More detailed analysis is available in:

```text
notebooks/02_business_eda.ipynb
docs/business_insights.md
```

---

## RAG Design

The current RAG implementation uses a local vector-search architecture.

The general process is:

```text
FAQ Documents
      ↓
Document Conversion
      ↓
Embedding Model
      ↓
FAISS Index
      ↓
Persisted Vector Store
```

At query time:

```text
Question
   ↓
Embedding
   ↓
Vector Similarity Search
   ↓
Top-k Documents
   ↓
Prompt Builder
   ↓
LLM
   ↓
Answer
```

The current implementation uses FAISS for vector retrieval and a Sentence Transformers embedding model.

This approach keeps the knowledge-base layer local and avoids requiring an external vector database for the current stage of development.

---

## Workflow Design

The workflow layer is designed around explicit intents and business rules.

Current workflow categories include:

```text
refund
payment
shipping
tracking
technical
account
ordering
crm
human_review
```

A simplified routing flow is:

```text
Incoming Message
       ↓
Intent Detection
       ↓
Intent → Workflow
       ↓
Priority / Business Rules
       ↓
Action Selection
       ↓
Workflow Execution
```

The separation between routing and decision-making is important because identifying what a customer wants is different from deciding what the system should do about it.

For example, two requests with the same intent may require different actions depending on their priority.

---

## Technology Stack

The main technologies currently used in the project include:

| Area | Technology |
|---|---|
| Programming Language | Python |
| API | FastAPI |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Embeddings | Sentence Transformers |
| Vector Search | FAISS |
| LLM Framework | LangChain |
| Local LLM | Ollama |
| Workflow | Custom workflow / routing layer |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Containerization | Docker |
| Exploration | Jupyter Notebooks |

---

## Project Structure

```text
AI-Customer-Support-Automation-Platform/
│
├── api/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── cleaned/
│   ├── features/
│   └── knowledge_base/
│
├── docs/
│   ├── architecture.md
│   ├── api_design.md
│   ├── business_insights.md
│   ├── data_pipeline.md
│   ├── data_quality.md
│   ├── data_sources.md
│   ├── datasets.md
│   ├── database_design.md
│   ├── deployment.md
│   ├── feature_strategy.md
│   ├── processing_strategy.md
│   ├── requirements.md
│   ├── schema.md
│   └── workflow.md
│
├── evaluation/
│   └── question.csv
│
├── knowledge_base/
│   ├── build_kb.py
│   ├── document_loader.py
│   ├── embedding_model.py
│   ├── retriever.py
│   └── vector_store.py
│
├── llm/
│   ├── config.py
│   ├── llm_factory.py
│   ├── prompt_builder.py
│   ├── prompt_templates.py
│   └── rag_generator.py
│
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   └── 02_business_eda.ipynb
│
├── scripts/
│   ├── standardize_data.py
│   ├── process_utility.py
│   ├── feature_engineering.py
│   └── pipeline.py
│
├── services/
│   └── qa_service.py
│
├── workflow/
│   ├── actions.py
│   ├── decision_engine.py
│   ├── decision_rules.py
│   ├── intent_detector.py
│   ├── intents.py
│   ├── router.py
│   ├── routes.py
│   ├── rules.py
│   ├── workflows.py
│   └── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

Make sure the following are installed:

- Python 3.12+
- Docker
- Docker Compose
- Ollama (if running the local LLM outside Docker)

Clone the repository:

```bash
git clone https://github.com/parsahdy/AI-Customer-Support-Automation-Platform.git
cd AI-Customer-Support-Automation-Platform
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root.

Example configuration:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_automation

OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=<your-local-model>
```

Do not commit API keys, credentials, or other secrets to the repository.

---

## Running with Docker

The project includes a Docker Compose configuration containing:

- FastAPI application
- PostgreSQL
- Ollama

Start the services with:

```bash
docker compose up --build
```

The API is exposed on:

```text
http://localhost:8000
```

The Ollama service is exposed on:

```text
http://localhost:11434
```

---

## Running the Data Pipeline

The complete data-processing pipeline can be executed with:

```bash
python -m scripts.pipeline
```

The pipeline executes:

```text
Dataset Standardization
        ↓
Data Cleaning
        ↓
Feature Engineering
```

Individual stages can also be executed separately when debugging or developing a specific processing step.

---

## Building the Knowledge Base

After preparing the FAQ dataset, the knowledge base can be built using:

```bash
python -m knowledge_base.build_kb
```

The process generates the vector index and document metadata under:

```text
data/knowledge_base/
```

The generated files include:

```text
vector_index.faiss
documents.json
```

---

## Running the API

The FastAPI application can be started with:

```bash
uvicorn api.app:app --reload
```

For production-style container execution, the included Dockerfile uses:

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

---

## Testing

The project includes tests for workflow-related components.

The current test structure includes:

```text
workflow/tests/
├── test_decision_engine.py
├── test_intent_detection.py
└── test_router.py
```

Tests can be expanded as additional automation components are introduced.

The long-term testing strategy is to keep unit tests around deterministic components such as:

- intent detection,
- routing,
- decision rules,
- data transformations,
- retrieval behavior,
- and service-layer logic.

Integration tests can then verify the interaction between the API, workflow engine, knowledge base, and LLM layer.

---

## Design Principles

Several architectural principles guide the project.

### 1. Business Logic Should Remain Explicit

Business rules such as routing, priority handling, and escalation should not depend entirely on an LLM.

Deterministic rules are easier to test, debug, and audit.

### 2. RAG Should Be Used for Knowledge

RAG is appropriate when the answer depends on relatively stable organizational knowledge such as:

- refund policies,
- shipping policies,
- product information,
- FAQs,
- support procedures.

It should not be treated as a replacement for transactional systems.

For example, a customer's current order status should ultimately come from an order-management or CRM system rather than from a static knowledge base.

### 3. Modular Components

The system is divided into independent components so that the implementation can evolve from a basic automation platform toward a more capable AI-agent architecture without requiring a complete rewrite.

### 4. Local-First Development

The current LLM integration supports Ollama, allowing development and experimentation with local models without requiring a paid external LLM API.

### 5. Data-Driven Automation

Business analysis is used to identify which support processes are good candidates for automation rather than assuming that every support request should be handled automatically.

---

## Future Roadmap

The project is being developed incrementally.

Planned areas include:

### Agentic Workflow

Evolve the current workflow engine toward an AI-agent architecture capable of:

- dynamic tool selection,
- multi-step reasoning,
- state management,
- controlled tool execution,
- workflow iteration,
- and human-in-the-loop decisions.

### Customer and CRM Integration

Introduce customer-specific data sources for use cases such as:

- order status,
- customer history,
- account information,
- customer segmentation,
- and CRM operations.

### Human-in-the-Loop

Introduce controlled human review for cases where:

- confidence is low,
- the requested action is sensitive,
- business rules require approval,
- or the system cannot safely complete the task.

### Evaluation

Expand evaluation beyond retrieval quality and response generation to include:

- retrieval relevance,
- answer faithfulness,
- routing accuracy,
- workflow correctness,
- escalation quality,
- and end-to-end task success.

### Observability

Add production-oriented capabilities such as:

- structured logging,
- monitoring,
- tracing,
- latency measurement,
- error tracking,
- and workflow metrics.

### Production Deployment

Future deployment work will focus on:

- scalable API services,
- persistent databases,
- production vector storage,
- asynchronous task processing,
- authentication,
- rate limiting,
- and deployment automation.

---

## Documentation

Additional technical documentation is available in the `docs/` directory.

Important documents include:

| Document | Purpose |
|---|---|
| `architecture.md` | Overall system architecture |
| `workflow.md` | Support workflow |
| `datasets.md` | Dataset descriptions |
| `data_sources.md` | System data sources |
| `data_quality.md` | Data-quality analysis |
| `business_insights.md` | Business and EDA findings |
| `processing_strategy.md` | Data-processing strategy |
| `feature_strategy.md` | Feature-engineering strategy |
| `schema.md` | Data/schema design |
| `requirements.md` | Project requirements |
| `deployment.md` | Deployment planning |

---

## Project Vision

The long-term vision is to evolve this project from a rule-based support automation platform into an intelligent customer-support agent capable of combining:

```text
Customer Context
       +
Business Rules
       +
Knowledge Retrieval
       +
External Tools
       +
LLM Reasoning
       +
Human Oversight
       ↓
Reliable Support Automation
```

The objective is not simply to build a chatbot.

The objective is to build a system that can determine:

> **What does the customer need, what information is required, what action should be taken, and when should a human take over?**

This distinction is central to the architecture of the project.

---

## License

This project is distributed under the license included in the repository.

See [`LICENSE`](LICENSE) for details.

---

## Author

**Parsa Hedayati**

GitHub: [@parsahdy](https://github.com/parsahdy)

---

## Disclaimer

This repository is an evolving engineering project. Some components represent the current implementation, while other parts describe planned architectural extensions.

Features such as full CRM integration, production-grade monitoring, advanced agentic behavior, and complete end-to-end automation are part of the project's development roadmap and should not be considered fully implemented unless reflected in the corresponding source code.
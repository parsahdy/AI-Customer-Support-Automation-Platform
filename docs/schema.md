# Data Schema

    This document defines the canonical schemas used to standardize the datasets used in the AI Customer Support Automation project.

    The project uses multiple data sources with different structures. Each source is mapped to a standardized domain-specific schema before being used by downstream components such as analytics, machine learning, workflow processing, CRM, and RAG.


# 1. Ticket Dataset

## Domain

`Ticket`

    This dataset is used as the primary source for customer support ticket classification and AI response analysis.

## Columns To Keep and Column Mapping

| Source Column | Standard Column | Description               |
| ------------- | --------------- | ------------------------- |
| `subject`     | `subject`       | Ticket subject            |
| `body`        | `message`       | Main customer message     |
| `answer`      | `response`      | Existing support response |
| `type`        | `type`          | Ticket type               |
| `queue`       | `category`      | Support category or queue |
| `priority`    | `priority`      | Ticket priority           |
| `language`    | `language`      | Ticket language           |
| `tag`         | `tag`           | Main ticket tag           |

## Columns To Drop

* `version`
* `tag_2`
* `tag_3`
* `tag_4`
* `tag_5`
* `tag_6`
* `tag_7`
* `tag_8`

## Notes

This dataset is mainly used for:

* Ticket classification
* Category prediction
* Priority analysis
* Language analysis
* Response generation evaluation
* Support workflow development

The original `answer` column is preserved as `response` because it may later be used as a reference response for evaluating AI-generated answers.

---

# 2. Customer Support Ticket Dataset

## Domain

`Customer + Ticket`

    This dataset contains both customer-related information and ticket-related information.

In the future database design, these fields may be separated into `Customer` and `Ticket` entities.

## Columns To Keep and Column Mapping

| Source Column                  | Standard Column       | Domain                    |
| ------------------------------ | --------------------- | ------------------------- |
| `Ticket ID`                    | `ticket_id`           | Ticket                    |
| `Customer Name`                | `customer_name`       | Customer                  |
| `Customer Email`               | `customer_email`      | Customer                  |
| `Customer Age`                 | `customer_age`        | Customer                  |
| `Customer Gender`              | `customer_gender`     | Customer                  |
| `Product Purchased`            | `product_purchased`   | Ticket / Customer Context |
| `Date of Purchase`             | `purchase_date`       | Customer Context          |
| `Ticket Type`                  | `ticket_type`         | Ticket                    |
| `Ticket Subject`               | `subject`             | Ticket                    |
| `Ticket Description`           | `message`             | Ticket                    |
| `Ticket Status`                | `status`              | Ticket                    |
| `Ticket Priority`              | `priority`            | Ticket                    |
| `Ticket Channel`               | `channel`             | Ticket                    |
| `Customer Satisfaction Rating` | `satisfaction_rating` | Customer Feedback         |

## Columns To Drop

* `Resolution`
* `First Response Time`
* `Time to Resolution`

## Notes

The columns `First Response Time` and `Time to Resolution` are not necessarily useless. They are excluded from the initial canonical ticket schema because they are derived operational metrics.

They may be reintroduced later for:

* Dashboard analytics
* SLA analysis
* Workflow performance evaluation
* Response-time prediction

The `Resolution` column is currently excluded from the initial schema but may be reconsidered later if it contains valuable information for evaluating automated support resolution.

---

# 3. Ecommerce FAQ Dataset

## Domain

`Knowledge Document`

    This dataset is used as a source for the Knowledge Base and Retrieval-Augmented Generation (RAG) pipeline.

## Columns To Keep and Column Mapping

| Source Column | Standard Column |
| ------------- | --------------- |
| `document_id` | `document_id`   |
| `question`    | `question`      |
| `answer`      | `answer`        |

## Notes

This dataset will not be treated as a customer ticket.

Instead, it will be processed as knowledge data and later transformed into documents and chunks for retrieval.

The expected future flow is:

Raw FAQ Data

↓

Document Preparation

↓

Text Chunking

↓

Embedding Generation

↓

Vector Database

↓

RAG Retrieval

---

# 4. Sales Pipeline Dataset

## Domain

`Sales Opportunity / CRM`

    This dataset is not a direct Customer dataset. It represents sales opportunities and can be used to enrich the CRM side of the project.

## Columns To Keep and Column Mapping

| Source Column    | Standard Column  |
| ---------------- | ---------------- |
| `opportunity_id` | `opportunity_id` |
| `Product`        | `product`        |
| `Account`        | `account`        |
| `deal_stage`     | `deal_stage`     |
| `close_date`     | `close_date`     |
| `close_value`    | `close_value`    |

## Columns To Drop

* `sales_agent`
* `engage_date`

## Notes

    This dataset can be used to simulate CRM context for customer interactions.

For example, a future workflow may use sales context when processing a customer request:

Customer Ticket

↓

Identify Customer / Account

↓

Retrieve CRM Context

↓

Check Related Opportunity

↓

Apply Workflow Decision

However, this dataset is not currently directly connected to the customer support ticket datasets because a reliable shared customer identifier has not yet been established.

---

# Canonical Domains

The current project data is organized into the following domains:

## Ticket

Contains customer support requests and their attributes.

Examples:

* `ticket_id`
* `subject`
* `message`
* `category`
* `priority`
* `status`

---

## Customer

Contains customer-related information.

Examples:

* `customer_id`
* `customer_name`
* `customer_email`
* `customer_age`
* `customer_gender`

---

## Knowledge Document

Contains information used by the RAG system.

Examples:

* `document_id`
* `question`
* `answer`

---

## Sales Opportunity

Contains CRM-related sales information.

Examples:

* `opportunity_id`
* `product`
* `account`
* `deal_stage`
* `close_date`
* `close_value`

---

# Important Standardization Decisions

The datasets are not merged into one large table.

Instead, each dataset is standardized according to its domain:

Raw Dataset

↓

Domain-Specific Standardization

↓

Ticket / Customer / Knowledge Document / Sales Opportunity

↓

Database and AI Pipelines

This prevents unrelated data from being combined into a single large and difficult-to-maintain table.

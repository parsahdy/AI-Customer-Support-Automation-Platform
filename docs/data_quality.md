# Data Quality Report
 
    This report summarizes the observed data quality characteristics of the four datasets profiled in the notebook 01_data_profiling.ipynb. The findings below are based on the visible dataset samples, descriptive statistics, and structural cues captured in that notebook rather than on a fresh re-run of the profiling code. 

# Dataset 1: Multi-language Support Tickets

## Missing Values
    The dataset includes dense core text fields such as subject, body, and answer, but the tag columns clearly contain optional values, with tag_5 through tag_8 showing NaN in the sample rows. The visible version summary also suggests that at least one numeric field is fully populated, while sparsity is concentrated in optional metadata columns rather than the primary ticket text. 

## Duplicate Rows
    The notebook view does not expose a direct duplicate-row count for this dataset. Based on the visible sample alone, there is no explicit evidence of repeated full rows, so duplicate detection should be confirmed with an exact row-level check before model training. 

## Text Quality
    This dataset appears strong for NLP use because it contains structured ticket triplets of issue text and answer text, and it supports multiple languages including English and German in the visible sample. At the same time, multilingual content increases preprocessing complexity because language-aware normalization, tokenization, and filtering may be required to avoid mixing distributions across languages. 

## Decision
    Use as the primary customer-support text dataset when the goal is ticket classification, response generation, or multilingual support modeling. Keep it only after handling sparse tag columns and defining a clear language strategy. 



# Dataset 2: Customer Support Tickets

## Missing Values
    This dataset shows substantial missingness in operational fields, with Resolution, Time to Resolution, and Customer Satisfaction Rating visibly missing in the sample rows. The descriptive statistics also show much lower non-null counts for Customer Age and especially Customer Satisfaction Rating, which indicates incomplete records across several business fields. 

## Duplicate Rows
    The notebook content shown here does not include a duplicate summary for this dataset. Because the table includes a Ticket ID column, duplicate validation should focus both on exact row duplication and on identifier uniqueness. 

## Text Quality
    The text fields are usable, but the sample suggests mixed realism: some ticket descriptions contain templated placeholders such as {product_purchased}, and some resolution texts read like synthetic or low-coherence generated language. That makes the dataset less reliable for high-quality response generation, though it may still be useful for classification tasks or workflow-status modeling. 

## Decision
    Use as a secondary structured support dataset, especially for metadata-driven experiments such as status prediction or priority analysis. Avoid using it as the main source for response-quality training unless the synthetic and noisy text patterns are cleaned first. 

# Dataset 3: Ecommerce FAQ Chatbot Dataset

## Missing Values
    The notebook shows a single questions field containing nested question-answer objects, and no visible missing-value summary is shown in the sampled output. From the displayed rows, the field appears populated, but nested-schema validation is still necessary to confirm that both question and answer keys are consistently present. 

## Duplicate Rows
    The notebook includes a sample that appears to surface repeated or near-repeated entries, such as similar product-request questions appearing more than once in the displayed rows. This suggests possible duplication or paraphrase-level redundancy that should be deduplicated before retrieval or FAQ training. 

## Text Quality
    The content is concise, task-oriented, and naturally aligned with chatbot FAQ use cases, which makes it cleaner than open-ended ticket datasets for retrieval or intent-answer matching. Its main limitation is narrower linguistic variety, since short FAQ pairs typically cover less conversational noise and fewer real escalation patterns. 

## Decision
    Use as the primary FAQ or retrieval dataset for an ecommerce chatbot knowledge base. Deduplicate semantically similar entries and flatten the nested JSON structure before indexing or fine-tuning. 


# Dataset 4: Sales Pipeline Dataset

## Missing Values
    The visible profiling focuses on business columns such as opportunity_id, sales_agent, product, account, deal_stage, engage_date, close_date, and close_value, and the numeric summary for close_value shows a full count for that field. However, the notebook excerpt does not provide a full missing-value audit across all columns, so date completeness and stage-specific null patterns still need confirmation. 

## Duplicate Rows
    No direct duplicate analysis is visible in the notebook excerpt for this dataset. Since opportunity_id is present, the highest-priority duplicate test should be uniqueness of that identifier rather than only raw row duplication. 

## Text Quality
    This is mostly a structured tabular dataset rather than a free-text dataset, so text quality is less important than categorical consistency and date/value integrity. The visible sample looks clean and business-oriented, making it appropriate for forecasting, pipeline analytics, or tabular ML rather than NLP-heavy customer-support tasks. 

## Decision
    Use for sales forecasting, deal-stage analysis, or structured business intelligence tasks, not as a core customer-support corpus. It is a clean complementary dataset if the broader project includes analytics beyond support automation. 

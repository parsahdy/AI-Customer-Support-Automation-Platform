# Ticket Dataset

## Input:
- subject
- message
- response
- type
- category
- priority
- language
- tag

## Processing:
- text cleaning
- text normalization
- missing value handling
- duplicate handling
- label standardization

## Output:
- clean_subject
- clean_message
- response
- type
- category
- priority
- language
- tag

## Future Usage:
- intent classification
- priority prediction
- workflow routing
- response evaluation



# Customer Support Dataset

## Input:
- customer_name
- customer_email
- customer_age	
- customer_gender
- product_purchased
- purchase_date
- subject
- message
- status
- priority
- customer_satisfaction_rating

## Processing:
- text cleaning
- text normalization
- missing value handling
- type conversion
- categorical standardization
- basic validation

## Output:
- ticket_id
- customer_name
- customer_email
- product_purchased
- clean_subject
- clean_message
- status
- priority
- customer_satisfaction_rating

## Future Usage:
- intent classification
- priority prediction
- workflow routing
- customer context analysis
- dashboard analytics



# FAQ Dataset

## Input:
- question
- answer

## Processing:
- text cleaning
- text normalization
- duplicate detection
- document preparation
- chunking preparation

## Output:
- document_id
- clean_question
- clean_answer
- canonical_topic 
- source

## Future Usage:
- knowledge retrieval
- semantic search
- response generation




# Sales Opportunities 

## Input:
- product
- account
- deal_stage
- close_date
- close_value

## Processing:
- categorical standardization
- type conversion
- missing value handling
- date parsing
- numeric validation
- business-rule validation

## Output:
- opportunity_id
- clean_product
- account
- deal_stage
- close_date
- close_value

## Future Usage:
- CRM
- business workflow
- sales analytics
- customer context enrichment
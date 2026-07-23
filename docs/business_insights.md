## Business Insights

### 1. Ticket Distribution
## Finding
    Support demand is concentrated in a small set of recurring categories in the first dataset. Technical Support accounts for 29.25% of tickets, followed by Product Support at 18.37%, Customer Service at 14.93%, and IT Support at 12.01%, while smaller categories such as Human Resources and General Inquiry represent a much smaller share of requests.
    02_business_eda.ipynb

## Business Implication
    This concentration suggests that a large portion of inbound support work is repetitive rather than evenly spread across many issue types. From an operations perspective, the support team is likely spending a disproportionate amount of effort on a few common request families, which makes those categories the best starting point for process redesign, standardization, and service-level monitoring.
    02_business_eda.ipynb

## Possible Automation
    Recurring categories such as Technical Support, Product Support, Customer Service, and IT Support are strong candidates for automated routing, intent classification, and response assistance. A practical workflow would first classify incoming tickets by category, then trigger a rules-based or retrieval-augmented response flow for common patterns before escalating uncertain or high-risk cases to human agents.
    02_business_eda.ipynb


### 2. Priority Distribution

## Finding
    Priority is not evenly distributed across categories in the first dataset. A Chi-square test found a statistically significant relationship between category and priority, with chi2(18) = 4667.36, a p-value far below 0.05, and Cramer's V of 0.29, indicating a moderate association.
    02_business_eda.ipynb

    Categories related to service disruption and technical problems carry the highest share of urgent work. Service Outages and Maintenance has 70.99% high-priority tickets, Technical Support has 58.60% high-priority tickets, and IT Support has 48.85% high-priority tickets, while categories such as Human Resources and General Inquiry skew more toward low or medium priority.
    02_business_eda.ipynb

## Business Implication
    Priority handling should not be designed as a one-size-fits-all workflow because urgency meaningfully depends on the category of the request. Operationally, this means outage- and support-related tickets should receive faster triage paths, stricter escalation rules, and higher staffing attention than administrative or general inquiry tickets.
    02_business_eda.ipynb

## Possible Automation
    Priority prediction can be partially automated by using category as a strong input signal in triage models. For example, the system can auto-flag outage and technical-support tickets for expedited handling, while medium-confidence categories can be routed through assisted prioritization rather than full automation.
    02_business_eda.ipynb

### 3. Knowledge Base Coverage

## Finding
    The notebook suggests that many requests are repetitive, but the response field itself is not directly suitable for statistical association testing because it contains free-text values with very high uniqueness. The category × response contingency table produced an extremely sparse structure, with 28,580 unique response values, making Chi-square and Cramer's V unreliable for measuring direct category-response relationships in that raw form.
    02_business_eda.ipynb

    At the same time, sampled examples within categories such as Technical Support, Service Outages and Maintenance, and Customer Service indicate that similar request themes often receive structurally similar responses, even if the wording differs. This pattern suggests that at least part of the support workload can be answered from reusable response templates or knowledge assets rather than fully custom handling every time.
    02_business_eda.ipynb

## Business Implication
    Knowledge base coverage should be evaluated semantically, not by exact text matching of raw responses. If recurring issue types already map to recurring response patterns, the business has a strong opportunity to build reusable articles, response playbooks, and retrieval-backed assistance that reduces agent effort and improves consistency.
    02_business_eda.ipynb

## Possible Automation
    A practical next step is to convert free-text responses into meaningful groups such as intent, topic, resolution type, or knowledge article cluster before measuring coverage. Once those groups exist, the workflow can classify the incoming request, retrieve the most relevant article or response template, and either draft a reply automatically or assist the agent with recommended resolutions.
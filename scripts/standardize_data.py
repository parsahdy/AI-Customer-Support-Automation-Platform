import pandas as pd
import json


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df
    
    
def standardize_tickets(df):
    columns_to_keep = [
        "subject",
        "body",
        "answer",
        "type",
        "queue",
        "priority",
        "language",
        "tag_1",
    ]

    df = df[columns_to_keep]

    columns_mapping = {
        "body": "message",
        "answer": "response",
        "queue": "category",
        "tag_1": "tag",
    }

    df = df.rename(columns=columns_mapping)

    return df


def standardize_customer_support(df):
    columns_to_keep = [
        "Ticket ID",
        "Customer Name",
        "Customer Email",
        "Customer Age",
        "Customer Gender",
        "Product Purchased",
        "Date of Purchase",
        "Ticket Type",
        "Ticket Subject",
        "Ticket Description",
        "Ticket Status",
        "Ticket Priority",
        "Ticket Channel",
        "Customer Satisfaction Rating"
    ]

    df = df[columns_to_keep]

    columns_mapping = {
        "Ticket ID": "ticket_id",
        "Customer Name": "customer_name",
        "Customer Email": "customer_email",
        "Customer Age": "customer_age",
        "Customer Gender": "customer_gender",
        "Product Purchased": "product_purchased",
        "Date of Purchase": "purchase_date",
        "Ticket Type": "ticket_type",
        "Ticket Subject": "subject",
        "Ticket Description": "message",
        "Ticket Status": "status",
        "Ticket Priority": "priority",
        "Ticket Channel": "channel",
        "Customer Satisfaction Rating": "customer_satisfaction_rating"
    }

    df = df.rename(columns=columns_mapping)

    return df


def standardize_knowledge_documents(df):

    df["document_id"] = [
        f"faq_{i}" for i in range(1, len(df) + 1)
    ]

    columns_to_keep = [
        "document_id",
        "question",
        "answer"
    ]

    df = df[columns_to_keep]

    return df


def convert_to_csv():

    file_path = r"data\raw\Ecommerce_FAQ_Chatbot_dataset.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame(data["questions"])

    df = standardize_knowledge_documents(df)

    df.to_csv(
        "ecommerce_faq_knowledge_base.csv",
        index=False,
        encoding="utf-8"
    )

    return df


def standardize_sales_opportunities(df):
    columns_to_keep = [
            "opportunity_id",
            "product",
            "account",
            "deal_stage",
            "close_date",
            "close_value"
        ]
    
    df = df[columns_to_keep]

    df["close_date"] = pd.to_datetime(df["close_date"])
    df["close_value"] = pd.to_numeric(df["close_value"])

    return df


def save_data(df, path):
    df.to_csv(path, index=False)


def main():
    tickets = load_data(r"data\raw\aa_dataset-tickets-multi-lang-5-2-50-version.csv")
    tickets = standardize_tickets(tickets)
    save_data(tickets, r"data\processed\tickets.csv")

    customer = load_data(r"data\raw\customer_support_tickets.csv")
    customer = standardize_customer_support(customer)
    save_data(customer, r"data\processed\customer_support.csv")

    faq_df = convert_to_csv()
    faq = standardize_knowledge_documents(faq_df)
    save_data(faq, r"data\processed\FAQ.csv")

    opportunities = load_data(r"data\raw\sales_pipeline.csv")
    opportunities = standardize_sales_opportunities(opportunities)
    save_data(opportunities, r"data\processed\sales_opportunities.csv")
    

if __name__ == "__main__":
    main()
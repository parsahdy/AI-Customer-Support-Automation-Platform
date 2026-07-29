from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "cleaned"
OUTPUT_DIR = PROJECT_ROOT / "data" / "features"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SHORT_MESSAGE_THRESHOLD = 220
LONG_MESSAGE_THRESHOLD = 540
CLOSE_VALUE_THRESHOLD = 3500


def add_text_length_features(df: pd.DataFrame, 
                             text_cols: list[str]
                             ) -> pd.DataFrame:

    for col in text_cols:
        if col in df.columns:
            df[f"{col}_length"] = df[col].str.len()

    return df


def add_word_count_features(df: pd.DataFrame, 
                             text_cols: list[str]
                             ) -> pd.DataFrame:

    for col in text_cols:
        if col in df.columns:
            df[f"{col}_word_count"] = df[col].str.split().str.len() 

    return df


def add_question_features(df: pd.DataFrame, 
                             text_cols: list[str]
                             ) -> pd.DataFrame:

    for col in text_cols:
        if col in df.columns:
            df[f"{col}_has_question"] = df[col].str.contains(r"\?", na=False)

    return df

def add_exclamation_features(df: pd.DataFrame, 
                             text_cols: list[str]
                             ) -> pd.DataFrame:

    for col in text_cols:
        if col in df.columns:
            df[f"{col}_has_exclamation"] = df[col].str.contains(r"!", na=False)

    return df


def add_digit_features(df: pd.DataFrame, 
                             text_cols: list[str]
                             ) -> pd.DataFrame:

    for col in text_cols:
        if col in df.columns:
            df[f"{col}_has_digits"] = df[col].str.contains(r"\d", na=False)

    return df


def add_avg_word_length(df: pd.DataFrame,
                            text_cols: list[str]) -> pd.DataFrame:

    for col in text_cols:
        if col in df.columns:
            df[f"{col}_avg_word_length"] = (
                df[col].str.replace(" ", "", regex=False).str.len() 
                /
                df[col].str.split().str.len().replace(0, pd.NA)
            )

    return df


def add_unique_word_ratio(df: pd.DataFrame,
                    text_cols: list[str]) -> pd.DataFrame:

    for col in text_cols:
        if col in df.columns:
            df[f"{col}_unique_word_ratio"] = (
                df[col].fillna("").str.split().apply(lambda x: len(set(x))) 
                /
                df[col].str.split().str.len().replace(0, pd.NA)
            )

    return df


def add_basic_text_features(df: pd.DataFrame,
                            text_cols: list[str]) -> pd.DataFrame:

    df = df.copy()

    text_cols = text_cols or []

    df = add_text_length_features(df, text_cols=text_cols)
    df = add_word_count_features(df, text_cols=text_cols)
    df = add_question_features(df, text_cols=text_cols)
    df = add_exclamation_features(df, text_cols=text_cols)
    df = add_avg_word_length(df, text_cols=text_cols)
    df = add_unique_word_ratio(df, text_cols=text_cols)
    df = add_digit_features(df, text_cols=text_cols) 

    return df


def create_ticket_features(df: pd.DataFrame,
                           text_cols: list[str]) -> pd.DataFrame:

    df = add_basic_text_features(df, text_cols=text_cols)

    df["message_length_category"] = "median"
    df.loc[df["message_length"] > LONG_MESSAGE_THRESHOLD, "message_length_status"] = "long"
    df.loc[df["message_length"] < SHORT_MESSAGE_THRESHOLD, "message_length_status"] = "short"

    df["is_high_priority"] = False
    df.loc[df["priority"] == "high", "is_high_priority"] = True

    return df


def create_customer_support_features(df: pd.DataFrame,
                           text_cols: list[str]) -> pd.DataFrame:


    df = add_basic_text_features(df, text_cols=text_cols)

    df["is_high_priority"] = False
    df.loc[df["priority"].isin(["critical", "high"]), "is_high_priority"] = True

    df["is_low_satisfaction"] = False
    df.loc[df["customer_satisfaction_rating"] <= 2, "is_low_satisfaction"] = True

    return df


def create_faq_features(df: pd.DataFrame,
                        text_cols: list[str]) -> pd.DataFrame:

    df = add_basic_text_features(df, text_cols=text_cols)

    return df


def create_sales_features(df: pd.DataFrame,
                          text_cols: list[str]) -> pd.DataFrame:

    df = add_basic_text_features(df, text_cols=text_cols)

    df["is_high_value_deal"] = False
    df.loc[df["close_value"] >= CLOSE_VALUE_THRESHOLD, "is_high_value_deal"] = True

    return df


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


DATASET_CONFIG = {
    "tickets": {
        "input_file": "tickets_clean.csv",
        "output_file": "tickets_features.csv",
        "text_cols": ["subject", "message", "response"],
        "category_cols": ["type", "category", "priority", "language", "tag"],
        "feature_creator": create_ticket_features,
    },
    "customer_support": {
        "input_file": "customer_support_clean.csv",
        "output_file": "customer_support_features.csv",
        "text_cols": ["subject", "message"],
        "category_cols": ["customer_gender", "ticket_type", "status", "priority", "ticket_channel"],
        "feature_creator": create_customer_support_features,
    },
    "faq": {
        "input_file": "faq_clean.csv",
        "output_file": "faq_features.csv",
        "text_cols": ["question", "answer"],
        "category_cols": [],
        "feature_creator": create_faq_features,
    },
    "sales": {
        "input_file": "sales_opportunities_clean.csv",
        "output_file": "sales_opportunities_features.csv",
        "text_cols": ["product", "account"],
        "category_cols": ["deal_stage"],
        "feature_creator": create_sales_features,
    },
}


def main() -> None:

    for dataset_name, cfg in DATASET_CONFIG.items():
        input_path = INPUT_DIR / cfg["input_file"]
        output_path = OUTPUT_DIR / cfg["output_file"]

        if not input_path.exists():
            print(f"[SKIP] {dataset_name}: input file not found -> {input_path}")
            continue

        print(f"[INFO] processing {dataset_name}...")

        df = load_csv(input_path)

        feature_creator = cfg["feature_creator"]

        new_df = feature_creator(
            df=df,
            text_cols=cfg.get("text_cols"),
        )

        save_csv(new_df, output_path)
        print(f"[DONE] saved -> {output_path}")


if __name__ == "__main__":
    main()
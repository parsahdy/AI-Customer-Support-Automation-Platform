from __future__ import annotations
from pathlib import Path

import html
import re
import unicodedata
import pandas as pd




PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "data" / "cleaned"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text) -> str:
    if pd.isna(text):
        return ""

    text = html.unescape(str(text))
    text = unicodedata.normalize("NFKC", text)

    # Remove HTML tags, URLs, mentions
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)

    # Convert separators/punctuation into spaces
    text = re.sub(r"[\-_]{2,}", " ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)

    # Collapse repeated spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text.lower()


def clean_category(value) -> str:
    if pd.isna(value):
        return ""

    value = html.unescape(str(value))
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"[\s\-_]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def clean_email(value) -> str:
    if pd.isna(value):
        return ""

    value = html.unescape(str(value))
    value = unicodedata.normalize("NFKC", value).strip().lower()
    value = re.sub(r"\s+", "", value)
    return value


def clean_numeric_value(value):
    if pd.isna(value):
        return pd.NA

    value = html.unescape(str(value)).strip()

    # Keep digits, decimal separators, minus sign, plus sign
    value = re.sub(r"[^0-9\.\,\-\+eE]", "", value)

    # Remove thousands separators if they exist
    # Example: "1,234.50" -> "1234.50"
    if value.count(",") > 0 and value.count(".") > 0:
        value = value.replace(",", "")
    elif value.count(",") > 0 and value.count(".") == 0:
        # Example: "1234,50" -> "1234.50"
        value = value.replace(",", ".")

    return pd.to_numeric(value, errors="coerce")


def clean_date_value(
    value,
    dayfirst: bool = False,
    yearfirst: bool = False,
    target_timezone: str | None = None,
    output_format: str | None = None,
):  
    if pd.isna(value):
        return "" if output_format else pd.NaT

    dt = pd.to_datetime(value, errors="coerce", dayfirst=dayfirst, yearfirst=yearfirst)

    if pd.isna(dt):
        return "" if output_format else pd.NaT

    if target_timezone is not None:
        if getattr(dt, "tzinfo", None) is None:
            dt = dt.tz_localize(target_timezone)
        else:
            dt = dt.tz_convert(target_timezone)

    if output_format is not None:
        return dt.strftime(output_format)

    return dt


def fill_numeric_missing(series: pd.Series, strategy: str = "median") -> pd.Series:
    if strategy == "median":
        return series.fillna(series.median())
    if strategy == "mean":
        return series.fillna(series.mean())
    if strategy == "interpolation":
        return series.interpolate(method="linear")
    raise ValueError("missing strategy must be 'median', 'mean' or 'interpolation'.")


def handle_numeric_outliers(series: pd.Series, strategy: str = "clip") -> pd.Series:
    if strategy == "clip":
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return series.clip(lower=lower, upper=upper)

    if strategy == "winsorize":
        lower = series.quantile(0.01)
        upper = series.quantile(0.99)
        return series.clip(lower=lower, upper=upper)

    raise ValueError("outlier strategy must be 'clip' or 'winsorize'.")


def scale_numeric_series(series: pd.Series, scaling: str = "minmax") -> pd.Series:
    if scaling == "minmax":
        col_min = series.min()
        col_max = series.max()
        if pd.isna(col_min) or pd.isna(col_max) or col_max == col_min:
            return series
        return (series - col_min) / (col_max - col_min)

    if scaling == "standard":
        col_mean = series.mean()
        col_std = series.std()
        if pd.isna(col_std) or col_std == 0:
            return series
        return (series - col_mean) / col_std

    raise ValueError("scaling must be 'minmax' or 'standard'.")


def process_dataframe(
    df: pd.DataFrame,
    *,
    text_cols: list[str] | None = None,
    category_cols: list[str] | None = None,
    email_cols: list[str] | None = None,
    numeric_cols: list[str] | None = None,
    date_cols: list[str] | None = None,
    id_cols: list[str] | None = None,
    fill_numeric_missing_values: bool = False,
    numeric_missing_strategy: str = "median",
    handle_outliers: bool = False,
    outlier_strategy: str = "clip",
    scaling: str | None = None,
    date_dayfirst: bool = False,
    date_yearfirst: bool = False,
    date_target_timezone: str | None = None,
    date_output_format: str | None = None,
) -> pd.DataFrame:
    
    df = df.copy()

    text_cols = text_cols or []
    category_cols = category_cols or []
    email_cols = email_cols or []
    numeric_cols = numeric_cols or []
    date_cols = date_cols or []
    id_cols = id_cols or []

    
    for col in id_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: "" if pd.isna(x) else str(x).strip())

    
    for col in email_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_email)

    
    for col in category_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_category)

    
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric_value)

            if fill_numeric_missing_values:
                df[col] = fill_numeric_missing(df[col], strategy=numeric_missing_strategy)

            if handle_outliers:
                df[col] = handle_numeric_outliers(df[col], strategy=outlier_strategy)

            if scaling is not None:
                df[col] = scale_numeric_series(df[col], scaling=scaling)


    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: clean_date_value(
                    x,
                    dayfirst=date_dayfirst,
                    yearfirst=date_yearfirst,
                    target_timezone=date_target_timezone,
                    output_format=date_output_format,
                )
            )

    return df


DATASET_CONFIG = {
    "tickets": {
        "input_file": "tickets.csv",
        "output_file": "tickets_clean.csv",
        "text_cols": ["subject", "message", "response"],
        "category_cols": ["type", "category", "priority", "language", "tag"],
        "email_cols": [],
        "numeric_cols": [],
        "date_cols": [],
        "id_cols": [],
    },
    "customer_support": {
        "input_file": "customer_support.csv",
        "output_file": "customer_support_clean.csv",
        "text_cols": ["customer_name", "product_purchased", "subject", "message"],
        "category_cols": ["customer_gender", "ticket_type", "status", "priority", "ticket_channel"],
        "email_cols": ["customer_email"],
        "numeric_cols": ["customer_age", "customer_satisfaction_rating"],
        "date_cols": ["purchase_date"],
        "id_cols": ["ticket_id"],
    },
    "faq": {
        "input_file": "faq.csv",
        "output_file": "faq_clean.csv",
        "text_cols": ["question", "answer"],
        "category_cols": [],
        "email_cols": [],
        "numeric_cols": [],
        "date_cols": [],
        "id_cols": ["document_id"],
    },
    "sales": {
        "input_file": "sales_opportunities.csv",
        "output_file": "sales_opportunities_clean.csv",
        "text_cols": ["product", "account"],
        "category_cols": ["deal_stage"],
        "email_cols": [],
        "numeric_cols": ["close_value"],
        "date_cols": ["close_date"],
        "id_cols": ["opportunity_id"],
    },
}


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main() -> None:
    for dataset_name, cfg in DATASET_CONFIG.items():
        input_path = INPUT_DIR / cfg["input_file"]
        output_path = OUTPUT_DIR / cfg["output_file"]

        if not input_path.exists():
            print(f"[SKIP] {dataset_name}: input file not found -> {input_path}")
            continue

        print(f"[INFO] Processing {dataset_name}...")

        df = load_csv(input_path)
        cleaned_df = process_dataframe(
            df,
            text_cols=cfg.get("text_cols"),
            category_cols=cfg.get("category_cols"),
            email_cols=cfg.get("email_cols"),
            numeric_cols=cfg.get("numeric_cols"),
            date_cols=cfg.get("date_cols"),
            id_cols=cfg.get("id_cols"),
            fill_numeric_missing_values=False,   
            numeric_missing_strategy="median",
            handle_outliers=False,               
            outlier_strategy="clip",
            scaling=None,                        
            date_dayfirst=False,
            date_yearfirst=False,
            date_target_timezone=None,
            date_output_format=None,
        )

        save_csv(cleaned_df, output_path)
        print(f"[DONE] Saved -> {output_path}")


if __name__ == "__main__":
    main()
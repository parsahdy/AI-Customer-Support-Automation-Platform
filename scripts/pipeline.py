from scripts import standardize_data, process_utility, feature_engineering
import time

PIPELINE_STEPS = [
    ("Dataset Standardization", standardize_data.main),
    ("Data Cleaning", process_utility.main),
    ("Feature Engineering", feature_engineering.main),
]


def run_pipeline():

    print("=" * 60)
    print("AI Customer Support Automation Pipeline")
    print("=" * 60)

    for step_name, step_func in PIPELINE_STEPS:

        try:

            print(f"\n[START] {step_name}")

            start = time.perf_counter()

            step_func()

            end = time.perf_counter()
            elapsed = end - start

            print(f"\n[DONE] {step_name} ({elapsed:.2f} esc)")

        except Exception as e:

            print("\n[FAILED] {step_name}")

            print(f"Error: {e}")

            break

    else:

        print("\nPipeline Completed Successfully.")



if __name__ == "__main__":
    run_pipeline()
import time

from app.services.data_generator import generate_data
from app.services.reconciliation_engine import reconcile_transactions


BENCHMARK_SIZES = [1000, 5000, 10000, 50000]


def run_scale_benchmark(db):
    results = []

    for count in BENCHMARK_SIZES:
        print(f"Running benchmark: {count} records")

        # Generate fresh dataset
        generate_data(db, count)

        # Measure reconciliation only
        start_time = time.perf_counter()

        reconciliation = reconcile_transactions(db)

        elapsed = time.perf_counter() - start_time

        throughput = (
            count / elapsed
            if elapsed > 0
            else 0
        )

        results.append({
            "records": count,
            "processing_time_seconds": round(elapsed, 4),
            "records_per_second": round(throughput, 2),
            "matched": reconciliation["matched"],
            "partial": reconciliation["partial"],
            "exceptions": reconciliation["exceptions"],
            "match_rate": reconciliation["match_rate"]
        })

    return results
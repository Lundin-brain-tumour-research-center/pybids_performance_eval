import os
import argparse
import time
from memory_profiler import memory_usage
from bids import BIDSLayout
import tqdm


__DIR__ = os.path.dirname(os.path.abspath(__file__))


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate the performance of PyBIDS on dummy BIDS datasets "
        "generated by `produce_dummy_bids_datasets.py`."
    )
    parser.add_argument(
        "--n_subjects",
        type=int,
        nargs="+",
        default=10,
        help="Number of subjects to include in the dataset",
    )
    parser.add_argument(
        "--datasets_root",
        type=str,
        default=os.path.join(os.path.dirname(__DIR__), "derivatives"),
        help="Path to the root directory containing the datasets, "
        "generated by the `produce_dummy_bids_datasets.py` script. "
        "Note that the dataset directories are expected to be named "
        "dummy-<n_subjects> where <n_subjects> is the number of subjects. "
        "Default: derivatives/ in the root directory.",
    )
    parser.add_argument(
        "-o",
        "--output_tsv",
        type=str,
        help="Path to output TSV file. "
        "If not specified, the results will be printed to stdout.",
    )

    return parser


def append_profiling_results(tsv_file: str, results: dict):
    """Append profiling results to a TSV file.

    Note that if the file does not exist, it will be created with a header.
    Otherwise, the header will be omitted, and only the results will be appended.

    Args:
        tsv_file: Path to TSV file.
        results: Dictionary of profiling results in the form of

            {
                "n_subjects": <n_subjects>,
                "mode": <mode>,
                "time": <time>,
                "memory": <memory>
            }

    """
    # Create TSV file if it does not exist
    if not os.path.exists(tsv_file):
        with open(tsv_file, "w") as f:
            f.write("n_subjects\tmode\ttime\tmemory\n")

    # Append results to TSV file
    with open(tsv_file, "a") as f:
        f.write(
            f"{results['n_subjects']}\t"
            f"{results['mode']}\t"
            f"{results['time']}\t"
            f"{results['memory']}\n"
        )


def create_bidslayout(dataset_path: str, mode: str) -> BIDSLayout:
    """Create a BIDSLayout object.

    Args:
        dataset_path: Path to BIDS dataset.
        mode: "no-database-load" or "database-load".

    Returns:
        BIDSLayout object.

    """
    if mode == "no-database-load":
        layout = BIDSLayout(
            dataset_path, config=os.path.join(__DIR__, "bids.json"), validate=False
        )
    elif mode == "database-load":
        layout = BIDSLayout(
            dataset_path,
            config=os.path.join(__DIR__, "bids.json"),
            validate=False,
            database_path=os.path.join(dataset_path, "code", "layout.db"),
        )
    else:
        raise ValueError(f"Invalid mode: {mode}")
    return layout


def main():
    parser = get_parser()
    args = parser.parse_args()

    # Load datasets first to save the database for each BIDSLayout object
    for n_subjects in tqdm.tqdm(
        args.n_subjects,
        total=len(args.n_subjects),
        desc="Creating database file for all datasets...",
    ):
        dataset_path = os.path.join(args.datasets_root, f"dummy-{n_subjects}")
        database_path = os.path.join(dataset_path, "code", "layout.db")
        if not os.path.exists(database_path):
            layout = BIDSLayout(
                dataset_path, config=os.path.join(__DIR__, "bids.json"), validate=False
            )
            layout.save(database_path)

    # Evaluate PyBIDS
    modes = ["no-database-load", "database-load"]
    for n_subjects in tqdm.tqdm(
        args.n_subjects,
        total=len(args.n_subjects),
        desc="Running evaluation on all datasets",
    ):
        dataset_path = os.path.join(args.datasets_root, f"dummy-{n_subjects}")
        for mode in modes:
            # Evaluate
            start_time = time.time()
            (memory, retval) = memory_usage(
                (create_bidslayout, (dataset_path, mode)), max_usage=True, retval=True
            )
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Print results
            results = {
                "n_subjects": n_subjects,
                "mode": mode,
                "time": elapsed_time,
                "memory": memory,
            }
            if args.output_tsv:
                append_profiling_results(args.output_tsv, results)
            else:
                print(results)

    print("Done!")


if __name__ == "__main__":
    main()

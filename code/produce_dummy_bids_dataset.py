import os
import shutil
import pandas as pd
import argparse
import logging
import tqdm


__DIR__ = os.path.dirname(os.path.abspath(__file__))


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Produce dummy BIDS dataset(s) for testing."
    )
    parser.add_argument(
        "--template_bids_dir",
        type=str,
        default=os.path.dirname(__DIR__),
        help="Path to template BIDS dataset"
        "If not specified, the template BIDS dataset will be the root directory.",
    )
    parser.add_argument(
        "--n_subjects",
        type=int,
        nargs="+",
        default=10,
        help="List of number of subjects to produce."
        "Each item in the list will produce a dataset with that number of subjects.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=os.path.join(os.path.dirname(__DIR__), "derivatives"),
        help="Path to output directory. "
        "If not specified, the output directory will be derivatives/ "
        "of the root directory.",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    # Read in template dataset
    template_bids_dir = args.template_bids_dir
    template_bids_dir = os.path.abspath(template_bids_dir)

    # Create output directory
    output_dir = args.output_dir
    output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create output dataset
    for n_subjects in tqdm.tqdm(
        args.n_subjects, total=len(args.n_subjects), desc="Creating dummy datasets"
    ):
        # Initialize dataset with dataset_description.json and participants.tsv
        # from template dataset
        output_dataset = os.path.join(output_dir, f"dummy-{n_subjects}")
        if os.path.exists(output_dataset):
            shutil.rmtree(output_dataset)
        os.makedirs(output_dataset)
        shutil.copyfile(
            os.path.join(template_bids_dir, "dataset_description.json"),
            os.path.join(output_dataset, "dataset_description.json"),
        )
        shutil.copyfile(
            os.path.join(template_bids_dir, "participants.tsv"),
            os.path.join(output_dataset, "participants.tsv"),
        )

        # Create participants.tsv
        participants_tsv = os.path.join(output_dataset, "participants.tsv")
        df = pd.DataFrame()
        df["participant_id"] = [f"sub-{i:06d}" for i in range(1, n_subjects + 1)]
        df.to_csv(participants_tsv, sep="\t", index=False)

        for subject_id in df["participant_id"]:
            # Copy the files from sub-000001 folder to the subject folder
            # and rename the files by replacing sub-000001 with the new subject id
            # e.g. sub-000001_T1w.nii.gz -> sub-000002_T1w.nii.gz
            subject_dir = os.path.join(output_dataset, subject_id)
            if os.path.exists(subject_dir):
                shutil.rmtree(subject_dir)
            shutil.copytree(
                os.path.join(template_bids_dir, "sub-000001"),
                os.path.join(output_dataset, subject_id),
            )
            for root, _, files in os.walk(os.path.join(output_dataset, subject_id)):
                for file in files:
                    old_file = os.path.join(root, file)
                    new_file = os.path.join(
                        root, file.replace("sub-000001", subject_id)
                    )
                    shutil.move(old_file, new_file)

    logging.info("Done!")


if __name__ == "__main__":
    main()

# Generate dummy BIDS datasets for performance evaluation of PyBIDS

This project has been developed to generate dummy BIDS datasets for testing PyBIDS performance on large datasets.

In particular, it contains a dummy BIDS dataset with one subject and python scripts to:
- generate dummy BIDS datasets with a varying number of subject
- evaluate pybids on these datasets

## Dependencies

- pandas
- tgdm
- argparse

## How to generate the dummy BIDS datasets

This is achieved by using the script `code/produce_dummy_bids_datasets.py`.

### Usage

```output
usage: produce_dummy_bids_dataset.py [-h] [--template_bids_dir TEMPLATE_BIDS_DIR]
                                     [--n_subjects N_SUBJECTS [N_SUBJECTS ...]] [--output_dir OUTPUT_DIR]

Produce dummy BIDS dataset(s) for testing.

options:
    -h, --help            show this help message and exit
    --template_bids_dir TEMPLATE_BIDS_DIR
                        Path to template BIDS datasetIf not specified, the template BIDS dataset will be the
                        root directory.
    --n_subjects N_SUBJECTS [N_SUBJECTS ...]
                        List of number of subjects to produce.Each item in the list will produce a dataset with
                        that number of subjects.
    --output_dir OUTPUT_DIR
                        Path to output directory. If not specified, the output directory will be derivatives/ of
                        the root directory.                     
```

### Example

If you wish to generate 4 dummy datasets in the `derivatives/` folder with a number of 10, 100, 1000, and 10000 subjects, this would correspond to the following command:

```bash
python /path/to/produce_dummy_bids_dataset.py --n_subjects 10 100 1000 10000
```

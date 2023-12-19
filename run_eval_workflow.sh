DIR="$( dirname "$0" )"
echo $DIR

OUTPUT_DIR="$DIR/derivatives"

# Remove output directory if it exists
if [ -d "$OUTPUT_DIR" ]; then
    echo "Removing existing $OUTPUT_DIR..."
    rm -rf "$OUTPUT_DIR"
fi

# Create dummy BIDS datasets
python "$DIR/code/produce_dummy_bids_datasets.py" \
    --n_subjects 10 100 1000 10000 \
    --output_dir "$OUTPUT_DIR"

# Remove output directory if it exists
if [ -f "$DIR/profiling_results.tsv" ]; then
    echo "Removing existing $DIR/profiling_results.tsv..."
    rm "$DIR/profiling_results.tsv"
fi

# Run evaluation
python "$DIR/code/evaluate_pybids.py"  \
    --n_subjects 10 100 1000 10000  \
    -o "$DIR/profiling_results.tsv"

# Plot results
python "$DIR/code/plot_results.py" \
    --input_tsv "$DIR/profiling_results.tsv"

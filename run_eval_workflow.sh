# Copyright 2023-2024 Lausanne University and Lausanne University Hospital, Switzerland & Contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

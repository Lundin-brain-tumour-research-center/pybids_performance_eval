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

import os
import argparse
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="""Plot the results of the PyBIDS evaluation and save them as HTML and PNG files.\n\n
 
        The output HTML files will be saved with the same prefix as the input TSV file,
        but with a suffix and extension added to the end. For example, if the input TSV
        file is named `profiling_results.tsv`, then the output HTML/PNG files will be named
        `profiling_results_time.html/png` and `profiling_results_memory.html/png`.
        
        """
    )
    parser.add_argument(
        "--input_tsv",
        type=str,
        required=True,
        help="Path to input TSV file. "
        "If not specified, the results will be read from stdin.",
    )

    return parser


def create_time_plot(results: pd.DataFrame, title: str, output_prefix: str):
    """Create and save a plotly plot of the timing results.

    Args:
        results: Pandas DataFrame of the results.
        title: Title of the plot.
        output_prefix: Path to output HTML file prefix (no suffix and extension).
    """
    # Create the bar plot
    fig = px.bar(
        results,
        x="n_subjects",
        y="time",
        color="mode",
        barmode="group",
        labels={"n_subjects": "Number of subjects", "time": "Time (s)"},
        height=600,
        width=800,
    )
    # Adjust the plot layout
    fig.update_layout(
        title=title,
        xaxis_title="Number of subjects",
        yaxis_title="Time (s)",
        legend_title="Mode",
    )
    # Make sure the x-axis to be categorical
    fig.update_xaxes(type="category")

    # Get the unique test types.
    # We expect there to be only one test type and we take the first one.
    test_type = results["test"].unique()[0]

    # Save the plot in HTML and PNG formats
    fig.write_html(output_prefix + f"_{test_type}_time.html")
    fig.write_image(output_prefix + f"_{test_type}_time.png")


def create_memory_plot(results: pd.DataFrame, title: str, output_prefix: str):
    """Create and save a plotly plot of the memory results.

    Args:
        results: Pandas DataFrame of the results.
        title: Title of the plot.
        output_prefix: Path to output HTML file prefix (no suffix and extension).
    """
    # Create the bar plot
    fig = px.bar(
        results,
        x="n_subjects",
        y="memory",
        color="mode",
        barmode="group",
        labels={"n_subjects": "Number of subjects", "memory": "Memory (MB)"},
        height=600,
        width=800,
    )
    # Adjust the plot layout
    fig.update_layout(
        title=title,
        xaxis_title="Number of subjects",
        yaxis_title="Memory (MB)",
        legend_title="Mode",
    )
    # Make sure the x-axis is categorical
    fig.update_xaxes(type="category")

    # Get the unique test types.
    # We expect there to be only one test type and we take the first one.
    test_type = results["test"].unique()[0]

    # Save the plot in HTML and PNG formats
    fig.write_html(output_prefix + f"_{test_type}_memory.html")
    fig.write_image(output_prefix + f"_{test_type}_memory.png")


def main():
    parser = get_parser()
    args = parser.parse_args()

    # Read in results
    results = pd.read_csv(args.input_tsv, sep="\t")

    # Create output HTML file prefix (no suffix and extension)
    output_prefix = os.path.splitext(args.input_tsv)[0]

    # Create and save plots
    create_time_plot(results[results["test"] == "init"], "PyBIDS Runtime Results (BIDSLayout Initialization)", output_prefix)
    create_memory_plot(results[results["test"] == "init"], "PyBIDS Memory Results (BIDSLayout Initialization)",  output_prefix)
    create_time_plot(results[results["test"] == "add_subject"], "PyBIDS Runtime Results (BIDSLayout Update)", output_prefix)
    create_memory_plot(results[results["test"] == "add_subject"], "PyBIDS Memory Results (BIDSLayout Update)",  output_prefix)


if __name__ == "__main__":
    main()

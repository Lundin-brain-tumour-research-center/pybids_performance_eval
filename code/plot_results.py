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


def create_time_plot(results: pd.DataFrame, output_prefix: str):
    """Create and save a plotly plot of the timing results.

    Args:
        results: Pandas DataFrame of the results.
        output_prefix: Path to output HTML file prefix (no suffix and extension).
    """
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
    fig.update_layout(
        title="PyBIDS evaluation",
        xaxis_title="Number of subjects",
        yaxis_title="Time (s)",
        legend_title="Mode",
    )
    fig.update_xaxes(type="category")
    fig.write_html(output_prefix + "_time.html")
    fig.write_image(output_prefix + "_time.png")


def create_memory_plot(results: pd.DataFrame, output_prefix: str):
    """Create and save a plotly plot of the memory results.

    Args:
        results: Pandas DataFrame of the results.
        output_prefix: Path to output HTML file prefix (no suffix and extension).
    """
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
    fig.update_layout(
        title="PyBIDS evaluation",
        xaxis_title="Number of subjects",
        yaxis_title="Memory (MB)",
        legend_title="Mode",
    )
    fig.update_xaxes(type="category")
    fig.write_html(output_prefix + "_memory.html")
    fig.write_image(output_prefix + "_memory.png")


def main():
    parser = get_parser()
    args = parser.parse_args()

    # Read in results
    results = pd.read_csv(args.input_tsv, sep="\t")

    # Create output HTML file prefix (no suffix and extension)
    output_prefix = os.path.splitext(args.input_tsv)[0]

    # Create and save plots
    create_time_plot(results, output_prefix)
    create_memory_plot(results, output_prefix)


if __name__ == "__main__":
    main()

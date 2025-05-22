import plotly.graph_objects as go
from plotly.graph_objects import Figure


def compress_legend(fig: Figure, ignore: list[str]) -> Figure:
    """
    Compresses the legend of a plotly Figure by grouping similar items.

    This function takes a plotly Figure and a list of legend items to ignore. It groups similar items in the legend,
    based on the names of the traces.

    Args:
        fig (plotly.graph_objects.Figure): The input Figure with the original legend.
        ignore (list[str]): A list of legend item names to ignore during the compression.

    Returns:
        plotly.graph_objects.Figure: The Figure with the compressed legend.

    Note:
        This function modifies the input Figure in-place, but also returns it for convenience.
    """

    group1_base, group2_base = fig.data[0].name.split(",")
    lines_marker_name = []
    start_x = []
    for i, trace in enumerate(fig.data):
        if trace.name in ignore:
            continue
        start_x.append(trace.x.min())
        part1, part2 = trace.name.split(",")
        if part1 == group1_base:
            lines_marker_name.append(
                {
                    "line": trace.line.to_plotly_json(),
                    "marker": trace.marker.to_plotly_json(),
                    "mode": trace.mode,
                    "name": part2.lstrip(" "),
                }
            )
        if part2 != group2_base:
            trace["name"] = ""
            trace["showlegend"] = False
        else:
            trace["name"] = part1

    ## Add the line/markers for the 2nd group
    for lmn in lines_marker_name:
        lmn["line"]["color"] = "black"
        lmn["marker"]["color"] = "black"
        fig.add_trace(go.Scatter(x=[min(start_x)], y=[None], **lmn))
    fig.update_layout(legend_title_text="", legend_itemclick=False, legend_itemdoubleclick=False)
    # return fig

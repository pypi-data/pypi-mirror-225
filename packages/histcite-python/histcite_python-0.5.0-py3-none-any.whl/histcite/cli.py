import os
import argparse
from histcite.read_file import ReadFile
from histcite.process_file import ProcessFile
from histcite.compute_metrics import ComputeMetrics
from histcite.network_graph import GraphViz


def main():
    parser = argparse.ArgumentParser(description="A Python interface for histcite.")
    parser.add_argument(
        "-f",
        "--folder_path",
        type=str,
        required=True,
        help="Folder path of literature metadata.",
    )
    parser.add_argument(
        "-t",
        "--source_type",
        type=str,
        required=True,
        choices=["wos", "cssci", "scopus"],
        help="Source type of literature metadata.",
    )
    parser.add_argument(
        "-n", "--node_num", type=int, default=50, help="N nodes with the highest LCS."
    )
    args = parser.parse_args()

    output_path = os.path.join(args.folder_path, "result")
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    docs_df = ReadFile(args.folder_path, args.source_type).read_all()
    process = ProcessFile(docs_df, args.source_type)
    process.extract_reference()
    citation_relationship, refs_df = process.process_citation()

    cm = ComputeMetrics(docs_df, refs_df, citation_relationship, args.source_type)
    cm.write2excel(os.path.join(output_path, "descriptive_statistics.xlsx"))

    doc_indices = (
        citation_relationship[citation_relationship["LCS"] > 0]
        .sort_values("LCS", ascending=False)
        .index[: args.node_num]
        .tolist()
    )
    graph = GraphViz(docs_df, citation_relationship, args.source_type)

    graph_dot_file = graph.generate_dot_file(doc_indices)
    graph_dot_path = os.path.join(output_path, "graph.dot")
    with open(graph_dot_path, "w") as f:
        f.write(graph_dot_file)
    graph._export_graph_node_info(os.path.join(output_path, "graph_node_info.xlsx"))

import os
from wg_torch.graph_ops import (
    graph_name_normalize,
)

def load_data_split(
    dataset_dir: str, graph_name: str, is_dataset_root_dir: bool = False
):
    import pickle

    save_dir = dataset_dir
    normalized_graph_name = graph_name_normalize(graph_name)
    if is_dataset_root_dir:
        save_dir = os.path.join(dataset_dir, normalized_graph_name, "converted")
    file_path = os.path.join(
        save_dir, normalized_graph_name + "_data_split.pkl"
    )
    with open(file_path, "rb") as f:
        data_split = pickle.load(f)
    return data_split


def load_node_pro(
    dataset_dir: str, graph_name: str, is_dataset_root_dir: bool = False
):
    import pickle

    save_dir = dataset_dir
    normalized_graph_name = graph_name_normalize(graph_name)
    if is_dataset_root_dir:
        save_dir = os.path.join(dataset_dir, normalized_graph_name, "converted")
    file_path = os.path.join(
        save_dir, normalized_graph_name + "_node_pro.pkl"
    )
    with open(file_path, "rb") as f:
        node_pro = pickle.load(f)
    return node_pro


def load_edge_pro(
    dataset_dir: str, graph_name: str, is_dataset_root_dir: bool = False
):
    import pickle

    save_dir = dataset_dir
    normalized_graph_name = graph_name_normalize(graph_name)
    if is_dataset_root_dir:
        save_dir = os.path.join(dataset_dir, normalized_graph_name, "converted")
    file_path = os.path.join(
        save_dir, normalized_graph_name + "_edge_pro.pkl"
    )
    with open(file_path, "rb") as f:
        edge_pro = pickle.load(f)
    return edge_pro


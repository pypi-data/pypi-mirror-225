import os
import sys
sys.path.append('..')
sys.path.append('.')
from optparse import OptionParser
import torch
from mpi4py import MPI
from wholegraph.torch import wholegraph_pytorch as wg
from wg_torch import graph_ops as graph_ops
from wg_torch.wm_tensor import *

from .load_ops import (
    load_data_split,
    load_node_pro,
    load_edge_pro
)

def load_graph_wg(root_dir, graph_name, source, use_nccl=False):
    wg.init_lib()
    torch.set_num_threads(1)
    comma = MPI.COMM_WORLD
    shared_comma = comma.Split_type(MPI.COMM_TYPE_SHARED)
    os.environ["RANK"] = str(comma.Get_rank())
    os.environ["WORLD_SIZE"] = str(comma.Get_size())
    # slurm in Selene has MASTER_ADDR env
    if "MASTER_ADDR" not in os.environ:
        os.environ["MASTER_ADDR"] = "localhost"
    if "MASTER_PORT" not in os.environ:
        os.environ["MASTER_PORT"] = "12335"
    local_rank = shared_comma.Get_rank()
    local_size = shared_comma.Get_size()
    print("Rank=%d, local_rank=%d" % (local_rank, comma.Get_rank()))
    dev_count = torch.cuda.device_count()
    assert dev_count > 0
    assert local_size <= dev_count
    torch.cuda.set_device(local_rank)
    torch.distributed.init_process_group(backend="nccl", init_method="env://")
    wm_comm = create_intra_node_communicator(
        comma.Get_rank(), comma.Get_size(), local_size
    )
    wm_embedding_comm = None
    if use_nccl:
        if comma.Get_rank() == 0:
            print("Using nccl embeddings.")
        wm_embedding_comm = create_global_communicator(
            comma.Get_rank(), comma.Get_size()
        )

    # train set, valid set, test set
    data_split = load_data_split(root_dir, graph_name, True)
    print("data_split", data_split)

    normalized_graph_name = graph_ops.graph_name_normalize(graph_name)
    save_dir = os.path.join(root_dir, normalized_graph_name, "converted")
    meta_data = graph_ops.load_meta_file(save_dir, normalized_graph_name)

    # node property
    node_pro = None
    if meta_data["nodes"][0]["has_pro"]:
        node_pro = load_node_pro(root_dir, graph_name, True)
    if node_pro is not None:
        print("node_pro_shape", node_pro.shape)

    # edge property
    edge_pro = None
    if meta_data["edges"][0]["has_pro"]:
        edge_pro = load_edge_pro(root_dir, graph_name, True)
    if edge_pro is not None:
        print("edge_pro_shape", edge_pro.shape)

    dist_homo_graph = graph_ops.HomoGraph()
    use_chunked = True
    use_host_memory = False
    dist_homo_graph.load(
        root_dir,
        graph_name,
        wm_comm,
        use_chunked,
        use_host_memory,
        wm_embedding_comm,
    )
    return data_split, dist_homo_graph


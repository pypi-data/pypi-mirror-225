"""
load zhuque graph
Args:
dataset_name: zhuque dataset name
data_loader: define data load param
algo_frame: algo frame, wholegraph/grapscope etc.
"""
# -*- coding:utf-8 -*-
import os.path
import yaml
import sys
sys.path.append('.')
#from .wg_load.data_load import load_graph_wg
from wg_load.data_load import load_graph_wg





LOCAL_DATASET_PATH = '/INPUT/datasets/'
LOCAL_DATALOADER_PATH = '/INPUT/dataloaders/'
OGB_LOAD_MAP = {
    ('pyg', 'node'): 'PygNodePropPredDataset',
    ('pyg', 'link'): 'PygLinkPropPredDataset',
    ('pyg', 'graph'): 'PygGraphPropPredDataset',
    ('dgl', 'node'): 'DglNodePropPredDataset',
    ('dgl', 'link'): 'DglLinkPropPredDataset',
    ('dgl', 'graph'): 'DglGraphPropPredDataset',
    ('none', 'node'): 'NodePropPredDataset',
    ('none', 'link'): 'LinkPropPredDataset',
    ('none', 'graph'): 'GraphPropPredDataset'
}
OGB_GS_LOAD_MAP = {
    'ogbl_collab': 'load_ogbl_collab',
    'ogbl_ddi': 'load_ogbl_ddi',
    'ogbn_arxiv': 'load_ogbn_arxiv',
    'ogbn_mag_small': 'load_ogbn_mag',
    'ogbn_proteins': 'load_ogbn_proteins'
}
NAS_BASE = '/mnt/zhuque_goofys'
k8s_volumes = {
    "data": {
        "type": "hostPath",
        "field": {
            "path": NAS_BASE,
            "type": "Directory"
        },
        "mounts": {
            "mountPath": "/zhuque_goofys"
        }
    }
}


def load_graph(args):
    data_loader = args.data_loader
    if not data_loader:
        raise Exception('please check dataloader parameters')
    dataloader_path = os.path.join(LOCAL_DATALOADER_PATH, data_loader + '.yml')
    try:
        dl_file = open(dataloader_path, "r", encoding="UTF-8")
        dataloader = yaml.load(dl_file, Loader=yaml.FullLoader)
    except:
        raise Exception('read dataloader file error,path=', dataloader_path)

    # 检测dataloader文件字段是否存在
    if 'storageFormat' not in dataloader.keys():
        raise Exception('check the dataloader, storageFormat does not exsits')
    storage_format = dataloader['storageFormat']
    if storage_format in ['csv', 'ogb', 'bin'] and 'platform' not in dataloader.keys():
        raise Exception('check the dataloader, platform does not exsits')

    # 朱雀平台格式csv数据集
    if storage_format == 'csv':
        platform = dataloader['platform']
        if platform == 'nmc':
            return load_graph_csv_gs(dataloader)
        elif platform == 'smc':
            return load_graph_wg(LOCAL_DATASET_PATH, dataloader['dataset'], 'csv')
        elif platform == 'dgl':
            return load_graph_csv_dgl(dataloader)
    elif storage_format == 'ogb':
        platform = dataloader['platform']
        if platform == 'ogbofficial':
            return load_graph_ogb_official(dataloader, args.frame_type)
        elif platform == 'smc':
            return load_graph_wg(LOCAL_DATASET_PATH, dataloader['ogbName'], 'ogb')
        elif platform == 'nmc':
            return load_graph_ogb_gs(dataloader)
    # elif storage_format in ('npy', 'npz'):
    #     return load_graph_numpy(dataloader)
    elif storage_format == 'bin':
        return load_graph_bin_dgl(dataloader)
    elif storage_format == 'other':
        return load_graph_other(dataloader)

    raise Exception('load data fail')


# 获取数据集路径
def get_dataset_path(args):
    data_loader = args.data_loader
    if not data_loader:
        raise Exception('please check dataloader parameters')
    dataloader_path = os.path.join(LOCAL_DATALOADER_PATH, data_loader + '.yml')
    try:
        dl_file = open(dataloader_path, "r", encoding="UTF-8")
        dataloader = yaml.load(dl_file, Loader=yaml.FullLoader)
    except:
        raise Exception('read dataloader file error,path=', dataloader_path)
    # 检测dataloader文件字段是否存在
    if 'storageFormat' not in dataloader.keys():
        raise Exception('check the dataloader, storageFormat does not exsits')
    storage_format = dataloader['storageFormat']
    if storage_format in ['csv', 'ogb', 'bin'] and 'platform' not in dataloader.keys():
        raise Exception('check the dataloader, platform does not exsits')

    # 朱雀平台格式csv数据集
    if storage_format == 'csv':
        return os.path.join(LOCAL_DATASET_PATH, dataloader['dataset'])
    elif storage_format == 'ogb':
        return os.path.join(LOCAL_DATASET_PATH, dataloader['ogbRoot'])
    elif storage_format == 'bin':
        return os.path.join(LOCAL_DATASET_PATH, dataloader['dataPath'])
    elif storage_format == 'other':
        return os.path.join(LOCAL_DATASET_PATH, dataloader['dataPath'])
    raise Exception('load data fail')


# 加载ogb格式数据集 官方方式
def load_graph_ogb_official(dataloader, frame_type):
    from ogb.graphproppred import PygGraphPropPredDataset, DglGraphPropPredDataset, GraphPropPredDataset
    from ogb.linkproppred import PygLinkPropPredDataset, DglLinkPropPredDataset, LinkPropPredDataset
    from ogb.nodeproppred import PygNodePropPredDataset, DglNodePropPredDataset, NodePropPredDataset

    if not frame_type:
        raise Exception('please check frame info')
    ogb_name = dataloader['ogbName']
    ogb_root = dataloader['ogbRoot']
    task = get_ogb_task(ogb_name)
    params = []
    normal_ogb_name = ogb_name.replace("_", "-")
    params.append('name=\'' + normal_ogb_name + '\'')
    params.append('root=\'' + ogb_root + '\'')
    # obj_str : PygNodePropPredDataset(name='ogbl-ddi', root=data_path)
    data_frame = get_data_frame(frame_type)
    obj_str = OGB_LOAD_MAP.get((data_frame, task)) + construct_param(params)
    print(obj_str)
    return eval(obj_str)


# 在graphscope框架加载ogb格式数据集
def load_graph_ogb_gs(dataloader):
    import graphscope as gs
    from graphscope.dataset.ogbl_collab import load_ogbl_collab
    from graphscope.dataset.ogbl_ddi import load_ogbl_ddi
    from graphscope.dataset.ogbn_arxiv import load_ogbn_arxiv
    from graphscope.dataset.ogbn_mag import load_ogbn_mag
    from graphscope.dataset.ogbn_proteins import load_ogbn_proteins


    sess = None
    ogb_name = dataloader['ogbName']
    ogb_root = dataloader['ogbRoot']
    normal_ogb_name = ogb_name.replace("-", "_")
    if normal_ogb_name not in OGB_GS_LOAD_MAP.keys():
        raise Exception(normal_ogb_name + ' is not supported in GraphScope,\n'
                       'supported list contains: \nogbl_collab\nogbl_ddi \nogbn_arxiv\nogbn_mag\nogbn_proteins\n')
    try:
        sess = gs.session(addr='127.0.0.1:59001', mount_dataset='/dataset')
        print(sess)
        params = []
        params.append('sess')
        params.append('\'' + ogb_root + '\'')
        obj_str = OGB_GS_LOAD_MAP.get(normal_ogb_name) + construct_param(params)
        # graph = load_ogbn_mag(sess, '/FILES/INPUT/ogbn_mag_small')
        print(obj_str)
        return eval(obj_str)
    except:
        print('load ogb graph in GraphScope error')
        raise Exception('load ogb graph in GraphScope error')
    finally:
        sess.close()



# 加载numpy格式数据集
def load_graph_numpy(dataloader):
    params = dataloader['params']
    obj_str = 'np.load' + construct_param(params)
    print(obj_str)
    return eval(obj_str)


# 在Dgl框架下加载bin格式数据集
def load_graph_bin_dgl(dataloader):
    import dgl
    from dgl.data import DGLDataset
    from dgl.dataloading import GraphDataLoader
    class LoadDataset(DGLDataset):
        def __init__(self):
            super().__init__(name='my_data')
        def process(self):
            pass
        def __getitem__(self, idx):
            return self.graph[idx]
        def __len__(self):
            return len(self.graph)
        def load(self):
            path = dataloader['dataPath']
            graph = dgl.load_graphs(path)[0]
            self.graph = graph
        def has_cache(self):
            if(os.path.exists(dataloader['dataPath'])):
                return True
            else:
                return False
    dataset = LoadDataset()
    dataloader = GraphDataLoader(dataset, batch_size=32, drop_last=False, shuffle=True, pin_memory=True)
    return dataset, dataloader


# 加载other格式数据集
def load_graph_other(dataloader):
    code = dataloader['code']
    data_path = dataloader['dataPath']
    print(code)
    exec_data = {'data_path': data_path}
    exec(code, globals(), exec_data)
    return exec_data["data"]


# 在graphscope框架加载csv格式数据集
def load_graph_csv_gs(dataloader):
    import graphscope as gs


    data_name = dataloader['dataset']
    data_path = os.path.join(LOCAL_DATASET_PATH, data_name)
    # sess = graphscope.session(mount_dataset="/dataset", k8s_volumes=k8s_volumes, k8s_coordinator_cpu=4,
    #                           k8s_coordinator_mem="8Gi")
    sess = gs.session(addr='127.0.0.1:59001', mount_dataset='/dataset')
    if dataloader["oidType"] == 'string':
        graph = sess.g(oid_type=dataloader["oidType"])
    else:
        graph = sess.g()
    for key, value in dataloader['vertices'].items():
        pro = []
        for feature in value['features']:
            pro.append((feature['name'], feature['type']))
        graph = graph.add_vertices(os.path.join(data_path, value['path']), label=key, vid_field=value['vidField'],
                                   properties=pro)
    for key, value in dataloader['edges'].items():
        pro = []
        for feature in value['features']:
            pro.append((feature['name'], feature['type']))
        graph = graph.add_edges(os.path.join(data_path, value['path']), label=key, src_label=value['srcLabel'],
                                dst_label=value['dstLabel'], src_field=0, dst_field=1, properties=pro)
    return graph


# 在pytorch框架加载csv格式数据集
def load_graph_csv_pytorch(dataloader):
    import torch
    import torch.utils.data as data
    import pandas as pd

    class PytorchDatasets(data.Dataset):
        def __init__(self, file_paths, transform=None):
            self.file_paths = file_paths
            self.transform = transform
            # 加载每个CSV文件并存储数据
            self.datasets = []
            for file_path in self.file_paths:
                df = pd.read_csv(file_path)
                self.datasets.append(df)

        def __len__(self):
            # 返回所有数据集的行数总和
            total_rows = 0
            for dataset in self.datasets:
                total_rows += len(dataset)
            return total_rows

        def __getitem__(self, index):
            # 根据索引获取数据
            start_index = 0
            for dataset in self.datasets:
                if index >= start_index and index < start_index + len(dataset):
                    return dataset[index - start_index]
                start_index += len(dataset)

        def __repr__(self):
            return f"CombinedDataset({', '.join(self.file_paths)})"

    return None

# 在dgl框架加载csv格式数据集(同构图)
def load_graph_csv_dgl(dataloader):
    import dgl
    import torch as th
    import pandas as pd
    data_name = dataloader['dataset']
    data_path = os.path.join(LOCAL_DATASET_PATH, data_name)
    g = None
    for key, value in dataloader['edges'].items():
        edges_data = pd.read_csv(os.path.join(data_path, value['path']))
        src = edges_data['src_vid'].to_numpy()
        dst = edges_data['dst_vid'].to_numpy()
        g = dgl.graph((src, dst))
        pro = []
        for feature in value['features']:
            pro.append((feature['name']))
        edges_feature = th.tensor(edges_data[pro].to_numpy())
        g.edata['edge'] = edges_feature
        break
    for key, value in dataloader['vertices'].items():
        nodes_data = pd.read_csv(os.path.join(data_path, value['path']))
        pro = []
        for feature in value['features']:
            pro.append((feature['name']))
        nodes_feature = th.tensor(nodes_data[pro].to_numpy())
        g.ndata['node'] = nodes_feature
        break
    return g


# 判断ogb数据集的任务类型
def get_ogb_task(data_name):
    if 'ogbn' in data_name:
        return 'node'
    elif 'ogbl' in data_name:
        return 'link'
    elif 'ogbg' in data_name:
        return 'graph'
    else:
        raise Exception('dataset name is invalid')


# 组装参数
def construct_param(params):
    param_str = ''
    for param in params:
        param_str = param_str + ',' + param
    if len(param_str) > 0:
        param_str = param_str[1:]
    param_str = '(' + param_str + ')'
    return param_str

def get_data_frame(frame_type):
    if frame_type == 'pytorch':
        return 'pyg'
    elif frame_type == 'dgl':
        return 'dgl'
    else:
        return 'none'

if __name__ == '__main__':
    from munch import DefaultMunch
    print('11')
    param = {'dataPath': '/mnt/zhuque_goofys/datasets/test.bin'}
    dataloader = DefaultMunch.fromDict(param)
    dataset, dataloader = load_graph_bin_dgl(dataloader)
    print(dataset)
    print(dataloader)
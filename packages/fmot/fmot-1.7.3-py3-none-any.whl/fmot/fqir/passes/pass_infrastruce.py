from .batchdim_removal import remove_batchdim
from .dimtag_removal import remove_named_dims
from .kernelize_lstm import kernelize_lstm
from .kernelize_temporal_unfold import kernelize_temporal_unfold
from .cleanup import uniquify_names, limit_biases, remove_unused_params, remove_null_shifts
from .kernelize_red_broad import kernelize_sum, kernelize_broadcast
from .fold_reused_params import fold_reused_params
from .stride_optimization import perform_stride_optimization
from .repeat_assign import dereference_repeated_assigns
from ..graph_proto import GraphProto

PASS_ORDER = [
    # remove_batchdim,
    kernelize_lstm,
    remove_null_shifts,
    perform_stride_optimization,
    dereference_repeated_assigns,
    kernelize_temporal_unfold,
    kernelize_sum,
    kernelize_broadcast,
    uniquify_names,
    limit_biases,
    remove_unused_params,
    fold_reused_params
]

def run_passes(graph):
    objs = {
        "graph": graph,
        "io_spec": None
        }
    for p in PASS_ORDER:
        ret = p(objs["graph"])
        if isinstance(ret, GraphProto):
            objs["graph"] = ret
        elif isinstance(ret, dict):
            objs.update(ret)

    graph = objs["graph"]
    return graph, objs
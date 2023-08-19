import torch
import numpy as np


def type_convert(*args, to_torch=True, to_cuda=True):
    converted_args = []
    if to_torch:
        if any([isinstance(x, torch.Tensor) for x in args]):
            devices = set([x.device for x in args if isinstance(x, torch.Tensor)])
            if torch.device("cpu") in devices:
                devices.remove(torch.device("cpu"))
            if len(devices) > 1:
                raise IOError("Cannot convert: Several GPU devices found")
            if len(devices) == 0:
                gpu_device = torch.device("cuda")
            else:
                gpu_device = devices.pop()
            for x in args:
                if isinstance(x, np.ndarray):
                    x = torch.from_numpy(x)
                    if x.dtype == torch.double:
                        x = x.float()
                if to_cuda and (x.device != gpu_device):
                    x = x.to(gpu_device)
                converted_args.append(x)
        # quick solution
        if any([x.dtype.is_floating_point for x in converted_args]):
            for i in range(len(converted_args)):
                converted_args[i] = converted_args[i].float()

    else:
        # all as numpy arrays
        for x in args:
            if isinstance(x, torch.Tensor):
                x = x.cpu().numpy()
            converted_args.append(x)
        common_type = np.find_common_type([x.dtype for x in converted_args], [])
        for i in range(len(converted_args)):
            converted_args[i] = converted_args[i].astype(common_type)
    return converted_args


def has_torch(*args):
    return any([isinstance(x, torch.Tensor) for x in args])


def torch_isin(a, b):
    b = b.squeeze()
    return (a[..., None] == b).any(-1)


def filter_with_map(a, mask, out_map=True, in_map=True):
    # out_map: filt2org: return the in_indices corresponding to a[mask] (injective)
    # in_map: org2filt: return the out_indices corresponding to a (-1 for invalid)
    if has_torch(a):
        filt2org = mask.nonzero().squeeze(0)
    else:
        filt2org = np.argwhere(mask)

    if not in_map:  # only mapping a[mask] -> a
        if out_map:
            return a[mask], filt2org
        return a[mask]
    # compute mapping a -> a[mask]
    if has_torch(a):
        org2filt = torch.cumsum(mask, 0) - 1
    else:
        org2filt = np.cumsum(mask, 0) - 1

    org2filt[~mask] = -1
    if out_map:
        return a[mask], filt2org, org2filt
    return a[mask], org2filt


def dims(elements):
    dim_list = []
    for elem in elements:
        if has_torch(elem):
            dim_list.append(elem.dim())
        else:
            dim_list.append(len(elem.shape))
    return dim_list


def get_dim(elem):
    if has_torch(elem):
        return elem.dim()
    return len(elem.shape)


def cat(elements, *args, **kwargs):
    ignore_none = kwargs.get("ignore_none", False)
    if len(elements) == 0:
        return torch.empty(0)
    dim_list = dims(elements)
    dim = kwargs.get("dim", kwargs.get("axis", args[0] if len(args) > 0 else 0))

    max_dim = max(max(dim_list), dim + 1)
    reshaped_elements = []
    for elem in elements:
        if elem is None:
            if ignore_none:
                continue
            else:
                raise IOError("None in input list encountered: maybe set ignore_none=True")

        if get_dim(elem) == max_dim - 1:
            if has_torch(elem):
                reshaped_elements.append(elem.unsqueeze(dim))
            else:
                reshaped_elements.append(np.expand_dims(elem, dim))
        else:
            reshaped_elements.append(elem)
    if has_torch(*elements):
        return torch.cat(type_convert(*reshaped_elements), dim=dim)
    return np.concatenate(reshaped_elements, axis=dim)


def unique_agg(coords, feats, agg="mean"):
    unique_coords, all2unique, unique_counts = torch.unique(coords, dim=0, return_inverse=True, return_counts=True)
    temp_sparse = torch.sparse.FloatTensor(torch.stack([all2unique, torch.arange(len(all2unique)).to(all2unique)], 0), feats)
    if agg == "sum":
        agg_feats = torch.sparse.sum(temp_sparse, 1).values()
    elif agg == "mean":
        agg_feats = torch.sparse.sum(temp_sparse, 1).values() / unique_counts.unsqueeze(1)
    else:
        raise NotImplementedError
    return unique_coords, agg_feats


def majority_agg(coords, labels):
    unique_coords, all2unique, unique_counts = torch.unique(coords, dim=0, return_inverse=True, return_counts=True)
    unique_labels, all2unique_labels = torch.unique(labels, return_inverse=True)
    continuous_labels = torch.arange(len(unique_labels)).to(unique_labels)

    temp_sparse = torch.sparse.FloatTensor(
        torch.stack([all2unique, torch.arange(len(all2unique)).to(all2unique), all2unique_labels], 0),
        torch.ones(len(all2unique_labels)).to(labels),
    )
    continuous_maj = torch.sparse.sum(temp_sparse, 1).to_dense().argmax(1)
    return (unique_coords, unique_labels[continuous_maj])

def tensor_mem(tensor, grad_sep=False):
    grad_mem = 0
    if tensor.grad is not None:
        grad_mem = tensor_mem(tensor.grad)
    numel = tensor.storage().size()
    element_size = tensor.storage().element_size()
    mem = numel * element_size / 1024 / 1024  # 32bit=4Byte, MByte
    if grad_sep:
        return np.array([mem, grad_mem], dtype=np.float64)
    return mem + grad_mem


def mem_report(container, grad_sep=False):
    if grad_sep:
        total_mem = np.array([0, 0], dtype=np.float64)
    else:
        total_mem = 0
    if isinstance(container, (list, tuple)):
        for elem in container:
            total_mem += mem_report(elem, grad_sep)
    elif isinstance(container, dict):
        for elem_name, elem in container.items():
            total_mem += mem_report(elem, grad_sep)
    elif isinstance(container, torch.Tensor):
        total_mem += tensor_mem(container, grad_sep)
    elif isinstance(container, torch.nn.Module):
        for name, param in container.named_parameters():
            total_mem += mem_report(param, grad_sep)
    else:
        pass

    return total_mem

from collections import defaultdict

def get_human_readable_count(number: int) -> str:
    """Abbreviates an integer number with K, M, B, T for thousands, millions, billions and trillions, respectively.

    """
    PARAMETER_NUM_UNITS = [" ", "K", "M", "B", "T"]
    assert number >= 0
    labels = PARAMETER_NUM_UNITS
    num_digits = int(np.floor(np.log10(number)) + 1 if number > 0 else 1)
    num_groups = int(np.ceil(num_digits / 3))
    num_groups = min(num_groups, len(labels))  # don't abbreviate beyond trillions
    shift = -3 * (num_groups - 1)
    number = number * (10**shift)
    index = num_groups - 1
    if index < 1 or number >= 100:
        return f"{int(number):,d} {labels[index]}"

    return f"{number:,.1f} {labels[index]}"


def num_params(model, d=1, convert_table=False):
    from rich.console import Console, Text
    from rich.table import Table

    depth_named_nums = defaultdict(int)
    depth_named_nums_trainable = defaultdict(int)
    for name, p in model.named_parameters():
        sub_names = name.split('.')
        level_name = ".".join(sub_names[:d])
        depth_named_nums[level_name] += p.numel()
        if p.requires_grad:
            depth_named_nums_trainable[level_name] += p.numel()
    
    depth_named_nums = {k: (depth_named_nums[k], depth_named_nums_trainable[k]) for k in depth_named_nums}
    table = Table(header_style="bold magenta")
    table.add_column("Name",justify="left", no_wrap=True)
    table.add_column("# Params")
    table.add_column("# Trainable")
    total_num_params = 0
    total_num_trainable_params = 0
    for depth_name, (num_params, num_trainable_params)  in depth_named_nums.items():
        table.add_row(depth_name, get_human_readable_count(num_params), get_human_readable_count(num_trainable_params))
        total_num_params += num_params
        total_num_trainable_params += num_trainable_params 
    grid = Table.grid(expand=True)
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()
    grid.add_row(f"[bold]Trainable params[/]: {get_human_readable_count(total_num_trainable_params)}")
    grid.add_row(f"[bold]Non-trainable params[/]: {get_human_readable_count(total_num_params-total_num_trainable_params)}")
    grid.add_row(f"[bold]Total params[/]: {get_human_readable_count(total_num_params)}")
    if convert_table:
        console = Console()
        with console.capture() as capture:
            console.print('')
            console.print(table)
            console.print(grid)
        return str(Text.from_ansi(capture.get()))
    else:
        console = Console()
        console.print(table)
        console.print(grid)
    return depth_named_nums

def stats(*arrays):
    from rich.console import Console
    from rich.table import Table
    table = Table()
    table.add_column("min")
    table.add_column("0.25")
    table.add_column("mean")
    table.add_column("0.75")
    table.add_column("max")
    table.add_column("var")

    for x in arrays:
        if isinstance(x, torch.Tensor):
            x_min = x.min().item()
            x_25 = x.quantile(0.25)
            x_mean = x.mean().item()
            x_75 = x.quantile(0.75)
            x_max = x.max().item()
            x_var = x.var()
        else:
            x_min = x.min()
            x_25 = np.quantile(x,0.25)
            x_mean = x.mean()
            x_75 = np.quantile(x,0.75)
            x_max = x.max()
            x_var = x.var()
        table.add_row(f"{x_min:.3}", f"{x_25:.3}", f"{x_mean:.3}", f"{x_75:.3}", f"{x_max:.3}", f"{x_var:.3}")

    console = Console()
    console.print(table)

def seq2gif(seq, gif_path, fps=10):
    from moviepy.editor import ImageSequenceClip
    # ensure [0,255] format
    seq = np.array(seq)
    if seq.max()<=1.0:
        seq = (seq*255).astype(np.uint8)
    clip = ImageSequenceClip([img for img in seq], fps=fps)
    clip.write_gif(gif_path, fps=fps, verbose=False, logger=None)



def render_mesh(mesh, H,W=None,intrinsics=None, cam_pose=None):
    import os
    os.environ['PYOPENGL_PLATFORM'] = 'egl'
    import pyrender
    if W is None:
        W = H
    if intrinsics is None:
        intrinsics = np.array([[W,0,W/2],[0,H,H/2],[0,0,1]])
    if cam_pose is None:
        from dutils import look_at
        cam_pose = look_at(np.array([1,1,1]),np.zeros(3)) @ np.diag([1,1,-1,1])

    scene = pyrender.Scene()
    scene.add(pyrender.Mesh.from_trimesh(mesh))
    camera = pyrender.IntrinsicsCamera(fx=intrinsics[0,0], fy=intrinsics[1,1], cx=intrinsics[0,2], cy=intrinsics[1,2])
    scene.add(camera,pose=cam_pose)
    light = pyrender.SpotLight(color=np.ones(3), intensity=10.0)
    scene.add(light,pose=cam_pose)
    r = pyrender.OffscreenRenderer(viewport_width=W,viewport_height=H)
    color, depth = r.render(scene)
    r.delete()
    return color
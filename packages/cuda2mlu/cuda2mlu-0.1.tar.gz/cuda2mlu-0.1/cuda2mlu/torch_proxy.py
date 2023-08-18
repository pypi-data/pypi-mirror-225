import torch
import torch_mlu
from functools import wraps

def device_override(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = tuple(x.replace("cuda", "mlu") if isinstance(x, str) and "cuda" in x else x for x in args)
        if 'device' in kwargs and kwargs['device'] != None:
            dst_device = torch.device(kwargs['device'])
            if dst_device.type == 'cuda':
                kwargs['device'] = torch.device('mlu', dst_device.index)
        return func(*args, **kwargs)
    return wrapper

def backend_override(func):
    @wraps(func)
    def wrapper(backend, **kwargs):
        dst_backend = torch.distributed.Backend(backend)
        if dst_backend == 'nccl':
            dst_backend = torch.distributed.Backend('cncl')
        return func(dst_backend, **kwargs)
    return wrapper

torch.Tensor.to = device_override(torch.Tensor.to)
torch.nn.Module.to = device_override(torch.nn.Module.to) #function
torch.zeros = device_override(torch.zeros) #method
torch.tensor = device_override(torch.tensor) #method
torch.linspace = device_override(torch.linspace) #method
torch.zeros = device_override(torch.zeros) #method
torch.ones = device_override(torch.ones) #method
torch.randn = device_override(torch.randn) #method
torch.arange = device_override(torch.arange) #method
torch.as_tensor = device_override(torch.as_tensor) #method
torch.randperm = device_override(torch.randperm) #method
torch.full = device_override(torch.full) #method

torch.Tensor.cuda = torch.Tensor.mlu #method
torch.nn.Module.cuda = torch.nn.Module.mlu #function
torch.cuda.is_available = torch.mlu.is_available #function
torch.cuda._lazy_init = torch.mlu._lazy_init #function
torch.cuda.current_device = torch.mlu.current_device #function
torch.cuda.set_device = torch.mlu.set_device #function
torch.cuda.synchronize = torch.mlu.synchronize #function
torch.cuda.current_stream = torch.mlu.current_stream #function
torch.cuda.default_stream = torch.mlu.default_stream #function
torch.cuda.device_count = torch.mlu.device_count #function
torch.cuda.get_rng_state = torch.mlu.get_rng_state #function
torch.cuda.get_device_properties = torch.mlu.get_device_properties #function
torch.cuda.FloatTensor = torch.mlu.FloatTensor #class
torch.cuda.HalfTensor = torch.mlu.HalfTensor #class
torch.cuda.ByteTensor = torch.mlu.ByteTensor #class
torch.cuda.CharTensor = torch.mlu.CharTensor #class
torch.cuda.ShortTensor = torch.mlu.ShortTensor #class
torch.cuda.IntTensor = torch.mlu.IntTensor #class
torch.cuda.BoolTensor = torch.mlu.BoolTensor #class
torch.cuda.DoubleTensor = torch.mlu.DoubleTensor #class
torch.cuda.LongTensor = torch.mlu.LongTensor #class
torch.cuda.amp.autocast = torch.mlu.amp.autocast #class
torch.cuda.amp.GradScaler = torch.mlu.amp.GradScaler #class

torch.backends.cudnn.set_flags = torch.backends.mlufusion.set_flags #function
torch.backends.cudnn.flags = torch.backends.mlufusion.flags #function
torch.backends.cudnn.CudnnModule = torch.backends.mlufusion.MluModule #class
torch.backends.cudnn.allow_tf32 = torch.backends.cnnl.allow_tf32 #bool

torch.distributed.init_process_group = backend_override(torch.distributed.init_process_group)


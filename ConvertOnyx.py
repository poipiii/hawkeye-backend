import torch
import torch.onnx

from neosr.neosr.models import build_model
from neosr.neosr.utils.options import parse_options

# change this to your root path
root_path = "C:\\Users\\javie\\Downloads\\hallucination\\neosr\\"
opt, _ = parse_options(root_path, is_train=False)
model = build_model(opt)

g = model.net_g.cpu()

sample = torch.randn(1, 3, 128, 128)

torch.onnx.export(
    g,  # model being run
    sample,  # model input (or a tuple for multiple inputs)
    f"{opt['name']}.onnx",  # where to save the model (can be a file or file-like object)
    export_params=True,  # store the trained parameter weights inside the model file
    opset_version=11,  # the ONNX version to export the model to
    do_constant_folding=True,  # whether to execute constant folding for optimization
    input_names=["input"],  # the model's input names
    output_names=["output"],  # the model's output names
    dynamic_axes={
        "input": {0: "batch_size", 2: "height", 3: "width"},  # variable length axes
        "output": {0: "batch_size", 2: "height", 3: "width"},
    },
)
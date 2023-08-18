import torch
import torchvision


class TesterModule:
    def __init__(self, config=None, logger=None) -> None:
        pass

    def test(model, epoch=0, rank='cuda', *args, **kwargs):
        model.eval()
        d = {"dice": 0, "mre": 0} # ....
        return d
        
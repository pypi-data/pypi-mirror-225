import argparse


def trans_args(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(description='')
    try:
        parser.add_argument("--base_dir", type=str, default="")
    except:
        print("Already add '--tag' ")
    try:
            parser.add_argument("-t", "--tag", type=str, default="")
    except:
        print("Already add '--tag' ")
    try:
        parser.add_argument("-et", "--extag", type=str, default="")
    except:
        print("Already add '--extag' ")
    try:
        parser.add_argument("-c", "--config", type=str, default='./configs/config.yaml') 
    except:
        print("Already add '--config' ")
    try: 
        parser.add_argument("-exp", "--experiment", type=str, default='', help="experiment name")
    except:
        print("Already add '--experiment' ")
    try:
        parser.add_argument("-st", "--stage", type=str, default="", help="stage name for multi-stage experiment ")
    except:
        print("Already add '--stage' ")
    try:
        parser.add_argument("--test", action="store_true")
    except:
        print("Already add '--test' ")
    try:
        parser.add_argument("--func", type=str, default="train", help=" function name for test specific funciton ")
    except:
        print("Already add '--func' ")
    try:
        parser.add_argument("--ms", action="store_true", help=" Turn on Multi stage mode ! ")
    except:
        print("Already add '--ms' ")
    try:
        parser.add_argument("--gpus", type=str, default='', help=" Turn on Multi stage mode ! ")
    except:
        print("Already add '--gpus' ")
    args = parser.parse_args()
    return args   
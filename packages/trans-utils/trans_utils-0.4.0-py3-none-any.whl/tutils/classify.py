
import SimpleITK as sitk
import numpy as np
# import matplotlib.pyplot as plt
# image = sitk.ReadImage(r"D:\Data\LIDC-IDRI\DOI\LIDC-IDRI-0162\1.3.6.1.4.1.14519.5.2.1.6279.6001.100063870746088919758706456900\1.3.6.1.4.1.14519.5.2.1.6279.6001.837810280808122125183730411210\000128.dcm")
import os
import pandas as pd
from shutil import move, copy


def collect_meta_info(dirpath = "/home1/quanquan/datasets/MR202012100551/"):
    dlist = []
    for fname in os.listdir(dirpath):
        try:
            image = sitk.ReadImage(os.path.join(dirpath, fname))
        except:
            continue
        d = {}
        d["name"] = fname
        for k in image.GetMetaDataKeys():
            v = image.GetMetaData(k)
            # print(k, ": ", v)
            d[k] = v
        dlist.append(d)
        # break

    data = pd.DataFrame(dlist)
    dirname = dirpath.split('/')[-1]
    data.to_csv(dirname+".csv")
    return data

def classify(pd_data, key="0008|103e", dirpath=None):
    names = []
    names.append("backup")
    dname = os.path.join(dirpath, names[0])
    if not os.path.exists(dname):
        os.makedirs(dname)

    for c, fname in zip(pd_data[key], pd_data['name']):
        if c not in names:
            names.append(c)
            dname = os.path.join(dirpath, c)
            if not os.path.exists(dname):
                os.makedirs(dname)
        copy(os.path.join(dirpath, fname), os.path.join(dirpath, c, fname))
        move(os.path.join(dirpath, fname), os.path.join(dirpath, "backup", fname))

    # import ipdb; ipdb.set_trace()
    

def main():
    dirpaths = os.listdir()
    dirpaths = [os.path.join("./", dirname) for dirname in dirpaths if os.path.isdir(dirname)]
    for dirpath in dirpaths:
        names = [fname for fname in os.listdir(dirpath) if fname.endswith("dcm")]
        if len(names) <= 0:
            print("Ignore ", dirpath)
            continue
        print("Processing ", dirpath)
        data = collect_meta_info(dirpath)
        classify(data, dirpath=dirpath)
        


if __name__ == '__main__':
    main()
    # data = pd.read_csv("mrdata.csv")

    # import ipdb; ipdb.set_trace()

# import ipdb; ipdb.set_trace()
    # image_array = np.squeeze(sitk.GetArrayFromImage(image)) 
    # plt.imshow(image_array)
    # plt.show()
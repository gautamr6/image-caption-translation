import math
import numpy as np

from PIL import Image
import requests
import matplotlib.pyplot as plt
# config InlineBackend.figure_format = 'retina'

import ipywidgets as widgets
from IPython.display import display, clear_output

import torch
from torch import nn
from torchvision.models import resnet50
import torchvision.transforms as T
torch.set_grad_enabled(False);
torch.set_printoptions(profile="full")

# COCO classes
CLASSES = [
    'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
    'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
    'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

# standard PyTorch mean-std input image normalization
transform = T.Compose([
    T.Resize(100),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

transformEmpty = T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

def plot_results(pil_img, prob, boxes):
    plt.figure(figsize=(16,10))
    plt.imshow(pil_img)
    ax = plt.gca()
    colors = COLORS * 100
    for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        cl = p.argmax()
        text = f'{CLASSES[cl]}: {p[cl]:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()

class Data:
    def __init__(self) -> None:
        pass
        # self.indexMap = indexes()
            
    def __iter__(self):
        self.index = 1
        return self
    
    def __next__(self):
        if self.index <= 27594:
            # Machine translations
            # imageIndex = self.indexMap[metadataLine[:-1]]
            imageFilename = "images-en-es/files/img" + str(self.index).zfill(8)
            try:
                imageFile = Image.open(imageFilename)
                imageArray = transform(imageFile).unsqueeze(0)
            except:
                imageArray = transformEmpty(torch.from_numpy(np.zeros((3, 100, 100)))).unsqueeze(0)
            self.index += 1
            return imageArray
        else:
            raise StopIteration

def main_func():
    model = torch.hub.load('facebookresearch/detr', 'detr_resnet50', pretrained=True)
    model.eval();

    dt = Data()
    dt_iter = iter(dt)

    i = 0

    f = open("objects.txt", "w")

    for img in dt_iter:
        i = i + 1
        if (i % 1000 == 0):
            print(i + "/27367 complete")
        # image = transform(img).unsqueeze(0)
        outputs = model(img)
        probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
        keep = probas.max(-1).values > 0.9
        try:
            max_prob, max_ind = torch.max(probas[keep], dim = 1)
        except: 
            max_ind = torch.zeros(1)

        f.write(str(max_ind) + "\n")
        # objects.append(max_ind)
    
    # f.write(objects)
    f.close()

main_func()
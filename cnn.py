import random

import torchvision
from PIL import Image
import cv2
import numpy as np
import torchvision.transforms as T
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__',
    'personne',
    'vélo',
    'voiture',
    'moto',
    'avion',
    'bus',
    'train',
    'camion',
    'bateau',
    'traffic light',
    'fire hydrant',
    'N/A',
    'stop sign',
    'parking meter',
    'banc',
    'oiseau',
    'chat',
    'chien',
    'cheval',
    'mouton',
    'vache',
    'éléphant',
    'ours',
    'zébra',
    'girafe',
    'N/A',
    'sac à dos',
    'parapluie',
    'N/A',
    'N/A',
    'handbag',
    'tie',
    'suitcase',
    'frisbee',
    'skis',
    'snowboard',
    'sports ball',
    'kite',
    'baseball bat',
    'baseball glove',
    'skateboard',
    'surfboard',
    'tennis racket',
    'bottle',
    'N/A',
    'wine glass',
    'cup',
    'Fourchette',
    'Couteau',
    'spoon',
    'bowl',
    'banana',
    'apple',
    'sandwich',
    'orange',
    'broccoli',
    'carrot',
    'hot dog',
    'pizza',
    'donut',
    'cake',
    'chaise',
    'couch',
    'potted plant',
    'bed', 'N/A',
    'dining table',
    'N/A',
    'N/A',
    'toilet',
    'N/A',
    'tv',
    'laptop',
    'mouse',
    'remote',
    'keyboard',
    'cell phone',
    'microwave',
    'oven',
    'toaster',
    'sink',
    'refrigerator',
    'N/A',
    'book',
    'clock',
    'vase',
    'scissors',
    'teddy bear',
    'hair drier',
    'toothbrush'
]

list_colors = [
    [0, 0, 255],
    [0, 255, 0],
    [0, 255, 255],
    [255, 0, 0],
    [255, 0, 255],
    [255, 255, 0],

    [0, 0, 127],
    [0, 127, 0],
    [0, 127, 127],
    [127, 0, 0],
    [127, 0, 127],
    [127, 127, 0],

    [0, 127, 255],
    [127, 0, 255],
    [127, 255, 0],

    [0, 255, 127],
    [255, 0, 127],
    [255, 127, 0]

]

def get_prediction(img_path, threshold):
    img = Image.open(img_path)
    transform = T.Compose([T.ToTensor()])
    img = transform(img)
    pred = model([img])
    pred_score = list(pred[0]['scores'].detach().numpy())
    pred_t = [pred_score.index(x) for x in pred_score if x>threshold][-1]
    masks = (pred[0]['masks']>0.5).squeeze().detach().cpu().numpy()
    pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())]
    pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())]
    masks = masks[:pred_t+1]
    pred_boxes = pred_boxes[:pred_t+1]
    pred_class = pred_class[:pred_t+1]

    return masks, pred_boxes, pred_class


def colour_mask(image, color):
    # colours = [[0, 255, 0],[0, 0, 255],[255, 0, 0],[0, 255, 255],[255, 255, 0],[255, 0, 255],[80, 70, 180],[250, 80, 190],[245, 145, 50],[70, 150, 250],[50, 190, 190]]

    v = random.random() / 2 + 0.5

    color = [int(color[0] * v), int(color[1] * v), int(color[2] * v)]

    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)
    r[image == 1], g[image == 1], b[image == 1] = color
    coloured_mask = np.stack([r, g, b], axis=2)
    return coloured_mask

def instance_segmentation_api(img_path, out_fp, threshold=0.5, rect_th=3, text_size=3, text_th=3):

    masks, boxes, pred_cls = get_prediction(img_path, threshold)




    img = cv2.imread(img_path)
    img //= 2

    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    SEEN = []
    for i in range(len(masks)):
        if not pred_cls[i] in SEEN:
            SEEN.append(pred_cls[i])
            if len(SEEN) > len(list_colors):
                break

        color = list_colors[SEEN.index(pred_cls[i])]
        rgb_mask = colour_mask(masks[i], color)
        img = cv2.addWeighted(img, 1, rgb_mask, 0.9, 0)
        x1, y1 = boxes[i][0]
        x2, y2 = boxes[i][1]
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        cv2.rectangle(img, [x1, y1], [x2, y2],color=color, thickness=2)
        cv2.putText(img,pred_cls[i], [x1, y1], cv2.FONT_HERSHEY_SIMPLEX, 1, color,thickness=1)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(out_fp, img)



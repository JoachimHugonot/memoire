import random
import torchvision
import cv2
import numpy as np
import torchvision.transforms as transforms

model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__',
    'Personne',
    'Vélo',
    'Voiture',
    'Moto',
    'Avion',
    'Bus',
    'Train',
    'Camion',
    'Bateau',
    'Feu de circulation',
    'Bouche d\'incendie',
    'N/A',
    'Stop',
    'Parcmètre',
    'Banc',
    'Oiseau',
    'Chat',
    'Chien',
    'Cheval',
    'Mouton',
    'Vache',
    'Eléphant',
    'Ours',
    'Zébre',
    'Girafe',
    'N/A',
    'Sac à dos',
    'Parapluie',
    'N/A',
    'N/A',
    'Sac à main',
    'Cravate',
    'Malette',
    'Frisbee',
    'Ski',
    'Snowboard',
    'Ballon',
    'Cerf-volant',
    'Batte',
    'Gant de baseball',
    'Skateboard',
    'Planche de surf',
    'Raquette',
    'Bouteille',
    'N/A',
    'Verre à vin',
    'Tasse',
    'Fourchette',
    'Couteau',
    'Cuillère',
    'Bol',
    'Banane',
    'Bomme',
    'Sandwich',
    'Orange',
    'Brocoli',
    'Carotte',
    'Hot-dog',
    'Pizza',
    'Donut',
    'Gâteau',
    'Chaise',
    'Canapé',
    'Plante en pot',
    'Lit',
    'N/A',
    'Table à manger',
    'N/A',
    'N/A',
    'Toilettes',
    'N/A',
    'Télévision',
    'Ordinateur',
    'Souris',
    'Télécommande',
    'Clavier',
    'Natel',
    'Micro-ondes',
    'Four',
    'Grille-pain',
    'Evier',
    'Réfrigérateur',
    'N/A',
    'Livre',
    'Horloge',
    'Vase',
    'Ciseaux',
    'Peluche',
    'Sèche-cheveux',
    'Brosse à dents'
]

list_colors = [
    [0, 0, 175],
    [0, 175, 0],
    [0, 175, 175],
    [175, 0, 0],
    [175, 0, 175],
    [175, 175, 0],

    [0, 0, 127],
    [0, 127, 0],
    [0, 127, 127],
    [127, 0, 0],
    [127, 0, 127],
    [127, 127, 0],

    [0, 127, 175],
    [127, 0, 175],
    [127, 175, 0],

    [0, 175, 127],
    [175, 0, 127],
    [175, 127, 0]

]


def get_prediction(img, threshold):
    transform = transforms.Compose([transforms.ToTensor()])
    img = transform(img)
    pred = model([img])
    pred_score = list(pred[0]['scores'].detach().numpy())
    if len([pred_score.index(x) for x in pred_score if x > threshold]) == 0:
        return [], [], []
    pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1]
    masks = (pred[0]['masks'] > 0.5).squeeze().detach().cpu().numpy()
    pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())]
    pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())]
    masks = masks[:pred_t + 1]
    pred_boxes = pred_boxes[:pred_t + 1]
    pred_class = pred_class[:pred_t + 1]

    return masks, pred_boxes, pred_class


def colour_mask(image, color):

    v = random.random() / 2 + 0.5

    color = [int(color[0] * v), int(color[1] * v), int(color[2] * v)]

    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)
    r[image == 1], g[image == 1], b[image == 1] = color
    coloured_mask = np.stack([r, g, b], axis=2)
    return coloured_mask


def instance_segmentation_api(img, threshold=0.5):
    if len(img.shape) == 3:
        h, w, _ = img.shape
    elif len(img.shape) == 2:
        h, w = img.shape
    ratio = h / 600
    new_h = int(h / ratio)
    new_w = int(w / ratio)
    img = cv2.resize(img, (new_w, new_h))
    img //= 2

    masks, boxes, pred_cls = get_prediction(img, threshold)

    seen = []
    colors = []
    for i in range(len(masks)):
        if not pred_cls[i] in seen:
            seen.append(pred_cls[i])
            if len(seen) > len(list_colors):
                break
            colors.append(list_colors[seen.index(pred_cls[i])])

        color = list_colors[seen.index(pred_cls[i])]
        rgb_mask = colour_mask(masks[i], color)
        img = cv2.addWeighted(img, 1, rgb_mask, 0.9, 0)

    return img, seen, colors

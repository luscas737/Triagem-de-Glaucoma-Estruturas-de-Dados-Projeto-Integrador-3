import json
import torch
import timm
import cv2
import numpy as np
from PIL import Image
from albumentations import Compose, Normalize
from albumentations.pytorch import ToTensorV2

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CFG_PATH = "models/convnext_tiny.json"
WEIGHTS_PATH = "models/convnext_tiny.pt.zip"

cfg = None
model = None

transform = Compose([
    Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
    ToTensorV2()
])

def carregar_modelo():
    global cfg, model

    if model is not None:
        return model

    with open(CFG_PATH) as f:
        cfg = json.load(f)

    model = timm.create_model(
        cfg["model_name"],
        pretrained=False,
        num_classes=11
    )

    model.head.fc = torch.nn.Sequential(
        model.head.fc,
        torch.nn.Sigmoid()
    )

    state_dict = torch.load(
        WEIGHTS_PATH,
        map_location=DEVICE
    )

    model.load_state_dict(
        state_dict,
        strict=False
    )

    model.to(DEVICE)
    model.eval()

    return model


def predict(image_path):

    modelo = carregar_modelo()

    img_size = cfg.get("IMG_SIZE", 224)

    image = Image.open(image_path).convert("RGB")
    image = np.array(image)

    image = cv2.resize(image, (img_size, img_size))

    tensor = transform(image=image)["image"]
    tensor = tensor.unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        pred = modelo(tensor)

    return pred.squeeze().cpu().numpy()
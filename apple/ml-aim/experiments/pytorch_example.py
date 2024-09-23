from PIL import Image

from aim.utils import load_pretrained
from aim.torch.data import val_transforms

default_model_name = "aim-600M-2B-imgs"

def load_image(image_name, model_name=default_model_name):
	print(f"Opening image: {image_name}")
	img = Image.open(image_name)
	print(f"Loading model: {model_name}")
	model = load_pretrained(model_name, backend="torch")
	transform = val_transforms()

	inp = transform(img).unsqueeze(0)
	logits, features = model(inp)
	return logits, features


default_hub = "torch" # huggingface

def load_model(model_name, hub="torch"):
	if hub == "torch":
		import torch
		return torch.hub.load("apple/ml-aim", model_name)
	elif hub == "huggingface":
		from aim.torch.models import AIMForImageClassification
		return AIMForImageClassification.from_pretrained(f"apple/{model_name}")
	else:
		raise Exception(f"Unrecognized hub value: {hub}")


# aim_600m = load_model("aim_600M", hub=which_hub)
# aim_1b   = load_model("aim_1B",   hub=which_hub)
# aim_3b   = load_model("aim_3B",   hub=which_hub)
# aim_7b   = load_model("aim_7B",   hub=which_hub)

logits, features = load_image("/Users/deanwampler/Pictures/Night Out 001.jpg")
print(f'logits: {logits}\n')
print(f'features: {features}')


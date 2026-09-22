import torch
import sys
import json
import albumentations as A


from app.ml.vendor.model import DETR



class SignDETRHandler:
    def __init__(self, model_path: str = "app/ml/vendor/pretrained/4426_model.pt"):
        """Load and initialize SignDETR model"""
        try:
            self.model = DETR(num_classes=3)
            self.model.eval()
            self.model.load_pretrained(model_path)
        except Exception as e:
            print(f"error loading model{e}")
        finally:
            print("")



        # Image transforms (from realtime.py)
        self.transforms = A.Compose([
            A.Resize(224, 224),
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
            A.ToTensorV2()
        ])
        self.classes = self.get_classes()


    def get_classes(self):
        config_path = "app/ml/vendor/config.json"
        try:
            with open(config_path) as f:
                config = json.load(f)
            classes = config['classes']
            assert len(classes) > 0, "Classes list cannot be empty"
            return classes
        except Exception as e:
            print(f"Something went wrong loading your config file: {e}")
            raise

    def detect(self, frame):
        """
        Run inference on a frame

        Args:
            frame: numpy array (BGR image)

        Returns:
            tuple: (sign_label, confidence_score)
        """
        # Transform frame
        transformed = self.transforms(image=frame)
        frame_tensor = torch.unsqueeze(transformed['image'], dim=0)

        # Inference
        with torch.no_grad():
            result = self.model(frame_tensor)

        # Parse results
        probabilities = result['pred_logits'].softmax(-1)[:, :, :-1]
        max_probs, max_classes = probabilities.max(-1)
        keep_mask = max_probs > 0.7  # Confidence threshold

        batch_indices, query_indices = torch.where(keep_mask)

        if len(batch_indices) == 0:
            # No detections
            return None, 0.0

        # Get best detection
        best_idx = max_probs[batch_indices, query_indices].argmax()
        best_class = max_classes[batch_indices, query_indices][best_idx].item()
        best_confidence = max_probs[batch_indices, query_indices][best_idx].item()

        sign = self.classes[best_class]

        return sign, best_confidence


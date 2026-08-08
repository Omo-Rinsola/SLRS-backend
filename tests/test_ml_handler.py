import cv2
import numpy as np
from pathlib import Path
from app.ml.signdetr_handler import SignDETRHandler

def test_handler():
    #  LOAD MODEL
    print("Loading model ....")
    try:
        handler = SignDETRHandler()
        print("Model loaded successfully0")

        # LOAD IMAGE
        test_dir = Path(__file__).parent
        image_path = test_dir / "images" / "thankyou.jpg"
        frame = cv2.imread(str(image_path))
        if frame is None:
            print("Image not found")
            return
        # DETECT IMAGE
        sign, best_confidence = handler.detect(frame)
        print(f"sign: {sign} \n confidence: {best_confidence}")
    except Exception as e:
        print("Model failed to load: ", e)
        raise


if __name__ == "__main__":
    test_handler()
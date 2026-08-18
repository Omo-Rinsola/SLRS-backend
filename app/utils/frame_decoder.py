import cv2
import numpy as np

def decode_frame(image_bytes):
    # convert to  1D unsigned 8-bit integer array
    img_buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    img_array = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
    return img_array

import base64
import cv2
import numpy as np

def decode_frame(b64_image_string):
    if "," in b64_image_string:
        b64_image_string = b64_image_string.split(",")[1]
    # decode string to raw image file bytes
    image_bytes = base64.b64decode(b64_image_string)
    # convert to  1D unsigned 8-bit integer array
    img_buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    img_array = cv2.imdecode(img_buffer, cv2.IMREAD_COLOR)
    return img_array

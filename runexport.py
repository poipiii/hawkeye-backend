# import onnxruntime
# import cv2
# import numpy as np
# import os

# # Define the path to the "after" folder
# AFTER_FOLDER = 'after'
# AFTER_FOLDER_PATH = os.path.join(os.getcwd(), AFTER_FOLDER)

# ort_session = onnxruntime.InferenceSession(
#     "run_cugan.onnx", providers=["CPUExecutionProvider"]
# )

# imgpath = "C:\\Users\\noel2\\hawkeye-backend\\before"
# img = cv2.imread(imgpath)[:512, -512:, :]
# img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)

# # img is a height x width x 3 array from 0 to 255.
# # model expects 1 x 3 x height x width from 0 to 1.
# down = img / 255
# down = down.astype(np.float32)
# down = down.transpose(2, 0, 1)[None, :, :, :]

# # send to onnxruntime
# ort_inputs = {"input": down}
# ort_outs = ort_session.run(None, ort_inputs)[0]

# # back to height x width x 3 array from 0 to 255
# ort_outs = ort_outs[0].transpose(1, 2, 0) * 255

# # save the processed images into the "after" folder
# cv2.imwrite(os.path.join(AFTER_FOLDER_PATH, "exportlow.png"), img)
# cv2.imwrite(os.path.join(AFTER_FOLDER_PATH, "exporthigh.png"), ort_outs)

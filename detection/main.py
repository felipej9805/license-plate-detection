import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr
import util
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def root_endpoint():
    return """
    <html>
    <head>
        <title>Home Detection Page</title>
    </head>
    <body>
        <h1>Welcome to the Home Detection Page!</h1>
    </body>
    </html>
    """


@app.route('/default', methods=['GET'])
def default_endpoint():
    return """
    <html>
    <head>
        <title>Default Endpoint</title>
    </head>
    <body>
        <h1>Welcome to the default endpoint!</h1>
    </body>
    </html>
    """


@app.route('/detection', methods=['GET'])
def api_endpoint():
    # define constants
    model_cfg_path = os.path.join('.', 'model', 'cfg', 'darknet-yolov3.cfg')
    model_weights_path = os.path.join('.', 'model', 'weights', 'model.weights')
    class_names_path = os.path.join('.', 'model', 'class.names')
    input_dir = "./data"

    for img_name in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_name)

        # load class names
        with open(class_names_path, 'r') as f:
            class_names = [j[:-1] for j in f.readlines() if len(j) > 2]
            f.close()

        # load model
        net = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)

        # load image
        img = cv2.imread(img_path)
        H, W, _ = img.shape

        # convert image
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True)

        # get detections
        net.setInput(blob)
        detections = util.get_outputs(net)

        # bboxes, class_ids, confidences
        bboxes = []
        class_ids = []
        scores = []

        for detection in detections:
            # [x1, x2, x3, x4, x5, x6, ..., x85]
            bbox = detection[:4]

            xc, yc, w, h = bbox
            bbox = [int(xc * W), int(yc * H), int(w * W), int(h * H)]

            bbox_confidence = detection[4]

            class_id = np.argmax(detection[5:])
            score = np.amax(detection[5:])

            bboxes.append(bbox)
            class_ids.append(class_id)
            scores.append(score)

        # apply nms
        bboxes, class_ids, scores = util.NMS(bboxes, class_ids, scores)

        # plot
        reader = easyocr.Reader(['en'])
        for bbox_, bbox in enumerate(bboxes):
            xc, yc, w, h = bbox

            # cv2.putText(img,
            #             class_names[class_ids[bbox_]],
            #             (int(xc - (w / 2)), int(yc + (h / 2) - 20)),
            #             cv2.FONT_HERSHEY_SIMPLEX,
            #             7,
            #             (0, 255, 0),
            #             15)
            license_plate = img[int(
                yc - (h / 2)):int(yc + (h / 2)), int(xc - (w / 2)):int(xc + (w / 2)), :].copy()
            img = cv2.rectangle(img,
                                (int(xc - (w / 2)), int(yc - (h / 2))),
                                (int(xc + (w / 2)), int(yc + (h / 2))),
                                (0, 255, 0),
                                10)

            license_plate_gray = cv2.cvtColor(
                license_plate, cv2.COLOR_BGR2GRAY)
            _, license_plate_thresh = cv2.threshold(
                license_plate_gray, 64, 255, cv2.THRESH_BINARY_INV)

            output = reader.readtext(license_plate_thresh)

            for out in output:
                text_bbox, text, text_score = out
                # if text_score > 0.1:
                output_text = text
                print(text, text_score)

    response = jsonify(message=output_text)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT_DETECTION', 5000))
    app.run(port=port)

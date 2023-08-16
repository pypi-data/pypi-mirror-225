import cv2
import numpy as np
import torch
from ..utils import F3Net


class Segment(object):
    def __init__(self, model_name='models/model-199-0.041477009654045105', image_size=(1900, 200), ctx_id=-1):
        self.model_name = model_name
        self.image_size = image_size
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.model = self.load_model()

    def load_model(self):
        net = F3Net()
        net.load_state_dict(torch.load(self.model_name, map_location=None if torch.cuda.is_available() else 'cpu'))
        if torch.cuda.is_available():
            net.to(self.device)
        net.eval()

        return net

    @staticmethod
    def to_tensor(image):
        temp = np.zeros((image.shape[0], image.shape[1], 3))
        if len(image.shape) == 2:
            image = image.reshape(image.shape[0], image.shape[1], 1)
            temp[:, :, 0] = (image[:, :, 0] - 124.55) / 56.77
            temp[:, :, 1] = (image[:, :, 0] - 124.55) / 56.77
            temp[:, :, 2] = (image[:, :, 0] - 124.55) / 56.77
        else:
            temp[:, :, 0] = (image[:, :, 0] - 124.55) / 56.77
            temp[:, :, 1] = (image[:, :, 1] - 118.90) / 55.97
            temp[:, :, 2] = (image[:, :, 2] - 102.94) / 57.50
        temp = temp.transpose((2, 0, 1))
        return torch.tensor(temp, requires_grad=False, device=torch.device('cuda'))

    def predict(self, image):
        temp = cv2.resize(image, self.image_size, interpolation=cv2.INTER_LINEAR)
        temp = self.to_tensor(temp)
        temp = temp.unsqueeze(0)
        pred = self.model(temp.float())[1]
        pred = (torch.sigmoid(pred[0, 0])).cpu().data.numpy()
        pred = np.asarray(pred * 255).astype(np.uint8)
        _, pred = cv2.threshold(pred, 128, 255, cv2.THRESH_BINARY)

        torch.cuda.empty_cache()
        return pred

    @staticmethod
    def get_mask(pred, w, h):
        contours = cv2.findContours(pred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        area = [cv2.contourArea(c) for c in contours]
        if len(area) == 0: return None
        max_idx = np.argmax(area)
        pred = cv2.fillPoly(pred, [contours[max_idx]], 255)

        h1, w1 = pred.shape
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(w1 / 4), int(h1 / 4)))
        pred = cv2.morphologyEx(pred, cv2.MORPH_OPEN, kernel, iterations=5)
        kernel = np.ones((7, 7), np.uint8)
        pred = cv2.dilate(pred, kernel, iterations=1)
        for k in range(len(contours)):
            if k != max_idx:
                cv2.fillPoly(pred, [contours[k]], 0)
        pred = cv2.resize(pred, (w, h), interpolation=cv2.INTER_LINEAR)

        return pred.astype(np.uint8)


import mxnet as mx
import numpy as np
from config import config


class Accuracy(mx.metric.EvalMetric):
    def __init__(self):
        super(Accuracy, self).__init__('acc')

    def update(self, labels, preds):
        # output: cls_prob_output, cls_keep_inds, bbox_pred_output,bbox_keep_inds, landmark_pred_output, landmark_keep_inds
        # label: type_label, label, bbox_target, landmark_target
        pred_label = mx.ndarray.argmax_channel(preds[0]).asnumpy().astype('int32')
        label = labels[1].asnumpy()

        # negative mining
        cls_keep = preds[1].asnumpy()
        keep = np.where(cls_keep == 1)[0]

        pred_label = pred_label[keep]
        label = label[keep]

        self.sum_metric += (pred_label.flat == label.flat).sum()
        self.num_inst += len(pred_label.flat)


class LogLoss(mx.metric.EvalMetric):
    def __init__(self):
        super(LogLoss, self).__init__('loss')

    def update(self, labels, preds):
        # output: cls_prob_output, cls_keep_inds, bbox_pred_output,bbox_keep_inds, landmark_pred_output, landmark_keep_inds
        # label: type_label, label, bbox_target, landmark_target
        pred_cls = preds[0].asnumpy()
        label = labels[1].asnumpy().astype('int32')

        cls_keep = preds[1].asnumpy()
        keep = np.where(cls_keep == 1)[0]

        pred_cls = pred_cls[keep].reshape(-1, 2)
        label = label[keep]

        cls = pred_cls[np.arange(label.shape[0]), label.flat]

        cls += config.EPS
        cls_loss = -1 * np.log(cls)

        cls_loss = np.sum(cls_loss)
        self.sum_metric += cls_loss
        self.num_inst += label.shape[0]


class BBOX_MSE(mx.metric.EvalMetric):
    def __init__(self):
        super(BBOX_MSE, self).__init__('boxL2')

    def update(self,labels, preds):
        # output: cls_prob_output, cls_keep_inds, bbox_pred_output,bbox_keep_inds, landmark_pred_output, landmark_keep_inds
        # label: type_label, label, bbox_target, landmark_target
        pred_delta = preds[2].asnumpy()
        bbox_target = labels[2].asnumpy()

        bbox_keep = preds[3].asnumpy()
        keep = np.where(bbox_keep == 1)[0]

        pred_delta = pred_delta[keep]
        bbox_target = bbox_target[keep]
        #print(preds)
        #print(labels)
        e = (pred_delta - bbox_target)**2
        error = np.sum(e)
        self.sum_metric += error
        self.num_inst += e.size
		
class BBOX_L1(mx.metric.EvalMetric):
    def __init__(self):
        super(BBOX_L1, self).__init__('boxL1')

    def update(self,labels, preds):
        # output: cls_prob_output, cls_keep_inds, bbox_pred_output,bbox_keep_inds, landmark_pred_output, landmark_keep_inds
        # label: type_label, label, bbox_target, landmark_target
        pred_delta = preds[2].asnumpy()
        bbox_target = labels[2].asnumpy()

        bbox_keep = preds[3].asnumpy()
        keep = np.where(bbox_keep == 1)[0]

        pred_delta = pred_delta[keep]
        bbox_target = bbox_target[keep]
        #print(preds)
        #print(labels)
        e = abs(pred_delta - bbox_target)
        error = np.sum(e)
        self.sum_metric += error
        self.num_inst += e.size

class LANDMARK_MSE(mx.metric.EvalMetric):
    def __init__(self):
        super(LANDMARK_MSE, self).__init__('lmL2')

    def update(self,labels, preds):
        # output: cls_prob_output, cls_keep_inds, bbox_pred_output,bbox_keep_inds, landmark_pred_output, landmark_keep_inds
        # label: type_label, label, bbox_target, landmark_target
        pred_delta = preds[4].asnumpy()
        landmark_target = labels[3].asnumpy()

        landmark_keep = preds[5].asnumpy()
        keep = np.where(landmark_keep == 1)[0]

        pred_delta = pred_delta[keep]
        landmark_target = landmark_target[keep]
        #print(preds)
        #print(labels)
        e = (pred_delta - landmark_target)**2
        error = np.sum(e)
        self.sum_metric += error
        self.num_inst += e.size

class LANDMARK_L1(mx.metric.EvalMetric):
    def __init__(self):
        super(LANDMARK_L1, self).__init__('lmL1')

    def update(self,labels, preds):
        # output: cls_prob_output, cls_keep_inds, bbox_pred_output,bbox_keep_inds, landmark_pred_output, landmark_keep_inds
        # label: type_label, label, bbox_target, landmark_target
        pred_delta = preds[4].asnumpy()
        landmark_target = labels[3].asnumpy()

        landmark_keep = preds[5].asnumpy()
        keep = np.where(landmark_keep == 1)[0]

        pred_delta = pred_delta[keep]
        landmark_target = landmark_target[keep]

        e = abs(pred_delta - landmark_target)
        error = np.sum(e)
        self.sum_metric += error
        self.num_inst += e.size
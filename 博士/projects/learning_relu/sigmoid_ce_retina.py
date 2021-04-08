import numpy as np
import torch


eps = np.finfo(np.float32).tiny


class SafeLog():
    r"""
    Safly perform log operation
    """
    default_hyper_params = dict()

    def __init__(self):
        super(SafeLog, self).__init__()

    def forward(self, t):
        return torch.log(torch.max(torch.tensor(eps, requires_grad=False), t))


class SigmoidCrossEntropyRetina():
    def forward(self, pred_data, target_data):
        r"""
        Focal loss
        :param pred: shape=(B, HW, C), classification logits (BEFORE Sigmoid)
        :param label: shape=(B, HW)
        """
        r"""
        Focal loss
        Arguments
        ---------
        pred: torch.Tensor
            classification logits (BEFORE Sigmoid)
            format: (B, HW)
        label: torch.Tensor
            training label
            format: (B, HW)

        Returns
        -------
        torch.Tensor
            scalar loss
            format: (,)
        """

        """设定参数"""
        self.alpha = 0.75
        self.gamma = 2

        pred = pred_data

        """调整形状"""
        pred = pred.permute(0, 2, 3, 1)
        pred = pred.reshape(pred.shape[0], -1, 1)

        label = target_data
        label = label.reshape(label.shape[0], -1, 1)
        mask = label >= 0
        mask = mask.type(torch.Tensor).to(label.device)
        vlabel = label * mask
        zero_mat = torch.zeros(pred.shape[0], pred.shape[1], pred.shape[2] + 1)

        one_mat = torch.ones(pred.shape[0], pred.shape[1], pred.shape[2] + 1)
        index_mat = vlabel.type(torch.LongTensor)

        onehot_ = zero_mat.scatter(2, index_mat, one_mat)
        onehot = onehot_[:, :, 1:].type(torch.Tensor).to(pred.device)

        pred = torch.sigmoid(pred)

        eps_torch = torch.tensor(eps, requires_grad=False).to(pred.device)
        pos_part = (1 - pred)**self.gamma * onehot * torch.log(torch.max(eps_torch, pred))
        neg_part = pred**self.gamma * (1 - onehot) * torch.log(torch.max(eps_torch, 1 - pred))  # safe log 是必须的，否则可能 nan
        loss = -(self.alpha * pos_part +
                 (1 - self.alpha) * neg_part).sum(dim=2) * mask.squeeze(2)

        positive_mask = (label > 0).type(torch.Tensor).to(pred.device)

        loss = loss.sum() / positive_mask.sum()

        return loss

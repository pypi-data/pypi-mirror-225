import torch
import torch.nn as nn
import torch.nn.functional as F

EPS = 1e-8


### TODO: Documentation
def Entropy(img, isprobability):
    """
    Helper function to compute the entropy over the batch.

    Args:
        img (torch.nn tensor): Inupt tensor for which entropy will be calculated.
        isprobability (bool): True if input values represent probabilities, False otherwise.

    :return: *(float)*: \n
        Entropy of the input tensor.
    """

    if isprobability:
        x_ = torch.clamp(img, min=EPS)
        b = x_ * torch.log(x_)
    else:
        b = F.softmax(img, dim=1) * F.log_softmax(img, dim=1)

    if len(b.size()) == 2:  # Sample-wise entropy
        return -b.sum(dim=1).mean()
    elif len(b.size()) == 1:  # Distribution-wise entropy
        return -b.sum()
    else:
        raise ValueError('Input tensor is %d-Dimensional' % (len(b.size())))


class SCANLoss(nn.Module):
    """
    Scan Loss algorithm architecture for pixel-based clustering.

    Args:
        entropy_weight (float): Coefficient by which to weight entropy component of loss value.
    """

    def __init__(self, entropy_weight=10):
        super(SCANLoss, self).__init__()
        self.softmax = nn.Softmax(dim=1)
        self.bce = nn.BCELoss()
        self.entropy_weight = entropy_weight

    def forward(self, anchors, neighbors):
        # Softmax
        b, n = anchors.size()
        # anchors_prob = self.softmax(anchors)
        # positives_prob = self.softmax(neighbors)
        anchors_prob = anchors
        positives_prob = neighbors

        # Similarity in output space
        similarity = torch.bmm(anchors_prob.view(b, 1, n), positives_prob.view(b, n, 1)).squeeze()
        ones = torch.ones_like(similarity)
        consistency_loss = self.bce(similarity, ones)

        # Entropy loss
        entropy_loss = Entropy(torch.mean(anchors_prob, 0), True)

        # Total loss
        total_loss = consistency_loss - self.entropy_weight * entropy_loss

        return total_loss, consistency_loss, entropy_loss

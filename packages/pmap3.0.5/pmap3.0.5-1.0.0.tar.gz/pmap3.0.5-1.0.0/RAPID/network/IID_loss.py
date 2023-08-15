# This is adapted from the https://github.com/xu-ji/IIC
import torch
import sys


### TODO: Documentation
def compute_joint(x_out, x_tf_out):
    bn, k = x_out.size()
    assert (x_tf_out.size(0) == bn and x_tf_out.size(1) == k), '{} {} {} {}'.format(bn, k, x_tf_out.size(0),
                                                                                    x_tf_out.size(1))
    p_i_j = x_out.unsqueeze(2) * x_tf_out.unsqueeze(1)  # bn, k, k
    p_i_j = p_i_j.sum(dim=0)  # k, k
    p_i_j = (p_i_j + p_i_j.t()) / 2.  # symmetrise
    p_i_j = p_i_j / p_i_j.sum()  # normalise
    return p_i_j


### TODO: Documentation
def IID_loss(x_out, x_tf_out, eps=sys.float_info.epsilon, lamb=1):
    bs, k = x_out.size()
    p_i_j = compute_joint(x_out, x_tf_out)
    assert (p_i_j.size() == (k, k))
    p_i = p_i_j.sum(dim=1).view(k, 1).expand(k, k)
    p_j = p_i_j.sum(dim=0).view(1, k).expand(k, k)
    p_i_j = p_i_j + eps
    p_j = p_j + eps
    p_i = p_i + eps
    loss = (- p_i_j * (torch.log(p_i_j) - lamb * torch.log(p_j) - lamb * torch.log(p_i))).sum()

    return loss

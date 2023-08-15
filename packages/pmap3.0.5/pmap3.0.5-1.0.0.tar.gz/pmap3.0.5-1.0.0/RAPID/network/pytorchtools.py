import torch
import numpy as np
#https://github.com/Bjarten/early-stopping-pytorch


class EarlyStopping:
    """
    Stops the training early if validation loss doesn't improve after a given patience.

    Args:
        patience (int, optional): Number of iterations to wait after last time validation loss improved (Default: 7).
        verbose (bool, optional): If True, prints a message for each validation loss improvement (Default: False).
        delta (float, optional): Minimum change in the monitored quantity to qualify as an improvement (Default: 0).
        path (str, optional): Path for the checkpoint to be saved to (Default: 'checkpoint.pt').
        trace_func (function, optional): Trace print function (Default: print).
    """
    def __init__(self, patience=7, verbose=False, delta=0, path='checkpoint.pt', trace_func=print):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.path = path
        self.trace_func = trace_func
        self.lossList = list(np.zeros(self.patience))

    def __call__(self, val_loss, model):
        """
        Args:
            val_loss (float): Validation loss.
            model (torch.nn model): Model used for pixel clustering.
        """
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
            self.lossList.insert(0,val_loss.cpu().detach().numpy())
            self.lossList.pop()
            self.save_checkpoint(val_loss, model)
        elif np.mean(self.lossList[0:int(self.patience/2)]) > np.mean(self.lossList[int(self.patience/2):]):
            self.counter += 1
            self.lossList.insert(0,val_loss.cpu().detach().numpy())
            self.lossList.pop()
            if self.counter >= self.patience/50:
                self.early_stop = True
        else:
            self.best_score = score
            self.lossList.insert(0,val_loss.cpu().detach().numpy())
            self.lossList.pop()
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        """
        Saves model when validation loss decrease.

        Args:
            val_loss (float): Validation loss.
            model (torch.nn model): Model used for pixel clustering.
        """
        if self.verbose:
            self.trace_func(f'loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss

import torch
import torch.nn as nn
import numpy as np
from .utils import exists

class Diffusion(object):
    def __init__(self, config):
        self.steps = config.steps
        self.begin_beta = config.begin_beta
        self.end_beta = config.end_beta
        
        try:
            self.betas = np.load(config.beta_path)
            assert(len(self.betas) == self.steps)
            assert(self.betas[0] == self.begin_beta)
            assert(self.betas[-1] == self.end_beta)
        except Exception as e:
            self.betas = np.linspace(self.end_beta, self.begin_beta, num = self.steps)
            np.save(config.beta_path, self.betas)
        
        self.betas = torch.tensor(self.betas)
        self.alphas = 1 - self.betas
        self.alpha_mul = torch.cumprod(self.alphas, dim = 0)
        
    def add_noise(self, x, device, given_tim = None):
        self = self.to(device)
        x = x.to(device)
        
        bsz = x.shape[0]
        ori_shape = x.shape
        x = x.reshape(bsz, -1)

        tim = torch.randint(0, self.steps, (bsz, )).to(device)
        if exists(given_tim):
            tim = torch.tensor(given_tim).to(device)
        alpha_muls = torch.gather(self.alpha_mul, dim = 0, index = tim).to(device).unsqueeze(1)
        noise = torch.randn_like(x).to(device)
        noised_x = torch.sqrt(alpha_muls) * x + torch.sqrt(1 - alpha_muls) * noise
        
        noised_x = noised_x.reshape(*ori_shape)
        noise = noise.reshape(*ori_shape)
        return noised_x.detach().to(torch.float), noise.detach().to(torch.float), tim.detach()

    def to(self, device):
        self.alphas = self.alphas.to(device)
        self.betas = self.betas.to(device)
        self.alpha_mul = self.alpha_mul.to(device)
        return self

    def denoise(self, x, step, pred_noise, device):
        x = x.to(device)
        pred_noise = pred_noise.to(device)
        self = self.to(device)
        
        x_now = (x - self.betas[step] * pred_noise / (torch.sqrt(1 - self.alpha_mul[step]))) * torch.sqrt(1 / self.alphas[step]) 
        if step > 0:
            z = torch.randn_like(x).to(device)
            x_now += torch.sqrt((1 - self.alpha_mul[step - 1]) / (1 - self.alpha_mul[step]) * self.betas[step]) * z
        return pred_noise, x_now
        
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class Attention_Bahdanau(nn.Module):
    def __init__(self, dim):
        super(Attention_Bahdanau, self).__init__()
        self.linear_out = nn.Linear(dim*2, dim)
        self.v = nn.Parameter(torch.rand(dim))
        stdv = 1. / math.sqrt(self.v.size(0))
        self.v.data.normal_(mean=0, std=stdv)

    def forward(self, hidden, encoder_outputs, src_len=None):
        # hidden.shape = layer * batch_size * hidden_size
        # encoder_outputs = batch_size * in_len * hidden_size
        max_len = encoder_outputs.size(1)
        batch_size = encoder_outputs.size(0)
        # H = batch_size * in_len * hidden_size
        H = hidden.repeat(max_len,1,1).transpose(0,1)
        attn_energies = self.score(H, encoder_outputs)

        if src_len is not None:
            mask = []
            for b in range(src_len.size(0)):
                mask.append([0] * src_len[b].item() + [1] * (encoder_outputs.size(1) - src_len[b].item()))
            mask = cuda_(torch.ByteTensor(mask).unsqueeze(1)) # [B,1,T]
            attn_energies = attn_energies.masked_fill(mask, -1e18)
        
        return F.softmax(attn_energies.view(-1, max_len), dim=1).view(batch_size, 1, -1)

    def score(self, hidden, encoder_outputs):
        # (batch, out_len, 2*hidden) -> (batch, out_len, hidden)
        # energy = batch_size * in_len * hidden_size
        energy = torch.tanh(self.linear_out(torch.cat([hidden, encoder_outputs], 2)))
        energy = energy.transpose(2,1) # [B*H*T]
        v = self.v.repeat(encoder_outputs.data.shape[0],1).unsqueeze(1) #[B*1*H]
        energy = torch.bmm(v,energy) # [B*1*T]
        return energy

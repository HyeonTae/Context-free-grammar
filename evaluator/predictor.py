import torch
from torch.autograd import Variable

from sklearn.decomposition import PCA


class Predictor(object):

    def __init__(self, model, src_vocab, tgt_vocab):
        if torch.cuda.is_available():
            self.model = model.cuda()
        else:
            self.model = model.cpu()
        self.model.eval()
        self.src_vocab = src_vocab
        self.tgt_vocab = tgt_vocab

    def get_decoder_features(self, src_seq):
        src_id_seq = torch.LongTensor([self.src_vocab.stoi[tok] for tok in src_seq]).view(1, -1)
        if torch.cuda.is_available():
            src_id_seq = src_id_seq.cuda()

        with torch.no_grad():
            softmax_list, _, other = self.model(src_id_seq, [len(src_seq)])

        return other

    def predict(self, src_seq):
        other = self.get_decoder_features(src_seq)

        length = other['length'][0]

        tgt_att_list = []
        encoder_outputs = []
        #principalComponents = []
        tgt_id_seq = [other['sequence'][di][0].data[0] for di in range(length)]
        if 'attention_score' in list(other.keys()):
            tgt_att_list = [other['attention_score'][di][0].data[0].cpu().numpy() for di in range(length)]
            encoder_outputs = other['encoder_outputs'].cpu().numpy()
            #pca = PCA(n_components=2)
            #principalComponents = pca.fit_transform(encoder_outputs)

        tgt_seq = [self.tgt_vocab.itos[tok] for tok in tgt_id_seq]
        return tgt_seq, tgt_att_list, encoder_outputs

    def predict_n(self, src_seq, n=1):
        other = self.get_decoder_features(src_seq)

        result = []
        for x in range(0, int(n)):
            length = other['topk_length'][0][x]
            tgt_id_seq = [other['topk_sequence'][di][0, x, 0].data[0] for di in range(length)]
            tgt_seq = [self.tgt_vocab.itos[tok] for tok in tgt_id_seq]
            result.append(tgt_seq)

        return result

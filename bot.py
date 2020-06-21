
import tensorflow as tf
import tensorlayer as tl
import numpy as np
from tensorlayer.cost import cross_entropy_seq, cross_entropy_seq_with_mask
from tqdm import tqdm
from sklearn.utils import shuffle
from data.twitter import data
from tensorlayer.models.seq2seq import Seq2seq
from tensorlayer.models.seq2seq_with_attention import Seq2seqLuongAttention
import os

class Chatbot:
    def __init__(self):
        data_corpus = "twitter"
        metadata, idx_q, idx_a = data.load_data(PATH='data/{}/'.format(data_corpus))
        src_vocab_size = len(metadata['idx2w']) # 8002 (0~8001)
        emb_dim = 1024

        word2idx = metadata['w2idx']   # dict  word 2 index
        idx2word = metadata['idx2w']   # list index 2 word

        unk_id = word2idx['unk']   # 1
        pad_id = word2idx['_']     # 0

        start_id = src_vocab_size  # 8002
        end_id = src_vocab_size + 1  # 8003

        word2idx.update({'start_id': start_id})
        word2idx.update({'end_id': end_id})
        idx2word = idx2word + ['start_id', 'end_id']
        
        
        src_vocab_size = tgt_vocab_size = src_vocab_size + 2

     #   num_epochs = 5
        vocabulary_size = src_vocab_size
        
        decoder_seq_length = 20
        self.unk_id=unk_id
        self.pad_id=pad_id
        self.start_id=start_id
        self.end_id=end_id
        self.word2idx=word2idx
        self.idx2word=idx2word
        self.model_ = Seq2seq(
            decoder_seq_length = decoder_seq_length,
            cell_enc=tf.keras.layers.GRUCell,
            cell_dec=tf.keras.layers.GRUCell,
            n_layer=3,
            n_units=256,
            embedding_layer=tl.layers.Embedding(vocabulary_size=vocabulary_size,        embedding_size=emb_dim),
            )
        load_weights = tl.files.load_npz(name='model.npz')
        tl.files.assign_weights(load_weights, self.model_)
    
    def inference(self,msg, top_n):
        self.model_.eval()        
        unk_id=self.unk_id
        pad_id=self.pad_id
        start_id=self.start_id
        end_id=self.end_id
        word2idx=self.word2idx
        idx2word=self.idx2word
      
     #Tokeizing the given input
        msg_id = [word2idx.get(w, unk_id) for w in msg.split(" ")]
        
    #Output of the give model    
        sentence_id = self.model_(inputs=[[msg_id]], seq_length=20, start_token=start_id, top_n = top_n)
        
 #Selecting the best of top Replies       
        sentence = []
        for w_id in sentence_id[0]:
            w = idx2word[w_id]
            if w == 'end_id':
                break
            sentence = sentence + [w]
        return sentence    

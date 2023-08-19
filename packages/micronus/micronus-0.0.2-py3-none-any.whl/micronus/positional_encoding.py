import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import convert_to_tensor, string
from tensorflow.keras.layers import Embedding, Layer
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization


class PositionEmbeddingFixedWeights(Layer):
    """ Initialize the PositionEmbeddingFixedWeights layer """
    def __init__(self, sequence_length, vocab_size, output_dim, **kwargs):
        super(PositionEmbeddingFixedWeights, self).__init__(**kwargs)
        word_embedding_matrix = self.get_position_encoding(vocab_size, output_dim)   
        position_embedding_matrix = self.get_position_encoding(sequence_length, output_dim)                                          
        self.word_embedding_layer = Embedding(
            input_dim=vocab_size, output_dim=output_dim,
            weights=[word_embedding_matrix],
            trainable=False
        )
        self.position_embedding_layer = Embedding(
            input_dim=sequence_length, output_dim=output_dim,
            weights=[position_embedding_matrix],
            trainable=False
        )
             
    def get_position_encoding(self, seq_len, d, n=10000):
        """

        Parameters
        ----------
        seq_len : int
            Length of the sequence.
            
        d : int
            Dimensionality of the embedding.
            
        n : int, optional
            Scaling factor for the encoding (Default value = 10000)

        Returns
        -------
        output : np.ndarray
            Position embedding matrix of shape (seq_len, d).

        """
        P = np.zeros((seq_len, d))
        for k in range(seq_len):
            for i in np.arange(int(d/2)):
                denominator = np.power(n, 2*i/d)
                P[k, 2*i] = np.sin(k/denominator)
                P[k, 2*i+1] = np.cos(k/denominator)
        return P
 
 
    def call(self, inputs):        
        """

        Parameters
        ----------
        inputs : tf.Tensor
            Input tensor of shape (batch_size, seq_len).
            
        Returns
        -------
        output : tf.Tensor
            Output tensor of shape (batch_size, seq_len, output_dim).

        """
        position_indices = tf.range(tf.shape(inputs)[-1])
        embedded_words = self.word_embedding_layer(inputs)
        embedded_indices = self.position_embedding_layer(position_indices)
        return embedded_words + embedded_indices
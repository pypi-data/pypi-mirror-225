import tensorflow as tf
from tensorflow import matmul, reshape, shape, transpose, cast, float32
from tensorflow.keras.layers import Dense, Layer
from keras.backend import softmax

class DotProductAttention(Layer):
    """ Class for scaled dot product attention"""
    def __init__(self, **kwargs):
        super(DotProductAttention, self).__init__(**kwargs)

    def call(self, queries, keys, values, d_k, mask=None):
        """

        Parameters
        ----------
        queries: Tensor
            The queries tensor with shape (batch_size, sequence_length_q, d_model).

        keys: Tensor
            The keys tensor with shape (batch_size, sequence_length_k, d_model).
        
        values: Tensor
            The values tensor with shape (batch_size, sequence_length_v, d_model).
        
        d_k: int
            The dimensionality of the keys.

        mask: Tensor, optional
            The mask tensor with shape (batch_size, sequence_length_q, sequence_length_k),
            used to mask elements in the attention scores. (default: None)

        Returns
        -------
        output: Tensor
            The attended output tensor with shape (batch_size, sequence_length_q, d_model).

        """
        scores = matmul(queries, keys, transpose_b=True) / tf.math.sqrt(cast(d_k, float32))
        
        if mask is not None:
            scores += -1e9 * mask

        weight = softmax(scores)

        return matmul(weight, values)

class MultiHeadAttention(Layer):
    """  Initialize the MultiHeadAttention layer """
    def __init__(self, h, d_k, d_v, d_model, **kwargs):
        super(MultiHeadAttention, self).__init__(**kwargs)
        self.attention = DotProductAttention()
        self.head = h
        self.d_k = d_k
        self.d_v = d_v
        self.d_model = d_model
        self.W_q = Dense(d_k)
        self.W_k = Dense(d_k)
        self.W_v = Dense(d_v)
        self.W_o = Dense(d_model)

    def reshape_tensor(self, x, head, flag):
        """
        Reshape the input tensor based on the attention head and flag.

        Parameters
        ----------
        x : tf.Tensor
            Input tensor.
        head : int
            Number of attention heads.
        flag : bool
            Flag indicating whether to reshape for attention calculation or output.

        Returns
        -------
        x : tf.Tensor
            Reshaped tensor.
        """
        if flag:
            x = reshape(x, shape=(shape(x)[0], shape(x)[1], head, -1))
            x = transpose(x, perm=(0, 2, 1, 3))
        else:
            x = transpose(x, perm=(0, 2, 1, 3))
            x = reshape(x, shape=(shape(x)[0], shape(x)[1], self.d_k))
        return x

    def call(self, queries, keys, values, mask=None):
        """
        Perform the forward pass of the MultiHeadAttention layer.

        Parameters
        ----------
        queries : tf.Tensor
            Query tensor.
        keys : tf.Tensor
            Key tensor.
        values : tf.Tensor
            Value tensor.
        mask : tf.Tensor, optional
            Mask tensor, indicating positions to be masked, by default None.

        Returns
        -------
        output : tf.Tensor
            Output tensor.
        """
        q_reshaped = self.reshape_tensor(self.W_q(queries), self.head, True)
        k_reshaped = self.reshape_tensor(self.W_k(keys), self.head, True)
        v_reshaped = self.reshape_tensor(self.W_v(values), self.head, True)

        o_reshaped = self.attention(q_reshaped, k_reshaped, v_reshaped, self.d_k, mask)
        
        output = self.reshape_tensor(o_reshaped, self.head, False)

        return self.W_o(output)

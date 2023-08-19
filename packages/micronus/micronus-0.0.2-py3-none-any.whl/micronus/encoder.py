from tensorflow.keras.layers import LayerNormalization, Layer, Dense, ReLU, Dropout, Input
from tensorflow.keras.models import Model
from micronus.multihead_attention import MultiHeadAttention
from micronus.positional_encoding import PositionEmbeddingFixedWeights

class AddNormalization(Layer):
    """ Initializing the normalization layer"""

    def __init__(self, **kwargs):
        super(AddNormalization, self).__init__(**kwargs)
        self.layer_norm = LayerNormalization()

    def call(self, x, sublayer_x):
        """

        Parameters
        ----------
        x :
            sublayer input
            
        sublayer_x :
            sublayer output

        Returns
        -------
        output :
            normalized sum

        """
        add = x + sublayer_x

        return self.layer_norm(add)

class FeedForward(Layer):
    """ Initializing the fully connected feed forward layer """

    def __init__(self, d_ff, d_model, **kwargs):
        super(FeedForward, self).__init__(**kwargs)
        self.fully_connected1 = Dense(d_ff)  
        self.fully_connected2 = Dense(d_model)
        self.activation = ReLU()

    def call(self, x):
        """

        Parameters
        ----------
        x :
            input from previous layer
            

        Returns
        -------
        output:
            output from fully connected feed forward layer with ReLU

        """
        x_fc1 = self.fully_connected1(x)

        return self.fully_connected2(self.activation(x_fc1))


class EncoderLayer(Layer):
    """ Define Encoder layer """

    def __init__(self, sequence_length, h, d_k, d_v, d_model, d_ff, rate, **kwargs):
        super(EncoderLayer, self).__init__(**kwargs)
        self.build(input_shape=[None, sequence_length, d_model])
        self.d_model = d_model
        self.sequence_length = sequence_length
        self.multihead_attention = MultiHeadAttention(h, d_k, d_v, d_model)
        self.dropout1 = Dropout(rate)
        self.add_norm1 = AddNormalization()
        self.feed_forward = FeedForward(d_ff, d_model)
        self.dropout2 = Dropout(rate)
        self.add_norm2 = AddNormalization()

    def build_graph(self):
        """ Build Encoder layer graph """
        input_layer = Input(shape=(self.sequence_length, self.d_model))
        return Model(inputs=[input_layer], outputs=self.call(input_layer, None, True))

    def call(self, x, padding_mask, training):
        """

        Parameters
        ----------
        x :
            input data
            
        padding_mask :
            padding condition
            
        training : 
            apply the Dropout layers

        Returns
        -------
        output:
            encoder layer output

        """
        multihead_output = self.multihead_attention(x, x, x, padding_mask)

        multihead_output = self.dropout1(multihead_output, training=training)

        addnorm_output = self.add_norm1(x, multihead_output)

        feedforward_output = self.feed_forward(addnorm_output)
        feedforward_output = self.dropout2(feedforward_output, training=training)

        return self.add_norm2(addnorm_output, feedforward_output)


class Encoder(Layer):
    """ Define Encoder block """

    def __init__(self, vocab_size, sequence_length, h, d_k, d_v, d_model, d_ff, n, rate, **kwargs):
        super(Encoder, self).__init__(**kwargs)
        self.pos_encoding = PositionEmbeddingFixedWeights(sequence_length, vocab_size, d_model)
        self.dropout = Dropout(rate)
        self.encoder_layer = [EncoderLayer(sequence_length,h, d_k, d_v, d_model, d_ff, rate) for _ in range(n)]

    def call(self, input_sentence, padding_mask, training):
        """

        Parameters
        ----------
        input_sentence :
            tokenized input
            
        padding_mask :
            suppress the zero padding
            
        training :
            apply the Dropout layers
            

        Returns
        -------
        output:
            encoder block output

        """
        pos_encoding_output = self.pos_encoding(input_sentence)

        x = self.dropout(pos_encoding_output, training=training)

        for i, layer in enumerate(self.encoder_layer):
            x = layer(x, padding_mask, training)

        return x

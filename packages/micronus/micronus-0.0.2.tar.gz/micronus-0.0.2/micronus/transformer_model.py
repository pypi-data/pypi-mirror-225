from micronus.encoder import Encoder, EncoderLayer
from micronus.decoder import Decoder, DecoderLayer
from tensorflow import math, cast, float32, linalg, ones, maximum, newaxis
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense
 
 
class TransformerModel(Model):
    """ Initialize the Transformer model. """
    def __init__(self, enc_vocab_size, dec_vocab_size, enc_seq_length, dec_seq_length, h, d_k, d_v, d_model, d_ff_inner, n, rate, **kwargs):
        super(TransformerModel, self).__init__(**kwargs)

        self.encoder_layer = EncoderLayer(enc_seq_length, h, d_k, d_v, d_model, d_ff_inner, rate)
        self.decoder_layer = DecoderLayer(dec_seq_length, h, d_k, d_v, d_model, d_ff_inner, rate)
 
        # Set up the encoder
        self.encoder = Encoder(enc_vocab_size, enc_seq_length, h, d_k, d_v, d_model, d_ff_inner, n, rate)
 
        # Set up the decoder
        self.decoder = Decoder(dec_vocab_size, dec_seq_length, h, d_k, d_v, d_model, d_ff_inner, n, rate)
 
        # Define the final dense layer
        self.model_last_layer = Dense(dec_vocab_size)
 
    def padding_mask(self, input):
        """

        Parameters
        ----------
        input : tf.Tensor
            Input tensor.

        Returns
        -------
        output : tf.Tensor
            Padding mask tensor
        """
        # Create mask which marks the zero padding values in the input by a 1.0
        mask = math.equal(input, 0)
        mask = cast(mask, float32)
 
        # The shape of the mask should be broadcastable to the shape
        # of the attention weights that it will be masking later on
        return mask[:, newaxis, newaxis, :]
 
    def lookahead_mask(self, shape):
        """

        Parameters
        ----------
        shape : tuple
            Shape of the lookahead mask.
            e.g. (batch_size, sequence_length)

        Returns
        -------
        output : tf.Tensor
            Lookahead mask tensor.
        
        Notes
        -----
        The lookahead mask is used to mask the future values in the decoder.
        This is used to avoid the model to predict the future values.
        
        Examples
        --------
        >>> lookahead_mask(shape=(2, 3))
        array([[1., 0., 0.],
               [1., 1., 0.]], dtype=float32)
        
        >>> lookahead_mask(shape=(3, 3))
        array([[1., 0., 0.],
               [1., 1., 0.],
               [1., 1., 1.]], dtype=float32)
        
        >>> lookahead_mask(shape=(4, 4))
        array([[1., 0., 0., 0.],
               [1., 1., 0., 0.],
               [1., 1., 1., 0.],
               [1., 1., 1., 1.]], dtype=float32)
        
        >>> lookahead_mask(shape=(5, 5))
        array([[1., 0., 0., 0., 0.],

        """
        # Mask out future entries by marking them with a 1.0
        mask = 1 - linalg.band_part(ones((shape, shape)), -1, 0)
 
        return mask
    
    def model_summary(self):
        """ Show model summary.

        Returns
        -------
        encoder_summary : tf.Tensor
            Encoder summary.
            
        decoder_summary : tf.Tensor
            Decoder summary.
        
        Notes
        -----
        The encoder summary shows the number of parameters in the encoder.
        The decoder summary shows the number of parameters in the decoder.
        
        Examples
        --------
        >>> model_summary()
        Encoder summary:
        Total params: 4,924
        Trainable params: 4,924
        Non-trainable params: 0
        Decoder summary:
        Total params: 4,924
        Trainable params: 4,924
        Non-trainable params: 0
        
        """
        # Show model summary
        encoder_summary = self.encoder_layer.build_graph().summary()
        decoder_summary = self.decoder_layer.build_graph().summary()
        return encoder_summary, decoder_summary
 
    def call(self, encoder_input, decoder_input, training):
        """

        Parameters
        ----------
        encoder_input : tf.Tensor
            Input tensor for the encoder
            
        decoder_input : tf.Tensor
            Input tensor for the decoder
            
        training : bool
            Whether the model is in training mode or not.
            This is used to determine whether to use the lookahead mask or not.
            
        Notes
        -----
        The lookahead mask is used to mask the future values in the decoder.
        This is used to avoid the model to predict the future values.
        
        Examples
        --------
        >>> call(encoder_input=tf.constant([[1, 2, 3, 4, 5]]),
        ...      decoder_input=tf.constant([[1, 2, 3, 4, 5]]),
        ...      training=False)
        array([[0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0, 0.0]], dtype=float32)
            

        Returns
        -------
        output : tf.Tensor
            Output tensor of the transformer model.

        """
 
        # Create padding mask to mask the encoder inputs and the encoder outputs in the decoder
        enc_padding_mask = self.padding_mask(encoder_input)
 
        # Create and combine padding and look-ahead masks to be fed into the decoder
        dec_in_padding_mask = self.padding_mask(decoder_input)
        dec_in_lookahead_mask = self.lookahead_mask(decoder_input.shape[1])
        dec_in_lookahead_mask = maximum(dec_in_padding_mask, dec_in_lookahead_mask)
 
        # Feed the input into the encoder
        encoder_output = self.encoder(encoder_input, enc_padding_mask, training)
 
        # Feed the encoder output into the decoder
        decoder_output = self.decoder(decoder_input, encoder_output, dec_in_lookahead_mask, enc_padding_mask, training)
 
        # Pass the decoder output through a final dense layer
        model_output = self.model_last_layer(decoder_output)
 
        return model_output
    

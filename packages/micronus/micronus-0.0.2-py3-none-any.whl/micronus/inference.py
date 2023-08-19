from pickle import load
import argparse

from tensorflow import Module
from tensorflow import convert_to_tensor, int64, TensorArray, argmax, newaxis, transpose
from keras.preprocessing.sequence import pad_sequences
from micronus.transformer_model import TransformerModel


# Define the model parameters
# h = 8  # Number of self-attention heads
# d_k = 64  # Dimensionality of the linearly projected queries and keys
# d_v = 64  # Dimensionality of the linearly projected values
# d_model = 512  # Dimensionality of model layers' outputs
# d_ff = 2048  # Dimensionality of the inner fully connected layer
# n = 6  # Number of layers in the encoder stack
 
# # Define the dataset parameters
# enc_seq_length = 7  # Encoder sequence length
# dec_seq_length = 12  # Decoder sequence length
# enc_vocab_size = 2405  # Encoder vocabulary size
# dec_vocab_size = 3858  # Decoder vocabulary size


# inferencing_model = TransformerModel(enc_vocab_size, dec_vocab_size, enc_seq_length, dec_seq_length, h, d_k, d_v, d_model, d_ff, n, 0)
# encoder_tokenizer = 'enc_tokenizer.pkl'
# decoder_tokenizer = 'dec_tokenizer.pkl'

class Infer(Module):
    """ Class for performing inference """
    def __init__(self, inferencing_model, encoder_tokenizer, decoder_tokenizer, **kwargs):
        super(Infer, self).__init__(**kwargs)
        self.transformer = inferencing_model
        self.enc_tokenizer = encoder_tokenizer
        self.dec_tokenizer = decoder_tokenizer
 
    def load_tokenizer(self, name):
        """

        Parameters
        ----------
        name : str
            Name of the tokenizer file to load. 
            The file should be saved using the `save_tokenizer` method.             

        Returns
        -------
        tokenizer : Tokenizer
            Tokenizer object. 

        """
        with open(name, 'rb') as handle:
            return load(handle)
 
    def __call__(self, sentence, enc_seq_length, dec_seq_length):
        # Append start and end of string tokens to the input sentence
        sentence[0] = "<START> " + sentence[0] + " <EOS>"
 
        # Load encoder and decoder tokenizers
        enc_tokenizer = self.load_tokenizer(self.enc_tokenizer)
        dec_tokenizer = self.load_tokenizer(self.dec_tokenizer)
 
        # Prepare the input sentence by tokenizing, padding and converting to tensor
        encoder_input = enc_tokenizer.texts_to_sequences(sentence)
        encoder_input = pad_sequences(encoder_input, maxlen=enc_seq_length, padding='post')
        encoder_input = convert_to_tensor(encoder_input, dtype=int64)
 
        # Prepare the output <START> token by tokenizing, and converting to tensor
        output_start = dec_tokenizer.texts_to_sequences(["<START>"])
        output_start = convert_to_tensor(output_start[0], dtype=int64)
 
        # Prepare the output <EOS> token by tokenizing, and converting to tensor
        output_end = dec_tokenizer.texts_to_sequences(["<EOS>"])
        output_end = convert_to_tensor(output_end[0], dtype=int64)
 
        # Prepare the output array of dynamic size
        decoder_output = TensorArray(dtype=int64, size=0, dynamic_size=True)
        decoder_output = decoder_output.write(0, output_start)
 
        for i in range(dec_seq_length):
 
            # Predict an output token
            prediction = self.transformer(encoder_input, transpose(decoder_output.stack()), training=False)
 
            prediction = prediction[:, -1, :]
 
            # Select the prediction with the highest score
            predicted_id = argmax(prediction, axis=-1)
            predicted_id = predicted_id[0][newaxis]
 
            # Write the selected prediction to the output array at the next available index
            decoder_output = decoder_output.write(i + 1, predicted_id)
 
            # Break if an <EOS> token is predicted
            if predicted_id == output_end:
                break
 
        output = transpose(decoder_output.stack())[0]
        output = output.numpy()
 
        output_str = []
 
        # Decode the predicted tokens into an output string
        for i in range(output.shape[0]):
 
            key = output[i]
            print(dec_tokenizer.index_word[key])
 
        return output_str

def main():
    parser = argparse.ArgumentParser(description="micronus inference parameters",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--h", type=int, default=8, help="Number of self-attention heads")
    parser.add_argument("--d_k" , type=int, default=64, help="Dimensionality of the linearly projected queries and keys")
    parser.add_argument("--d_v", type=int, default=64, help="Dimensionality of the linearly projected values")
    parser.add_argument("--d_model", type=int, default=512, help="Dimensionality of model layers' outputs")
    parser.add_argument("--d_ff", type=int, default=2048, help="Dimensionality of the inner fully connected layer")
    parser.add_argument("--n", type=int, default=6, help="Number of layers in the encoder stack")

    parser.add_argument("--enc_seq_length", type=int, default=7, help="Encoder sequence length")
    parser.add_argument("--dec_seq_length", type=int, default=12, help="Decoder sequence length")
    parser.add_argument("--enc_vocab_size", type=int, default=2405, help="Encoder vocabulary size")
    parser.add_argument("--dec_vocab_size", type=int, default=3858, help="Decoder vocabulary size")

    parser.add_argument("--encoder_tokenizer", type=str, default='enc_tokenizer.pkl', help="Encoder tokenizer")
    parser.add_argument("--decoder_tokenizer", type=str, default='dec_tokenizer.pkl', help="Decoder tokenizer")

    parser.add_argument("--sentence", type=str, default='Hello world', help="your_input_sentence_here")

    args = vars(parser.parse_args())
    

    h = args["h"]  
    d_k = args["d_k"]
    d_v = args["d_v"]
    d_model = args["d_model"]
    d_ff = args["d_ff"]
    n =  args["n"]

    enc_seq_length = args["enc_seq_length"]
    dec_seq_length = args["dec_seq_length"]
    enc_vocab_size = args["enc_vocab_size"]
    dec_vocab_size = args["dec_vocab_size"]

    inferencing_model = TransformerModel(enc_vocab_size, dec_vocab_size, enc_seq_length, dec_seq_length, h, d_k, d_v, d_model, d_ff, n, 0)
    encoder_tokenizer = args["encoder_tokenizer"]
    decoder_tokenizer = args["decoder_tokenizer"]
    
    infer = Infer(inferencing_model, encoder_tokenizer, decoder_tokenizer, enc_seq_length, dec_seq_length)
    
    sentence = args["sentence"]
    output = infer(sentence, enc_seq_length, dec_seq_length)
    
    print("Generated Output:", " ".join(output))
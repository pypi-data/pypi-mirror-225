
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import LearningRateSchedule
from tensorflow.keras.metrics import Mean
from tensorflow import data, train, math, reduce_sum, cast, equal, argmax, float32, GradientTape, function
from keras.losses import sparse_categorical_crossentropy
from micronus.transformer_model import TransformerModel
from micronus.data_pipeline import PrepareDataset
from time import time
from pickle import dump
import argparse

# Define the model parameters
# h = 8  # Number of self-attention heads
# d_k = 64  # Dimensionality of the linearly projected queries and keys
# d_v = 64  # Dimensionality of the linearly projected values
# d_model = 512  # Dimensionality of model layers' outputs
# d_ff = 2048  # Dimensionality of the inner fully connected layer
# n = 6  # Number of layers in the encoder stack

# epochs = 20
# batch_size = 64
# beta_1 = 0.9
# beta_2 = 0.98
# epsilon = 1e-9
# dropout_rate = 0.1
 
# DATASET='english-german.pkl'
 
# Implementing a learning rate scheduler
class LRScheduler(LearningRateSchedule):
    """ Learning rate scheduler for Transformer """

    def __init__(self, d_model, warmup_steps=4000, **kwargs):
        super(LRScheduler, self).__init__(**kwargs)
 
        self.d_model = cast(d_model, float32)
        self.warmup_steps = warmup_steps
 
    def __call__(self, step_num):
 
        # Linearly increasing the learning rate for the first warmup_steps, and decreasing it thereafter
        arg1 = step_num ** -0.5
        arg2 = step_num * (self.warmup_steps ** -1.5)
 
        return (self.d_model ** -0.5) * math.minimum(arg1, arg2)
 
  
# Prepare the training dataset
def data_process(DATASET, batch_size):
    """

    Parameters
    ----------
    DATASET : str
        The input dataset.
        

    Returns
    -------
    trainX : 
    Training input data.
`    trainY : 
        Training target data.
    valX : 
        Validation input data.
    valY : 
        Validation target data.
    train_orig : 
        Original training data.
    val_orig : 
        Original validation data.
    enc_seq_length : 
        Length of the input sequence.
    dec_seq_length : 
        Length of the target sequence.
    enc_vocab_size : 
        Vocabulary size of the input sequence.
    dec_vocab_size : 
        Vocabulary size of the target sequence.
    train_dataset : 
        Training dataset.
    val_dataset : 
        Validation dataset.`

    """
    dataset = PrepareDataset()
    trainX, trainY, valX, valY, train_orig, val_orig, enc_seq_length, dec_seq_length, enc_vocab_size, dec_vocab_size = dataset(DATASET)
    
    print(enc_seq_length, dec_seq_length, enc_vocab_size, dec_vocab_size)

    # Prepare the training dataset batches
    train_dataset = data.Dataset.from_tensor_slices((trainX, trainY))
    train_dataset = train_dataset.batch(batch_size)
    
    # Prepare the validation dataset batches
    val_dataset = data.Dataset.from_tensor_slices((valX, valY))
    val_dataset = val_dataset.batch(batch_size)


    return trainX, trainY, valX, valY, train_orig, val_orig, enc_seq_length, dec_seq_length, enc_vocab_size, dec_vocab_size, train_dataset, val_dataset

 
# Defining the loss function
def loss_fcn(target, prediction):
    """

    Parameters
    ----------
    target : 
        Target data.
    prediction : 
        Model prediction.    

    Returns
    -------
    loss : 
        Computed loss value.

    """
    # Create mask so that the zero padding values are not included in the computation of loss
    padding_mask = math.logical_not(equal(target, 0))
    padding_mask = cast(padding_mask, float32)
 
    # Compute a sparse categorical cross-entropy loss on the unmasked values
    loss = sparse_categorical_crossentropy(target, prediction, from_logits=True) * padding_mask
 
    # Compute the mean loss over the unmasked values
    return reduce_sum(loss) / reduce_sum(padding_mask)
 
 
# Defining the accuracy function
def accuracy_fcn(target, prediction):
    """

    Parameters
    ----------
    target : 
        Target data.
    prediction : 
        Model prediction.    

    Returns
    -------
    accuracy : 
        Computed accuracy value.

    """
    # Create mask so that the zero padding values are not included in the computation of accuracy
    padding_mask = math.logical_not(equal(target, 0))
 
    # Find equal prediction and target values, and apply the padding mask
    accuracy = equal(target, argmax(prediction, axis=2))
    accuracy = math.logical_and(padding_mask, accuracy)
 
    # Cast the True/False values to 32-bit-precision floating-point numbers
    padding_mask = cast(padding_mask, float32)
    accuracy = cast(accuracy, float32)
 
    # Compute the mean accuracy over the unmasked values
    return reduce_sum(accuracy) / reduce_sum(padding_mask)
 
 
# Speeding up the training process
@function
def train_step(encoder_input, decoder_input, decoder_output, training_model, optimizer, train_loss, train_accuracy):
    """

    Parameters
    ----------
    encoder_input : Tensor
        Input tensor for the encoder.
        
    decoder_input : Tensor
        Input tensor for the decoder.
        
    decoder_output : Tensor
        Expected output tensor for the decoder.
        

    Returns
    -------
    None
        The function updates the trainable variables of the model.

    """
    with GradientTape() as tape:
 
        # Run the forward pass of the model to generate a prediction
        prediction = training_model(encoder_input, decoder_input, training=True)
 
        # Compute the training loss
        loss = loss_fcn(decoder_output, prediction)
 
        # Compute the training accuracy
        accuracy = accuracy_fcn(decoder_output, prediction)
 
    # Retrieve gradients of the trainable variables with respect to the training loss
    gradients = tape.gradient(loss, training_model.trainable_weights)
 
    # Update the values of the trainable variables by gradient descent
    optimizer.apply_gradients(zip(gradients, training_model.trainable_weights))
 
    train_loss(loss)
    train_accuracy(accuracy)
 

def main():
    parser = argparse.ArgumentParser(description="micronus training parameters", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            
    parser.add_argument("--h", type=int, default=8, help="Number of self-attention heads")
    parser.add_argument("--d_k", type=int, default=64, help="Dimensionality of the linearly projected queries and keys")
    parser.add_argument("--d_v", type=int, default=64, help="Dimensionality of the linearly projected values")
    parser.add_argument("--d_model", type=int, default=512, help="Dimensionality of model layers' outputs")
    parser.add_argument("--d_ff", type=int, default=2048, help="Dimensionality of the inner fully connected layer")
    parser.add_argument("--n", type=int, default=6, help="Number of layers in the encoder stack")

    parser.add_argument("--epochs", type=int, default=20, help="Number of epochs to train for")
    parser.add_argument("--batch_size", type=int, default=64, help="Batch size")
    parser.add_argument("--beta_1", type=float, default=0.9, help="Adam optimizer beta 1")
    parser.add_argument("--beta_2", type=float, default=0.98, help="Adam optimizer beta 2")
    parser.add_argument("--epsilon", type=float, default=1e-9, help="Adam optimizer epsilon")
    parser.add_argument("--dropout_rate", type=float, default=0.1, help="Dropout rate")

    parser.add_argument("--dataset", type=str, default="english-german.pkl", help="Name of the dataset file")

    args = vars(parser.parse_args())
    
    h = args["h"]
    d_k = args["d_k"]
    d_v = args["d_v"]
    d_model = args["d_model"]
    d_ff = args["d_ff"]
    n =  args["n"]

    epochs = args["epochs"]
    batch_size = args["batch_size"]
    beta_1 = args["beta_1"]
    beta_2 = args["beta_2"]
    epsilon = args["epsilon"]
    dropout_rate = args["dropout_rate"]
    DATASET = args["dataset"]

    # Instantiate an Adam optimizer
    optimizer = Adam(LRScheduler(d_model), beta_1, beta_2, epsilon)


    trainX, trainY, valX, valY, train_orig, val_orig, enc_seq_length, dec_seq_length, enc_vocab_size, dec_vocab_size, train_dataset, val_dataset = data_process(DATASET)

    # Create model
    training_model = TransformerModel(enc_vocab_size, dec_vocab_size, enc_seq_length, dec_seq_length, h, d_k, d_v, d_model, d_ff, n, dropout_rate)

    # Include metrics monitoring
    train_loss = Mean(name='train_loss')
    train_accuracy = Mean(name='train_accuracy')
    val_loss = Mean(name='val_loss')
    
    # Create a checkpoint object and manager to manage multiple checkpoints
    ckpt = train.Checkpoint(model=training_model, optimizer=optimizer)
    ckpt_manager = train.CheckpointManager(ckpt, "./checkpoints", max_to_keep=None)
    
    # Initialise dictionaries to store the training and validation losses
    train_loss_dict = {}
    val_loss_dict = {}

    for epoch in range(epochs):
    
        train_loss.reset_states()
        train_accuracy.reset_states()
        val_loss.reset_states()
    
        print("\nStart of epoch %d" % (epoch + 1))
    
        start_time = time()
    
        # Iterate over the dataset batches
        for step, (train_batchX, train_batchY) in enumerate(train_dataset):
    
            # Define the encoder and decoder inputs, and the decoder output
            encoder_input = train_batchX[:, 1:]
            decoder_input = train_batchY[:, :-1]
            decoder_output = train_batchY[:, 1:]
    
            train_step(encoder_input, decoder_input, decoder_output, training_model, optimizer, train_loss, train_accuracy)
    
            if step % 50 == 0:
                print(f'Epoch {epoch + 1} Step {step} Loss {train_loss.result():.4f} Accuracy {train_accuracy.result():.4f}')
    
        # Run a validation step after every epoch of training
        for val_batchX, val_batchY in val_dataset:
    
            # Define the encoder and decoder inputs, and the decoder output
            encoder_input = val_batchX[:, 1:]
            decoder_input = val_batchY[:, :-1]
            decoder_output = val_batchY[:, 1:]
    
            # Generate a prediction
            prediction = training_model(encoder_input, decoder_input, training=False)
    
            # Compute the validation loss
            loss = loss_fcn(decoder_output, prediction)
            val_loss(loss)
    
        # Print epoch number and accuracy and loss values at the end of every epoch
        print("Epoch %d: Training Loss %.4f, Training Accuracy %.4f, Validation Loss %.4f" % (epoch + 1, train_loss.result(), train_accuracy.result(), val_loss.result()))
    
        # Save a checkpoint after every epoch
        if (epoch + 1) % 1 == 0:
    
            save_path = ckpt_manager.save()
            print("Saved checkpoint at epoch %d" % (epoch + 1))
    
            # Save the trained model weights
            training_model.save_weights("weights/wghts" + str(epoch + 1) + ".ckpt")
    
            train_loss_dict[epoch] = train_loss.result()
            val_loss_dict[epoch] = val_loss.result()
    
    # Save the training loss values
    with open('./train_loss.pkl', 'wb') as file:
        dump(train_loss_dict, file)
    
    # Save the validation loss values
    with open('./val_loss.pkl', 'wb') as file:
        dump(val_loss_dict, file)
    
    print("Total time taken: %.2fs" % (time() - start_time))

if __name__ == '__main__':
    main()

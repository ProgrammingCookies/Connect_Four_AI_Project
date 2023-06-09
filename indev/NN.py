import tensorflow as tf

#Made by Axel Lindqvist 01-04-2023
#Intialize NN
def nnInit():
    # Define the input layer
    input_layer = tf.keras.layers.Input(shape=(6,7,3))

    # Reshape the input layer to have a single channel
    reshaped_input = tf.reshape(input_layer, [-1, 6, 7, 3])

    # Define the convolutional layer with  21 neurons in the second layer. Each neuron being covering one 3x3 patch of the gameboard. 
    conv_layer = tf.keras.layers.Conv2D(filters=3, kernel_size=(3, 3), strides=(1, 1), padding="valid", activation="relu")(reshaped_input)

    # Flatten the output of the convolutional layer
    flattened_layer = tf.keras.layers.Flatten()(conv_layer)

    # Define the output layer with 7 neurons
    output_layer = tf.keras.layers.Dense(units=7, activation="softmax")(flattened_layer)

    # Create the model with the input and output layers
    model = tf.keras.models.Model(inputs=input_layer, outputs=output_layer)

    # Compile the model
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.CategoricalCrossentropy(), metrics=["accuracy"])

    # Print the model summary
    model.summary()
    return model;

#Made by Axel Lindqvist 01-04-2023
#Remaking a square into one hot encoding
#Process the board and remake it into one hot enconding
def oneHotEncoding(board):
    # Convert the array to one-hot encoding using tf.one_hot()
    one_hot_arr = tf.one_hot(board, depth=3)

    # Reshape the one-hot array to match the expected input shape of the model
    one_hot_arr = tf.reshape(one_hot_arr, [1, 6, 7, 3])
    return one_hot_arr;

#Made by Axel Lindqvist 01-04-2023
#Make prediction with the board
def nnPrediction(board, model):
    oneHot = oneHotEncoding(board)
    return int(tf.argmax(model.predict(oneHot), axis=1))

#Made by Axel Lindqvist 01-04-2023
#In the NN the value 1 is friendly piece and 2 is enemy, 0 is empty
def understandableBoard(board, color):
    c = copy.deepcopy(board)
    for x in range(len(c[0])):
        for y in range(c):
            if c[y][x] == None:
                c[y][x] = 0
            elif color == 0:
                c[y][x] += 1
            else:
                c[y][x] = 2 - c[y][x]  
    return c
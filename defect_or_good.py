# -*- coding: utf-8 -*-
"""defect_or_good.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yQYx30vYrMS3VfABXnfazrvC45aT0NX_
"""

#import libraries
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

model = tf.keras.Sequential([  # Note the input shape is the desired size of the image 150x150 with 3 bytes color
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(150, 150,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2), 
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'), 
    tf.keras.layers.MaxPooling2D(2,2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(), 
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'), 
    # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class ('defect') and 1 for the other ('good')
    tf.keras.layers.Dense(1, activation='sigmoid')])

model.summary()

model.compile(optimizer="adam",
              loss='binary_crossentropy',
              metrics = ['accuracy'])

train_images = "/content/drive/My Drive/real-life-industrial-dataset-of-casting-product/casting_data/train"
test_images = "/content/drive/My Drive/real-life-industrial-dataset-of-casting-product/casting_data/test"

print('total training defect images :', len(os.listdir(r"/content/drive/My Drive/real-life-industrial-dataset-of-casting-product/casting_data/train/def_front" ) ))
print('total training good images :', len(os.listdir(r"/content/drive/My Drive/real-life-industrial-dataset-of-casting-product/casting_data/train/ok_front" ) ))

print('total validation defect images :', len(os.listdir(r"/content/drive/My Drive/real-life-industrial-dataset-of-casting-product/casting_data/test/def_front") ))
print('total validation good images :', len(os.listdir(r"/content/drive/My Drive/real-life-industrial-dataset-of-casting-product/casting_data/test/ok_front") ))

# All images will be rescaled by 1./255.
train_datagen = ImageDataGenerator( rescale = 1.0/255.0 )
test_datagen  = ImageDataGenerator( rescale = 1.0/255.0 )

train_generator = train_datagen.flow_from_directory(train_images,
                                                    batch_size=32,
                                                    class_mode='binary',
                                                    target_size=(150, 150))     
validation_generator =  test_datagen.flow_from_directory(test_images,
                                                         batch_size=32,
                                                         class_mode  = 'binary',
                                                         target_size = (150, 150))

history = model.fit(train_generator,
                              validation_data=validation_generator,
                              steps_per_epoch=10,
                              epochs=10,
                              validation_steps=100)


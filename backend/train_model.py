from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Constants
IMAGE_SIZE = (225, 225)
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 3

# Dataset paths
TRAIN_DIR = 'plant-disease-recognition-dataset/train/train'
TEST_DIR = 'plant-disease-recognition-dataset/test/test'

# Data augmentation for training and validation
train_val_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

# Data generator for testing (only rescaling)
test_datagen = ImageDataGenerator(rescale=1.0 / 255)

# Train generator
train_generator = train_val_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

# Validation generator
val_generator = train_val_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Test generator
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(225, 225, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

# Compile
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# Evaluate on test set
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"\n📊 Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"🧪 Test Loss: {test_loss:.4f}")

# Save the model
model.save('model.h5')
print("✅ Model saved as model.h5")

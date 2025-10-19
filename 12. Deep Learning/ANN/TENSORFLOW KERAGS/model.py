import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, losses

# 1️⃣ Load and preprocess dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

# 2️⃣ Define a simple ANN model builder
def build_model():
    model = models.Sequential([
        layers.Flatten(input_shape=(28, 28)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

# 3️⃣ Define multiple optimizers
optimizers_dict = {
    "SGD": optimizers.SGD(learning_rate=0.01, momentum=0.9),
    "RMSprop": optimizers.RMSprop(learning_rate=0.001),
    "Adam": optimizers.Adam(learning_rate=0.001),
    "Adagrad": optimizers.Adagrad(learning_rate=0.01),
    "Nadam": optimizers.Nadam(learning_rate=0.001)
}

# 4️⃣ Define multiple loss functions (for classification)
loss_functions = {
    "sparse_categorical_crossentropy": losses.SparseCategoricalCrossentropy(),
    "categorical_crossentropy": losses.CategoricalCrossentropy(from_logits=False),
    "kullback_leibler_divergence": losses.KLDivergence()
}

# 5️⃣ Prepare one-hot labels for losses needing them
y_train_onehot = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test_onehot = tf.keras.utils.to_categorical(y_test, num_classes=10)

# 6️⃣ Train & evaluate each optimizer-loss combination
results = []

for opt_name, opt in optimizers_dict.items():
    for loss_name, loss_fn in loss_functions.items():
        print(f"\n🔹 Training with Optimizer = {opt_name}, Loss = {loss_name}")
        
        model = build_model()
        
        # Use correct label format for loss type
        if "sparse" in loss_name:
            y_train_use, y_test_use = y_train, y_test
        else:
            y_train_use, y_test_use = y_train_onehot, y_test_onehot
        
        model.compile(optimizer=opt, loss=loss_fn, metrics=['accuracy'])
        
        history = model.fit(
            x_train, y_train_use,
            epochs=5,
            batch_size=64,
            verbose=0,       # set to 1 or 2 to see details
            validation_split=0.2
        )

        test_loss, test_acc = model.evaluate(x_test, y_test_use, verbose=0)
        results.append((opt_name, loss_name, test_acc))
        print(f"✅ Test Accuracy: {test_acc:.4f}")

# 7️⃣ Show summary of results
print("\n📊 Final Accuracy Comparison:")
print("-" * 60)
for opt_name, loss_name, acc in results:
    print(f"Optimizer: {opt_name:10s} | Loss: {loss_name:30s} | Accuracy: {acc:.4f}")

import os
from typing import Tuple
import numpy as np
from PIL import Image
import tensorflow as tf


def build_model(input_shape: Tuple[int, int, int] = (200, 200, 3)) -> tf.keras.Model:
    """Builds the CNN model matching the notebook architecture."""
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=input_shape),
        tf.keras.layers.MaxPool2D(2, 2),

        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(2, 2),

        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(2, 2),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.compile(
        loss="binary_crossentropy",
        optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
        metrics=["accuracy"],
    )

    return model


def preprocess_image(img: Image.Image, target_size=(200, 200)) -> np.ndarray:
    """Resize and scale the PIL image to the model input.

    Notes:
    - The original notebook used custom rescale factors (2/200 or 1/200).
      Using 1/255 is the common approach and produces stable predictions.
      This function uses 1/255 scaling.
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size)
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr


class MoodModel:
    """Wrapper around the TensorFlow model to simplify loading and prediction."""

    def __init__(self, weights_path: str = None):
        self.model = build_model()
        self.class_mapping = {0: "not happy", 1: "happy"}
        if weights_path and os.path.exists(weights_path):
            try:
                self.model.load_weights(weights_path)
            except Exception:
                # If weights are incompatible, ignore and keep untrained model
                pass

    def predict_pil(self, img: Image.Image) -> Tuple[str, float]:
        x = preprocess_image(img)
        prob = float(self.model.predict(x)[0][0])
        # Threshold at 0.5 (sigmoid)
        label = 1 if prob >= 0.5 else 0
        return self.class_mapping[label], prob

    def save_weights(self, path: str):
        self.model.save_weights(path)


if __name__ == "__main__":
    # quick smoke test
    m = MoodModel()
    from PIL import Image

    img = Image.new("RGB", (200, 200), color=(128, 128, 128))
    print(m.predict_pil(img))

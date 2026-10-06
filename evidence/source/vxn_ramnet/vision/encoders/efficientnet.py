from __future__ import annotations

import hashlib
import math
from importlib import metadata
from pathlib import Path
from typing import Sequence

import numpy as np

from vxn_ramnet.algorithms.similarity import l2_normalize_rows
from vxn_ramnet.config.models import EncoderSettings
from vxn_ramnet.core.exceptions import ModelLoadError
from vxn_ramnet.io.checksums import sha256_file
from vxn_ramnet.vision.preprocessing import load_rgb


class EfficientNetB0VisualEncoder:
    """Frozen Keras EfficientNetB0 embedding adapter.

    TensorFlow is imported lazily and remains an optional dependency.
    """

    def __init__(self, settings: EncoderSettings):
        self.settings = settings
        try:
            import tensorflow as tf
            from tensorflow.keras.applications import EfficientNetB0
            from tensorflow.keras.applications.efficientnet import preprocess_input
        except ImportError as exc:
            raise ModelLoadError("TensorFlow is required. Install with: pip install 'vxn-ramnet[vision]'") from exc
        self._tf = tf
        self._preprocess = preprocess_input
        height, width = settings.input_size
        keras_weights = None if settings.weights == "local" else settings.weights
        if keras_weights == "imagenet" and not settings.allow_remote_weight_resolution:
            raise ModelLoadError("Remote/cache ImageNet weight resolution is disabled; provide a local weights_path")
        try:
            self._model = EfficientNetB0(
                input_shape=(height, width, 3), include_top=False, weights=keras_weights, pooling="avg"
            )
            if settings.weights == "local":
                # Keras adds this weight-free layer only for weights='imagenet'.
                # Loading identical arrays into weights=None otherwise changes
                # descriptors. Recreate that graph without resolving remote weights.
                if settings.local_preprocessing == "keras_imagenet":
                    scale = tf.keras.layers.Rescaling([1.0 / math.sqrt(v) for v in (0.229, 0.224, 0.225)])

                    def call_layer(layer, *args, **kwargs):
                        output = layer(*args, **kwargs)
                        return scale(output) if isinstance(layer, tf.keras.layers.Normalization) else output

                    self._model = tf.keras.models.clone_model(self._model, call_function=call_layer)
                self._model.load_weights(str(settings.weights_path))
            self._model.trainable = False
            self._model(np.zeros((1, height, width, 3), dtype=np.float32), training=False)
            digest = hashlib.sha256()
            for weight in self._model.get_weights():
                values = np.asarray(weight)
                digest.update(str(values.shape).encode("ascii"))
                digest.update(str(values.dtype).encode("ascii"))
                digest.update(values.tobytes(order="C"))
        except Exception as exc:
            raise ModelLoadError(f"Could not initialize EfficientNetB0: {exc}") from exc
        self._manifest = {
            "encoder": "efficientnet_b0",
            "input_size": [height, width],
            "embedding_dimension": int(self._model.output_shape[-1]),
            "weights_source": str(settings.weights_path) if settings.weights_path else settings.weights,
            "weights_sha256": sha256_file(settings.weights_path) if settings.weights_path else None,
            "loaded_weights_sha256": digest.hexdigest(),
            "architecture_preprocessing": settings.local_preprocessing
            if settings.weights == "local"
            else "keras_imagenet",
            "preprocessing": "PIL EXIF transpose, RGB 0..255 float32, bilinear resize, optional horizontal flip; Keras EfficientNet built-in rescaling; unit L2 descriptor",
            "tensorflow_version": getattr(tf, "__version__", None) or metadata.version("tensorflow"),
            "trainable": False,
        }

    @property
    def manifest(self) -> dict:
        return dict(self._manifest)

    def encode(self, frame_paths: Sequence[Path], *, flip: bool = False) -> np.ndarray:
        if not frame_paths:
            raise ValueError("No frame paths were provided")
        chunks = []
        for start in range(0, len(frame_paths), self.settings.batch_size):
            paths = frame_paths[start : start + self.settings.batch_size]
            batch = np.stack([load_rgb(path, self.settings.input_size, flip) for path in paths])
            batch = self._preprocess(batch)
            output = np.asarray(self._model(batch, training=False), dtype=np.float32)
            chunks.append(l2_normalize_rows(output))
        return np.vstack(chunks).astype(np.float32)

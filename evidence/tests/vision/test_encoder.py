import os

import numpy as np
import pytest
from PIL import Image

from vxn_ramnet.config.models import EncoderSettings
from vxn_ramnet.vision.encoders.efficientnet import EfficientNetB0VisualEncoder
from vxn_ramnet.vision.preprocessing import load_rgb

pytestmark = pytest.mark.vision


def test_preprocessing_has_correct_shape_range_and_horizontal_flip(tmp_path):
    pixels = np.arange(8 * 10 * 3, dtype=np.uint8).reshape(8, 10, 3)
    path = tmp_path / "rgb.png"
    Image.fromarray(pixels).save(path)
    original, flipped = load_rgb(path, (8, 10)), load_rgb(path, (8, 10), True)
    assert original.shape == (8, 10, 3)
    assert original.dtype == np.float32
    assert np.array_equal(original[:, ::-1], flipped)


def test_real_frozen_imagenet_encoder_is_normalized_and_content_identified(tmp_path):
    pytest.importorskip("tensorflow")
    if os.environ.get("VISIONX_TEST_IMAGENET") != "1":
        pytest.skip("Set VISIONX_TEST_IMAGENET=1 to run the declared ImageNet weight smoke test")
    path = tmp_path / "image.png"
    pixels = np.random.default_rng(17).integers(0, 256, (224, 224, 3), dtype=np.uint8)
    Image.fromarray(pixels).save(path)
    encoder = EfficientNetB0VisualEncoder(EncoderSettings(batch_size=1))
    values = encoder.encode([path])
    flipped = encoder.encode([path], flip=True)
    assert values.shape == flipped.shape == (1, 1280)
    assert np.isfinite(values).all()
    assert np.allclose(np.linalg.norm(values, axis=1), 1.0, atol=1e-5)
    assert len(encoder.manifest["loaded_weights_sha256"]) == 64
    assert encoder.manifest["trainable"] is False
    # Exercise the no-network local-weight path with the same actual weights.
    weights = tmp_path / "approved.weights.h5"
    encoder._model.save_weights(str(weights))
    local = EfficientNetB0VisualEncoder(
        EncoderSettings(weights="local", weights_path=weights, allow_remote_weight_resolution=False)
    )
    assert np.allclose(local.encode([path]), values, atol=1e-5)
    assert local.manifest["loaded_weights_sha256"] == encoder.manifest["loaded_weights_sha256"]
    assert local.manifest["weights_sha256"] is not None

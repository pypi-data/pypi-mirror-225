import pickle
from pathlib import Path

from jax.tree_util import tree_flatten, tree_unflatten

_SUFFIX = ".cgp"

def save(model, fname):
    file_path = Path(fname)

    if file_path.suffix != _SUFFIX:
        file_path = file_path.with_suffix(_SUFFIX)

    model_flat = tree_flatten(model)

    with open(file_path, "wb") as f:
        pickle.dump(model_flat, f)


def load(fname):
    file_path = Path(fname)

    assert file_path.suffix == _SUFFIX, f"File extension must be {_SUFFIX}, given file has {file_path.suffix}!"

    with open(file_path, "rb") as f:
        model_flat, model_struct = pickle.load(f)

    return tree_unflatten(model_struct, model_flat)
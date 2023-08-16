# Implementation of rebotics_sdk.rcdb.Unpacker

It's a rust library to unpack labels and embeddings from rcdb file. Duplicating functionality of following python code:

```python
from rebotics_sdk.rcdb import Unpacker
import numpy as np


def unpack(filepath: str):
    unpacker = Unpacker(filepath)
    
    with unpacker:
        metadata = unpacker.get_metadata()
        features = np.empty(
            (metadata.count, 512), dtype=np.float32
        )
        labels_np = np.empty(metadata.count, dtype=object)
    
        for i, entry in enumerate(unpacker.entries()):
            labels_np[i] = entry.label
            features[i] = entry.feature_vector
    
    return labels_np, features_np
```

Via `maturin` and `pyo3` it has a python interface. Which can be accessed via:

```python
import numpy as np
import rcdb_unpacker

labels, features = rcdb_unpacker.unpack("path/to/file")
# one thing to note is that labels is a list of strings, while features is np.array
# so you have to format labels to np.array in CORE usage

labels = np.array(labels, dtype=object)
```

It only solves unpacking for classification service in CORE utilizing 100% of the CPU capacity and yielding x3 speedup in comparison to pure python implementation.

## Setup rust
Follow instructions from here https://rustup.rs/
You can use jetbrains Clion with rust plugin.

To build:
```bash
cargo build
```


To run tests:
```bash
cargo test --package rcdb_unpacker --lib tests
```


## Development for python

* Create a virtual environment `python3 -m venv venv`
* Install requirements.txt
* use `maturin` for building the python package. More info here: https://github.com/PyO3/maturin

```bash
# build and install the package to local environment
maturin develop  # equivalent of pip install -e . 

```

### Deployment to PyPI


## TODO:
* [ ] Add tests
* [ ] Split mappings for python and other platforms
* [ ] arm64 support
* [ ] Add mappings for iOS and Android

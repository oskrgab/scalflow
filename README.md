# scalflow

A Python toolkit for Special Core Analysis (SCAL) and petrophysics: relative
permeability, capillary pressure, core data, and well logs.

> **Note:** `scalflow` was previously published as `relperm`. The old package is
> deprecated — please migrate to `scalflow`.

## Installation

```bash
pip install scalflow
```

## Usage

```python
import numpy as np
from scalflow import s_eff, krw

sw = np.linspace(0.2, 0.9, 50)
se = s_eff(sw, swr=np.float64(0.2), snwr=np.float64(0.1))
kr = krw(se, krw0=np.float64(0.8), nw=np.float64(2.0))
```

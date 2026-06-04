# Getting Started

## Installation

Install scalflow using uv:

```bash
uv pip install scalflow
```

## Basic Usage

Here's a simple example computing wetting-phase relative permeability with the
Corey model:

```python
import numpy as np
from scalflow import s_eff, krw

# Define wetting-phase saturation values
sw = np.linspace(0.2, 0.9, 100)

# Effective saturation, then relative permeability
se = s_eff(sw, swr=np.float64(0.2), snwr=np.float64(0.1))
kr = krw(se, krw0=np.float64(0.8), nw=np.float64(2.0))
```

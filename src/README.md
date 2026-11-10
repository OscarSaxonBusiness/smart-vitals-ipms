# src/

Code you use more than once, written as functions, like the Week 5 pipeline (`check_range`, `fill_short_gaps`, ...): the simulator, the API and the notebooks can then share it.

In a notebook inside `notebooks/`, add the project folder to the path first:

```python
import sys
sys.path.append("..")
from src.cleaning import check_range
```

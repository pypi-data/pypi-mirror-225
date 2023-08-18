# py-find-aws-region
Python package to choose the best AWS region based on latency.

## Basic Usage

```python
from find_aws_regions import get_regions_by_latency

results = get_regions_by_latency()

print(results)
```

`get_regions_by_latency()` will return a list of dictionaries with the following keys:

- `region_name`: The AWS region code (e.g. `us-east-1`)
- `latency`: The latency in milliseconds (e.g. `47.345`)

### Limit the tested regions

You can limit the tested regions by passing a list of region codes to `get_regions_by_latency()`:

```python
from find_aws_regions import get_regions_by_latency

results = get_regions_by_latency(['us-east-1', 'us-west-2'])
```

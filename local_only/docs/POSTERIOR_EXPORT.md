# Posterior export and conversion

Preferred posterior format in this repo is a `.npy` file containing an array of dict draws saved with
`np.save(..., allow_pickle=True)`.

If you have posterior draws in CSV, convert with:

```bash
python -m scripts.convert_posterior_csv_to_npy --csv <file.csv> --kind behavior --out outputs/posterior_samples/behavior_posterior.npy
```

Supported kinds:
- behavior, clinical, insurance, passthrough, data_quality, mapping

Validation uses Pydantic schemas in `src/model/param_schema.py`.

# A Simple Data Validator

This is a simple data validation framework, built to be easy to add new stuff to.

The main goal for this little project was to have a baseline I could use for my daily work, where I can add new configs and validation rules on the fly without a bunch of hassle.

Its main "feature" is that it **doesn't load the whole file into memory.** It reads row-by-row, so it's memory-friendly and won't (praying) crash on huge datasets.

## Setup

Uses `uv` but `pip` is fine.

```bash
# Install dependencies
uv pip install -r requirements.txt 

# Run the tests
python -m unittest discover
```

## How to Run It

It's all run from `main.py`:

```bash
# Basic run
python -m src.main --config_file test.yaml --data_file test.csv

# Run with performance profiling (memory + time)
python -m src.main --config_file test.yaml --data_file test.csv --profile
```

## How to Add New Stuff

This is the whole point of the project. It's meant to be easy.

### 1. How to add a new file type:

1.  Create a new `MyCoolReader.py` in `src/readers/`.
2.  Make sure your `MyCoolReader` class inherits from `BaseReader` and has a `.read()` method that `yield`s a dictionary for each row.
3.  Add it to the `_readers` dictionary in `src/readers/reader_factory.py`.

### 2. How to add a new config setting:

1.  Add the new field to the `Config` class in `src/config/config_model.py`.
2.  Pydantic will automatically validate the config file's structure.
3.  If you need custom logic (like our `ALLOWED_DATA_TYPES` check), add a `@field_validator` for it.

### 3. How to add a new data validation:

1.  Create your `MyNewValidator.py` in `src/validations/`.
2.  Your class should inherit from `BaseValidator` (and have a `.validate(row)` method).
3.  Instantiate it in `main.py` and add it to the `validators` list. The `ValidationManager` will handle the rest.

## Contributing

This repository will be updated through time as I find new things to add. Feel free to contribute!
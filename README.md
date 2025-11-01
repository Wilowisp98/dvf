How to add a new file type?
-> create a *file_type* reader .py with a reader class.
-> Add that reader class to the reader_factory.

How to add a new config?
-> Add the config to config_model.py
-> Build the validation on config_validator.py

How to add a new validation?
-> Build a new validation on the validations folder with the BaseValidator.
-> Add the validation to the main.py
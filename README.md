# bp2022-ap1

## Environment variables

We're using `dotenv` to load environment variables. We have three files that contain environment variables.
If you want to use an environment variable, please use them from `src/constants.py` or `test/constants.py`. 

:information_source: We'll probably load them into `os,environ` as soon as the flask application is initialized. 

### `.env.shared`

This file contains harmless environment variables.

### `.env.secret`

This file contains secret variables, that shouldn't be shared. It overrides variables from `.env.shared`.
Only variable declarations in `os.environ` override variables in `.env.secret`.

### `.env.test`

This file contains variables for the test environment.
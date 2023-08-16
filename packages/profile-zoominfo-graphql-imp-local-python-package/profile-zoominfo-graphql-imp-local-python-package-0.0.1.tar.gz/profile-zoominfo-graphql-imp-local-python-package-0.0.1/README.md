# python-package-template
To create local package and remote package layers (not to create GraphQL and REST-API layers)

# directory structure
Root directory should have only .github/, ,gitignore, README.md and the project directory (i.e. location_local_python_package same as repo) - This will allow is to easily switch to mono repo<br> 
/location_local<br>
/location_local/get_country_name<br>
/location_local/get_country_name/src<br>
/location_local/get_country_name/src/get_country_name.py<br>
/location_local/get_country_name/tests<br>
/location_local/get_country_name/tests/get_country_name_test.py<br>

# database Python scripts in /db folder
Please place <table-name>.py in /db<br>
No need for seperate file for _ml table<br>
Please delete the example file if not needed<br>
  
# Create the files to create the database schema, tables, view and populate metadata and Test-Data
/db/<table-name>.py - CREATE SCHEMA ... CREATE TABLE ... CREATE VIEW ... including _ml_table<br>
/db/<table-name>_insert.py to create metadata and Test-Data records

# Update the setup.py (i.e.name, version)
 
# Please create test directory inside the directory of the project i.e. /<project-name>/tests

# Update the serverless.yml in the root directory
provider:
  stage: play1
  
Update the endpoints in serverless.yml

# Working with VS Code
Please make sure you push to the repo launch.json fie that enables to run and debug the code<br>

# Unit-Test
We prefer using pytest and not unittest package<br>

Please create pytest.init in the project-directory and not in the root directory
```
[pytest]
markers =
    test: custom mark for tests
```

# When you took care of all the TODOs in the repo, using our infrastructure classes (i.e. Logger, Database, Url, Importer ...) your Feature Branch GitHub Actions Workflow is Green without warnings, all tests are running in GHA, code is documented, README.md is clean and self explained, test coverage is above 90% and all your lines are covered with Unit-Tests, you can filter and analyse your records in Logz.io, pull dev to your Feature Branch and only then create Pull Request to dev

# ZoomAPI Python Wrapper

This Python script provides a wrapper class, `ZoomAPI`, for interacting with the Zoom API. It allows you to perform various actions such as retrieving user information, getting access tokens, and making API requests.

## Prerequisites

Before using this script, you need to have the following:

1. A valid Zoom account.
2. A Zoom App with OAuth settings. Make sure you have the `CLIENT_ID` and `CLIENT_SECRET`.
3. Access Token: You can use the `ACCESS_TOKEN` if you have it. Alternatively, you can use the `get_access_token` method to obtain an access token.
4. Redirect URL: Required for obtaining an access token using OAuth.

## Usage

1. Import the `ZoomAPI` class:
    ```python
    from ZoomAPI import ZoomAPI
    ```

2. Create an instance of the `ZoomAPI` class:
    ```python
    zoom = ZoomAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN, redirect_url=REDIRECT_URL)
    ```

3. Available Methods:
   - `get_access_token(redirect_url)`: Obtain an access token using OAuth.
   - `print_json_pretty(json_data)`: Pretty-print JSON data.
   - `get_user_by_email(email)`: Get user information by email.
   - `get_user_id(email)`: Get the user ID by email.
   - `get_user_by_id(user_id)`: Get user information by ID.
   - `get_users()`: Get a list of all users.

4. Example Usage:
   ```python
   email = "example@example.com"
   user_data = zoom.get_user_by_email(email)
   print(user_data)


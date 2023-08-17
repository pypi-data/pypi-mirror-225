
# Bitwarden Passwordless.dev Python 3.8 SDK Client

A Python client library for interacting with the Bitwarden Passwordless.dev API.

## Installation

1. Install the package using pip:

```bash
pip install passwordless-38
```

## Usage

### Configuration

You can store the API configurations in a file named `passwordlessconfig.ini` for easier management and security.

#### Creating a Configuration File

Create a file named `passwordlessconfig.ini` in the same directory as your script, with the following content:

```ini
[API]
API_URL = https://v4.passwordless.dev
API_SECRET = Your-API-Secret-Here
API_KEY = Your-API-Key-Here
VERIFY = False
```

Replace the values with your actual API secret and public API key.

The `PasswordlessClient` class will automatically read this file and use the specified configurations when making requests to the Passwordless.dev API.

#### Reading the Configuration in Code

Use the `configparser` module to read the configuration file and pass the keys to the `PasswordlessClient`:

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_secret = config['passwordless']['api_secret']
# api_key can be accessed similarly if needed

```
### Importing the Client

Once the package is installed, you can import the `PasswordlessClient` class in your Python script or application:

```python
from passwordless-38 import PasswordlessClient
```

### Creating a Client Instance

Create an instance of the `PasswordlessClient` class, providing your API private secret:

```python
client = PasswordlessClient(api_secret)
```

### Using the Client's Methods

You can now use the various methods provided by the `PasswordlessClient` class to interact with the Passwordless.dev API.


### Register Token

Register a new token using the `register_token` method:

```python
result = client.register_token(user_id="some-user-id", username="username@example.com", displayname="John Doe")
```

### Sign In Verification

Verify a sign-in token using the `signin_verify` method:

```python
result = client.signin_verify(token="your-token-here")
```

### Alias Management

Manage aliases using the `alias` method:

```python
result = client.alias(user_id="user-id", aliases=["alias1@example.com", "alias2@example.com"])
```

### Credentials Management

List and delete credentials using the `credentials_list` and `credentials_delete` methods:

```python
# List credentials
result = client.credentials_list(user_id="user-id")

# Delete credential
result = client.credentials_delete(credential_id="credential-id")
```

## Example Application

This section provides an example of how the `PasswordlessClient` class can be used in an application to interact with the Passwordless.dev API.

### 1. Import and Initialize the Client

First, ensure that the `passwordlessconfig.ini` file is created with the correct configurations as described in the Configuration section.

Then, import and initialize the client:

```python
from passwordless-38 import PasswordlessClient

client = PasswordlessClient()  # Reads from passwordlessconfig.ini
```

### 2. Register a New User

```python
user_id = "some-user-id"
username = "username@example.com"
displayname = "John Doe"

result = client.register_token(user_id, username, displayname)
print("Registration Result:", result)
```

### 3. Verify a Sign-In Token

```python
token = "your-token-here"
result = client.signin_verify(token)
print("Verification Result:", result)
```

### 4. Manage Aliases

```python
aliases = ["alias1@example.com", "alias2@example.com"]
result = client.alias(user_id, aliases)
print("Alias Management Result:", result)
```

### 5. List and Delete Credentials

```python
# List credentials
result = client.credentials_list(user_id)
print("Credentials List:", result)

# Delete a specific credential
credential_id = "credential-id"
result = client.credentials_delete(credential_id)
print("Credential Deletion Result:", result)
```

These examples demonstrate a typical workflow for interacting with the Passwordless.dev API. By using the `PasswordlessClient` class, you can easily integrate authentication and authorization features into your Python application.

## License

This project is licensed under the MIT License.

## Contributing

Please refer to the CONTRIBUTING.md file for details on contributing to this project.

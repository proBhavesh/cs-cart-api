# Backend

This directory contains all the code and resources related to the backend of our project.

## Structure

The directory is structured as follows:

- `api/` - Contains code related to different API services.
  - `auth.py` - This script handles all authentication-related tasks.
  - `store.py` - This script handles session storage.
- `.env` - Contains environment variables such as ADMIN_EMAIL and ADMIN_API_KEY.

## Setup

1. Make sure Python 3.7+ is installed on your system.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Set up your `.env` file with the following variables:
   - `ADMIN_EMAIL`: The email for the admin account.
   - `ADMIN_API_KEY`: The API key for the admin account.
4. Run `python main.py` to start the application.

## Usage

In `main.py`, the `AuthService` is used to send authentication requests. Currently, it is set up to send an authentication request for "vendor@example.com". If you need to authenticate with another account, you can uncomment the last line and replace "vendor2@example.com" with the desired email.

```python
print(auth_service.send_auth_request("vendor2@example.com"))
```

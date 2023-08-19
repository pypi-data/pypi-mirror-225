import google.auth
from google.auth.exceptions import DefaultCredentialsError
from google.auth.transport.requests import AuthorizedSession

# Applications using RBM transport must supply Default Application Credentials,
# or provide their own rbm_http override. See README.md.
try:
    credentials, project = google.auth.default(
        'https://www.googleapis.com/auth/rcsbusinessmessaging'
    )
except DefaultCredentialsError:
    credentials = None

http = AuthorizedSession(credentials)  # OAuth wrapper for requests

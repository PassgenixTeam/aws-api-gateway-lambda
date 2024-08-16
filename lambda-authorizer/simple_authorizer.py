import base64
import traceback

USERNAME = "admin"
PASSWORD = "admin"


def lambda_handler(event, context):
    """
    Reference: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-lambda-authorizer.html
    Version: 2.0
    Response Type: Simple

    Validate the incoming token and produce the principal user identifier
    associated with the token. This can be accomplished in a number of ways:

    1. Call out to the OAuth provider
    2. Decode a JWT token inline
    3. Lookup in a self-managed DB
    """

    try:
        client_token = event["headers"]["authorization"]
        print("Client token: " + client_token)

        encoded_credentials = client_token.split(" ")[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":")

        if username == USERNAME and password == PASSWORD:
            print("Allowed")
            return {
                "isAuthorized": True,
                "context": {"username": username, "token": client_token},
            }
        else:
            raise Exception("Username or password is incorrect")

    except Exception as error:
        traceback.print_exc()
        return {
            "isAuthorized": False,
            "context": {
                "error": str(error),
            },
        }

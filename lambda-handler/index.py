import traceback
from api_response import (
    Ok,
    BaseException,
    NotFound,
    MethodNotAllowed,
    InternalServerError,
)


def lambda_handler(event, context):
    """
    AWS Lambda handler function to handle API Gateway calls.
    Reference: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    Version: 2.0

    Args:
        event (dict): Payload from the API Gateway call.
        context (object): The context object passed to the Lambda function.

    Returns:
        dict: The response data to be returned by the Lambda function.

    Raises:
        NotFound: If the requested path is not found.
        MethodNotAllowed: If the requested method is not allowed.
        InternalServerError: If an unexpected error occurs.
    """

    try:
        http_request = event["requestContext"]["http"]

        # Extract the path and method from the HTTP request
        path = http_request["path"]
        method = http_request["method"]

        # Handle asset requests
        first_path = path.split("/")[1]
        match first_path:
            case "assets":
                match method:
                    case "GET":
                        asset_path = "/".join(path.split("/")[2:])
                        extension = asset_path.split(".")[-1]
                        if extension in ["html", "css", "js"]:
                            return Ok(
                                open(f"assets/{asset_path}").read(),
                                headers={"Content-Type": f"text/{extension}"},
                                is_json=False,
                            ).get_response()
                        else:
                            return Ok(
                                open(f"assets/{asset_path}").read(),
                                headers={"Content-Type": "*/*"},
                                is_json=False,
                            ).get_response()

        # Handle API requests
        match path:
            case "/test/path":
                match method:
                    case "GET":
                        result = get_test_path()
                        print(Ok(result).get_response())
                        return Ok(result).get_response()

                    case _:
                        raise MethodNotAllowed("Method not implemented.")

            case _:
                raise NotFound("Path not implemented.")

    except BaseException as error:
        traceback.print_exc()
        return error.get_response()

    except Exception as error:
        traceback.print_exc()
        return InternalServerError(error).get_response()


def get_test_path():
    # Implement logic here
    return [{"foo1": "bar1"}, {"foo2": "bar2"}]

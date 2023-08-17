import requests
from .. import error


def response_check(response: requests.Response):
    if response.status_code >= 300:
        raise error.OMNI_INFER_API_ERROR("Error response status code: " + str(response.status_code) + "  Error url"
                                         + response.url)


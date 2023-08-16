import json
import requests
from tqdm import tqdm
from io import BytesIO
from typing import Optional,  Callable, Iterable
from requests.models import Response
from google.oauth2.credentials import Credentials  # type:ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type:ignore
import gp_wrapper.objects.core.media_item
from ...utils import RequestType, Printable, HeaderType, MimeType, ProgressBarInjector
from ...utils import EMPTY_PROMPT_MESSAGE, SCOPES, MEDIA_ITEMS_CREATE_ENDPOINT


class GooglePhotos(Printable):
    """A wrapper class over GooglePhotos API to get 
    higher level abstraction for easy use
    """
    # TODO implement quota

    def __init__(self, client_secrets_path: str = "./client_secrets.json") -> None:
        flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)  # noqa
        self.credentials: Credentials = flow.run_local_server(
            authorization_prompt_message=EMPTY_PROMPT_MESSAGE
        )
        self.session = requests.Session()
        self.session.credentials = self.credentials  # type:ignore

    def request(
            self,
            req_type: RequestType,
            endpoint: str,
            header_type: HeaderType = HeaderType.JSON,
            # mime_type: Optional[MimeType] = None,
            tqdm_options: Optional[dict] = None,
            **kwargs
    ) -> Response:
        """core request function to handle request for all other classes

        Args:
            req_type (RequestType): the type of request
            endpoint (str): the endpoint 
            header_type (HeaderType, optional): which header type should the request use. Defaults to HeaderType.JSON.

        Returns:
            Response: the response of the request
        """
        headers: dict = {"Authorization": f"Bearer {self.credentials.token}"}
        if header_type != HeaderType.DEFAULT:
            headers["Content-Type"] = f"application/{header_type.value}"

        if tqdm_options:
            kwargs['data'] = \
                ProgressBarInjector(
                    kwargs['data'],
                    tqdm_options
            )

        request_map: dict[RequestType, Callable[..., Response]] = {
            RequestType.GET: self.session.get,
            RequestType.POST: self.session.post,
            RequestType.PATCH: self.session.patch,
        }
        return request_map[req_type](url=endpoint, headers=headers, **kwargs)

    def _get_media_item_id(self, upload_token: str) -> "gp_wrapper.objects.core.media_item.CoreMediaItem":
        payload = {
            "newMediaItems": [
                {
                    "simpleMediaItem": {
                        "uploadToken": upload_token
                    }
                }
            ]
        }
        response = self.request(
            RequestType.POST,
            MEDIA_ITEMS_CREATE_ENDPOINT,
            HeaderType.DEFAULT,
            json=payload,
        )
        j = response.json()
        if "newMediaItemResults" in j:
            dct = j['newMediaItemResults'][0]['mediaItem']
            return gp_wrapper.objects.core.media_item.CoreMediaItem._from_dict(self, dct)  # pylint: disable=protected-access #noqa
        # TODO fix this
        print(json.dumps(j, indent=4))
        raise AttributeError("'newMediaItemResults' not found in response")


__all__ = [
    "GooglePhotos"
]

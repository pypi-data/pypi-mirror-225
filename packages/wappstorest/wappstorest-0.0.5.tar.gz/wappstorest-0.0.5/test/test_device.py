import uuid
import logging

from pytest_httpx import HTTPXMock

from wappstorest import WappstoEnv
from wappstorest import WappstoPath
from wappstorest import WappstoRest
from wappstorest import WappstoService


logging.root.level = logging.DEBUG


class TestDeviceRest:
    def test_getDevice(self, httpx_mock: HTTPXMock):
        pass
        # session_uuid = uuid.UUID('2d94624a-0a3d-45c6-88ee-ecbf3ff3a980')

        # httpx_mock.add_response(
        #     method="GET",
        #     url='https://wappsto.com/services/2.1/user/me',
        #     match_headers={
        #         'x-session': str(session_uuid),
        #         "Accept": "application/json",
        #         "Content-type": "application/json",
        #     },
        #     json={
        #         'first_name': 'Tom',
        #         'meta': {
        #             'id': str(uuid.uuid4()),
        #             'type': 'user',
        #         }
        #     },  # The Reply
        # )

        # rest = WappstoRest(
        #     env=WappstoEnv.PROD,
        #     session=session_uuid,
        # )

        # reply = rest.service(WappstoService.USER).service_id('me').get()

        # assert reply.first_name == 'Tom'
        # # assert reply.first_name == 'Tom'

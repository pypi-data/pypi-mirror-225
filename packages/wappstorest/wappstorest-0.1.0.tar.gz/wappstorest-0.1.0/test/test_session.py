import uuid
import json
import logging

from pytest_httpx import HTTPXMock

from wappstorest import WappstoEnv
from wappstorest import WappstoPath
from wappstorest import WappstoSchema
from wappstorest import WappstoRest
from wappstorest import WappstoService


logging.root.level = logging.DEBUG


class TestSessionRest:
    def test_create(self, httpx_mock: HTTPXMock):
        session_id: str = str(uuid.uuid4())

        httpx_mock.add_response(
            method="POST",
            url='https://wappsto.com/services/2.1/session',
            match_headers={
                "Accept": "application/json",
                "Content-type": "application/json",
            },
            match_content=json.dumps({
                'username': 'Tom',
                'password': 'the_password_1234'
            }).encode(),
            json={
                'username': 'Tom',
                'meta': {
                    'id': session_id,
                    'type': 'user',
                }
            },  # The Reply
        )

        rest = WappstoRest(
            env=WappstoEnv.PROD
        )

        reply = rest.service(
            WappstoService.SESSION
        ).create(
            data=WappstoSchema.create.Session(
                username='Tom',
                password='the_password_1234'
            )
        )

        assert type(reply) == WappstoSchema.response.User
        assert reply.username == 'Tom'
        assert str(reply.meta.id) == session_id

    def test_get(self, httpx_mock: HTTPXMock):
        session_id: str = str(uuid.uuid4())
        count = 10
        httpx_mock.add_response(
            method="GET",
            url='https://wappsto.com/services/2.1/session',
            match_headers={
                "Accept": "application/json",
                "Content-type": "application/json",
                "x-session": session_id,
            },
            json={
              "count": count,
              "more": False,
              "limit": 1000,
              "meta": {
                "type": "idlist",
                "version": "2.1"
              },
              "child": [
                {
                  "type": "session",
                  "version": "2.1"
                }
              ],
              "id": [
                session_id,
              ] + [str(uuid.uuid4()) for _ in range(count)]
            },  # The Reply
        )

        rest = WappstoRest(
            env=WappstoEnv.PROD
        )
        rest.set_session(session_id)

        reply = rest.service(
            WappstoService.SESSION
        ).get()

        assert type(reply) == WappstoSchema.response.IdList
        assert session_id in reply.id
        assert reply.count == count

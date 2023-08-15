#
# Copyright (c) 2021 Nitric Technologies Pty Ltd.
#
# This file is part of Nitric Python 3 SDK.
# See https://github.com/nitrictech/python-sdk for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Union
from grpclib.client import Channel
from grpclib import GRPCError
from nitric.exception import exception_from_grpc_error
from nitric.utils import new_default_channel
from nitric.proto.nitric.websocket.v1 import (
    WebsocketServiceStub,
    WebsocketSendRequest,
)


class Websocket(object):
    """Nitric generic Websocket client."""

    def __init__(self):
        """Construct a Nitric Websocket Client."""
        self._channel: Union[Channel, None] = new_default_channel()
        # Had to make unprotected (publically accessible in order to use as part of bucket reference)
        self.websocket_stub = WebsocketServiceStub(channel=self._channel)

    async def send(self, socket: str, connection_id: str, data: bytes):
        """Send data to a connection on a socket."""
        try:
            await self.websocket_stub.send(
                websocket_send_request=WebsocketSendRequest(socket=socket, connection_id=connection_id, data=data)
            )
        except GRPCError as grpc_err:
            raise exception_from_grpc_error(grpc_err)

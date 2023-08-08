"""
The MIT License (MIT)

Copyright (c) 2023-present STACiA

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

if TYPE_CHECKING:
    from aiohttp import ClientResponse

__all__ = (
    'BadRequest',
    'Forbidden',
    'HTTPException',
    'InternalServerError',
    'NotFound',
    'RateLimited',
    'ValorantError',
)


class ValorantError(Exception):
    """Exception that's raised when a Valorant API request operation fails."""

    pass


class HTTPException(ValorantError):
    """Exception that's raised when an HTTP request operation fails.
    Attributes
    ------------
    response: :class:`aiohttp.ClientResponse`
        The response of the failed HTTP request. This is an
        instance of :class:`aiohttp.ClientResponse`. In some cases
        this could also be a :class:`requests.Response`.
    text: :class:`str`
        The text of the error. Could be an empty string.
    status: :class:`int`
        The status code of the HTTP request.
    code: :class:`int`
        The Valorantx specific error code for the failure.
    """

    def __init__(self, response: ClientResponse, message: Optional[Union[str, Dict[str, Any]]]):
        self.response: ClientResponse = response
        self.status: int = response.status  # This attribute is filled by the library even if using requests # noqa: E501
        self.text: str
        if isinstance(message, dict):
            self.text = message.get('message') or message.get('error', '')
        else:
            self.text = message or ''

        fmt = '{0.status} {0.reason}'
        if len(self.text):
            fmt += ': {2}'

        super().__init__(fmt.format(self.response, self.text))


class BadRequest(HTTPException):
    """Exception that's raised for when status code 400 occurs.
    Subclass of :exc:`HTTPException`
    """

    pass


class Forbidden(HTTPException):
    """Exception that's raised for when status code 403 occurs.
    Subclass of :exc:`HTTPException`
    """

    pass


class NotFound(HTTPException):
    """Exception that's raised for when status code 404 occurs.
    Subclass of :exc:`HTTPException`
    """

    pass


class InternalServerError(HTTPException):
    """Exception that's raised for when status code 500 occurs.
    Subclass of :exc:`HTTPException`
    """

    pass


class RateLimited(HTTPException):
    """Exception that's raised for when a 429 status code occurs.
    Subclass of :exc:`HTTPException`.
    """

    pass

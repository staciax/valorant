"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

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


# source : https://github.com/Rapptz/discord.py/blob/master/discord/asset.py
from __future__ import annotations

import io
import os
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

import yarl

from . import utils
from .file import File

if TYPE_CHECKING:
    from typing_extensions import Self

    from .cache import CacheState

MISSING = utils.MISSING


class AssetMixin:
    __slots__ = ()
    url: str
    _state: CacheState

    async def read(self):
        """|coro|
        Retrieves the content of this asset as a :class:`bytes` object.
        Raises
        ------
        Exception
            There was no internal connection state.
        HTTPException
            Downloading the asset failed.
        NotFound
            The asset was deleted.
        Returns
        -------
        :class:`bytes`
            The content of the asset.
        """
        if self._state is None:
            raise ValueError('Asset has no client')

        return await self._state.http.read_from_url(self.url)

    async def save(self, fp: Union[str, bytes, os.PathLike[Any], io.BufferedIOBase], *, seek_begin: bool = True) -> int:
        """|coro|
        Saves this asset into a file-like object.
        Parameters
        ----------
        fp: Union[:class:`io.BufferedIOBase`, :class:`os.PathLike`]
            The file-like object to save this asset to or the filename
            to use. If a filename is passed then a file is created with that
            filename and used instead.
        seek_begin: :class:`bool`
            Whether to seek to the beginning of the file after saving is
            successfully done.
        Raises
        ------
        Exception
            There was no internal connection state.
        HTTPException
            Downloading the asset failed.
        NotFound
            The asset was deleted.
        Returns
        --------
        :class:`int`
            The number of bytes written.
        """
        data = await self.read()
        if isinstance(fp, io.BufferedIOBase):
            written = fp.write(data)
            if seek_begin:
                fp.seek(0)
            return written
        else:
            with open(fp, 'wb') as f:
                return f.write(data)

    async def to_file(self, *, filename: Optional[str] = MISSING) -> File:
        """|coro|
        Converts the asset into a :class:`File`
        Parameters
        -----------
        filename: Optional[:class:`str`]
            The filename of the file. If not provided, then the filename from
            the asset's URL is used.
        Raises
        ------
        Exception
            The asset does not have an associated state.
        ValueError
            The asset is a unicode emoji.
        TypeError
            The asset is a sticker with lottie type.
        HTTPException
            Downloading the asset failed.
        NotFound
            The asset was deleted.
        Returns
        -------
        :class:`File`
            The asset as a file suitable for sending.
        """
        data = await self.read()
        file_filename = filename if filename is not MISSING else yarl.URL(self.url).name
        return File(io.BytesIO(data), filename=file_filename)


class Asset(AssetMixin):

    """Represents a CDN asset on Valorant.
    .. container:: operations
        .. describe:: str(x)
            Returns the URL of the CDN asset.
        .. describe:: len(x)
            Returns the length of the CDN asset's URL.
        .. describe:: x == y
            Checks if the asset is equal to another asset.
        .. describe:: x != y
            Checks if the asset is not equal to another asset.
        .. describe:: hash(x)
            Returns the hash of the asset.
    """

    __slot__: Tuple[str, ...] = ('_client', '_url', '_video', '_animated')

    def __init__(self, state: CacheState, url: str, *, animated: bool = False, video: bool = False) -> None:
        self._state = state
        self._url = url
        self._video = video
        self._animated = animated

    @classmethod
    def _from_url(cls, state: CacheState, url: Optional[str] = None, *, animated: bool = False) -> Self:
        if url is None:
            raise TypeError('Expected URL, not NoneType')

        video = True if url.endswith('.mp4') else False
        if not animated and url.endswith('.gif'):
            animated = True
        return cls(state=state, url=url, animated=animated, video=video)

    def __str__(self) -> str:
        return str(self._url)

    def __len__(self) -> int:
        return len(self._url)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Asset) and self._url == other._url

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self._url)

    @property
    def url(self) -> str:
        """:class:`str`: Returns the underlying URL of the asset."""
        return self._url

    @property
    def animated(self) -> bool:
        """:class:`bool`: Returns whether the asset is animated."""
        return self._animated

    @property
    def video(self) -> bool:
        """:class:`bool`: Returns whether the asset is a video."""
        return self._video

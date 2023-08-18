from __future__ import annotations
import mimetypes
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING
from pywa import utils

if TYPE_CHECKING:
    from pywa.client import WhatsApp


@dataclass(frozen=True, slots=True, kw_only=True)
class MediaBase(ABC, utils.FromDict):
    """Base class for all media types."""

    _client: WhatsApp = field(repr=False, hash=False, compare=False)

    @property
    @abstractmethod
    def id(self) -> str: ...

    @property
    @abstractmethod
    def sha256(self) -> str: ...

    @property
    @abstractmethod
    def mime_type(self) -> str: ...

    def get_media_url(self) -> str:
        """Gets the URL of the media. (expires after 5 minutes)"""
        return self._client.get_media_url(media_id=self.id).url

    @property
    def extension(self) -> str | None:
        """Gets the extension of the media (with dot. eg: .jpg, .mp4, ...)"""
        return mimetypes.guess_extension(self.mime_type)

    def download(
            self,
            path: str | None = None,
            filename: str | None = None,
            in_memory: bool = False,
    ) -> bytes | str:
        """
        Download a media file from WhatsApp servers.
            - Same as :func:`~pywa.client.WhatsApp.download_media` with ``media_url=media.get_media_url()``

        >>> message.image.download()

        Args:
            path: The path where to save the file (if not provided, the current working directory will be used).
            filename: The name of the file (if not provided, it will be guessed from the URL + extension).
            in_memory: Whether to return the file as bytes instead of saving it to disk (default: False).

        Returns:
            The path of the saved file if ``in_memory`` is False, the file as bytes otherwise.
        """
        return self._client.download_media(
            url=self.get_media_url(),
            path=path,
            filename=filename,
            in_memory=in_memory
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class Image(MediaBase):
    """
    Represents an image.

    Attributes:
        id: The ID of the image.
        sha256: The SHA256 hash of the image.
        mime_type: The MIME type of the image.
    """
    id: str
    sha256: str
    mime_type: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Video(MediaBase):
    """
    Represents a video.

    Attributes:
        id: The ID of the video.
        sha256: The SHA256 hash of the video.
        mime_type: The MIME type of the video.
    """
    id: str
    sha256: str
    mime_type: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Sticker(MediaBase):
    """
    Represents a sticker.

    Attributes:
        id: The ID of the sticker.
        sha256: The SHA256 hash of the sticker.
        mime_type: The MIME type of the sticker.
        animated: Whether the sticker is animated.
    """
    id: str
    sha256: str
    mime_type: str
    animated: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class Document(MediaBase):
    """
    Represents a document.

    Attributes:
        id: The ID of the document.
        sha256: The SHA256 hash of the document.
        mime_type: The MIME type of the document.
        filename: The filename of the document (optional).
    """
    id: str
    sha256: str
    mime_type: str
    filename: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class Audio(MediaBase):
    """
    Represents an audio.

    Attributes:
        id: The ID of the audio.
        sha256: The SHA256 hash of the audio.
        mime_type: The MIME type of the audio.
        voice: Whether the audio is a voice message or just an audio file.
    """
    id: str
    sha256: str
    mime_type: str
    voice: bool


@dataclass(frozen=True, slots=True)
class MediaUrlResponse(utils.FromDict):
    """
    Represents a media response.

    Attributes:
        id: The ID of the media.
        url: The URL of the media (valid for 5 minutes).
        mime_type: The MIME type of the media.
        sha256: The SHA256 hash of the media.
        file_size: The size of the media in bytes.
    """
    _client: WhatsApp = field(repr=False, hash=False, compare=False)
    id: str
    url: str
    mime_type: str
    sha256: str
    file_size: int

    def download(
            self,
            filepath: str | None = None,
            filename: str | None = None,
            in_memory: bool = False,
    ) -> bytes | str:
        """
        Download a media file from WhatsApp servers.

        Args:
            filepath: The path where to save the file (if not provided, the current working directory will be used).
            filename: The name of the file (if not provided, it will be guessed from the URL + extension).
            in_memory: Whether to return the file as bytes instead of saving it to disk (default: False).

        Returns:
            The path of the saved file if ``in_memory`` is False, the file as bytes otherwise.
        """
        return self._client.download_media(url=self.url, path=filepath, filename=filename, in_memory=in_memory)


class CacheControl(utils.StrEnum):
    """
    The Cache-Control header tells us how to handle asset caching.
        - Used by :class:`~pywa.types.media.MediaUrlToCache`.

    Attributes:
        MAX_AGE: Indicates that the asset can be cached for a specific time (``max_age``).
        NO_CACHE: Indicates the asset can be cached but should be updated if the ``last_modified`` value is
            different from a previous response.
        NO_STORE: Indicates that the asset should not be cached.
        PRIVATE: Indicates that the asset is personalized for the recipient and should not be cached.
    """
    MAX_AGE = "max-age"
    NO_CACHE = "no-cache"
    NO_STORE = "no-store"
    PRIVATE = "private"


@dataclass(slots=True)
class MediaUrlToCache:
    """
    Represents a media url to cache.

    `Media HTTP Caching on developers.facebook.com <https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages#media-http-caching>`_

    Example:

        >>> media_url = MediaUrlToCache(
        ...     url="https://example.com/image.png",
        ...     cache_control=CacheControl.MAX_AGE,
        ...     max_age=604800
        ... )

        >>> media_url = MediaUrlToCache(
        ...     url="https://example.com/image.png",
        ...     cache_control=CacheControl.NO_CACHE,
        ...     last_modified=datetime.now()
        ... )

    Attributes:
        url: The media url.
        cache_control: The Cache-Control header tells us how to handle asset caching.
        max_age: When cache_control is ``max-age``, Indicates how many seconds (n) to cache the asset.
         WhatsApp will reuse the cached asset in subsequent messages until this time is exceeded, after which we will
         request the asset again, if needed.
        last_modified: When cache_control is ``no-cache``, Indicates when the asset was last modified.
        etag: When no cache control is provided, The ETag header is a unique string that identifies a specific version
            of an asset.
    """
    url: str
    cache_control: CacheControl | None = None
    max_age: int | None = None
    last_modified: datetime | None = None
    etag: str | None = None

    def __post_init__(self):
        """Validate the values."""
        if self.cache_control == CacheControl.MAX_AGE and not self.max_age:
            raise ValueError("`max_age` must be provided when cache_control is max-age.")
        if self.cache_control == CacheControl.NO_CACHE and not self.last_modified:
            raise ValueError("`last_modified` must be provided when cache_control is no-cache.")
        if not self.cache_control and not self.etag:
            raise ValueError("`etag` must be provided when cache_control is not provided.")

    def to_headers(self):
        """Get the media url to cache as headers."""
        headers = {}
        if self.cache_control == CacheControl.MAX_AGE:
            headers["Cache-Control"] = self.cache_control.value + f"={self.max_age}"
        elif self.cache_control == CacheControl.NO_CACHE:
            headers["Cache-Control"] = self.cache_control.value
            headers["Last-Modified"] = self.last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
        elif self.cache_control in (CacheControl.NO_STORE, CacheControl.PRIVATE):
            headers["Cache-Control"] = self.cache_control.value
        else:
            headers["ETag"] = self.etag
        return headers

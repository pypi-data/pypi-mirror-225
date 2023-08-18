import pathlib
import math
from threading import Thread, Semaphore
from typing import Generator, Optional, Iterable
from queue import Queue
from requests.models import Response
from gp_wrapper.objects.core.gp import GooglePhotos
from gp_wrapper.objects.core.media_item.core_media_item import CoreMediaItem
from gp_wrapper.objects.core.media_item.filters import SearchFilter
from gp_wrapper.utils import NextPageToken, Path
from .core import GooglePhotos, CoreMediaItem, MEDIA_ITEM_LIST_DEFAULT_PAGE_SIZE,\
    MEDIA_ITEM_LIST_MAXIMUM_PAGE_SIZE, MEDIA_ITEM_BATCH_CREATE_MAXIMUM_IDS
from ..utils import MediaItemMaskTypes, NewMediaItem, SimpleMediaItem


class MediaItem(CoreMediaItem):
    """The advanced wrapper class over the 'MediaItem' object

    Args:
        gp (GooglePhotos): Google Photos object
        id (MediaItemID): the id of the MediaItem
        productUrl (str): the utl to view this item in the browser
        mimeType (str): the type of the media
        mediaMetadata (dict | MediaMetadata): metadata
        filename (str): name of media
        baseUrl (str, optional): ?. Defaults to "".
        description (str, optional): media's description. Defaults to "".
    """
    # ================================= STATIC HELPER METHODS =================================

    @staticmethod
    def _from_core(c: CoreMediaItem) -> "MediaItem":
        return MediaItem(**c.__dict__)

    # ================================= ADDITIONAL STATIC METHODS =================================

    @staticmethod
    def from_dict(gp: GooglePhotos, dct: dict) -> "MediaItem":
        return MediaItem._from_core(MediaItem._from_dict(gp, dct))

    @staticmethod
    def search_all(
        gp: GooglePhotos,
        albumId: str | None = None,
        pageSize: int = 25,
        filters: SearchFilter | None = None,
        orderBy: str | None = None,
        tokens_to_use: int = math.inf,  # type:ignore
        pre_fetch: bool = False
    ) -> Generator["MediaItem", None, None]:
        """like CoreGPMediaItem.search but automatically converts the objects to the
        higher order class and automatically uses the tokens to get all objects

        Additional Args:
            tokens_to_use (int): how many times to use the token automatically to fetch the next batch.
                Defaults to using all tokens.
            pre_fetch (Boolean): whether to non-blocking-ly fetch ALL available items using the tokens
                Defaults to False.
        """
        q: Queue[MediaItem] = Queue()
        sem = Semaphore(0)
        if not (0 < tokens_to_use):
            raise ValueError(
                "'tokens_to_use' should be a positive integer")

        def inner_logic(blocking: bool = True) -> Optional[Generator]:
            nonlocal tokens_to_use
            core_gen, pageToken = CoreMediaItem.search(
                gp, albumId, pageSize, None, filters, orderBy)
            tokens_to_use -= 1
            for o in (MediaItem._from_core(o) for o in core_gen):
                if blocking:
                    yield o
                else:
                    q.put(o)
                sem.release()
            while pageToken and tokens_to_use > 0:
                core_gen, pageToken = CoreMediaItem.search(
                    gp, albumId, pageSize, pageToken, filters, orderBy)
                tokens_to_use -= 1
                for o in (MediaItem._from_core(o) for o in core_gen):
                    if blocking:
                        yield o
                    else:
                        q.put(o)
                    sem.release()
        if pre_fetch:
            # TODO fix this part
            raise NotImplementedError("pre_fetch is currently not supported")
            t = Thread(target=inner_logic, args=(False,))
            t.start()
            with sem:
                # re-add value that was used as a barrier
                sem.release()
                while not q.empty():
                    with sem:
                        yield q.get()
        else:
            yield from inner_logic()  # type:ignore

    @staticmethod
    def all_media(gp: GooglePhotos) -> Generator["MediaItem", None, None]:
        lst, token = MediaItem.list(
            gp, MEDIA_ITEM_LIST_MAXIMUM_PAGE_SIZE, None)
        yield from lst
        while token:
            lst, token = MediaItem.list(
                gp, MEDIA_ITEM_LIST_MAXIMUM_PAGE_SIZE, token)
            yield from lst

    @staticmethod
    def add_to_library(gp: GooglePhotos, paths: Iterable[Path]) -> list[Optional["MediaItem"]]:
        items: list[NewMediaItem] = []
        for path in paths:
            token = MediaItem.upload_media(gp, path)
            filename = pathlib.Path(path).stem
            item = NewMediaItem("", SimpleMediaItem(token, filename))
            items.append(item)
        batches: list[list[NewMediaItem]] = []
        batch: list[NewMediaItem] = []
        for item in items:
            if len(batch) >= MEDIA_ITEM_BATCH_CREATE_MAXIMUM_IDS:
                batches.append(batch)
                batch = []
            batch.append(item)
        batches.append(batch)
        res = []
        for batch in batches:
            res.extend(
                [item.mediaItem for item in MediaItem.batchCreate(gp, batch)])
        return res

    # ================================= OVERRIDDEN INSTANCE METHODS =================================

    @staticmethod
    def list(  # type:ignore
        gp: GooglePhotos,
        pageSize: int = MEDIA_ITEM_LIST_DEFAULT_PAGE_SIZE,
        pageToken: Optional[str] = None
    ) -> tuple[list["MediaItem"], NextPageToken | None]:
        lst, token = CoreMediaItem.list(gp, pageSize, pageToken)
        return [MediaItem._from_core(o) for o in lst], token
    # ================================= ADDITIONAL INSTANCE METHODS =================================

    def set_description(self, description: str) -> Response:
        return self.patch(MediaItemMaskTypes.DESCRIPTION, description)


__all__ = [
    "MediaItem",
    "MediaItemMaskTypes"
]

import typing as T
from multiprocessing.pool import ThreadPool
from pydantic import BaseModel
import strawberry
from enum import Enum


class VerticalAlign(str, Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class Image(BaseModel):
    height: int
    width: int
    url: str
    public_cloudinary_id: str
    vertical_align: VerticalAlign | None = None

    @classmethod
    def from_url_or_bytes(cls, url_or_bytes: T.Union[str, bytes]) -> "Image":
        from quilt.vendors import Cloudinary

        cloudinary_image = Cloudinary.upload_image(url_or_bytes)
        return cls(
            height=cloudinary_image.height,
            width=cloudinary_image.width,
            url=cloudinary_image.secure_url,
            public_cloudinary_id=cloudinary_image.public_id,
        )

    @classmethod
    def from_url_or_bytes_lst(
        cls, url_or_bytes_lst: T.List[T.Union[str, bytes]]
    ) -> T.List["Image"]:
        pool = ThreadPool(processes=5)
        results = []
        for i in url_or_bytes_lst:
            results.append(pool.apply_async(cls.from_url_or_bytes, (i,)))
        return [result.get() for result in results]


strawberry.enum(VerticalAlign)


@strawberry.experimental.pydantic.type(model=Image, name="Image", all_fields=True)
class ImageStraw:
    pass


@strawberry.experimental.pydantic.input(model=Image, name="ImageInput", all_fields=True)
class ImageStrawInput:
    pass


class SmallImage(BaseModel):
    url: str
    public_cloudinary_id: T.Optional[str] = None
    height: T.Optional[int] = None
    width: T.Optional[int] = None


@strawberry.experimental.pydantic.type(
    model=SmallImage, name="SmallImage", all_fields=True
)
class SmallImageStraw:
    pass

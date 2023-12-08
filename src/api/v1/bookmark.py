import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_user_id
from src.api.paginator import PaginationSchema
from src.repos.bookmark_repo import BookmarkRepo, get_bookmark_repo
from src.repos.errors import BookmarkAlreadyExistsError, BookmarkNotFoundError
from src.schemas.bookmark_schema import BookmarkAddSchema, BookmarkCreatedSchema, BookmarkSchema

router = APIRouter(tags=["Bookmark"], dependencies=[Depends(get_user_id)])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[BookmarkSchema],
)
async def get_list(
    repo: BookmarkRepo = Depends(get_bookmark_repo),
    pagination: PaginationSchema = Depends(),
) -> list[BookmarkSchema]:
    bookmark_list = await repo.get_list(pagination.limit, pagination.offset)

    return [BookmarkSchema(**i.model_dump()) for i in bookmark_list]


@router.get(
    "/user/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=list[BookmarkSchema],
)
async def get_list_by_user_id(
    user_id: uuid.UUID,
    repo: BookmarkRepo = Depends(get_bookmark_repo),
    pagination: PaginationSchema = Depends(),
) -> list[BookmarkSchema]:
    bookmark_list = await repo.get_list_by_user_id(
        user_id=user_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    return [BookmarkSchema(**i.model_dump()) for i in bookmark_list]


@router.get(
    "/{bookmark_id}/",
    status_code=status.HTTP_200_OK,
    response_model=BookmarkSchema,
)
async def get(
    bookmark_id: uuid.UUID,
    repo: BookmarkRepo = Depends(get_bookmark_repo),
) -> BookmarkSchema:
    try:
        bookmark = await repo.get(bookmark_id)
    except BookmarkNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return BookmarkSchema(**bookmark.model_dump())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookmarkCreatedSchema,
)
async def add(
    bookmark_schema: BookmarkAddSchema,
    user_id: uuid.UUID = Depends(get_user_id),
    repo: BookmarkRepo = Depends(get_bookmark_repo),
) -> BookmarkCreatedSchema:
    try:
        id_ = await repo.add(
            film_id=bookmark_schema.film_id,
            user_id=user_id,
        )
    except BookmarkAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return BookmarkCreatedSchema(id=id_)


@router.delete(
    "/{bookmark_id}/",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
async def delete(
    bookmark_id: uuid.UUID,
    repo: BookmarkRepo = Depends(get_bookmark_repo),
) -> Response:
    try:
        await repo.delete(bookmark_id)
    except BookmarkNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_200_OK)

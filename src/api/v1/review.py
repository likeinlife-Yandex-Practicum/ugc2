import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_user_id
from src.api.paginator import PaginationSchema
from src.repos.errors import ReviewAlreadyExistsError, ReviewNotFoundError
from src.repos.review_repo import ReviewRepo, get_review_repo
from src.schemas.review_schema import ReviewAddSchema, ReviewCreatedSchema, ReviewSchema, ReviewUpdateSchema

router = APIRouter(tags=["Review"], dependencies=[Depends(get_user_id)])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewSchema],
)
async def get_list(
    repo: ReviewRepo = Depends(get_review_repo),
    pagination: PaginationSchema = Depends(),
) -> list[ReviewSchema]:
    review_list = await repo.get_list(pagination.limit, pagination.offset)

    return [ReviewSchema(**i.model_dump()) for i in review_list]


@router.get(
    "/{review_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ReviewSchema,
)
async def get(
    review_id: uuid.UUID,
    repo: ReviewRepo = Depends(get_review_repo),
) -> ReviewSchema:
    try:
        review = await repo.get(review_id)
    except ReviewNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ReviewSchema(**review.model_dump())


@router.get(
    "/film/{film_id}/",
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewSchema],
)
async def get_by_film_id(
    film_id: uuid.UUID,
    repo: ReviewRepo = Depends(get_review_repo),
    pagination: PaginationSchema = Depends(),
) -> list[ReviewSchema]:
    review_list = await repo.get_list_by_film_id(
        film_id=film_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    return [ReviewSchema(**i.model_dump()) for i in review_list]


@router.get(
    "/user/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewSchema],
)
async def get_by_user_id(
    user_id: uuid.UUID,
    repo: ReviewRepo = Depends(get_review_repo),
    pagination: PaginationSchema = Depends(),
) -> list[ReviewSchema]:
    review_list = await repo.get_list_by_user_id(
        user_id=user_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    return [ReviewSchema(**i.model_dump()) for i in review_list]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewCreatedSchema,
)
async def add(
    review_schema: ReviewAddSchema,
    user_id: uuid.UUID = Depends(get_user_id),
    repo: ReviewRepo = Depends(get_review_repo),
) -> ReviewCreatedSchema:
    try:
        id_ = await repo.add(
            score=review_schema.score,
            review_string=review_schema.review,
            film_id=review_schema.film_id,
            user_id=user_id,
        )
    except ReviewAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ReviewCreatedSchema(id=id_)


@router.delete(
    "/{review_id}/",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
async def delete(
    review_id: uuid.UUID,
    repo: ReviewRepo = Depends(get_review_repo),
) -> Response:
    try:
        await repo.delete(review_id)
    except ReviewNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_200_OK)


@router.patch(
    "/{review_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ReviewSchema,
)
async def update(
    review_id: uuid.UUID,
    review_schema: ReviewUpdateSchema = Depends(),
    repo: ReviewRepo = Depends(get_review_repo),
) -> ReviewSchema:
    try:
        review = await repo.update(
            id_=review_id,
            score=review_schema.score,
            review_string=review_schema.review,
        )
    except ReviewNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ReviewSchema(**review.model_dump())

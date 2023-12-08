import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_user_id
from src.api.paginator import PaginationSchema
from src.repos.appraisal_repo import AppraisalRepo, get_appraisal_repo
from src.repos.errors import AppraisalAlreadyExistsError, AppraisalNotFoundError, ReviewNotFoundError
from src.schemas.appraisal_schema import (
    AppraisalAddSchema,
    AppraisalSchema,
    AppraisalUpdateSchema,
    ReviewAppraisalSchema,
)

router = APIRouter(tags=["Appraisal"], dependencies=[Depends(get_user_id)])


@router.get(
    "/{review_id}/",
    status_code=status.HTTP_200_OK,
    response_model=list[AppraisalSchema],
)
async def get_by_review_id(
    review_id: uuid.UUID,
    pagination: PaginationSchema = Depends(),
    repo: AppraisalRepo = Depends(get_appraisal_repo),
) -> list[AppraisalSchema]:
    try:
        appraisal_list = await repo.get_by_review_id(
            review_id=review_id,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    except ReviewNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [ReviewAppraisalSchema(**i.model_dump()).appraisal for i in appraisal_list]


@router.get(
    "/user/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewAppraisalSchema],
)
async def get_by_user_id(
    user_id: uuid.UUID,
    pagination: PaginationSchema = Depends(),
    repo: AppraisalRepo = Depends(get_appraisal_repo),
) -> list[ReviewAppraisalSchema]:
    try:
        appraisal_list = await repo.get_by_user_id(
            user_id=user_id,
            limit=pagination.limit,
            offset=pagination.offset,
        )
    except ReviewNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return [ReviewAppraisalSchema(**i.model_dump()) for i in appraisal_list]


@router.post(
    "/{review_id}/",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def add(
    appraisal_schema: AppraisalAddSchema,
    review_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_user_id),
    repo: AppraisalRepo = Depends(get_appraisal_repo),
) -> Response:
    try:
        await repo.add(
            review_id=review_id,
            score=appraisal_schema.score,
            user_id=user_id,
        )
    except AppraisalAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    except ReviewNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/{review_id}/",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
async def delete(
    review_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_user_id),
    repo: AppraisalRepo = Depends(get_appraisal_repo),
) -> Response:
    try:
        await repo.delete(review_id, user_id)
    except AppraisalNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_200_OK)


@router.patch(
    "/{review_id}/",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
async def update(
    review_id: uuid.UUID,
    appraisal_schema: AppraisalUpdateSchema,
    user_id: uuid.UUID = Depends(get_user_id),
    repo: AppraisalRepo = Depends(get_appraisal_repo),
) -> Response:
    try:
        await repo.update(
            user_id=user_id,
            review_id=review_id,
            score=appraisal_schema.score,
        )
    except AppraisalNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_200_OK)

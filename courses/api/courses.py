from typing import List

from fastapi import APIRouter, Depends, Response, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from courses.schema.courses import CreateCourse, DefaultCourse, UpdateCourse, AuthenticationRequired
from database import get_session
from models import Course
from users.authentications.authenticators import is_user_authenticated
from users.schemas.users import DefaultUser

courses_router = APIRouter(prefix="/courses")


@courses_router.get('/', tags=['courses'], response_model=List[DefaultCourse])
async def get_courses_view(
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    return await Course.filter(session, user_id=user.id)


@courses_router.post('/', tags=['courses'], response_model=DefaultCourse)
async def create_course_view(
        course: CreateCourse,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    return await Course.create(session, user_id=user.id, **course.dict())


@courses_router.get('/{course_id}/', tags=['courses'], response_model=DefaultCourse)
async def get_course_view(
        course_id: int,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    return await Course.get(session, id=course_id, user_id=user.id)


@courses_router.patch('/{course_id}/', tags=['courses'], response_model=DefaultCourse)
async def update_course_view(
        course_id: int,
        update_course: UpdateCourse,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    course = await Course.get(session, id=course_id, user_id=user.id)
    if course is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await course.update(session, entity_id=course_id, **update_course.dict(exclude_unset=True))
    return course


@courses_router.delete('/{course_id}/', tags=['courses'])
async def delete_course_view(
        course_id: int,
        session: AsyncSession = Depends(get_session),
        user: DefaultUser = Depends(is_user_authenticated)
):
    await Course.delete(session, id=course_id, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@courses_router.post('/token-required/', tags=['courses'])
async def authorization_required(
        authentication_required: AuthenticationRequired,
        user: DefaultUser = Depends(is_user_authenticated),
):
    if user.email == authentication_required.email:
        return {'success': 'yes', 'message': 'Hello! You are successfully authorized'}

    return {'success': 'no', 'message': 'Email is not valid'}


@courses_router.post('/send-file/', tags=['courses'])
async def send_file(file: UploadFile, user: DefaultUser = Depends(is_user_authenticated)):
    return {'filename': file.filename}


@courses_router.post('/send-file/test/', tags=['courses'])
async def send_file_test(file: UploadFile, user: DefaultUser = Depends(is_user_authenticated)):
    if file.filename != 'hello.png':
        return {'success': 'no', 'message': f'Your file "{file.file}" is not valid'}

    return {'success': 'yes', 'message': 'Your file successfully accepted!'}

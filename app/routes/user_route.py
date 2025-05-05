from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import JSONResponse

from app.dependecies.user import get_user_service
from app.schemas import UserCreate, UserResponse
from app.services.user_service import UserService

app = FastAPI()
router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    request: UserCreate, user_service: UserService = Depends()
):
    """
    Creates a new user in the database.

    This endpoint accepts a JSON payload in the shape of the UserCreate schema
    and creates a new user in the database.

    Args:
        request (UserCreate): The JSON payload containing the user to create.
        user_service (UserService, optional): The user service dependency for handling user operations.

    Returns:
        dict: A response containing a success message.
    """
    
    await user_service.create_user(request)
    return {"message": "User created successfully!"}


@router.get("/users/{id}", response_model=UserResponse, status_code=200)
async def get_user_by_id(
    id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Retrieves a user by their ID.

    This endpoint accepts a user ID and returns a JSONResponse with the user data.

    Args:
        id (str): The ID of the user to retrieve.
        user_service (UserService, optional): The user service dependency for handling user operations.

    Returns:
        UserResponse: The response model containing the user data.
    """
    user = await user_service.get_user_by_id(id)

    return JSONResponse(content=user)

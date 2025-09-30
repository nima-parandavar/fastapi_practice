from fastapi import HTTPException, status


class User:
    not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

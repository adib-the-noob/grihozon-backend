from rest_framework.response import Response
from rest_framework import status


class APIResponse(Response):
    def __init__(
        self,
        *,
        success: bool = True,
        message: str = "",
        data=None,
        errors=None,
        status_code=status.HTTP_200_OK,
        meta: dict | None = None,
        headers=None
    ):
        payload = {
            "success": success,
            "message": message,
            "data": data,
            "errors": errors,
            "meta": meta,
        }
        super().__init__(payload, status=status_code, headers=headers)

    @classmethod
    def success(
        cls,
        *,
        data=None,
        message="OK",
        meta=None,
        status_code=status.HTTP_200_OK,
        headers=None
    ):
        return cls(
            success=True,
            message=message,
            data=data,
            meta=meta,
            status_code=status_code,
            headers=headers,
        )

    @classmethod
    def error(
        cls,
        *,
        message="Error",
        errors=None,
        meta=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        headers=None
    ):
        return cls(
            success=False,
            message=message,
            errors=errors,
            meta=meta,
            status_code=status_code,
            headers=headers,
        )




from fastapi import FastAPI, HTTPException, Request, Response,status
from fastapi.responses import JSONResponse


class ShippinError(Exception):
    """Base class for all exceptions in Shippin API."""
    status=status.HTTP_400_BAD_REQUEST

class EntityNotFoundError(ShippinError):
    """Entity not found in database"""
    status=status.HTTP_404_NOT_FOUND
    
class ClientNotAuthorizedError(ShippinError):
    """Client is not authorized to perform the requested action"""
    status=status.HTTP_401_UNAUTHORIZED

class ClientNotVerifiedError(ShippinError):
    """Client is not verified"""
    status=status.HTTP_403_FORBIDDEN

class BadCredentialsError(ShippinError):
    """Invalid user email or password"""
    status=status.HTTP_401_UNAUTHORIZED

class InvalidTokenError(ShippinError):
    """Access token is invalid or expired"""
    status=status.HTTP_401_UNAUTHORIZED

class DeliveryPartnerNotAvailableError(ShippinError):
    """No delivery partner is available for assignment"""
    status=status.HTTP_503_SERVICE_UNAVAILABLE

class NothingToUpdateError(ShippinError):
    """No data provided to update"""

def _get_exception_handler(status:int, detail:str):
    def handler(request:Request, exception:Exception)->Response:
        raise HTTPException(
            status_code=status,
            detail=detail
        )
    return handler


def add_exception_handlers(app:FastAPI):
    for exception_class in ShippinError.__subclasses__():
        app.add_exception_handler(
            exception_class,
            _get_exception_handler(exception_class.status, exception_class.__doc__ or "An error occurred"),
        )

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    def internal_server_exception_handler(request:Request, exception:HTTPException)->Response:
        return JSONResponse(
            content={"detail":"Something went wrong on the server."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={"X-Error":f"{exception}"},

        )

    
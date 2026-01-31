# from fastapi import Request
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
#
#
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     # You can customize the body however you like
#     return JSONResponse(
#         status_code=400,
#         content={
#             "detail": [".".join(e["loc"]) + ": " + e["msg"] for e in exc.errors()],
#             "body": exc.body,
#             "message": "Bad Request",
#         },
#     )
#
#
# async def not_found_exception_handler(
#         request: Request,
#         exc: RequestValidationError
# ):
#     # You can customize the body however you like
#     return JSONResponse(
#         status_code=404,
#         content={
#             "detail": str(exc),
#             "message": "De door u gevraagde resource kon niet gevonden worden."
#         },
#     )
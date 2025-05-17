from sanic import Blueprint

from sanic_ext import render
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.models import *

# from app.services.user import UserService

bp = Blueprint("main", url_prefix="/")
# user_service = UserService()


@bp.route("/", methods=["GET"])
async def index(request):
    return await render("index.html", context={})

"""Main routes for podcaster project"""

from sanic import Blueprint, response
from sanic_ext import render
from tortoise.exceptions import DoesNotExist, IntegrityError
from datetime import datetime

from app.models import Category, CategoryIdentification, Source, Podcast
from app.services import (
    CategoryService,
    CategoryIdentificationService,
    SourceService,
    PodcastService,
)
from app.utils.helpers import inject_template_context as inj

bp = Blueprint("main", url_prefix="/")


@bp.route("/", methods=["GET"])
async def index(request):
    """Render index page"""
    recent_podcasts = await PodcastService.get_recent(limit=25)
    podcasts_count = await PodcastService.count()
    categories_count = await CategoryService.count()
    channels_count = await SourceService.count()
    return await render(
        "index.html",
        context=inj(
            {
                "podcasts": recent_podcasts,
                "categories_count": categories_count,
                "podcasts_count": podcasts_count,
                "channels_count": channels_count,
            }
        ),
    )


# Category routes
@bp.route("/categories", methods=["GET"])
async def categories_list(request):
    """Render categories list"""
    categories = await CategoryService.get_all()
    return await render("categories/list.html", context=inj({"categories": categories}))


@bp.route("/categories", methods=["POST"])
async def categories_create(request):
    """Create new category"""
    name = request.form.get("name")

    if not name:
        return response.text("Category name is required", status=400)

    try:
        category = await CategoryService.create(name=name)
        # If it's an HTMX request, return just the new row
        if request.headers.get("HX-Request"):
            return await render("categories/row.html", context={"category": category})
        return response.redirect("/categories")
    except IntegrityError:
        return response.text("Category with this name already exists", status=400)


@bp.route("/categories/<category_id:int>", methods=["GET"])
async def categories_detail(request, category_id):
    """Render category detail"""
    category = await CategoryService.get_by_id(category_id)

    if not category:
        return response.redirect("/categories")

    identifications = await CategoryIdentificationService.get_by_category(category_id)

    return await render(
        "categories/detail.html",
        context={"category": category, "identifications": identifications},
    )


@bp.route("/categories/<category_id:int>", methods=["POST"])
async def categories_update(request, category_id):
    """Update category"""
    category = await CategoryService.get_by_id(category_id)

    if not category:
        if request.headers.get("HX-Request"):
            return response.text("Category not found", status=404)
        return response.redirect("/categories")

    name = request.form.get("name")

    if not name:
        if request.headers.get("HX-Request"):
            return response.text("Category name is required", status=400)
        return response.redirect(f"/categories/{category_id}/edit")

    try:
        updated_category = await CategoryService.update(id=category_id, name=name)

        # If it's an HTMX request, return just the updated row
        if request.headers.get("HX-Request"):
            return await render(
                "categories/row.html", context={"category": updated_category}
            )

        return response.redirect(f"/categories/{category_id}")
    except IntegrityError:
        if request.headers.get("HX-Request"):
            return response.text("Category with this name already exists", status=400)
        return response.redirect(f"/categories/{category_id}/edit")


@bp.route("/categories/<category_id:int>/delete", methods=["POST"])
async def categories_delete(request, category_id):
    """Delete category"""
    success = await CategoryService.delete(category_id)

    if request.headers.get("HX-Request"):
        if success:
            return response.text("")
        return response.text("Category not found", status=404)

    return response.redirect("/categories")


# Category Identification routes
@bp.route("/identifications", methods=["GET"])
async def identifications_list(request):
    """Render identifications list"""
    identifications = await CategoryIdentificationService.get_all()
    categories = await CategoryService.get_all()
    return await render(
        "identifications/list.html",
        context=inj({"identifications": identifications, "categories": categories}),
    )


@bp.route("/identifications", methods=["POST"])
async def identifications_create(request):
    """Create new identification"""
    name = request.form.get("name")
    category_id = request.form.get("category_id")

    if not name or not category_id:
        return response.text("All fields are required", status=400)

    try:
        identification = await CategoryIdentificationService.create(
            name=name, category_id=int(category_id)
        )

        # For HTMX requests, return just the new row
        if request.headers.get("HX-Request"):
            # Get all categories for the select dropdown in edit mode
            categories = await CategoryService.get_all()
            return await render(
                "identifications/row.html",
                context=inj(
                    {"identification": identification, "categories": categories}
                ),
            )

        return response.redirect("/identifications")
    except IntegrityError:
        return response.text(
            "An error occurred while creating the identification", status=400
        )


@bp.route("/identifications/<identification_id:int>", methods=["POST"])
async def identifications_update(request, identification_id):
    """Update identification"""
    identification = await CategoryIdentificationService.get_by_id(identification_id)

    if not identification:
        if request.headers.get("HX-Request"):
            return response.text("Identification not found", status=404)
        return response.redirect("/identifications")

    name = request.form.get("name")
    category_id = request.form.get("category_id")

    if not name or not category_id:
        if request.headers.get("HX-Request"):
            return response.text("All fields are required", status=400)
        return response.redirect("/identifications")

    updated_identification = await CategoryIdentificationService.update(
        id=identification_id, name=name, category_id=int(category_id)
    )

    if request.headers.get("HX-Request"):
        # Get all categories for the select dropdown in edit mode
        categories = await CategoryService.get_all()
        return await render(
            "identifications/row.html",
            context={
                "identification": updated_identification,
                "categories": categories,
            },
        )

    return response.redirect("/identifications")


@bp.route("/identifications/<identification_id:int>/delete", methods=["POST"])
async def identifications_delete(request, identification_id):
    """Delete identification"""
    success = await CategoryIdentificationService.delete(identification_id)

    if request.headers.get("HX-Request"):
        if success:
            return response.text("")
        return response.text("Identification not found", status=404)

    return response.redirect("/identifications")


# Source routes
@bp.route("/sources", methods=["GET"])
async def sources_list(request):
    """Render sources list"""
    sources = await SourceService.get_all()
    return await render("sources/list.html", context=inj({"sources": sources}))


@bp.route("/sources", methods=["POST"])
async def sources_create(request):
    """Create new source"""
    url = request.form.get("url")
    name = request.form.get("name")
    tg_channel = request.form.get("tg_channel")

    only_related = request.form.get("only_related")

    if not url or not name:
        return response.text("All fields are required", status=400)

    source = await SourceService.create(url=url, name=name, only_related=only_related)

    if not source:
        return response.text("Source with this URL already exists", status=400)

    if request.headers.get("HX-Request"):
        return await render("sources/row.html", context={"source": source})

    return response.redirect("/sources")


@bp.route("/sources/<source_id:int>/delete", methods=["POST"])
async def sources_delete(request, source_id):
    """Delete source"""
    success = await SourceService.delete(source_id)

    if request.headers.get("HX-Request"):
        if success:
            return response.text("")
        return response.text("Source not found"), 404

    return response.redirect("/sources")


# Podcast routes
@bp.route("/podcasts", methods=["GET"])
async def podcasts_list(request):
    """Render podcasts list"""
    podcasts = await PodcastService.get_all()
    return await render("podcasts/list.html", context=inj({"podcasts": podcasts}))


@bp.route("/podcasts/activate/<podcast_id:int>", methods=["GET"])
async def podcasts_activate(request, podcast_id):
    """Render podcast detail"""
    podcast = await PodcastService.get_by_id(podcast_id)
    if not podcast:
        return response.redirect("/podcasts")

    await PodcastService.activate(id=podcast.id)

    return await render("podcasts/activated.html", context={"p": podcast})


@bp.route("/podcasts/deactivate/<podcast_id:int>", methods=["GET"])
async def podcasts_deactivate(request, podcast_id):
    """Render podcast detail"""
    podcast = await PodcastService.get_by_id(podcast_id)
    if not podcast:
        return response.redirect("/podcasts")
    await PodcastService.deactivate(id=podcast.id)

    return await render("podcasts/deactivated.html", context={"p": podcast})


@bp.route("/podcasts/<podcast_id:int>/delete", methods=["POST"])
async def podcasts_delete(request, podcast_id):
    """Delete podcast"""
    success = await PodcastService.delete(podcast_id)

    if request.headers.get("HX-Request"):
        if success:
            return response.text("")
        return response.text("Podcast not found"), 404

    return response.redirect("/podcasts")

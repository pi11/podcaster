"""Services for podcaster project"""

import traceback
from datetime import datetime, timedelta

from typing import List, Optional, Dict, Any
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.models import Category, CategoryIdentification, Source, Podcast, TgChannel

PUBLICATION_SPEED = 60 * 4  # 4 hourse


class CategoryService:
    """Service for category operations"""

    @staticmethod
    async def get_all() -> List[Category]:
        """Get all categories"""
        return await Category.all().prefetch_related("identifications")

    @staticmethod
    async def count() -> int:
        """Get categories count"""
        return await Category.all().count()

    @staticmethod
    async def get_by_id(id: int) -> Optional[Category]:
        """Get category by id"""
        try:
            return await Category.get(id=id).prefetch_related("identifications")
        except DoesNotExist:
            return None

    @staticmethod
    async def create(name: str) -> Category:
        """Create new category"""
        return await Category.create(name=name)

    @staticmethod
    async def update(id: int, name: str) -> Optional[Category]:
        """Update category"""
        try:
            category = await Category.get(id=id)
            category.name = name
            await category.save()
            return category
        except DoesNotExist:
            return None

    @staticmethod
    async def delete(id: int) -> bool:
        """Delete category"""
        try:
            category = await Category.get(id=id)
            await category.delete()
            return True
        except DoesNotExist:
            return False


class CategoryIdentificationService:
    """Service for category identification operations"""

    @staticmethod
    async def get_all() -> List[CategoryIdentification]:
        """Get all category identifications"""
        return await CategoryIdentification.all().prefetch_related("category")

    @staticmethod
    async def get_by_id(id: int) -> Optional[CategoryIdentification]:
        """Get category identification by id"""
        try:
            return await CategoryIdentification.get(id=id).prefetch_related("category")
        except DoesNotExist:
            return None

    @staticmethod
    async def get_by_category(category_id: int) -> List[CategoryIdentification]:
        """Get category identifications by category id"""
        return await CategoryIdentification.filter(category_id=category_id)

    @staticmethod
    async def create(name: str, category_id: int) -> CategoryIdentification:
        """Create new category identification"""
        return await CategoryIdentification.create(name=name, category_id=category_id)

    @staticmethod
    async def update(
        id: int, name: str, category_id: int
    ) -> Optional[CategoryIdentification]:
        """Update category identification"""
        try:
            identification = await CategoryIdentification.get(id=id)
            identification.name = name
            identification.category_id = category_id
            await identification.save()
            return identification
        except DoesNotExist:
            return None

    @staticmethod
    async def delete(id: int) -> bool:
        """Delete category identification"""
        try:
            identification = await CategoryIdentification.get(id=id)
            await identification.delete()
            return True
        except DoesNotExist:
            return False


class SourceService:
    """Service for source operations"""

    @staticmethod
    async def get_all() -> List[Source]:
        """Get all sources"""
        return await Source.all()

    @staticmethod
    async def count() -> int:
        """Get channels count"""
        return await Source.all().count()

    @staticmethod
    async def get_by_id(id: int) -> Optional[Source]:
        """Get source by id"""
        try:
            return await Source.get(id=id)
        except DoesNotExist:
            return None

    @staticmethod
    async def create(url: str, name: str, only_related: bool = False) -> Source:
        """Create new source"""
        try:
            return await Source.create(url=url, name=name, only_related=only_related)
        except IntegrityError:
            # Handle duplicate URL
            return None

    @staticmethod
    async def update(id: int, url: str, name: str) -> Optional[Source]:
        """Update source"""
        try:
            source = await Source.get(id=id)
            source.url = url
            source.name = name
            await source.save()
            return source
        except DoesNotExist:
            return None
        except IntegrityError:
            # Handle duplicate URL
            return None

    @staticmethod
    async def delete(id: int) -> bool:
        """Delete source"""
        try:
            source = await Source.get(id=id)
            await source.delete()
            return True
        except DoesNotExist:
            return False


class PodcastService:
    """Service for podcast operations"""

    @staticmethod
    async def get_all() -> List[Podcast]:
        """Get all podcasts"""
        return await Podcast.all().prefetch_related("source")

    @staticmethod
    async def get_good() -> List[Podcast]:
        """Get podcasts ready for posting"""
        return (
            await Podcast.filter(is_active=True, is_posted=False, is_processed=True)
            .order_by("publication_date")
            .first()
        )

    @staticmethod
    async def check_theme(id: int) -> bool:
        """Check if podcast has related themes
        and disable if no
        returns False if podcast is not suitable"""
        podcast = await Podcast.get(id=id)
        check_str = f"{podcast.name} {podcast.description}"
        cats = await CategoryService.get_all()
        good = False
        for cat in cats:
            _ = cat.name.lower()
            if _ in check_str:
                await podcast.categories.add(cat)
                print(f"Added cat {cat} to {podcast.name}")
                good = True
        podcast.is_active = good
        await podcast.save()
        return good

    @staticmethod
    async def add_categories(id: int) -> None:
        """Add corresponding categories to podcast"""
        podcast = await Podcast.get(id=id)
        cats = await CategoryService.get_all()
        add = False
        desc = f"{podcast.name} {podcast.description}".lower()
        for cat in cats:
            _ = cat.name.lower()
            if _ in desc:
                await podcast.categories.add(cat)
                print(f"added cat {cat} to {podcast.name}")

    @staticmethod
    async def get_by_id(id: int) -> Optional[Podcast]:
        """Get podcast by id"""
        try:
            return await Podcast.get(id=id).prefetch_related("source")
        except DoesNotExist:
            return None

    @staticmethod
    async def get_recent(limit: int = 10) -> List[Podcast]:
        """Get recent podcasts"""
        return (
            await Podcast.all()
            .order_by("-publication_date")
            .limit(limit)
            .prefetch_related("categories")
        )

    @staticmethod
    async def get_next_publication_date() -> datetime:
        """Get next free publication date for podcast"""
        last_podcast = (
            await Podcast.filter(is_active=True, is_posted=False)
            .order_by("-publication_date")
            .first()
        )
        if not last_podcast:
            return datetime.now()
        else:
            return last_podcast.publication_date + timedelta(minutes=PUBLICATION_SPEED)

    @staticmethod
    async def get_by_source(source_id: int) -> List[Podcast]:
        """Get podcasts by source id"""
        return await Podcast.filter(source_id=source_id).prefetch_related("source")

    @staticmethod
    async def count(
        source_id: Optional[int] = None,
        is_posted: Optional[bool] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> int:
        """
        Count podcasts with optional filtering

        Args:
            source_id: Filter by source ID
            is_posted: Filter by posted status
            from_date: Filter by publication date >= from_date
            to_date: Filter by publication date <= to_date

        Returns:
            Number of podcasts matching the filters
        """
        query = Podcast.all()

        # Apply filters
        if source_id is not None:
            query = query.filter(source_id=source_id)

        if is_posted is not None:
            query = query.filter(is_posted=is_posted)

        if from_date is not None:
            query = query.filter(publication_date__gte=from_date)

        if to_date is not None:
            query = query.filter(publication_date__lte=to_date)

        return await query.count()

    @staticmethod
    async def create(data: Dict[str, Any]) -> Optional[Podcast]:
        """Create new podcast"""
        try:
            return await Podcast.create(**data)
        except IntegrityError:
            # Handle duplicate URL
            print(traceback.format_exc())
            return None

    @staticmethod
    async def update(id: int, data: Dict[str, Any]) -> Optional[Podcast]:
        """Update podcast"""
        try:
            podcast = await Podcast.get(id=id)

            for key, value in data.items():
                setattr(podcast, key, value)

            await podcast.save()
            return podcast
        except DoesNotExist:
            return None
        except IntegrityError:
            # Handle duplicate URL
            return None

    @staticmethod
    async def toggle_posted(id: int) -> Optional[Podcast]:
        """Toggle is_posted status"""
        try:
            podcast = await Podcast.get(id=id)
            podcast.is_posted = not podcast.is_posted
            await podcast.save()
            return podcast
        except DoesNotExist:
            return None

    @staticmethod
    async def activate(id: int) -> Optional[Podcast]:
        """activte status"""
        try:
            podcast = await Podcast.get(id=id)
            podcast.is_active = True
            await podcast.save()
            return podcast
        except DoesNotExist:
            return None

    @staticmethod
    async def deactivate(id: int) -> Optional[Podcast]:
        """deactivte status"""
        try:
            podcast = await Podcast.get(id=id)
            podcast.is_active = False
            await podcast.save()
            return podcast
        except DoesNotExist:
            return None

    @staticmethod
    async def delete(id: int) -> bool:
        """Delete podcast"""
        try:
            podcast = await Podcast.get(id=id)
            await podcast.delete()
            return True
        except DoesNotExist:
            return False


class TgService:
    """Service for source operations"""

    @staticmethod
    async def get_all() -> List[TgChannel]:
        """Get all tgs"""
        return await TgChannel.all()

    @staticmethod
    async def count() -> int:
        """Get channels count"""
        return await TgChannel.all().count()

    @staticmethod
    async def get_by_id(id: int) -> Optional[TgChannel]:
        """Get tg by id"""
        try:
            return await TgChannel.get(id=id)
        except DoesNotExist:
            return None

    @staticmethod
    async def create(tg_id: str, name: str, auto_post: bool = False) -> TgChannel:
        """Create new tg"""
        try:
            return await TgChannel.create(tg_id=tg_id, name=name, auto_post=auto_post)
        except IntegrityError:
            # Handle duplicate URL
            return None

    @staticmethod
    async def delete(id: int) -> bool:
        """Delete tg"""
        try:
            tg = await TgChannel.get(id=id)
            await tg.delete()
            return True
        except DoesNotExist:
            return False

"""Services for podcaster project"""

import traceback
from datetime import datetime

from typing import List, Optional, Dict, Any
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.models import Category, CategoryIdentification, Source, Podcast


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
    async def create(url: str, name: str) -> Source:
        """Create new source"""
        try:
            return await Source.create(url=url, name=name)
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
            .prefetch_related("source")
        )

    @staticmethod
    def get_next_publication_date() -> datetime:
        """Get next free publication date for podcast"""
        return datetime.now()  # FIXME

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

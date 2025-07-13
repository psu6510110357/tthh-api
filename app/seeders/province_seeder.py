import datetime
import uuid
from app.models.province_model import DBProvince
from app.core.database import get_session, init_db, close_db


async def seed_provinces():
    await init_db()  # Initialize the database engine
    # await drop_db_and_tables()  # Drop existing tables if needed
    provinces = [
        {"name": "Province A", "is_secondary": False, "tax_reduction_info": "Info A"},
        {"name": "Province B", "is_secondary": True, "tax_reduction_info": "Info B"},
        {"name": "Province C", "is_secondary": False, "tax_reduction_info": "Info C"},
    ]

    async for session in get_session():
        for province_data in provinces:
            province = DBProvince(
                id=uuid.uuid4(),
                created_date=datetime.datetime.now(),
                updated_date=datetime.datetime.now(),
                **province_data,
            )
            session.add(province)
        await session.commit()

    await close_db()  # Close the database engine after seeding


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_provinces())

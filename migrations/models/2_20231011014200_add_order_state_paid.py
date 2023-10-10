from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inbound_order" ALTER COLUMN "state" TYPE VARCHAR(9) USING "state"::VARCHAR(9);
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inbound_order" ALTER COLUMN "state" TYPE VARCHAR(9) USING "state"::VARCHAR(9);
    """

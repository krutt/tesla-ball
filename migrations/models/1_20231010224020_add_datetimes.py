from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "earn_order" ALTER COLUMN "order_id" SET;
        ALTER TABLE "inbound_order" ALTER COLUMN "order_id" SET;
        ALTER TABLE "swap_order" ALTER COLUMN "order_id" SET;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "earn_order" ALTER COLUMN "order_id" SET;
        ALTER TABLE "swap_order" ALTER COLUMN "order_id" SET;
        ALTER TABLE "inbound_order" ALTER COLUMN "order_id" SET;"""

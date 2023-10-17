from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "earn_order" ADD COLUMN "state" VARCHAR(9) NOT NULL DEFAULT 'pending';
        ALTER TABLE "swap_order" ADD COLUMN "state" VARCHAR(9) NOT NULL DEFAULT 'pending';
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "earn_order" DROP COLUMN "state";
        ALTER TABLE "swap_order" DROP COLUMN "state";
    """

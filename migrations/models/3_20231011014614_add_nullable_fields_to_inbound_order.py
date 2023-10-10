from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inbound_order" ADD "txid" VARCHAR(255);
        ALTER TABLE "inbound_order" ADD "invoice" VARCHAR(255);
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inbound_order" DROP COLUMN "txid";
        ALTER TABLE "inbound_order" DROP COLUMN "invoice";
    """

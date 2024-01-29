from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
  return """
        ALTER TABLE "inbound_order" RENAME COLUMN "invoice" TO "bolt11";
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
  return """
        ALTER TABLE "inbound_order" RENAME COLUMN "bolt11" TO "invoice";
    """

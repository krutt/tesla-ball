from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
  return """
        ALTER TABLE "inbound_order" ALTER COLUMN "invoice" TYPE VARCHAR(379) USING "invoice"::VARCHAR(379);
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
  return """
        ALTER TABLE "inbound_order" ALTER COLUMN "invoice" TYPE VARCHAR(255) USING "invoice"::VARCHAR(255);
    """

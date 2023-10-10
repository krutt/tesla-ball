from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "earn_order" (
    "id" SERIAL NOT NULL PRIMARY KEY
);
COMMENT ON TABLE "earn_order" IS 'Class mapping Object Relation to table `earn_order`';
CREATE TABLE IF NOT EXISTS "inbound_order" (
    "id" SERIAL NOT NULL PRIMARY KEY
);
COMMENT ON TABLE "inbound_order" IS 'Class mapping Object Relation to table `inbound_order`';
CREATE TABLE IF NOT EXISTS "swap_order" (
    "id" SERIAL NOT NULL PRIMARY KEY
);
COMMENT ON TABLE "swap_order" IS 'Class mapping Object Relation to table `swap_order`';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

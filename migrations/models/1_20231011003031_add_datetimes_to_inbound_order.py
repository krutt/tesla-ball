from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inbound_order" ADD "state" VARCHAR(9) NOT NULL  DEFAULT 'pending';
        ALTER TABLE "inbound_order" ADD "port" INT NOT NULL  DEFAULT 9735;
        ALTER TABLE "inbound_order" ADD "pubkey" VARCHAR(66) NOT NULL;
        ALTER TABLE "inbound_order" ADD "remote_balance" INT NOT NULL  DEFAULT 20000;
        ALTER TABLE "inbound_order" ADD "host" VARCHAR(255) NOT NULL;
        ALTER TABLE "inbound_order" ADD "fee_rate" INT NOT NULL  DEFAULT 6;
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inbound_order" DROP COLUMN "state";
        ALTER TABLE "inbound_order" DROP COLUMN "port";
        ALTER TABLE "inbound_order" DROP COLUMN "pubkey";
        ALTER TABLE "inbound_order" DROP COLUMN "remote_balance";
        ALTER TABLE "inbound_order" DROP COLUMN "host";
        ALTER TABLE "inbound_order" DROP COLUMN "fee_rate";
    """

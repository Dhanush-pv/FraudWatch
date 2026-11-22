CREATE SCHEMA IF NOT EXISTS payments;
CREATE SCHEMA IF NOT EXISTS ops;

CREATE TABLE IF NOT EXISTS payments.transactions (
    transaction_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL UNIQUE,
    event_version INTEGER NOT NULL CHECK (event_version >= 1),
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL,
    transaction_timestamp TIMESTAMPTZ NOT NULL,
    customer_id TEXT NOT NULL,
    card_id TEXT NOT NULL,
    merchant_id TEXT NOT NULL,
    merchant_category TEXT NOT NULL,
    merchant_country CHAR(2) NOT NULL,
    device_id TEXT NOT NULL,
    ip_address INET NOT NULL,
    channel TEXT NOT NULL CHECK (channel IN ('POS','ECOMMERCE','ATM','MOBILE')),
    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
    currency CHAR(3) NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('AUTHORIZED','DECLINED','REVERSED')),
    is_fraud BOOLEAN,
    source_system TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_transactions_customer_time
    ON payments.transactions(customer_id, transaction_timestamp DESC);
CREATE INDEX IF NOT EXISTS ix_transactions_card_time
    ON payments.transactions(card_id, transaction_timestamp DESC);
CREATE INDEX IF NOT EXISTS ix_transactions_merchant_time
    ON payments.transactions(merchant_id, transaction_timestamp DESC);
CREATE INDEX IF NOT EXISTS ix_transactions_event_time
    ON payments.transactions(event_timestamp);

CREATE TABLE IF NOT EXISTS ops.cdc_outbox (
    outbox_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at TIMESTAMPTZ
);

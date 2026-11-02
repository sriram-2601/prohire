-- Supabase (PostgreSQL) Production Schema for Indigo.ai
-- Run this script in your Supabase SQL Editor if setting up tables manually.
-- The FastAPI backend will also automatically run CREATE TABLE IF NOT EXISTS on startup
-- when DATABASE_URL is configured in backend/.env or Render environment variables.

-- 1. Conversations Table
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,                           -- UUID string
    title TEXT NOT NULL DEFAULT 'New Chat',        -- Chat title (auto-generated from first message)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- Timestamp when created
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- Timestamp when last message was sent
    archived_at TIMESTAMPTZ                        -- NULL = active, set = archived (auto-purged after retention)
);

-- 2. Messages Table
CREATE TABLE IF NOT EXISTS messages (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Indexes for High-Performance Queries
CREATE INDEX IF NOT EXISTS idx_messages_conversation_created 
    ON messages(conversation_id, created_at ASC);

CREATE INDEX IF NOT EXISTS idx_conversations_archived 
    ON conversations(archived_at);

CREATE INDEX IF NOT EXISTS idx_conversations_updated 
    ON conversations(updated_at DESC);

-- Migration script to add new User entity properties
-- This would be used with Flyway or similar migration tool

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS location VARCHAR(255),
ADD COLUMN IF NOT EXISTS website VARCHAR(255),
ADD COLUMN IF NOT EXISTS followers_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS following_count INTEGER DEFAULT 0;

-- Update existing records with default values
UPDATE users 
SET 
    location = NULL,
    website = NULL, 
    followers_count = 0,
    following_count = 0
WHERE location IS NULL OR website IS NULL OR followers_count IS NULL OR following_count IS NULL;

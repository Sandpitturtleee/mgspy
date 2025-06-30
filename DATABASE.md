# Database Schema Documentation

---

## Table: `activity_data`

**Purpose:**  
Tracks player activity timestamps for each character profile.

| Column   | Type      | Constraints | Description                              |
|----------|-----------|-------------|------------------------------------------|
| profile  | INTEGER   | NOT NULL    | Profile identifier                       |
| char     | INTEGER   | NOT NULL    | Character identifier (per profile)       |
| datetime | TIMESTAMP | NOT NULL    | Activity record timestamp (UTC suggested)|

---

## Table: `profile_data`

**Purpose:**  
Stores basic profile information for characters in the game.

| Column   | Type         | Constraints | Description                          |
|----------|--------------|-------------|--------------------------------------|
| profile  | INTEGER      | NOT NULL    | Profile identifier                   |
| char     | INTEGER      | NOT NULL    | Character identifier (per profile)   |
| nick     | VARCHAR(255) |             | Character nickname                   |
| lvl      | INTEGER      |             | Character level                      |
| clan     | VARCHAR(255) |             | Character's clan name (if any)       |
| world    | VARCHAR(255) |             | World/server where character exists  |

---

### Relationships

- The pair (`profile`, `char`) acts as the key to associate entries in `activity_data` with records in `profile_data`.

---
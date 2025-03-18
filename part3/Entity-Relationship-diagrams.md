```mermaid
erDiagram
    User ||--o{ Place : owns
    User ||--o{ Review : authors
    Place ||--o{ Review : "has reviews"
    Place ||--o{ Place_Amenity : "has amenities"
    Amenity ||--o{ Place_Amenity : "available in places"

    User {
        CHAR(36) id
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        BOOLEAN is_admin
        DATETIME created_at
        DATETIME updated_at
    }
    Place {
        CHAR(36) id
        VARCHAR title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id
        DATETIME created_at
        DATETIME updated_at
    }
    Review {
        CHAR(36) id
        TEXT text
        INT rating
        CHAR(36) user_id
        CHAR(36) place_id
        DATETIME created_at
        DATETIME updated_at
    }
    Amenity {
        CHAR(36) id
        VARCHAR name
        DATETIME created_at
        DATETIME updated_at
    }
    Place_Amenity {
        CHAR(36) place_id
        CHAR(36) amenity_id
        DATETIME created_at
        DATETIME updated_at
    }


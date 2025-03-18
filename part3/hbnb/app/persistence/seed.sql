-- Insert Administrator User
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$KbQYq/j9FQ4lQbPT7G5eze9uJPP5mF/.lqCpZQTxj8iO1mU1QStH6', -- bcrypt hash of "admin1234"
    TRUE
)
ON CONFLICT (id) DO NOTHING;

-- Insert Initial Amenities
INSERT INTO Amenity (id, name)
VALUES
    ('b0c7c154-2df7-4cb7-8ef9-dce29bb9d6d5', 'WiFi'),
    ('a6d3a3f5-4137-4bd6-93b5-62d89d89e50d', 'Swimming Pool'),
    ('9fc75c16-3ad6-4c3f-a82d-90a8cfd91b60', 'Air Conditioning')
ON CONFLICT (id) DO NOTHING;

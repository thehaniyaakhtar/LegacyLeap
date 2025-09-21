-- Table to store uploaded legacy files
CREATE TABLE IF NOT EXISTS legacy_files (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store transformed/modernized records
CREATE TABLE IF NOT EXISTS modernized_data (
    id SERIAL PRIMARY KEY,
    legacy_file_id INT REFERENCES legacy_files(id),
    transformed_content JSONB,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to track microservices operations (optional)
CREATE TABLE IF NOT EXISTS microservices_log (
    id SERIAL PRIMARY KEY,
    modernized_id INT REFERENCES modernized_data(id),
    service_name VARCHAR(100),
    status VARCHAR(50),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

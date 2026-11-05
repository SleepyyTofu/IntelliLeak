
CREATE DATABASE IF NOT EXISTS fyp_leakage_system
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE fyp_leakage_system;

CREATE TABLE IF NOT EXISTS analysis_logs (
    id INT(11) NOT NULL AUTO_INCREMENT,
    entered_text LONGTEXT DEFAULT NULL,
    uploaded_filename VARCHAR(255) DEFAULT NULL,
    findings LONGTEXT DEFAULT NULL,
    total_score INT(11) DEFAULT NULL,
    overall_risk VARCHAR(50) DEFAULT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

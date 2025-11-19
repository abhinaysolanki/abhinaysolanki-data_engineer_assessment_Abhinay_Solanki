-- Create database
CREATE DATABASE IF NOT EXISTS property_db;
USE property_db;

-- PROPERTY TABLE
CREATE TABLE property (
  property_id INT AUTO_INCREMENT PRIMARY KEY,
  property_title VARCHAR(512),
  address VARCHAR(512),
  market VARCHAR(100),
  street_address VARCHAR(512),
  city VARCHAR(100),
  state VARCHAR(50),
  zip VARCHAR(20),
  property_type VARCHAR(50),
  highway VARCHAR(50),
  train VARCHAR(50),
  tax_rate DECIMAL(8,4),
  sqft_basement INT,
  htw VARCHAR(10),
  pool VARCHAR(10),
  commercial VARCHAR(10),
  water VARCHAR(100),
  sewage VARCHAR(100),
  year_built INT,
  sqft_mu INT,
  sqft_total VARCHAR(50),
  parking VARCHAR(100),
  basement_yes_no VARCHAR(20),
  layout VARCHAR(100),
  rent_restricted VARCHAR(10),
  neighborhood_rating DECIMAL(4,2),
  latitude DECIMAL(10,6),
  longitude DECIMAL(10,6),
  subdivision VARCHAR(255),
  school_average DECIMAL(5,2)
);

-- PROPERTY FEATURES TABLE
CREATE TABLE property_features (
    feature_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    bed INT,
    bath INT,
    sqft_total VARCHAR(50),
    pool VARCHAR(10),
    parking VARCHAR(100),
    basement_yes_no VARCHAR(20),
    FOREIGN KEY(property_id) REFERENCES property(property_id)
);

-- PROPERTY LOCATION TABLE
CREATE TABLE property_location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    street VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(100),
    zip VARCHAR(20),
    latitude DECIMAL(12, 8),
    longitude DECIMAL(12, 8),
    subdivision VARCHAR(255),
    neighborhood_rating DECIMAL(5,2),
    FOREIGN KEY(property_id) REFERENCES property(property_id)
);

-- PROPERTY FINANCIALS TABLE
CREATE TABLE property_financials (
    financial_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    taxes DECIMAL(10,2),
    net_yield DECIMAL(5,2),
    irr DECIMAL(5,2),
    selling_reason VARCHAR(255),
    rent_restricted VARCHAR(10),
    school_average DECIMAL(5,2),
    closing_cost DECIMAL(12,2),
    FOREIGN KEY(property_id) REFERENCES property(property_id)
);

-- PROPERTY WORKFLOW TABLE
CREATE TABLE property_workflow (
    workflow_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    status VARCHAR(50),
    due_diligence_date DATE,
    purchase_date DATE,
    closing_date DATE,
    workflow_notes VARCHAR(1000),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);

-- LEADS TABLE
CREATE TABLE leads (
  lead_id INT AUTO_INCREMENT PRIMARY KEY,
  property_id INT NOT NULL,
  reviewed_status VARCHAR(255),
  most_recent_status VARCHAR(255),
  source VARCHAR(255),
  occupancy VARCHAR(100),
  net_yield DECIMAL(8,4),
  irr DECIMAL(8,4),
  selling_reason VARCHAR(255),
  seller_retained_broker VARCHAR(255),
  final_reviewer VARCHAR(255),
  FOREIGN KEY (property_id) REFERENCES property(property_id)
);

-- PROPERTY VALUATION TABLE
CREATE TABLE property_valuation (
    valuation_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    valuation_amount DECIMAL(12,2),
    valuation_date DATE,
    valuation_type VARCHAR(50),
    val_source VARCHAR(100),
    FOREIGN KEY(property_id) REFERENCES property(property_id)
);

-- HOA TABLE
CREATE TABLE hoa (
    hoa_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa_amount DECIMAL(12,2),
    hoa_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);

-- REHAB TABLE
CREATE TABLE rehab (
    rehab_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab DECIMAL(12,2),
    rehab_calculation VARCHAR(255),
    paint VARCHAR(10),
    flooring_flag VARCHAR(10),
    foundation_flag VARCHAR(10),
    roof_flag VARCHAR(10),
    hvac_flag VARCHAR(10),
    kitchen_flag VARCHAR(10),
    bathroom_flag VARCHAR(10),
    appliances_flag VARCHAR(10),
    windows_flag VARCHAR(10),
    landscaping_flag VARCHAR(10),
    trashout_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);


**Data Engineering Assessment – ETL Pipeline**

Candidate: Abhinay Singh Solanki
Role: Data Engineer

**Overview**

This project delivers a complete end-to-end ETL solution that transforms a complex, unstructured property JSON dataset into a fully normalized MySQL relational database.

The raw data includes multiple unrelated business attributes (property details, valuation, financials, HOA, rehab, leads, location), all mixed in a single JSON record.
This pipeline separates each attribute group into the correct table, establishes relationships, and loads clean, validated data into MySQL.

Key Objectives

> Normalize the raw dataset using business logic from Field Config.xlsx

> Design and create a relational schema (9 fully normalized tables)

> Build a robust ETL pipeline using Python

> Validate referential integrity across all tables

> Run database inside Docker as per assessment instructions

> Deliver reproducible scripts (SQL + ETL + documentation)

**Project Structure**

project/
│── data/
│    └── raw/
│         └── input.json
│
│── src/
│    ├── create_tables.sql
│    ├── etl.py
│    ├── requirements.txt
│    └── README.md
│
└── docker-compose.initial.yml  (optional)

**Database Normalization (Final Schema)**

The JSON was broken into 9 normalized tables:

Table Name	Purpose

> property	Core property details
> property_location	Street, city, coordinates, subdivision
> property_features	Bed, bath, pool, parking, basement
> property_financials	Taxes, IRR, net yield, closing cost
> property_valuation	List price, ARV, Zestimate, rent estimates
> hoa	HOA amount + flag
> rehab	All rehab cost flags
> leads	Lead-level status and source details
> property_workflow	(Optional extra workflow fields)

**ER Diagram (Conceptual)**

property (PK)
   │
   ├──< leads
   ├──< property_location
   ├──< property_features
   ├──< property_financials
   ├──< property_valuation
   ├──< hoa
   └──< rehab
Everything is linked through property_id, ensuring clean referential integrity.

**How to Run the Project**

#   Install Python Requirements
pip install -r requirements.txt

# Start MySQL Using Docker (per instructions)

docker run --name mysql_ctn \
-e MYSQL_ROOT_PASSWORD=abhinay \
-p 3306:3306 -d mysql:8

MySQL will now run at:

Host: 127.0.0.1
Port: 3306
User: root
Password: abhinay

# Create Database Schema

mysql -u root -p < src/create_tables.sql

# Run the ETL Pipeline

python src/etl.py

If successful, you will see:If successful, you will see:

ETL Completed Successfully

# Validation Checklist

✔ Row counts match JSON
✔ FKs validated using left joins
✔ No orphaned rows in child tables
✔ All required tables populated
✔ Data types cleaned (decimal, int, flags)
✔ ARV / Zestimate cleaned from malformed JSON values

# Deliverables Included

File	                Description
create_tables.sql	    Full normalized schema
etl.py	                Complete working ETL pipeline
requirements.txt	    Dependency list
README.md	            Documentation (this file)
input.json	            Raw source file

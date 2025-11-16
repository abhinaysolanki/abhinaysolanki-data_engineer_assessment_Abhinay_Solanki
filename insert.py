import json
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    port=3307,  # aapka MySQL port
    user="root",
    password="abhinay",
    database="property_db"
)
cursor = conn.cursor()

# Text to number mapping
text_to_int = {
    "Zero": 0, "One": 1, "Two": 2, "Three": 3,
    "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
    "Eight": 8, "Nine": 9, "Ten": 10
}

# Load JSON file
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for record in data:

    # Clean numeric fields
    bed_value = record.get("Bed")
    if isinstance(bed_value, str):
        bed_value = text_to_int.get(bed_value.strip(), None)

    bath_value = record.get("Bath")
    if isinstance(bath_value, str):
        bath_value = text_to_int.get(bath_value.strip(), None)

    # SQFT_Total as string (to avoid truncate error)
    sqft_total = record.get("SQFT_Total")
    if sqft_total is not None:
        sqft_total = str(sqft_total)

    # -------- property table --------
    cursor.execute("""
        INSERT INTO property (property_title, source, market, property_type, year_built)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        record.get("Property_Title"),
        record.get("Source"),
        record.get("Market"),
        record.get("Property_Type"),
        record.get("Year_Built"),
    ))

    property_id = cursor.lastrowid

    # -------- property_features --------
    cursor.execute("""
        INSERT INTO property_features (property_id, bed, bath, sqft_total, pool, parking, basement)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        property_id,
        bed_value,
        bath_value,
        sqft_total,
        record.get("Pool"),
        record.get("Parking"),
        record.get("BasementYesNo"),
    ))

    # -------- property_location --------
    cursor.execute("""
        INSERT INTO property_location (property_id, street, city, state, zip, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        property_id,
        record.get("Street_Address"),
        record.get("City"),
        record.get("State"),
        record.get("Zip"),
        record.get("Latitude"),
        record.get("Longitude"),
    ))

    # -------- property_financials --------
    cursor.execute("""
        INSERT INTO property_financials (property_id, tax_rate, taxes, irr, net_yield)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        property_id,
        record.get("Tax_Rate"),
        record.get("Taxes"),
        record.get("IRR"),
        record.get("Net_Yield"),
    ))

    # -------- property_workflow --------
    cursor.execute("""
        INSERT INTO property_workflow (property_id, most_recent_status, reviewed_status, final_reviewer)
        VALUES (%s, %s, %s, %s)
    """, (
        property_id,
        record.get("Most_Recent_Status"),
        record.get("Reviewed_Status"),
        record.get("Final_Reviewer"),
    ))

  # -------- property_valuation --------
valuations = record.get("Valuation", [])
if valuations and isinstance(valuations, list):
    for val in valuations:
        # Safely convert string with commas to float
        def to_float(v):
            if v is None:
                return None
            if isinstance(v, str):
                return float(v.replace(",", ""))
            return float(v)

        cursor.execute("""
            INSERT INTO property_valuation (property_id, arv, as_is, rental, price_min, price_max)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            property_id,
            to_float(val.get("ARV")),
            to_float(val.get("As_is")),
            to_float(val.get("Rental")),
            to_float(val.get("Price_Min")),
            to_float(val.get("Price_Max")),
        ))


# Save everything
conn.commit()
conn.close()

print("SUCCESS — JSON data inserted into MySQL 🎉")

import pandas as pd
import mysql.connector

# --------------------------------------------
# DB CONNECTION (Docker MySQL)
# --------------------------------------------
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="abhinay",
    database="property_db",
    port=3306
)

cursor = connection.cursor()

# --------------------------------------------
# LOAD JSON
# --------------------------------------------
df = pd.read_json(r"C:\Users\singh\Downloads\100x\data\raw\input.json")
print("JSON Loaded ✓")
print(df.head(2))

print("\n Columns in JSON:")
print(df.columns.tolist())


# ================================================================
#  PROPERTY TABLE
# ================================================================
property_df = df[['Property_Title', 'City', 'State', 'Zip']]
property_ids = []

for _, row in property_df.iterrows():
    cursor.execute("""
        INSERT INTO property (property_title, city, state, zip)
        VALUES (%s, %s, %s, %s)
    """, (
        row['Property_Title'],
        row['City'],
        row['State'],
        row['Zip']
    ))
    connection.commit()
    property_ids.append(cursor.lastrowid)

print(f"Property table Load ✓ — {len(property_ids)} rows inserted")


# ================================================================
#  LEADS TABLE
# ================================================================
leads_df = df[['Reviewed_Status', 'Most_Recent_Status', 'Source', 'Occupancy',
               'Net_Yield', 'IRR', 'Selling_Reason', 'Seller_Retained_Broker', 'Final_Reviewer']]

for i, row in leads_df.iterrows():
    cursor.execute("""
        INSERT INTO leads
        (property_id, reviewed_status, most_recent_status, source, occupancy,
         net_yield, irr, selling_reason, seller_retained_broker, final_reviewer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        property_ids[i],
        row['Reviewed_Status'],
        row['Most_Recent_Status'],
        row['Source'],
        row['Occupancy'],
        row['Net_Yield'],
        row['IRR'],
        row['Selling_Reason'],
        row['Seller_Retained_Broker'],
        row['Final_Reviewer']
    ))

connection.commit()
print("Leads table Load ✓")


# ================================================================
#  PROPERTY LOCATION
# ================================================================
location_df = df[['Street_Address', 'City', 'State', 'Zip', 'Latitude', 'Longitude']]

for i, row in location_df.iterrows():
    cursor.execute("""
        INSERT INTO property_location
        (property_id, street, city, state, zip, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        property_ids[i],
        row['Street_Address'],
        row['City'],
        row['State'],
        row['Zip'],
        row['Latitude'],
        row['Longitude']
    ))

connection.commit()
print("Property_location table Load ✓")


# ================================================================
#  PROPERTY FEATURES
# ================================================================
features_df = df[['Bed', 'Bath', 'SQFT_Total', 'Pool', 'Parking', 'BasementYesNo']]

for i, row in features_df.iterrows():
    cursor.execute("""
        INSERT INTO property_features
        (property_id, bed, bath, sqft_total, pool, parking, basement_yes_no)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        property_ids[i],
        row['Bed'],
        row['Bath'],
        row['SQFT_Total'],
        row['Pool'],
        row['Parking'],
        row['BasementYesNo']
    ))

connection.commit()
print("property_features table Load ✓")


# ================================================================
#  FINANCIALS
# ================================================================
fin_df = df[['Taxes', 'Net_Yield', 'IRR', 'Selling_Reason', 'Rent_Restricted', 'School_Average']]

for i, row in fin_df.iterrows():
    cursor.execute("""
        INSERT INTO property_financials
        (property_id, taxes, net_yield, irr, selling_reason, rent_restricted, school_average)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        property_ids[i],
        row['Taxes'],
        row['Net_Yield'],
        row['IRR'],
        row['Selling_Reason'],
        row['Rent_Restricted'],
        row['School_Average']
    ))

connection.commit()
print("property_financials table Load ✓")


# ================================================================
#  VALUATIONS
# ================================================================
for i, record in enumerate(df['Valuation']):
    if isinstance(record, list):
        for v in record:
            cursor.execute("""
                INSERT INTO property_valuation
                (property_id, arv)
                VALUES (%s, %s)
            """, (
                property_ids[i],
                v.get("ARV")
            ))
connection.commit()
print("property_valuation table Load ✓")


# ================================================================
# LAST — CLOSE CONNECTION
# ================================================================
cursor.close()
connection.close()
print("\n ETL Completed Successfully")

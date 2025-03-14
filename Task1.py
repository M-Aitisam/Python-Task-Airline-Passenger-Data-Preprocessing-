import pandas as pd
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import re

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    data = []
    for record in root.findall("record"):
        entry = {child.tag: child.text for child in record}
        data.append(entry)
    return data

def normalize_phone_number(phone):
    if phone and isinstance(phone, str):
        phone = re.sub(r"[^0-9+]", "", phone)
        return re.sub(r"(\d{3})(\d{3})(\d{4})", r"\1-\2-\3", phone)
    return "Unknown"

def normalize_datetime(date_str):
    formats = ["%Y-%m-%d %H:%M:%S", "%d/%m/%Y %I:%M %p", "%m-%d-%Y %H:%M"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d %H:%M:%S UTC")
        except (ValueError, TypeError):
            continue
    return "Unknown"

def estimate_ticket_price(ticket_class):
    prices = {"Economy": 200.00, "Business": 500.00, "First": 1000.00, "Unknown": 0.00}
    return prices.get(ticket_class, 0.00)

def preprocess_data():
    online_booking = pd.DataFrame(load_json("online_booking.json"))
    travel_agency = pd.DataFrame(load_xml("third_party_travel_agency.xml"))
    airport_checkin = pd.DataFrame(load_json("airport_check_in_data.json"))

    # Process online booking data
    online_booking = online_booking.assign(
        passenger_name=online_booking["first_name"] + " " + online_booking["last_name"],
        email=online_booking.get("contact_email", pd.Series()).fillna("Unknown"),
        phone_number=online_booking.get("contact_phone", pd.Series()).apply(normalize_phone_number),
        ticket_class=online_booking.get("ticket_class", pd.Series()).fillna("Unknown"),
        seat_number=online_booking.get("seat_number", pd.Series()).fillna("Unassigned"),
        departure_airport=online_booking.get("departure_airport", pd.Series()).fillna("Unknown"),
        arrival_airport=online_booking.get("arrival_airport", pd.Series()).fillna("Unknown"),
        departure_time_utc=online_booking.get("departure_time", pd.Series()).apply(normalize_datetime),
        arrival_time_utc=online_booking.get("arrival_time", pd.Series()).apply(normalize_datetime),
        payment_status="Completed"
    )

    # Process travel agency data
    travel_agency = travel_agency.assign(
        passenger_name=travel_agency.get("passenger_name", pd.Series()).fillna("Unknown"),
        email=travel_agency.get("email", pd.Series()).fillna("Unknown"),
        phone_number=travel_agency.get("phone_number", pd.Series()).apply(normalize_phone_number),
        ticket_class=travel_agency.get("ticket_class", pd.Series()).fillna("Unknown"),
        seat_number=travel_agency.get("seat_number", pd.Series()).fillna("Unassigned"),
        departure_airport=travel_agency.get("departure_airport", pd.Series()).fillna("Unknown"),
        arrival_airport=travel_agency.get("arrival_airport", pd.Series()).fillna("Unknown"),
        departure_time_utc=travel_agency.get("departure_time", pd.Series()).apply(normalize_datetime),
        arrival_time_utc=travel_agency.get("arrival_time", pd.Series()).apply(normalize_datetime),
        payment_status=travel_agency.get("payment_status", pd.Series()).fillna("Unknown")
    )

    # Process airport check-in data
    airport_checkin = airport_checkin.assign(
        passenger_name=airport_checkin.get("passenger_name", pd.Series()).fillna("Unknown"),
        email=airport_checkin.get("email", pd.Series()).fillna("Unknown"),
        phone_number=airport_checkin.get("phone_number", pd.Series()).apply(normalize_phone_number),
        ticket_class=airport_checkin.get("ticket_class", pd.Series()).fillna("Unknown"),
        seat_number=airport_checkin.get("seat_number", pd.Series()).fillna("Unassigned"),
        departure_airport=airport_checkin.get("departure_airport", pd.Series()).fillna("Unknown"),
        arrival_airport=airport_checkin.get("arrival_airport", pd.Series()).fillna("Unknown"),
        departure_time_utc=airport_checkin.get("departure_time", pd.Series()).apply(normalize_datetime),
        arrival_time_utc=airport_checkin.get("arrival_time", pd.Series()).apply(normalize_datetime),
        ticket_price_usd=pd.to_numeric(airport_checkin.get("ticket_price_usd", pd.Series()), errors="coerce").fillna(0.00),
        payment_status=airport_checkin.get("payment_status", pd.Series()).fillna("Unknown")
    )

    # Merge all data
    all_data = pd.concat([online_booking, travel_agency, airport_checkin], ignore_index=True)

    # Ensure ticket price is set
    all_data["ticket_price_usd"] = all_data.apply(
        lambda row: row["ticket_price_usd"] if row["ticket_price_usd"] else estimate_ticket_price(row["ticket_class"]),
        axis=1
    )

    # Ensure required columns exist
    all_data = all_data.assign(
        booking_id=all_data.get("booking_id", pd.Series()).fillna("Unknown"),
        flight_number=all_data.get("flight_number", pd.Series()).fillna("Unknown")
    )

    # Remove duplicates based on unique identifiers
    all_data.drop_duplicates(subset=["booking_id", "passport_number"], keep="first", inplace=True)

    # Define final column order
    final_columns = [
        "booking_id", "passenger_name", "passport_number", "email", "phone_number",
        "flight_number", "departure_airport", "departure_time_utc",
        "arrival_airport", "arrival_time_utc", "ticket_class", "seat_number",
        "ticket_price_usd", "payment_status"
    ]

    # Select and reorder columns
    all_data = all_data[[col for col in final_columns if col in all_data.columns]]

    # Save to CSV
    all_data.to_csv("cleaned_passenger_data.csv", index=False)
    print("Data preprocessing complete. CSV file saved.")

preprocess_data()

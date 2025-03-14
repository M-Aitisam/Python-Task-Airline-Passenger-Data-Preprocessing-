# Airline Passenger Data & Statistical Analysis

## Project Overview
This project involves two key tasks:
1. **Airline Passenger Data Preprocessing:** Cleaning and merging passenger data from multiple sources to create a structured dataset.
2. **Statistical Analysis:** Calculating and interpreting mean, median, and mode for different datasets to understand their effectiveness in representing data.

## Task 1: Airline Passenger Data Preprocessing

### Problem Statement
An airline collects passenger booking and check-in data from three sources:
- **Online Booking System (JSON)**: Direct bookings via website/app.
- **Third-Party Travel Agency (XML)**: External agency bookings.
- **Airport Check-In System (JSON)**: Actual check-in records.

Since no single source has complete information, merging them requires handling missing values, inconsistencies, and duplicates.

### Dataset Issues & Preprocessing Approach

#### **Handling Missing Values**
- **Missing Ticket Class** (Third-Party Travel Agency) → Fill with `"Unknown"`
- **Missing Seat Number** (Online Booking) → Fill with `"Unassigned"`
- **Missing Ticket Price** (Airport Check-In) → Estimate based on ticket class
- **Missing Airport Information** → Fill with `"Unknown"`
- **Missing Payment Status** → Set to `"Completed"` for online bookings and `"Unknown"` for check-ins

#### **Data Normalization**
- **Date & Time** → Convert to `YYYY-MM-DD HH:MM:SS UTC` format
- **Phone Numbers** → Standardize format (`+CountryCode-XXX-XXX-XXXX`)

#### **Final Preprocessing Steps**
1. Extract relevant fields from each dataset.
2. Normalize date-time formats, phone numbers, and ticket class values.
3. Remove duplicate records, keeping the most complete entries.
4. Save the cleaned data as a structured CSV file.

### **Final CSV Format**
| Column | Description |
|--------|-------------|
| booking_id | Unique booking identifier |
| passenger_name | Full name of passenger |
| passport_number | Passport ID |
| email | Contact email |
| phone_number | Standardized phone number |
| flight_number | Flight identifier |
| departure_airport | Departure airport code |
| departure_time_utc | Standardized UTC departure time |
| arrival_airport | Arrival airport code |
| arrival_time_utc | Standardized UTC arrival time |
| ticket_class | Economy, Business, First, or Unknown |
| seat_number | Assigned or "Unassigned" |
| ticket_price_usd | Ticket price or `0.00` if unknown |
| payment_status | Completed, Pending, or Unknown |

## Task 2: Mean, Median, and Mode Analysis

### **Problem Statement**
This task explores the effectiveness of mean, median, and mode in different datasets. The goal is to analyze which measure provides the most representative value.

### **Datasets Used**
1. **Income Distribution Dataset** (100+ data points) → Includes high-income outliers.
2. **Product Rating Dataset** (50+ ratings) → Discrete values (1-5) with a clear mode.
3. **Temperature Dataset** (30+ days) → Normally distributed with minor outliers.

### **Analysis Steps**
For each dataset:
1. Calculate **Mean, Median, and Mode**.
2. Determine which measure best represents the dataset.
3. Explain why that measure is most suitable.
4. Provide a real-world example where using the wrong measure could mislead analysis.

### **Key Insights**
- **Income Distribution:** Median is the best measure due to skewness from high-income outliers.
- **Product Ratings:** Mode is the best measure as it represents the most common customer rating.
- **Temperature Data:** Mean is the best measure since the data is normally distributed.

## Conclusion
This project successfully cleanses and merges airline passenger data into a structured format while demonstrating the importance of choosing the right statistical measure for different types of datasets.

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Install dependencies:
   ```bash
   pip install pandas numpy statistics scipy
   ```
3. Run the preprocessing script:
   ```bash
   python preprocess.py
   ```
4. Run the statistical analysis script:
   ```bash
   python analysis.py
   ```

## Author
[Aitisam Ahmed]


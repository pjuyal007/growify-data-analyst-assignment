# Data Quality Report

## Overview
This report documents the data quality issues identified in the raw datasets (`campaigns_raw.csv` and `shopify_raw.csv`) and the steps taken to clean and prepare the data for analysis.

---

## Dataset 1: Campaigns Data

### 🔴 Issues Identified

1. **Missing Values**
   - Significant null values in multiple columns such as:
     - Campaign Name
     - Ad Set Name
     - Clicks
     - Impressions
     - Spend columns
     - Conversion-related columns

2. **Missing Dates**
   - Around ~5000 missing values in the Date column

3. **Duplicate Rows**
   - Duplicate records present in dataset

4. **Inconsistent Date Formats**
   - Dates were not in a standard datetime format

5. **Incorrect / Missing Metrics**
   - CTR values not matching formula (Clicks / Impressions)
   - CPC, CPM, ROI not provided or inconsistent

6. **String Inconsistencies**
   - Mixed case values (e.g., Facebook vs facebook)
   - Presence of 'nan' as string instead of actual null

7. **Outliers**
   - Some abnormal spend values observed

---

### ✅ Cleaning Steps Performed

1. **Handled Missing Dates**
   - Rows with missing Date were removed due to analytical importance

2. **Handled Missing Values**
   - Numeric columns → filled with 0 (logical for counts/metrics)
   - Text columns → filled with 'unknown'

3. **Removed Duplicates**
   - Used `.drop_duplicates()` to remove duplicate rows

4. **Standardized Date Format**
   - Converted Date column to datetime format using pandas

5. **Recalculated Metrics**
   - CTR = Clicks / Impressions
   - CPC = Spend / Clicks
   - CPM = (Spend / Impressions) * 1000
   - ROI = (Revenue - Spend) / Spend

6. **Normalized Text Columns**
   - Converted all text columns to lowercase
   - Removed inconsistencies in naming

7. **Handled 'nan' String Values**
   - Replaced string 'nan' with 'unknown'

---

## Dataset 2: Shopify Sales Data

### 🔴 Issues Identified

1. **Missing Values**
   - Missing values in:
     - Product-related columns
     - Customer-related columns
     - Sales metrics

2. **Duplicate Rows**
   - Duplicate entries present

3. **Inconsistent Date Formats**
   - Multiple timestamp columns required formatting

4. **String Issues**
   - 'nan' stored as string in some text fields

---

### ✅ Cleaning Steps Performed

1. **Handled Missing Values**
   - Numeric columns → filled with 0
   - Text columns → filled with 'unknown'

2. **Removed Duplicates**
   - Duplicate rows removed

3. **Date Standardization**
   - Converted all date and timestamp columns to proper datetime format

4. **Normalized Text Columns**
   - Standardized text values to lowercase

5. **Handled 'nan' Strings**
   - Replaced 'nan' values with 'unknown'

---

## 🧠 Design Decisions

- Rows with missing Date were dropped as time-based analysis is critical
- Numeric nulls replaced with 0 to preserve records
- Text nulls replaced with 'unknown' to avoid data loss
- Metrics recalculated to ensure accuracy instead of relying on raw data

---

## 📊 Final Outcome

- Clean, consistent datasets ready for SQL ingestion
- Reliable metrics for analysis and reporting
- Structured data suitable for:
  - SQL schema (star schema)
  - Power BI dashboards
  - AI insight tool

---

## 🚀 Conclusion

Data quality issues were systematically identified and resolved to ensure accuracy, consistency, and usability across the entire data pipeline. The cleaned data now serves as a single source of truth for downstream analytics and AI-driven insights.

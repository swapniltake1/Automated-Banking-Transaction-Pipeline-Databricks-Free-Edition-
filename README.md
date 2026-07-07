# Banking Data Engineering Platform

## Overview

An end-to-end Banking Data Engineering project built on **Databricks
Free Edition** using the Medallion Architecture (Bronze, Silver, Gold).

The project demonstrates how banking transaction data can be ingested,
validated, transformed, enriched, analyzed, and reported using Delta
Lake and PySpark.

## Features

-   Dynamic source discovery
-   Dynamic CSV ingestion
-   Medallion Architecture
-   Delta Lake storage
-   Audit logging
-   Fraud detection
-   SQL analytics
-   Dashboard-ready Gold layer
-   Modular notebook design
-   Databricks Free Edition compatible

## Tech Stack

-   Databricks Free Edition
-   Apache Spark
-   PySpark
-   Delta Lake
-   Unity Catalog
-   SQL
-   Python

## Project Structure

``` text
Banking_Data_Engineering/
│
├── notebooks/
│   ├── 99_Config
│   ├── 98_Utilities
│   ├── 97_Logger
│   ├── 00_Project_Setup
│   ├── 01_Precheck
│   ├── 02_Master_Data_Load
│   ├── 03_Ingestion
│   ├── 04_Data_Validation
│   ├── 05_Bronze_to_Silver
│   ├── 06_Fraud_Detection
│   ├── 07_Gold_Layer
│   ├── 08_Audit_Logging
│   ├── 09_SQL_Analytics
│   ├── 10_Dashboard
│   └── 11_Master_Pipeline
│
├── sample_data/
├── docs/
├── architecture/
├── sql/
├── tests/
└── README.md
```

## Pipeline Flow

``` text
Reference Data
        │
        ▼
Master Data Load
        │
Incoming Transactions
        │
        ▼
Bronze
        │
        ▼
Data Validation
        │
        ├── Validated
        └── Rejected
               │
               ▼
Bronze to Silver
        │
        ▼
Fraud Detection
        │
        ▼
Gold Layer
        │
        ▼
SQL Analytics
        │
        ▼
Dashboard
```

## Notebook Execution Order

1.  00_Project_Setup
2.  01_Precheck
3.  02_Master_Data_Load
4.  03_Ingestion
5.  04_Data_Validation
6.  05_Bronze_to_Silver
7.  06_Fraud_Detection
8.  07_Gold_Layer
9.  08_Audit_Logging
10. 09_SQL_Analytics
11. 10_Dashboard

Or execute **11_Master_Pipeline** to run the complete workflow.

## Sample Data

Mastrdata datasets: - Customers - Accounts - Branches - Banks - Account
Types - Transaction Types - Currencies

Transaction sources: - ATM - UPI - NEFT - RTGS - CARD -
INTERNET_BANKING - MOBILE_BANKING - BRANCH

## Gold Layer Outputs

-   Daily Transaction Summary
-   Branch Performance Summary
-   Customer Summary
-   Fraud Transactions

## Future Enhancements

-   Metadata-driven pipeline
-   Incremental loading
-   Watermark processing
-   Advanced fraud detection
-   CI/CD integration
-   Unit testing
-   Data quality scorecards

## Author

**Swapnil Take**

Azure Data Engineer \| PySpark \| SQL \| Delta Lake \| Databricks \|
Data Engineering

# Databricks notebook source
# DBTITLE 1,Bronze Layer - Banking Transactions Ingestion
# MAGIC %md
# MAGIC # Bronze Layer - Banking Transactions Ingestion
# MAGIC
# MAGIC This notebook ingests raw banking transaction data into a Delta Lake bronze table.
# MAGIC
# MAGIC **Purpose:**
# MAGIC - Land raw transaction data from source systems
# MAGIC - Preserve original data with minimal transformation
# MAGIC - Add metadata columns for audit and lineage tracking
# MAGIC
# MAGIC **Bronze Layer Characteristics:**
# MAGIC - Schema-on-read approach
# MAGIC - Immutable raw data storage
# MAGIC - Supports historical analysis and reprocessing

# COMMAND ----------

# DBTITLE 1,Setup - Define paths and catalog
# Define your catalog, schema, and table names
catalog_name = "main"  # Change to your catalog
schema_name = "banking_pipeline"  # Change to your schema
bronze_table = "bronze_transactions"

# Full table reference
full_table_name = f"{catalog_name}.{schema_name}.{bronze_table}"

print(f"Bronze table: {full_table_name}")

# COMMAND ----------

# DBTITLE 1,Create bronze Delta table
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name

# Sample: Read CSV data from data_input folder
# Adjust the path to your actual data source
data_path = "/Workspace/Users/swapniltake1@outlook.com/Automated-Banking-Transaction-Pipeline-Databricks-Free-Edition-/data_input/*.csv"

# Read raw transaction data
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(data_path)

# Add audit columns for tracking
df_bronze = df_raw \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("source_file", input_file_name())

# Write to Delta table
df_bronze.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(full_table_name)

print(f"✓ Data ingested to {full_table_name}")
print(f"Total records: {df_bronze.count()}")

# COMMAND ----------

# DBTITLE 1,Query bronze table
# MAGIC %sql
# MAGIC -- Query the bronze table to verify ingestion
# MAGIC -- Replace with your actual catalog.schema.table
# MAGIC SELECT * FROM main.banking_pipeline.bronze_transactions LIMIT 10;

# COMMAND ----------



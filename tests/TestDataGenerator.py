# Databricks notebook source
# DBTITLE 1,Banking Test Data Generator
# MAGIC %md
# MAGIC # Banking Test Data Generator
# MAGIC
# MAGIC This notebook contains a comprehensive class to generate Excel test files for:
# MAGIC * **Transaction Data** - For incoming folder (ATM, UPI, NEFT, RTGS, CARD, etc.)
# MAGIC * **Master Data** - For master_data folder (Customers, Accounts, Branches)
# MAGIC
# MAGIC ## Features
# MAGIC * Generates realistic banking transaction data
# MAGIC * Creates Excel files (.xlsx format)
# MAGIC * Supports multiple source systems
# MAGIC * Configurable record counts
# MAGIC * Automatic file placement in correct folders
# MAGIC * CSV and Excel format support

# COMMAND ----------

# DBTITLE 1,Load Configuration
# MAGIC %run ./99_Config

# COMMAND ----------

# DBTITLE 1,Import Required Libraries
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime, timedelta
import random
import pandas as pd

print("✅ Libraries imported successfully")

# COMMAND ----------

# DBTITLE 1,TestDataGenerator Class - Main Implementation
class BankingTestDataGenerator:
    """
    Comprehensive Test Data Generator for Banking Transaction Pipeline
    
    Generates realistic test data for:
    - Transaction files (incoming folder)
    - Master data files (customers, accounts, branches)
    
    Supports both CSV and Excel formats
    """
    
    def __init__(self, base_path, source_systems, valid_transaction_types):
        """
        Initialize the test data generator
        
        Args:
            base_path: Base path for volumes (e.g., /Volumes/catalog/schema/volume)
            source_systems: List of source systems (ATM, UPI, NEFT, etc.)
            valid_transaction_types: List of valid transaction types
        """
        self.base_path = base_path
        self.source_systems = source_systems
        self.valid_transaction_types = valid_transaction_types
        self.incoming_path = f"{base_path}/incoming"
        self.master_data_path = f"{base_path}/master_data"
        
        # Define data ranges
        self.currencies = ["INR", "USD", "EUR", "GBP"]
        self.customer_segments = ["RETAIL", "CORPORATE", "SME", "PREMIUM"]
        self.account_types = ["SAVINGS", "CURRENT", "SALARY", "FIXED_DEPOSIT"]
        self.branch_cities = ["MUMBAI", "DELHI", "BANGALORE", "CHENNAI", "KOLKATA", 
                             "HYDERABAD", "PUNE", "AHMEDABAD", "JAIPUR", "LUCKNOW"]
        
    def _generate_transaction_id(self, index, source_system):
        """Generate unique transaction ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{source_system}_{timestamp}_{index:06d}"
    
    def _generate_customer_id(self):
        """Generate customer ID"""
        return f"CUST{random.randint(10000, 99999)}"
    
    def _generate_account_number(self):
        """Generate account number"""
        return f"{random.randint(1000, 9999)}{random.randint(10000000, 99999999)}"
    
    def _generate_branch_code(self):
        """Generate branch code"""
        return f"BR{random.randint(1, 100):03d}"
    
    def _random_timestamp(self, days_back=30):
        """Generate random timestamp within specified days"""
        days_ago = random.randint(0, days_back)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        return datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    
    def generate_transactions(self, source_system, num_records=1000, days_back=30):
        """
        Generate transaction data for a specific source system
        
        Args:
            source_system: Source system name (ATM, UPI, etc.)
            num_records: Number of transaction records to generate
            days_back: Number of days back to generate timestamps
            
        Returns:
            Pandas DataFrame with transaction data
        """
        print(f"Generating {num_records} transactions for {source_system}...")
        
        transactions = []
        
        for i in range(num_records):
            # Generate transaction data
            transaction = {
                'transaction_id': self._generate_transaction_id(i, source_system),
                'customer_id': self._generate_customer_id(),
                'account_number': self._generate_account_number(),
                'transaction_type': random.choice(self.valid_transaction_types),
                'amount': round(random.uniform(100, 100000), 2),
                'currency': random.choice(self.currencies) if source_system in ['CARD', 'INTERNET_BANKING'] else 'INR',
                'branch': self._generate_branch_code(),
                'transaction_timestamp': self._random_timestamp(days_back)
            }
            
            # Add source-specific fields
            if source_system == 'ATM':
                transaction['atm_id'] = f"ATM{random.randint(1000, 9999)}"
                transaction['card_number'] = f"****{random.randint(1000, 9999)}"
            elif source_system == 'UPI':
                transaction['upi_id'] = f"{random.choice(['user', 'mobile', 'email'])}@{random.choice(['paytm', 'gpay', 'phonepe'])}"
            elif source_system == 'CARD':
                transaction['card_number'] = f"****{random.randint(1000, 9999)}"
                transaction['merchant_name'] = random.choice(['Amazon', 'Flipkart', 'Swiggy', 'Zomato', 'MakeMyTrip'])
            
            transactions.append(transaction)
        
        df = pd.DataFrame(transactions)
        print(f"✅ Generated {len(df)} transactions for {source_system}")
        return df
    
    def generate_customers(self, num_records=500):
        """
        Generate customer master data
        
        Args:
            num_records: Number of customer records to generate
            
        Returns:
            Pandas DataFrame with customer data
        """
        print(f"Generating {num_records} customer records...")
        
        first_names = ['Rajesh', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Sanjay', 'Kavita', 
                      'Rahul', 'Pooja', 'Arjun', 'Divya', 'Rohan', 'Neha', 'Karan']
        last_names = ['Sharma', 'Patel', 'Kumar', 'Singh', 'Reddy', 'Nair', 'Gupta', 'Mehta', 
                     'Shah', 'Desai', 'Iyer', 'Joshi', 'Rao', 'Kapoor', 'Malhotra']
        
        customers = []
        
        for i in range(num_records):
            customer_id = f"CUST{10000 + i}"
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            customer = {
                'customer_id': customer_id,
                'first_name': first_name,
                'last_name': last_name,
                'full_name': f"{first_name} {last_name}",
                'email': f"{first_name.lower()}.{last_name.lower()}@email.com",
                'phone': f"+91{random.randint(7000000000, 9999999999)}",
                'date_of_birth': (datetime.now() - timedelta(days=random.randint(7300, 25550))).date(),
                'customer_segment': random.choice(self.customer_segments),
                'kyc_status': random.choice(['COMPLETED', 'PENDING', 'IN_PROGRESS']),
                'registration_date': (datetime.now() - timedelta(days=random.randint(1, 1825))).date(),
                'city': random.choice(self.branch_cities),
                'state': random.choice(['MAHARASHTRA', 'KARNATAKA', 'DELHI', 'TAMIL_NADU', 'WEST_BENGAL']),
                'pincode': random.randint(100001, 999999)
            }
            customers.append(customer)
        
        df = pd.DataFrame(customers)
        print(f"✅ Generated {len(df)} customer records")
        return df
    
    def generate_accounts(self, num_records=800):
        """
        Generate account master data
        
        Args:
            num_records: Number of account records to generate
            
        Returns:
            Pandas DataFrame with account data
        """
        print(f"Generating {num_records} account records...")
        
        accounts = []
        
        for i in range(num_records):
            account = {
                'account_number': self._generate_account_number(),
                'customer_id': f"CUST{random.randint(10000, 10500)}",
                'account_type': random.choice(self.account_types),
                'branch_code': self._generate_branch_code(),
                'opening_date': (datetime.now() - timedelta(days=random.randint(1, 1825))).date(),
                'current_balance': round(random.uniform(1000, 500000), 2),
                'currency': 'INR',
                'status': random.choice(['ACTIVE', 'INACTIVE', 'DORMANT', 'CLOSED']),
                'overdraft_limit': round(random.uniform(0, 50000), 2) if random.random() > 0.7 else 0.0,
                'interest_rate': round(random.uniform(3.5, 7.5), 2),
                'last_transaction_date': (datetime.now() - timedelta(days=random.randint(0, 90))).date()
            }
            accounts.append(account)
        
        df = pd.DataFrame(accounts)
        print(f"✅ Generated {len(df)} account records")
        return df
    
    def generate_branches(self, num_records=100):
        """
        Generate branch master data
        
        Args:
            num_records: Number of branch records to generate
            
        Returns:
            Pandas DataFrame with branch data
        """
        print(f"Generating {num_records} branch records...")
        
        branches = []
        
        for i in range(1, num_records + 1):
            city = random.choice(self.branch_cities)
            branch = {
                'branch_code': f"BR{i:03d}",
                'branch_name': f"{city} {random.choice(['Main', 'East', 'West', 'North', 'South'])} Branch",
                'city': city,
                'state': random.choice(['MAHARASHTRA', 'KARNATAKA', 'DELHI', 'TAMIL_NADU', 'WEST_BENGAL']),
                'address': f"{random.randint(1, 999)} {random.choice(['MG Road', 'Park Street', 'Main Street', 'Commercial Complex'])}",
                'pincode': random.randint(100001, 999999),
                'phone': f"+91{random.randint(2000000000, 2999999999)}",
                'email': f"{city.lower()}.branch@bank.com",
                'ifsc_code': f"BANK000{i:04d}",
                'manager_name': f"{random.choice(['Rajesh', 'Amit', 'Sanjay', 'Vikram'])} {random.choice(['Sharma', 'Patel', 'Kumar', 'Singh'])}",
                'opening_date': (datetime.now() - timedelta(days=random.randint(365, 7300))).date(),
                'branch_type': random.choice(['RETAIL', 'CORPORATE', 'SME', 'UNIVERSAL'])
            }
            branches.append(branch)
        
        df = pd.DataFrame(branches)
        print(f"✅ Generated {len(df)} branch records")
        return df

# COMMAND ----------

# DBTITLE 1,TestDataGenerator Class - File Operations
class BankingTestDataGenerator(BankingTestDataGenerator):
    """
    Extended class with file saving operations
    """
    
    def save_to_excel(self, df, file_path, sheet_name='Sheet1'):
        """
        Save DataFrame to Excel file using Spark
        
        Args:
            df: Pandas DataFrame
            file_path: Full file path (without extension)
            sheet_name: Excel sheet name
        """
        try:
            # Convert pandas to Spark DataFrame
            spark_df = spark.createDataFrame(df)
            
            # Save as CSV first (Spark doesn't directly support Excel)
            temp_csv_path = f"{file_path}.csv"
            spark_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(temp_csv_path)
            
            # Find the actual CSV file
            files = dbutils.fs.ls(temp_csv_path)
            csv_file = [f.path for f in files if f.path.endswith('.csv')][0]
            
            # Read CSV and save as Excel using pandas
            csv_content = spark.read.csv(csv_file, header=True, inferSchema=True).toPandas()
            
            # Save to Excel
            excel_path = f"{file_path}.xlsx"
            
            # For Databricks, we need to write to DBFS first
            with pd.ExcelWriter(excel_path.replace('/Volumes', '/dbfs/Volumes'), engine='openpyxl') as writer:
                csv_content.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Clean up temp CSV
            dbutils.fs.rm(temp_csv_path, True)
            
            print(f"✅ Saved Excel file: {excel_path}")
            return excel_path
            
        except Exception as e:
            print(f"❌ Error saving Excel file: {str(e)}")
            # Fallback to CSV if Excel fails
            csv_path = f"{file_path}.csv"
            spark_df = spark.createDataFrame(df)
            spark_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(csv_path)
            print(f"⚠️ Saved as CSV instead: {csv_path}")
            return csv_path
    
    def save_to_csv(self, df, file_path):
        """
        Save DataFrame to CSV file
        
        Args:
            df: Pandas DataFrame
            file_path: Full file path (without extension)
        """
        try:
            spark_df = spark.createDataFrame(df)
            csv_path = f"{file_path}.csv"
            spark_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(csv_path)
            print(f"✅ Saved CSV file: {csv_path}")
            return csv_path
        except Exception as e:
            print(f"❌ Error saving CSV file: {str(e)}")
            raise
    
    def generate_all_transaction_files(self, records_per_source=1000, format='csv'):
        """
        Generate transaction files for all source systems
        
        Args:
            records_per_source: Number of records per source system
            format: 'csv' or 'excel'
        """
        print("="*80)
        print("GENERATING TRANSACTION FILES FOR ALL SOURCE SYSTEMS")
        print("="*80)
        
        generated_files = []
        
        for source_system in self.source_systems:
            print(f"\n[{source_system}] Processing...")
            
            # Generate transactions
            df = self.generate_transactions(source_system, records_per_source)
            
            # Create file path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"transactions_{timestamp}"
            file_path = f"{self.incoming_path}/{source_system}/{file_name}"
            
            # Save file
            if format.lower() == 'excel':
                saved_path = self.save_to_excel(df, file_path, sheet_name='Transactions')
            else:
                saved_path = self.save_to_csv(df, file_path)
            
            generated_files.append({
                'source_system': source_system,
                'file_path': saved_path,
                'record_count': len(df)
            })
        
        print("\n" + "="*80)
        print(f"✅ COMPLETED: Generated {len(generated_files)} transaction files")
        print("="*80)
        
        return generated_files
    
    def generate_all_master_data(self, format='csv'):
        """
        Generate all master data files (customers, accounts, branches)
        
        Args:
            format: 'csv' or 'excel'
        """
        print("="*80)
        print("GENERATING MASTER DATA FILES")
        print("="*80)
        
        generated_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate Customers
        print("\n[CUSTOMERS] Processing...")
        customers_df = self.generate_customers(500)
        customer_file = f"{self.master_data_path}/customers/customers_{timestamp}"
        if format.lower() == 'excel':
            saved_path = self.save_to_excel(customers_df, customer_file, 'Customers')
        else:
            saved_path = self.save_to_csv(customers_df, customer_file)
        generated_files.append({'type': 'customers', 'path': saved_path, 'count': len(customers_df)})
        
        # Generate Accounts
        print("\n[ACCOUNTS] Processing...")
        accounts_df = self.generate_accounts(800)
        account_file = f"{self.master_data_path}/accounts/accounts_{timestamp}"
        if format.lower() == 'excel':
            saved_path = self.save_to_excel(accounts_df, account_file, 'Accounts')
        else:
            saved_path = self.save_to_csv(accounts_df, account_file)
        generated_files.append({'type': 'accounts', 'path': saved_path, 'count': len(accounts_df)})
        
        # Generate Branches
        print("\n[BRANCHES] Processing...")
        branches_df = self.generate_branches(100)
        branch_file = f"{self.master_data_path}/branches/branches_{timestamp}"
        if format.lower() == 'excel':
            saved_path = self.save_to_excel(branches_df, branch_file, 'Branches')
        else:
            saved_path = self.save_to_csv(branches_df, branch_file)
        generated_files.append({'type': 'branches', 'path': saved_path, 'count': len(branches_df)})
        
        print("\n" + "="*80)
        print(f"✅ COMPLETED: Generated {len(generated_files)} master data files")
        print("="*80)
        
        return generated_files

# COMMAND ----------

# DBTITLE 1,Usage Examples
# MAGIC %md
# MAGIC ## Usage Examples
# MAGIC
# MAGIC Below are examples of how to use the `BankingTestDataGenerator` class to create test data.

# COMMAND ----------

# DBTITLE 1,Initialize the Generator
# Initialize the test data generator
generator = BankingTestDataGenerator(
    base_path=BASE_PATH,
    source_systems=SOURCE_SYSTEMS,
    valid_transaction_types=VALID_TRANSACTION_TYPES
)

print("✅ Test Data Generator initialized successfully")
print(f"\nConfiguration:")
print(f"  Base Path: {BASE_PATH}")
print(f"  Source Systems: {len(SOURCE_SYSTEMS)}")
print(f"  Transaction Types: {len(VALID_TRANSACTION_TYPES)}")

# COMMAND ----------

# DBTITLE 1,Example 1: Generate Single Source Transaction File
# MAGIC %md
# MAGIC ### Example 1: Generate Transaction File for Single Source System

# COMMAND ----------

# DBTITLE 1,Generate ATM Transactions
# Generate 500 ATM transactions and save as CSV
print("Generating ATM transaction file...")
print("="*80)

atm_df = generator.generate_transactions(
    source_system='ATM',
    num_records=500,
    days_back=30
)

# Display sample data
print("\nSample ATM Transactions:")
display(atm_df.head(10))

# Save to CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"{generator.incoming_path}/ATM/atm_transactions_{timestamp}"
saved_file = generator.save_to_csv(atm_df, file_path)

print(f"\n✅ ATM transaction file created: {saved_file}")

# COMMAND ----------

# DBTITLE 1,Example 2: Generate All Transaction Files
# MAGIC %md
# MAGIC ### Example 2: Generate Transaction Files for ALL Source Systems
# MAGIC
# MAGIC This will create transaction files for all configured source systems (ATM, UPI, NEFT, RTGS, CARD, INTERNET_BANKING, MOBILE_BANKING, BRANCH).

# COMMAND ----------

# DBTITLE 1,Generate All Transaction Files (CSV)
# Generate transaction files for all source systems
# Use CSV format for better compatibility

transaction_files = generator.generate_all_transaction_files(
    records_per_source=1000,  # 1000 records per source system
    format='csv'              # Use CSV format
)

# Display summary
print("\n" + "="*80)
print("TRANSACTION FILES SUMMARY")
print("="*80)

for file_info in transaction_files:
    print(f"\n{file_info['source_system']:20} | Records: {file_info['record_count']:6} | Path: {file_info['file_path']}")

print(f"\n{'='*80}")
print(f"Total Files Generated: {len(transaction_files)}")
print(f"Total Records: {sum(f['record_count'] for f in transaction_files):,}")
print("="*80)

# COMMAND ----------

# DBTITLE 1,Example 3: Generate Master Data Files
# MAGIC %md
# MAGIC ### Example 3: Generate Master Data Files (Customers, Accounts, Branches)

# COMMAND ----------

# DBTITLE 1,Generate All Master Data Files
# Generate all master data files
master_files = generator.generate_all_master_data(format='csv')

# Display summary
print("\n" + "="*80)
print("MASTER DATA FILES SUMMARY")
print("="*80)

for file_info in master_files:
    print(f"\n{file_info['type'].upper():20} | Records: {file_info['count']:6} | Path: {file_info['path']}")

print(f"\n{'='*80}")
print(f"Total Master Files: {len(master_files)}")
print(f"Total Records: {sum(f['count'] for f in master_files):,}")
print("="*80)

# COMMAND ----------

# DBTITLE 1,Example 4: Generate Custom Data
# MAGIC %md
# MAGIC ### Example 4: Generate Custom Customer Data and Preview

# COMMAND ----------

# DBTITLE 1,Generate and Preview Customer Data
# Generate custom customer data
customers_df = generator.generate_customers(num_records=100)

print(f"Generated {len(customers_df)} customer records")
print("\nSample Customer Data:")
display(customers_df.head(20))

# Show data statistics
print("\nCustomer Segment Distribution:")
print(customers_df['customer_segment'].value_counts())

print("\nKYC Status Distribution:")
print(customers_df['kyc_status'].value_counts())

# COMMAND ----------

# DBTITLE 1,Example 5: Generate Custom Account Data
# MAGIC %md
# MAGIC ### Example 5: Generate Custom Account Data and Preview

# COMMAND ----------

# DBTITLE 1,Generate and Preview Account Data
# Generate custom account data
accounts_df = generator.generate_accounts(num_records=150)

print(f"Generated {len(accounts_df)} account records")
print("\nSample Account Data:")
display(accounts_df.head(20))

# Show data statistics
print("\nAccount Type Distribution:")
print(accounts_df['account_type'].value_counts())

print("\nAccount Status Distribution:")
print(accounts_df['status'].value_counts())

print("\nAverage Balance by Account Type:")
print(accounts_df.groupby('account_type')['current_balance'].mean().round(2))

# COMMAND ----------

# DBTITLE 1,Example 6: Generate Branch Data
# MAGIC %md
# MAGIC ### Example 6: Generate Branch Master Data

# COMMAND ----------

# DBTITLE 1,Generate and Preview Branch Data
# Generate branch data
branches_df = generator.generate_branches(num_records=50)

print(f"Generated {len(branches_df)} branch records")
print("\nSample Branch Data:")
display(branches_df.head(20))

# Show data statistics
print("\nBranch Distribution by City:")
print(branches_df['city'].value_counts())

print("\nBranch Type Distribution:")
print(branches_df['branch_type'].value_counts())

# COMMAND ----------

# DBTITLE 1,Quick Commands
# MAGIC %md
# MAGIC ## Quick Commands Reference
# MAGIC
# MAGIC ### Generate Everything (Complete Test Data Setup)
# MAGIC
# MAGIC ```python
# MAGIC # Initialize generator
# MAGIC generator = BankingTestDataGenerator(
# MAGIC     base_path=BASE_PATH,
# MAGIC     source_systems=SOURCE_SYSTEMS,
# MAGIC     valid_transaction_types=VALID_TRANSACTION_TYPES
# MAGIC )
# MAGIC
# MAGIC # Generate all transaction files (CSV format)
# MAGIC transaction_files = generator.generate_all_transaction_files(
# MAGIC     records_per_source=1000,
# MAGIC     format='csv'
# MAGIC )
# MAGIC
# MAGIC # Generate all master data files
# MAGIC master_files = generator.generate_all_master_data(format='csv')
# MAGIC
# MAGIC print(f"\n✅ Complete! Generated {len(transaction_files)} transaction files and {len(master_files)} master data files")
# MAGIC ```
# MAGIC
# MAGIC ### Generate Single Source System
# MAGIC
# MAGIC ```python
# MAGIC # For specific source system
# MAGIC df = generator.generate_transactions('UPI', num_records=500)
# MAGIC file_path = f"{generator.incoming_path}/UPI/upi_test_data"
# MAGIC generator.save_to_csv(df, file_path)
# MAGIC ```
# MAGIC
# MAGIC ### Format Options
# MAGIC
# MAGIC * **CSV Format** (Recommended): `format='csv'`
# MAGIC * **Excel Format**: `format='excel'` (may fallback to CSV if Excel writer fails)
# MAGIC
# MAGIC ### Customization Options
# MAGIC
# MAGIC * `records_per_source`: Number of transactions per source system (default: 1000)
# MAGIC * `num_records`: Number of records for master data (customers: 500, accounts: 800, branches: 100)
# MAGIC * `days_back`: Number of days back for transaction timestamps (default: 30)
# MAGIC * `format`: File format - 'csv' or 'excel'

# COMMAND ----------

# DBTITLE 1,One-Click Generate All Test Data
# MAGIC %md
# MAGIC ## 🚀 One-Click: Generate Complete Test Data
# MAGIC
# MAGIC Run this cell to generate all test data in one go!

# COMMAND ----------

# DBTITLE 1,Generate Complete Test Data Suite
def generate_complete_test_data(records_per_source=500, format='csv'):
    """
    One-click function to generate all test data
    
    Args:
        records_per_source: Number of transaction records per source system
        format: 'csv' or 'excel'
    """
    print("\n" + "#"*100)
    print("#" + " "*38 + "BANKING TEST DATA GENERATOR" + " "*35 + "#")
    print("#"*100)
    
    start_time = datetime.now()
    
    try:
        # Initialize generator
        generator = BankingTestDataGenerator(
            base_path=BASE_PATH,
            source_systems=SOURCE_SYSTEMS,
            valid_transaction_types=VALID_TRANSACTION_TYPES
        )
        
        # Step 1: Generate Transaction Files
        print("\n[STEP 1/2] Generating Transaction Files...")
        transaction_files = generator.generate_all_transaction_files(
            records_per_source=records_per_source,
            format=format
        )
        
        # Step 2: Generate Master Data Files
        print("\n[STEP 2/2] Generating Master Data Files...")
        master_files = generator.generate_all_master_data(format=format)
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "#"*100)
        print("#" + " "*42 + "GENERATION COMPLETE" + " "*40 + "#")
        print("#"*100)
        
        print(f"\n✅ Successfully generated all test data!")
        print(f"\n{'Metric':<40} {'Count':>15}")
        print("-"*55)
        print(f"{'Transaction Source Systems':<40} {len(transaction_files):>15}")
        print(f"{'Total Transaction Records':<40} {sum(f['record_count'] for f in transaction_files):>15,}")
        print(f"{'Master Data Types':<40} {len(master_files):>15}")
        print(f"{'Total Master Data Records':<40} {sum(f['count'] for f in master_files):>15,}")
        print(f"{'Total Files Generated':<40} {len(transaction_files) + len(master_files):>15}")
        print(f"{'Execution Time (seconds)':<40} {duration:>15.2f}")
        print("-"*55)
        
        print("\n" + "="*100)
        print("FILES GENERATED:")
        print("="*100)
        
        print("\n[TRANSACTION FILES]")
        for f in transaction_files:
            print(f"  ✓ {f['source_system']:20} - {f['record_count']:5} records")
        
        print("\n[MASTER DATA FILES]")
        for f in master_files:
            print(f"  ✓ {f['type'].upper():20} - {f['count']:5} records")
        
        print("\n" + "="*100)
        print("✅ Test data is ready for pipeline ingestion!")
        print("="*100)
        
        return {
            'transaction_files': transaction_files,
            'master_files': master_files,
            'duration': duration
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        raise

# Example: Uncomment to run
# result = generate_complete_test_data(records_per_source=500, format='csv')

# COMMAND ----------

# DBTITLE 1,Verification and Next Steps
# MAGIC %md
# MAGIC ## ✅ Verification & Next Steps
# MAGIC
# MAGIC ### Verify Generated Files
# MAGIC
# MAGIC ```python
# MAGIC # Check incoming folder
# MAGIC for source in SOURCE_SYSTEMS:
# MAGIC     path = f"{BASE_PATH}/incoming/{source}"
# MAGIC     try:
# MAGIC         files = dbutils.fs.ls(path)
# MAGIC         print(f"{source:20} - {len(files)} file(s)")
# MAGIC     except:
# MAGIC         print(f"{source:20} - No files")
# MAGIC
# MAGIC # Check master data folder
# MAGIC for data_type in ['customers', 'accounts', 'branches']:
# MAGIC     path = f"{BASE_PATH}/master_data/{data_type}"
# MAGIC     try:
# MAGIC         files = dbutils.fs.ls(path)
# MAGIC         print(f"{data_type:20} - {len(files)} file(s)")
# MAGIC     except:
# MAGIC         print(f"{data_type:20} - No files")
# MAGIC ```
# MAGIC
# MAGIC ### Run Your Pipeline
# MAGIC
# MAGIC After generating test data:
# MAGIC
# MAGIC 1. **Run 03_Ingestion** notebook to ingest transaction files into Bronze layer
# MAGIC 2. **Run 02_Master_Data_Load** to load customer, account, and branch data
# MAGIC 3. **Run 04_Data_Validation** to validate and cleanse data
# MAGIC 4. **Run remaining notebooks** to complete the pipeline
# MAGIC
# MAGIC ### Tips
# MAGIC
# MAGIC * **CSV Format** is recommended for better compatibility with Spark Auto Loader
# MAGIC * Start with **smaller datasets** (100-500 records) for testing
# MAGIC * Increase to **1000+ records** for performance testing
# MAGIC * Monitor execution time and adjust batch sizes accordingly

# COMMAND ----------



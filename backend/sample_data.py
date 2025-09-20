"""
Sample AS/400 data files for demonstration purposes
"""

# Sample AS/400 Flat File (Fixed Width)
SAMPLE_FLAT_FILE = """CUST001JOHN DOE    123 MAIN ST    NEW YORK    NY10001 555-0123
CUST002JANE SMITH  456 OAK AVE   CHICAGO     IL60601 555-0456
CUST003BOB JOHNSON 789 PINE RD   LOS ANGELES CA90210 555-0789
CUST004ALICE BROWN 321 ELM ST    HOUSTON     TX77001 555-0321
CUST005CHARLIE WILSON 654 MAPLE DR MIAMI     FL33101 555-0654"""

# Sample AS/400 Flat File (Delimited)
SAMPLE_DELIMITED_FILE = """CUST_ID|CUST_NAME|ADDRESS|CITY|STATE|ZIP|PHONE
CUST001|JOHN DOE|123 MAIN ST|NEW YORK|NY|10001|555-0123
CUST002|JANE SMITH|456 OAK AVE|CHICAGO|IL|60601|555-0456
CUST003|BOB JOHNSON|789 PINE RD|LOS ANGELES|CA|90210|555-0789
CUST004|ALICE BROWN|321 ELM ST|HOUSTON|TX|77001|555-0321
CUST005|CHARLIE WILSON|654 MAPLE DR|MIAMI|FL|33101|555-0654"""

# Sample DB2 Table Definition (DDS)
SAMPLE_DDS_FILE = """A                                      UNIQUE
A          R CUSTOMER
A            CUSTID         10A        TEXT('Customer ID')
A            CUSTNAME       30A        TEXT('Customer Name')
A            ADDRESS        50A        TEXT('Street Address')
A            CITY           20A        TEXT('City')
A            STATE           2A        TEXT('State')
A            ZIPCODE         5A        TEXT('ZIP Code')
A            PHONE          12A        TEXT('Phone Number')
A            CREATEDATE      8A        TEXT('Creation Date')
A            STATUS          1A        TEXT('Status')
A          K CUSTID"""

# Sample DB2 Table Definition (SQL)
SAMPLE_SQL_FILE = """CREATE TABLE CUSTOMER (
    CUSTID CHAR(10) NOT NULL,
    CUSTNAME VARCHAR(30) NOT NULL,
    ADDRESS VARCHAR(50),
    CITY VARCHAR(20),
    STATE CHAR(2),
    ZIPCODE CHAR(5),
    PHONE VARCHAR(12),
    CREATEDATE DATE,
    STATUS CHAR(1) DEFAULT 'A',
    PRIMARY KEY (CUSTID)
);"""

# Sample Green Screen Interface
SAMPLE_GREEN_SCREEN = """Customer Information System
=====================================

Customer ID: [CUST001    ]
Name:        [JOHN DOE                    ]
Address:     [123 MAIN ST                 ]
City:        [NEW YORK            ]
State:      [NY]
ZIP:        [10001]
Phone:      [555-0123]

F3=Exit  F5=Refresh  F12=Cancel
=====================================

Function: [DSP]  (DSP=Display, UPD=Update, ADD=Add, DEL=Delete)
"""

# Sample RPG Program
SAMPLE_RPG_PROGRAM = """     H DEBUG(*YES)
     F* Customer Master File
     FCUSTOMER  IF   E           K DISK
     F* Display File
     FDSPCUST   CF   E             WORKSTN
     D* Data Structures
     D CustomerDS       DS
     D  CustID                10A
     D  CustName              30A
     D  Address               50A
     D  City                  20A
     D  State                  2A
     D  ZipCode                5A
     D  Phone                 12A
     D  CreateDate             8A
     D  Status                 1A
     C* Main Procedure
     C                   BEGSR
     C                   EXSR ReadCustomer
     C                   ENDSR
     C* Read Customer Record
     C     ReadCustomer  BEGSR
     C                   READ CUSTOMER
     C                   IF %EOF
     C                   EXSR EndProgram
     C                   ENDIF
     C                   MOVE CUSTID CustomerDS.CustID
     C                   MOVE CUSTNAME CustomerDS.CustName
     C                   MOVE ADDRESS CustomerDS.Address
     C                   MOVE CITY CustomerDS.City
     C                   MOVE STATE CustomerDS.State
     C                   MOVE ZIPCODE CustomerDS.ZipCode
     C                   MOVE PHONE CustomerDS.Phone
     C                   MOVE CREATEDATE CustomerDS.CreateDate
     C                   MOVE STATUS CustomerDS.Status
     C                   ENDSR
     C* End Program
     C     EndProgram    BEGSR
     C                   SETON LR
     C                   ENDSR"""

# Sample Order Data (Fixed Width)
SAMPLE_ORDER_FILE = """ORD001CUST001202401011000.50A
ORD002CUST002202401021500.75A
ORD003CUST001202401031200.25A
ORD004CUST003202401042000.00A
ORD005CUST002202401051750.30A"""

# Sample Product Data (Delimited)
SAMPLE_PRODUCT_FILE = """PROD_ID|PROD_NAME|CATEGORY|PRICE|STOCK_QTY|STATUS
PROD001|Widget A|Electronics|29.99|100|A
PROD002|Widget B|Electronics|39.99|50|A
PROD003|Gadget X|Tools|19.99|200|A
PROD004|Gadget Y|Tools|24.99|75|A
PROD005|Thing Z|Accessories|9.99|300|A"""

# Sample Employee Data (DDS)
SAMPLE_EMPLOYEE_DDS = """A                                      UNIQUE
A          R EMPLOYEE
A            EMPID           6A         TEXT('Employee ID')
A            EMPNAME         25A        TEXT('Employee Name')
A            DEPT            10A        TEXT('Department')
A            JOBTITLE        20A        TEXT('Job Title')
A            SALARY          7P 2       TEXT('Annual Salary')
A            HIREDATE        8A         TEXT('Hire Date')
A            STATUS          1A         TEXT('Status')
A          K EMPID"""

# Sample Inventory Data (Fixed Width)
SAMPLE_INVENTORY_FILE = """ITEM001WIDGET A     ELECTRONICS 29.99 100 A
ITEM002WIDGET B     ELECTRONICS 39.99  50 A
ITEM003GADGET X     TOOLS       19.99 200 A
ITEM004GADGET Y     TOOLS       24.99  75 A
ITEM005THING Z      ACCESSORIES  9.99 300 A"""

# Sample Financial Data (Delimited)
SAMPLE_FINANCIAL_FILE = """ACCT_ID|ACCT_NAME|ACCT_TYPE|BALANCE|STATUS|OPEN_DATE
100001|Cash Account|Asset|50000.00|A|20240101
100002|Accounts Receivable|Asset|25000.00|A|20240101
200001|Accounts Payable|Liability|15000.00|A|20240101
300001|Retained Earnings|Equity|60000.00|A|20240101
400001|Sales Revenue|Revenue|100000.00|A|20240101"""

def get_sample_data():
    """Return all sample data files"""
    return {
        "flat_file_fixed": SAMPLE_FLAT_FILE,
        "flat_file_delimited": SAMPLE_DELIMITED_FILE,
        "dds_file": SAMPLE_DDS_FILE,
        "sql_file": SAMPLE_SQL_FILE,
        "green_screen": SAMPLE_GREEN_SCREEN,
        "rpg_program": SAMPLE_RPG_PROGRAM,
        "order_file": SAMPLE_ORDER_FILE,
        "product_file": SAMPLE_PRODUCT_FILE,
        "employee_dds": SAMPLE_EMPLOYEE_DDS,
        "inventory_file": SAMPLE_INVENTORY_FILE,
        "financial_file": SAMPLE_FINANCIAL_FILE
    }

def create_sample_files():
    """Create sample files in the backend directory"""
    import os
    
    sample_dir = "sample_files"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    
    samples = get_sample_data()
    
    for filename, content in samples.items():
        filepath = os.path.join(sample_dir, f"{filename}.txt")
        with open(filepath, 'w') as f:
            f.write(content)
    
    print(f"Created {len(samples)} sample files in {sample_dir}/")

if __name__ == "__main__":
    create_sample_files()

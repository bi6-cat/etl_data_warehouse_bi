CREATE DATABASE DB_mart
ON 
( NAME = CustomerDB_Data, FILENAME = 'E:\UNIVERSITY SUBJECTS\PTIT subjects\Database management system\DB_mart.mdf', SIZE = 10MB, MAXSIZE = 100MB, FILEGROWTH = 5MB )
LOG ON 
( NAME = CustomerDB_Log, FILENAME = 'E:\UNIVERSITY SUBJECTS\PTIT subjects\Database management system\DB_mart.ldf', SIZE = 5MB, MAXSIZE = 50MB, FILEGROWTH = 2MB );

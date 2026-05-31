-- SQL Server Schema for Book Rental System
-- Character set: Unicode (nvarchar)

IF EXISTS (SELECT name FROM sys.databases WHERE name = 'BookRentalDB')
    DROP DATABASE BookRentalDB;

CREATE DATABASE BookRentalDB
    COLLATE Latin1_General_CI_AS;

USE BookRentalDB;

-- Table: Customers
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerCode VARCHAR(20) UNIQUE NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    Phone VARCHAR(20),
    Address NVARCHAR(200),
    Email VARCHAR(100),
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);

-- Table: Users
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(20) NOT NULL CHECK (Role IN ('Admin', 'Customer')),
    CustomerID INT,
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE SET NULL
);

-- Table: Books
CREATE TABLE Books (
    BookID INT IDENTITY(1,1) PRIMARY KEY,
    BookCode VARCHAR(20) UNIQUE NOT NULL,
    Title NVARCHAR(200) NOT NULL,
    Author NVARCHAR(100) NOT NULL,
    Category NVARCHAR(100),
    Publisher NVARCHAR(100),
    PublishYear INT,
    BookStatus VARCHAR(20) NOT NULL DEFAULT 'Available' CHECK (BookStatus IN ('Available', 'Rented', 'Damaged', 'Lost')),
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);

-- Table: RentalOrders
CREATE TABLE RentalOrders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    OrderCode VARCHAR(20) UNIQUE NOT NULL,
    CustomerID INT NOT NULL,
    RentDate DATETIME NOT NULL,
    ExpectedReturnDate DATETIME NOT NULL,
    ReturnDate DATETIME,
    OrderStatus VARCHAR(20) NOT NULL DEFAULT 'Renting' CHECK (OrderStatus IN ('Renting', 'Returned', 'Overdue')),
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE RESTRICT,
    INDEX idx_customer (CustomerID),
    INDEX idx_status (OrderStatus)
);

-- Table: RentalOrderDetails
CREATE TABLE RentalOrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    BookID INT NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE(),
    UNIQUE (OrderID, BookID),
    FOREIGN KEY (OrderID) REFERENCES RentalOrders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID) ON DELETE RESTRICT,
    INDEX idx_book (BookID)
);

-- Create Indexes
CREATE INDEX idx_users_username ON Users(Username);
CREATE INDEX idx_customers_code ON Customers(CustomerCode);
CREATE INDEX idx_books_code ON Books(BookCode);
CREATE INDEX idx_orders_code ON RentalOrders(OrderCode);

-- Create default Admin account
INSERT INTO Users (Username, Password, Role) VALUES ('admin', '123', 'Admin');

-- Insert sample data
INSERT INTO Customers (CustomerCode, FullName, Phone, Address, Email) VALUES
('C001', N'Nguyễn Thanh Bình', '0900111222', N'Hà Nội', 'binh.nt@email.com'),
('C002', N'Lê Thị Hoa', '0911222333', N'Đà Nẵng', 'hoa.le@email.com');

INSERT INTO Books (BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus) VALUES
('IT01', N'Python Cơ Bản', N'Nguyễn Văn A', N'Công nghệ thông tin', N'NXB Giáo Dục', 2021, 'Available'),
('IT02', N'Lập Trình C++ Nâng Cao', N'Lê B', N'Công nghệ thông tin', N'NXB Trẻ', 2020, 'Available');
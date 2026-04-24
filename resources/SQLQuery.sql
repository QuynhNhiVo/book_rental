USE BookRentalDB;
GO

-- 1. Tạo bảng Khách hàng (Customers)
CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerCode VARCHAR(20) UNIQUE NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    Phone VARCHAR(20),
    Address NVARCHAR(200),
    Email VARCHAR(100)
);
GO

-- 2. Tạo bảng Người dùng (Users)
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    UserName VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Role VARCHAR(20) NOT NULL,
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID)
);
GO

-- 3. Tạo bảng Sách (Books)
CREATE TABLE Books (
    BookID INT IDENTITY(1,1) PRIMARY KEY,
    BookCode VARCHAR(20) UNIQUE NOT NULL,
    Title NVARCHAR(200) NOT NULL,
    Author NVARCHAR(100) NOT NULL,
    Category NVARCHAR(100),
    Publisher NVARCHAR(100),
    PublishYear INT,
    BookStatus VARCHAR(20) NOT NULL
);
GO

-- 4. Tạo bảng Đơn thuê sách (RentalOrders)
CREATE TABLE RentalOrders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    OrderCode VARCHAR(20) UNIQUE NOT NULL,
    CustomerID INT NOT NULL FOREIGN KEY REFERENCES Customers(CustomerID),
    RentDate DATETIME NOT NULL,
    ExpectedReturnDate DATETIME NOT NULL,
    ReturnDate DATETIME,
    OrderStatus VARCHAR(20) NOT NULL
);
GO

-- 5. Tạo bảng Chi tiết đơn thuê (RentalOrderDetails)
CREATE TABLE RentalOrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL FOREIGN KEY REFERENCES RentalOrders(OrderID),
    BookID INT NOT NULL FOREIGN KEY REFERENCES Books(BookID)
);
GO

PRINT N'✅ Đã tạo cấu trúc 5 bảng thành công!';

USE BookRentalDB;
GO

-- 1. Xóa dữ liệu theo trình tự ngược (con trước cha sau) để tránh lỗi ràng buộc
DELETE FROM RentalOrderDetails;
DELETE FROM RentalOrders;
DELETE FROM Users;
DELETE FROM Customers;
DELETE FROM Books;

-- 2. Đặt lại bộ đếm ID về 0
DBCC CHECKIDENT ('RentalOrderDetails', RESEED, 0);
DBCC CHECKIDENT ('RentalOrders', RESEED, 0);
DBCC CHECKIDENT ('Users', RESEED, 0);
DBCC CHECKIDENT ('Customers', RESEED, 0);
DBCC CHECKIDENT ('Books', RESEED, 0);
GO

-- 3. Nạp Khách hàng
INSERT INTO Customers (CustomerCode, FullName, Phone, Address, Email) VALUES
('C001', N'Nguyễn Thanh Bình', '0900111222', N'Hà Nội', 'binh.nt@email.com'), -- ID sẽ là 1
('C002', N'Lê Thị Hoa', '0911222333', N'Đà Nẵng', 'hoa.le@email.com'),      -- ID sẽ là 2
('C003', N'Trần Tuấn Anh', '0922333444', N'TP.HCM', 'anh.tran@email.com'),   -- ID sẽ là 3
('C004', N'Phạm Mai Phương', '0933444555', N'Cần Thơ', 'phuong.pm@email.com'),-- ID sẽ là 4
('C005', N'Hoàng Khắc Tiệp', '0944555666', N'Hải Phòng', 'tiep.hk@email.com');-- ID sẽ là 5

-- 4. Nạp Users (Đảm bảo CustomerID 1, 2, 3, 4, 5 đã tồn tại ở bước trên)
INSERT INTO Users (UserName, Password, Role, CustomerID) VALUES
('admin_vip', '123456', 'Admin', NULL),
('binhnt', '123', 'Customer', 1),
('hoale', '123', 'Customer', 2),
('tuananh', '123', 'Customer', 3),
('maiphuong', '123', 'Customer', 4),
('khactiep', '123', 'Customer', 5);

-- 5. Nạp Sách
INSERT INTO Books (BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus) VALUES
('IT01', N'Python Cơ Bản', N'Nguyễn Văn A', N'Công nghệ thông tin', N'NXB Giáo Dục', 2021, 'Rented'),
('IT02', N'Lập Trình C++ Nâng Cao', N'Lê B', N'Công nghệ thông tin', N'NXB Trẻ', 2020, 'Available'),
('IT03', N'Cấu Trúc Dữ Liệu', N'Trần C', N'Công nghệ thông tin', N'NXB Khoa Học', 2019, 'Rented'),
('LIT01', N'Chí Phèo', N'Nam Cao', N'Văn học Việt Nam', N'NXB Văn Học', 2015, 'Available'),
('LIT02', N'Tắt Đèn', N'Ngô Tất Tố', N'Văn học Việt Nam', N'NXB Văn Học', 2016, 'Rented'),
('SCI01', N'Lược Sử Thời Gian', N'Stephen Hawking', N'Khoa học', N'NXB Trẻ', 2018, 'Available'),
('SCI02', N'Vũ Trụ', N'Carl Sagan', N'Khoa học', N'NXB Thế Giới', 2020, 'Rented'),
('ECO01', N'Tư Duy Nhanh Và Chậm', N'Daniel Kahneman', N'Kinh tế', N'NXB Tổng Hợp', 2021, 'Available'),
('ECO02', N'Cha Giàu Cha Nghèo', N'Robert Kiyosaki', N'Kinh tế', N'NXB Trẻ', 2019, 'Available'),
('SKILL1', N'Muôn Kiếp Nhân Sinh', N'Nguyên Phong', N'Kỹ năng sống', N'NXB Tổng Hợp', 2020, 'Rented');

-- 6. Nạp Đơn thuê (RentalOrders)
INSERT INTO RentalOrders (OrderCode, CustomerID, RentDate, ExpectedReturnDate, ReturnDate, OrderStatus) VALUES
('ORD_2023_001', 1, '2023-10-01', '2023-10-15', '2023-10-14', 'Returned'), -- ID 1
('ORD_2023_002', 2, '2023-11-01', '2023-11-15', NULL, 'Renting'),         -- ID 2
('ORD_2023_003', 3, '2023-09-01', '2023-09-10', NULL, 'Renting'),         -- ID 3
('ORD_2023_004', 4, '2023-08-01', '2023-08-10', '2023-08-09', 'Returned'), -- ID 4
('ORD_2023_005', 5, '2023-11-10', '2023-11-20', NULL, 'Renting');         -- ID 5

-- 7. Nạp Chi tiết đơn thuê (RentalOrderDetails)
-- Chú ý: Cần đảm bảo ID của Order và Book khớp với dữ liệu vừa nạp
INSERT INTO RentalOrderDetails (OrderID, BookID) VALUES
(1, 2), (1, 4), 
(2, 1), (2, 3), 
(3, 5), (3, 7), 
(4, 8), (4, 9), 
(5, 10);
GO

PRINT N'✅ Đã nạp dữ liệu TEST thành công không còn lỗi ràng buộc!';
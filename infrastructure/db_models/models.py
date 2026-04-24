from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, NVARCHAR, VARCHAR
from sqlalchemy.orm import relationship
from .base import Base

class UserModel(Base):
    __tablename__ = 'Users'
    # Dữ liệu
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(VARCHAR(50), unique=True, nullable=False)
    Password = Column(VARCHAR(100), nullable=False)
    Role = Column(VARCHAR(20), nullable=False)
    CustomerID = Column(Integer, ForeignKey('Customers.CustomerID'), nullable=True)

    customer = relationship("CustomerModel", back_populates="user", uselist=False)
    
class CustomerModel(Base):
    __tablename__ = 'Customers'
    CustomerID = Column(Integer, primary_key=True, autoincrement=True) 
    CustomerCode = Column(VARCHAR(20), unique=True, nullable=False) 
    FullName = Column(NVARCHAR(100), nullable=False)
    Phone = Column(VARCHAR(20), nullable=True)
    Address = Column(NVARCHAR(200), nullable=True)
    Email = Column(VARCHAR(100), nullable=True)

    user = relationship("UserModel", back_populates="customer")
    orders = relationship("RentalOrderModel", back_populates="customer")

class BookModel(Base):
    __tablename__ = 'Books'

    BookID = Column(Integer, primary_key=True, autoincrement=True)
    BookCode = Column(VARCHAR(20), unique=True, nullable=False)
    Title = Column(NVARCHAR(200), nullable=False)
    Author = Column(NVARCHAR(100), nullable=False)
    Category = Column(NVARCHAR(100), nullable=True)
    Publisher = Column(NVARCHAR(100), nullable=True)
    PublishYear = Column(Integer, nullable=True)
    BookStatus = Column(VARCHAR(20), nullable=False)

    order_details = relationship("RentalOrderDetailModel", back_populates="book")


class RentalOrderModel(Base):
    __tablename__ = 'RentalOrders'

    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    OrderCode = Column(VARCHAR(20), unique=True, nullable=False)
    CustomerID = Column(Integer, ForeignKey('Customers.CustomerID'), nullable=False)
    RentDate = Column(DateTime, nullable=False)
    ExpectedReturnDate = Column(DateTime, nullable=False)
    ReturnDate = Column(DateTime, nullable=True)
    OrderStatus = Column(VARCHAR(20), nullable=False)

    customer = relationship("CustomerModel", back_populates="orders")
    details = relationship("RentalOrderDetailModel", back_populates="order", cascade="all, delete-orphan")


class RentalOrderDetailModel(Base):
    __tablename__ = 'RentalOrderDetails'

    OrderDetailID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('RentalOrders.OrderID'), nullable=False)
    BookID = Column(Integer, ForeignKey('Books.BookID'), nullable=False)

    order = relationship("RentalOrderModel", back_populates="details")
    book = relationship("BookModel", back_populates="order_details")
from sqlalchemy.orm import Session
from infrastructure.db_models.models import CustomerModel
from domain.models.customer import Customer
from sqlalchemy import or_

class CustomerRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, customer_id: int):
        return self.db.query(CustomerModel).filter(CustomerModel.CustomerID == customer_id).first()

    def get_by_code(self, customer_code: str):
        return self.db.query(CustomerModel).filter(CustomerModel.CustomerCode == customer_code).first()

    def get_all(self):
        return self.db.query(CustomerModel).all()

    def add_customer(self, customer: Customer):
        new_customer = CustomerModel(
            CustomerCode=customer.customer_code,
            FullName=customer.full_name,
            Phone=customer.phone,
            Address=customer.address,
            Email=customer.email
        )
        self.db.add(new_customer)
        self.db.commit()
        return new_customer
    
    def search_customers(self, keyword: str):
        """Tìm kiếm khách hàng theo Mã, Tên hoặc Số điện thoại"""
        # Sử dụng ilike để tìm kiếm không phân biệt hoa thường và chứa từ khóa (LIKE %keyword%)
        return self.db.query(CustomerModel).filter(
            or_(
                CustomerModel.CustomerCode.ilike(f"%{keyword}%"),
                CustomerModel.FullName.ilike(f"%{keyword}%"),
                CustomerModel.Phone.ilike(f"%{keyword}%")
            )
        ).all()
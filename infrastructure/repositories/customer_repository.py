from sqlalchemy.orm import Session
from infrastructure.db_models.models import CustomerModel
from domain.models.customer import Customer

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
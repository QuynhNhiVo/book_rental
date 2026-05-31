from ..models.customer import Customer
from ..utils.exceptions import CustomerNotFoundError

class CustomerService:
    """
    Service quản lý các nghiệp vụ liên quan đến Khách hàng.
    """
    
    def __init__(self, customer_repository):
        self.customer_repo = customer_repository
    
    def create_customer(self, customer: Customer) -> int:
        return self.customer_repo.create(customer)
    
    def get_all_customers(self) -> list:
        return self.customer_repo.get_all()
    
    def get_customer_by_id(self, customer_id: int) -> Customer:
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(customer_id=customer_id)
        return customer
    
    def update_customer(self, customer: Customer) -> bool:
        if not self.customer_repo.get_by_id(customer.customer_id):
            raise CustomerNotFoundError(customer_id=customer.customer_id)
        return self.customer_repo.update(customer)
    
    def delete_customer(self, customer_id: int) -> bool:
        if not self.customer_repo.get_by_id(customer_id):
            raise CustomerNotFoundError(customer_id=customer_id)
        return self.customer_repo.delete(customer_id)

from domain.models.customer import Customer

class CustomerService:
    def __init__(self, customer_repository, order_repository):
        self.customer_repo = customer_repository
        self.order_repo = order_repository # Cần OrderRepo để check rule khi xóa

    def add_customer(self, customer: Customer):
        """Thêm khách hàng"""
        existing = self.customer_repo.get_by_code(customer.customer_code)
        if existing:
            raise ValueError("Lỗi: Mã khách hàng đã tồn tại.")
        return self.customer_repo.add_customer(customer)

    def get_all_customers(self):
        return self.customer_repo.get_all()

    def search_customers(self, keyword: str):
        """Tìm khách hàng theo mã, tên, SĐT"""
        if not keyword:
            return self.customer_repo.get_all()
        return self.customer_repo.search_customers(keyword)

    def delete_customer(self, customer_code: str):
        """Xóa khách hàng"""
        customer = self.customer_repo.get_by_code(customer_code)
        if not customer:
            raise ValueError("Không tìm thấy khách hàng.")
    
        # Quy tắc: Không cho xóa khách hàng nếu đang có đơn thuê chưa trả
        has_active_orders = self.order_repo.check_active_orders_by_customer(customer.customer_id)
        if has_active_orders:
            raise ValueError("Từ chối xóa: Khách hàng này đang có đơn thuê chưa trả.")
            
        return self.customer_repo.delete_customer(customer_code)
    
    def update_customer(self, customer_code: str, update_data: dict):
        customer = self.customer_repo.get_by_code(customer_code)
        if not customer:
            raise ValueError("Không tìm thấy khách hàng.")
        return self.customer_repo.update(customer.CustomerID, update_data)
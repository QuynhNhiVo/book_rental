from datetime import datetime, timedelta

class ReportService:
    """
    Service xử lý các báo cáo và thống kê.
    """
    
    def __init__(self, book_repository, order_repository, customer_repository):
        self.book_repo = book_repository
        self.order_repo = order_repository
        self.customer_repo = customer_repository
    
    def get_system_statistics(self) -> dict:
        """Thống kê tổng quan cho Admin."""
        book_stats = self.book_repo.get_rental_statistics()
        customers = self.customer_repo.get_all()
        all_orders = self.order_repo.get_all()
        active_orders = sum(1 for o in all_orders if o.order_status == 'Renting')
        
        return {
            'total_books': book_stats.get('available_count', 0) + book_stats.get('rented_count', 0),
            'available_books': book_stats.get('available_count', 0),
            'rented_books': book_stats.get('rented_count', 0),
            'total_customers': len(customers),
            'active_orders': active_orders
        }
    
    def get_user_statistics(self, customer_id: int) -> dict:
        """Thống kê cá nhân cho User/Customer."""
        if not customer_id:
            return {
                'current_rentals': 0,
                'active_rentals': 0,
                'completed_rentals': 0,
                'total_history': 0,
                'available_books': 0
            }

        all_user_orders = self.order_repo.get_customer_orders(customer_id)
        book_stats = self.book_repo.get_rental_statistics()
        
        active_rentals = [o for o in all_user_orders if o.order_status == 'Renting']
        completed_rentals = [o for o in all_user_orders if o.order_status == 'Returned']
        
        return {
            'current_rentals': len(active_rentals),
            'active_rentals': len(active_rentals),
            'completed_rentals': len(completed_rentals),
            'total_history': len(all_user_orders),
            'available_books': book_stats.get('available_count', 0)
        }

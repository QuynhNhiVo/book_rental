class ReportService:
    def __init__(self, book_repository, order_repository):
        self.book_repo = book_repository
        self.order_repo = order_repository

    def get_inventory_stats(self):
        """Thống kê sách đang được thuê và sách có sẵn [cite: 185, 186]"""
        books = self.book_repo.get_all()
        rented = sum(1 for b in books if b.BookStatus == 'Rented')
        available = sum(1 for b in books if b.BookStatus == 'Available')
        
        return {
            "Total": len(books),
            "Available": available,
            "Rented": rented
        }

    def get_book_rental_frequency(self):
        """Thống kê số lượt thuê theo sách [cite: 187]"""
        # Gọi hàm được viết riêng bằng raw SQLAlchemy group_by trong OrderRepository
        return self.order_repo.get_rental_frequency_stats()
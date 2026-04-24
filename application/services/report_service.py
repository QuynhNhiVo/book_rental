from sqlalchemy import func
from infrastructure.db_models.models import BookModel, RentalOrderDetailModel

class ReportService:
    def __init__(self, book_repository, order_repository):
        self.book_repo = book_repository
        self.order_repo = order_repository

    def get_inventory_stats(self):
        """Thống kê sách đang được thuê và sách có sẵn"""
        books = self.book_repo.get_all()
        rented = sum(1 for b in books if b.BookStatus == 'Rented')
        available = sum(1 for b in books if b.BookStatus == 'Available')
        
        return {
            "Total": len(books),
            "Available": available,
            "Rented": rented
        }

    def get_book_rental_frequency(self):
        """Thống kê số lượt thuê theo sách"""
        # Truy vấn Group By trực tiếp bằng SQLAlchemy session
        session = self.book_repo.db
        results = session.query(
            BookModel.BookCode,
            BookModel.Title,
            func.count(RentalOrderDetailModel.BookID).label('RentalCount')
        ).join(RentalOrderDetailModel, BookModel.BookID == RentalOrderDetailModel.BookID) \
         .group_by(BookModel.BookCode, BookModel.Title) \
         .order_by(func.count(RentalOrderDetailModel.BookID).desc()).all()
        
        return [{"BookCode": r.BookCode, "Title": r.Title, "RentalCount": r.RentalCount} for r in results]
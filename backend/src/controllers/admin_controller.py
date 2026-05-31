from flask import request, jsonify, g
from ..models.book import Book

class AdminController:
    """
    Controller xử lý các yêu cầu của quản trị viên (Admin).
    """
    def __init__(self, book_service, customer_service, order_service, report_service):
        self.book_service = book_service
        self.customer_service = customer_service
        self.order_service = order_service
        self.report_service = report_service

    def get_all_books(self):
        books = self.book_service.get_all_books()
        return jsonify({'success': True, 'data': [b.to_dict() for b in books]})

    def create_book(self):
        try:
            data = request.get_json()
            book = Book(
                book_code=data['book_code'],
                title=data['title'],
                author=data['author'],
                category=data.get('category'),
                publisher=data.get('publisher'),
                publish_year=data.get('publish_year')
            )
            self.book_service.create_book(book)
            return jsonify({'success': True, 'message': 'Thêm sách thành công'}), 201
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

    def get_stats(self):
        stats = self.report_service.get_system_statistics()
        return jsonify({'success': True, 'data': stats})

    def get_all_orders(self):
        orders = self.order_service.get_all_orders()
        return jsonify({'success': True, 'data': [o.__dict__ for o in orders]})

    def return_book(self, order_id):
        try:
            self.order_service.process_return(order_id)
            return jsonify({'success': True, 'message': 'Đã trả sách thành công'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400
            
    def get_all_customers(self):
        customers = self.customer_service.get_all_customers()
        return jsonify({'success': True, 'data': [{'id': c.customer_id, 'code': c.customer_code, 'name': c.fullname} for c in customers]})

from flask import request, jsonify, g
from datetime import datetime
from ..models.order import RentalOrder

class UserController:
    """
    Controller xử lý các yêu cầu từ phía khách hàng (Customer).
    """
    def __init__(self, book_service, order_service, report_service):
        self.book_service = book_service
        self.order_service = order_service
        self.report_service = report_service

    def get_books(self):
        books = self.book_service.get_all_books()
        return jsonify({'success': True, 'data': [b.to_dict() for b in books]})

    def create_rental(self):
        try:
            data = request.get_json()
            cid = g.auth_context.get('customer_id')
            if not cid:
                return jsonify({'success': False, 'message': 'Không tìm thấy thông tin khách hàng.'}), 400
            
            expected_date = datetime.fromisoformat(data['expected_return_date'])
            order = RentalOrder(
                order_code=f"UORD{int(datetime.now().timestamp())}",
                customer_id=cid,
                rent_date=datetime.now(),
                expected_return_date=expected_date
            )
            oid = self.order_service.create_order(order, data['book_ids'])
            return jsonify({'success': True, 'message': 'Thuê sách thành công!', 'data': {'order_id': oid}}), 201
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

    def get_current_rentals(self):
        cid = g.auth_context.get('customer_id')
        orders = self.order_service.get_customer_renting_orders(cid)
        return jsonify({'success': True, 'data': [o.__dict__ for o in orders]})

    def get_history(self):
        cid = g.auth_context.get('customer_id')
        orders = self.order_service.get_customer_orders(cid)
        return jsonify({'success': True, 'data': [o.__dict__ for o in orders]})

    def get_dashboard_stats(self):
        try:
            cid = g.auth_context.get('customer_id')
            stats = self.report_service.get_user_statistics(cid)
            return jsonify({'success': True, 'data': stats})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

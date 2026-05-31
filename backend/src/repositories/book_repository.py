from ..configs.database import get_connection, execute_query, fetch_one, fetch_query
from ..models.book import Book

class BookRepository:
    """
    Repository quản lý dữ liệu Sách.
    """
    
    def create(self, book: Book) -> int:
        conn = get_connection()
        if not conn: return None
        try:
            query = """
                INSERT INTO Books (BookCode, Title, Author, Category, Publisher, PublishYear, BookStatus)
                VALUES (@book_code, @title, @author, @category, @publisher, @publish_year, @book_status)
            """
            return execute_query(conn, query, {
                'book_code': book.book_code, 
                'title': book.title, 
                'author': book.author, 
                'category': book.category, 
                'publisher': book.publisher, 
                'publish_year': book.publish_year, 
                'book_status': book.book_status
            })
        finally:
            conn.close()
    
    def get_by_id(self, book_id: int) -> Book:
        conn = get_connection()
        if not conn: return None
        try:
            query = "SELECT * FROM Books WHERE BookID = @book_id"
            result = fetch_one(conn, query, {'book_id': book_id})
            return self._map_to_book(result) if result else None
        finally:
            conn.close()

    def get_all(self) -> list:
        conn = get_connection()
        if not conn: return []
        try:
            query = "SELECT * FROM Books ORDER BY BookCode"
            results = fetch_query(conn, query)
            return [self._map_to_book(row) for row in results]
        finally:
            conn.close()

    def update(self, book: Book) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            query = """
                UPDATE Books 
                SET BookCode = @book_code, Title = @title, Author = @author, Category = @category,
                    Publisher = @publisher, PublishYear = @publish_year, BookStatus = @book_status
                WHERE BookID = @book_id
            """
            result = execute_query(conn, query, {
                'book_code': book.book_code, 'title': book.title, 'author': book.author, 
                'category': book.category, 'publisher': book.publisher, 
                'publish_year': book.publish_year, 'book_status': book.book_status, 
                'book_id': book.book_id
            })
            return result is not None
        finally:
            conn.close()

    def delete(self, book_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            query = "DELETE FROM Books WHERE BookID = @book_id"
            result = execute_query(conn, query, {'book_id': book_id})
            return result is not None
        finally:
            conn.close()

    def get_rental_statistics(self) -> dict:
        conn = get_connection()
        if not conn: return {}
        try:
            available = fetch_one(conn, "SELECT COUNT(*) as count FROM Books WHERE BookStatus = 'Available'")
            rented = fetch_one(conn, "SELECT COUNT(*) as count FROM Books WHERE BookStatus = 'Rented'")
            return {
                'available_count': available.get('count', 0) if available else 0,
                'rented_count': rented.get('count', 0) if rented else 0
            }
        finally:
            conn.close()

    def _map_to_book(self, row: dict) -> Book:
        return Book(
            book_id=row.get('BookID'),
            book_code=row.get('BookCode'),
            title=row.get('Title'),
            author=row.get('Author'),
            category=row.get('Category'),
            publisher=row.get('Publisher'),
            publish_year=row.get('PublishYear'),
            book_status=row.get('BookStatus')
        )

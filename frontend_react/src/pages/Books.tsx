import React, { useState, useEffect } from 'react'
import { Plus, Edit2, Trash2, Search, BookOpen, Calendar } from 'lucide-react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import { apiService } from '../services/apiService'

import { ADMIN_BOOKS, USER_BOOKS, USER_RENTALS_CREATE } from '../constants/api'

interface Book {
  book_id: number
  book_code: string
  title: string
  author: string
  category: string
  book_status: string
  publisher?: string
  publish_year?: number
}

export default function Books() {
  const [books, setBooks] = useState<Book[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isRentModalOpen, setIsRentModalOpen] = useState(false)
  const [editingBook, setEditingBook] = useState<Book | null>(null)
  const [rentingBook, setRentingBook] = useState<Book | null>(null)
  const [formData, setFormData] = useState<Partial<Book>>({})
  const [expectedReturnDate, setExpectedReturnDate] = useState('')

  const userRole = localStorage.getItem('role') as 'Admin' | 'Customer'
  const apiEndpoint = userRole === 'Admin' ? ADMIN_BOOKS : USER_BOOKS

  const fetchBooks = async () => {
    try {
      setIsLoading(true)
      const data = await apiService.get<Book[]>(apiEndpoint)
      setBooks(data)
    } catch (error) {
      console.error('Error fetching books:', error)
      alert('Không thể tải danh sách sách')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchBooks()
  }, [])

  const filteredBooks = books.filter(
    (book) =>
      book.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.author?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.book_code?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDelete = async (id: number) => {
    if (confirm('Bạn chắc chắn muốn xóa?')) {
      try {
        await apiService.delete(`${ADMIN_BOOKS}/${id}`)
        setBooks(books.filter((b) => b.book_id !== id))
      } catch (error) {
        alert('Lỗi khi xóa sách: ' + error)
      }
    }
  }

  const handleEdit = (book: Book) => {
    setEditingBook(book)
    setFormData(book)
    setIsModalOpen(true)
  }

  const handleRent = (book: Book) => {
    setRentingBook(book)
    const nextWeek = new Date()
    nextWeek.setDate(nextWeek.getDate() + 7)
    setExpectedReturnDate(nextWeek.toISOString().split('T')[0])
    setIsRentModalOpen(true)
  }

  const handleRentSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!rentingBook) return
    try {
      await apiService.post(USER_RENTALS_CREATE, {
        book_ids: [rentingBook.book_id],
        expected_return_date: expectedReturnDate
      })
      alert('Đã tạo đơn thuê sách thành công!')
      setIsRentModalOpen(false)
      fetchBooks()
    } catch (error) {
      alert('Lỗi khi thuê sách: ' + error)
    }
  }

  const handleAddNew = () => {
    setEditingBook(null)
    setFormData({
      book_code: '',
      title: '',
      author: '',
      category: '',
      book_status: 'Available'
    })
    setIsModalOpen(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingBook) {
        await apiService.put(`${ADMIN_BOOKS}/${editingBook.book_id}`, formData)
      } else {
        await apiService.post(ADMIN_BOOKS, formData)
      }
      setIsModalOpen(false)
      fetchBooks()
    } catch (error) {
      alert('Lỗi khi lưu sách: ' + error)
    }
  }

  const getStatusBadge = (status: string) => {
    if (status === 'Available') return <span className="badge badge-success">✓ Có sẵn</span>
    if (status === 'Rented') return <span className="badge badge-warning">🔄 Đang thuê</span>
    return <span className="badge badge-danger">✗ {status}</span>
  }

  const columns = [
    { key: 'book_code', label: 'Mã sách' },
    { key: 'title', label: 'Tiêu đề' },
    { key: 'author', label: 'Tác giả' },
    { key: 'category', label: 'Thể loại' },
    {
      key: 'book_status',
      label: 'Trạng thái',
      render: (value: string) => getStatusBadge(value),
    },
  ]

  return (
    <div className="p-4 lg:p-8 bg-gray-100 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {userRole === 'Admin' ? 'Quản lý sách' : 'Thư viện sách'}
        </h1>

        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Tìm kiếm sách, tác giả, mã sách..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10"
            />
          </div>
          {userRole === 'Admin' && (
            <button onClick={handleAddNew} className="btn-primary flex items-center gap-2">
              <Plus size={20} /> Thêm sách
            </button>
          )}
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-10">Đang tải dữ liệu...</div>
      ) : (
        <Table
          columns={columns}
          data={filteredBooks}
          actions={(row) => (
            <div className="flex gap-2">
              {userRole === 'Admin' ? (
                <>
                  <button onClick={() => handleEdit(row)} className="p-2 text-blue-600 hover:bg-blue-50 rounded">
                    <Edit2 size={18} />
                  </button>
                  <button onClick={() => handleDelete(row.book_id)} className="p-2 text-red-600 hover:bg-red-50 rounded">
                    <Trash2 size={18} />
                  </button>
                </>
              ) : (
                <button 
                  onClick={() => handleRent(row)} 
                  disabled={row.book_status !== 'Available'}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm font-bold transition-all ${
                    row.book_status === 'Available' 
                    ? 'bg-primary-600 text-white hover:bg-primary-700' 
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  }`}
                >
                  <BookOpen size={16} /> Thuê sách
                </button>
              )}
            </div>
          )}
        />
      )}

      {/* Admin Create/Edit Modal */}
      <Modal
        title={editingBook ? 'Chỉnh sửa sách' : 'Thêm sách mới'}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mã sách</label>
            <input 
              type="text" 
              value={formData.book_code || ''} 
              onChange={e => setFormData({...formData, book_code: e.target.value})}
              className="input-field" 
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tiêu đề</label>
            <input 
              type="text" 
              value={formData.title || ''} 
              onChange={e => setFormData({...formData, title: e.target.value})}
              className="input-field" 
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tác giả</label>
            <input 
              type="text" 
              value={formData.author || ''} 
              onChange={e => setFormData({...formData, author: e.target.value})}
              className="input-field" 
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Thể loại</label>
            <input 
              type="text" 
              value={formData.category || ''} 
              onChange={e => setFormData({...formData, category: e.target.value})}
              className="input-field" 
            />
          </div>
          <div className="flex gap-3 mt-6">
            <button type="submit" className="flex-1 btn-primary">Lưu</button>
            <button type="button" onClick={() => setIsModalOpen(false)} className="flex-1 btn-outline">Hủy</button>
          </div>
        </form>
      </Modal>

      {/* User Rent Modal */}
      <Modal
        title="Xác nhận thuê sách"
        isOpen={isRentModalOpen}
        onClose={() => setIsRentModalOpen(false)}
      >
        {rentingBook && (
          <form onSubmit={handleRentSubmit} className="space-y-4">
            <div className="bg-primary-50 p-4 rounded-xl border border-primary-100 flex items-center gap-4">
              <div className="bg-primary-600 text-white p-3 rounded-lg">
                <BookOpen size={24} />
              </div>
              <div>
                <h3 className="font-bold text-primary-900">{rentingBook.title}</h3>
                <p className="text-sm text-primary-700">{rentingBook.author}</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-2">
                <Calendar size={16} /> Ngày trả dự kiến
              </label>
              <input 
                type="date" 
                value={expectedReturnDate} 
                min={new Date().toISOString().split('T')[0]}
                onChange={e => setExpectedReturnDate(e.target.value)}
                className="input-field" 
                required
              />
              <p className="text-xs text-gray-500 mt-1 italic">Lưu ý: Bạn nên trả sách đúng hạn để tránh phát sinh phí phạt.</p>
            </div>

            <div className="flex gap-3 mt-6">
              <button type="submit" className="flex-1 btn-primary">Xác nhận thuê</button>
              <button type="button" onClick={() => setIsRentModalOpen(false)} className="flex-1 btn-outline">Hủy</button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  )
}

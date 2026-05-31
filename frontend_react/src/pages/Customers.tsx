import { useState, useEffect } from 'react'
import { Edit2, Trash2, Search } from 'lucide-react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import apiService from '../services/apiService'
import { ADMIN_CUSTOMERS } from '../constants/api'

interface Customer {
  id: number
  code: string
  name: string
  phone?: string
  address?: string
  email?: string
}

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null)

  const fetchCustomers = async () => {
    try {
      setIsLoading(true)
      const data = await apiService.get<Customer[]>(ADMIN_CUSTOMERS)
      setCustomers(data)
    } catch (error) {
      console.error('Error fetching customers:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => { fetchCustomers() }, [])

  const filteredCustomers = customers.filter(
    (c) =>
      c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.code?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleEdit = (customer: Customer) => {
    setEditingCustomer(customer)
    setIsModalOpen(true)
  }

  const columns = [
    { key: 'code', label: 'Mã KH' },
    { key: 'name', label: 'Tên khách hàng' },
  ]

  return (
    <div className="p-4 lg:p-8 bg-gray-100 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Quản lý khách hàng</h1>
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Tìm kiếm khách hàng..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10"
            />
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-10">Đang tải dữ liệu...</div>
      ) : (
        <Table
          columns={columns}
          data={filteredCustomers}
          actions={(row) => (
            <div className="flex gap-2">
              <button onClick={() => handleEdit(row)} className="p-2 text-blue-600 hover:bg-blue-50 rounded">
                <Edit2 size={18} />
              </button>
              <button className="p-2 text-red-600 hover:bg-red-50 rounded">
                <Trash2 size={18} />
              </button>
            </div>
          )}
        />
      )}

      <Modal
        title={editingCustomer ? 'Chỉnh sửa khách hàng' : 'Thêm khách hàng'}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      >
        <p className="py-4">Tính năng chỉnh sửa khách hàng đang được cập nhật.</p>
        <button onClick={() => setIsModalOpen(false)} className="w-full btn-primary">Đóng</button>
      </Modal>
    </div>
  )
}

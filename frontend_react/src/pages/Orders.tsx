import { useState, useEffect } from 'react'
import { CheckCircle, Search } from 'lucide-react'
import Table from '../components/Table'
import apiService from '../services/apiService'
import { ADMIN_ORDERS } from '../constants/api'

interface Order {
  order_id: number
  order_code: string
  customer_id: number
  order_status: string
  rent_date: string
  expected_return_date: string
  return_date?: string
}

export default function Orders() {
  const [orders, setOrders] = useState<Order[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  const fetchOrders = async () => {
    try {
      setIsLoading(true)
      const data = await apiService.get<Order[]>(ADMIN_ORDERS)
      setOrders(data)
    } catch (error) {
      console.error('Error fetching orders:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => { fetchOrders() }, [])

  const handleReturn = async (id: number) => {
    try {
      await apiService.put(`${ADMIN_ORDERS}/${id}/return`, {})
      alert('Đã trả sách thành công!')
      fetchOrders()
    } catch (error) {
      alert('Lỗi khi trả sách: ' + error)
    }
  }

  const getStatusBadge = (status: string) => {
    if (status === 'Renting') return <span className="badge badge-warning">Đang thuê</span>
    if (status === 'Returned') return <span className="badge badge-success">Đã trả</span>
    return <span className="badge badge-danger">{status}</span>
  }

  const columns = [
    { key: 'order_code', label: 'Mã đơn' },
    { key: 'rent_date', label: 'Ngày thuê', render: (v: string) => new Date(v).toLocaleDateString() },
    { key: 'order_status', label: 'Trạng thái', render: (v: string) => getStatusBadge(v) },
  ]

  return (
    <div className="p-4 lg:p-8 bg-gray-100 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Quản lý đơn thuê</h1>
        <div className="flex-1 relative max-w-md">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Tìm kiếm mã đơn..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field pl-10"
          />
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-10">Đang tải dữ liệu...</div>
      ) : (
        <Table
          columns={columns}
          data={orders.filter(o => o.order_code.includes(searchTerm))}
          actions={(row) => (
            row.order_status === 'Renting' && (
              <button onClick={() => handleReturn(row.order_id)} className="btn-outline btn-sm flex items-center gap-1">
                <CheckCircle size={16} /> Trả sách
              </button>
            )
          )}
        />
      )}
    </div>
  )
}

import { useState, useEffect } from 'react'
import { ShoppingBag, Clock, BookOpen } from 'lucide-react'
import Table from '../components/Table'
import apiService from '../services/apiService'
import { USER_RENTALS_CURRENT, USER_RENTALS_HISTORY } from '../constants/api'

interface UserOrdersProps {
  mode: 'current' | 'history'
}

interface Order {
  order_id: number
  order_code: string
  order_status: string
  rent_date: string
  expected_return_date: string
  return_date?: string
}

export default function UserOrders({ mode }: UserOrdersProps) {
  const [orders, setOrders] = useState<Order[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const endpoint = mode === 'current' ? USER_RENTALS_CURRENT : USER_RENTALS_HISTORY

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        setIsLoading(true)
        const data = await apiService.get<Order[]>(endpoint)
        setOrders(data)
      } catch (error) {
        console.error('Error fetching user orders:', error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchOrders()
  }, [mode])

  const getStatusBadge = (status: string) => {
    if (status === 'Renting') return <span className="badge badge-warning">Đang thuê</span>
    if (status === 'Returned') return <span className="badge badge-success">Đã trả</span>
    return <span className="badge badge-danger">{status}</span>
  }

  const columns = [
    { key: 'order_code', label: 'Mã đơn' },
    { key: 'rent_date', label: 'Ngày thuê', render: (v: string) => new Date(v).toLocaleDateString() },
    { key: 'expected_return_date', label: 'Hạn trả', render: (v: string) => new Date(v).toLocaleDateString() },
    { key: 'order_status', label: 'Trạng thái', render: (v: string) => getStatusBadge(v) },
  ]

  return (
    <div className="p-4 lg:p-8 bg-gray-100 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
          {mode === 'current' ? <ShoppingBag className="text-primary-600" /> : <Clock className="text-primary-600" />}
          {mode === 'current' ? 'Sách đang thuê' : 'Lịch sử thuê sách'}
        </h1>
        <p className="text-gray-600">
          {mode === 'current' ? 'Danh sách các cuốn sách bạn đang mượn từ thư viện.' : 'Tất cả các đơn thuê bạn đã thực hiện trong quá khứ.'}
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-10">Đang tải dữ liệu...</div>
      ) : orders.length === 0 ? (
        <div className="card text-center py-20">
          <div className="flex justify-center mb-4">
            <div className="bg-gray-100 p-4 rounded-full text-gray-400">
              <BookOpen size={48} />
            </div>
          </div>
          <h3 className="text-xl font-bold text-gray-900">Không có dữ liệu</h3>
          <p className="text-gray-500 mt-2">Bạn chưa có đơn thuê nào trong mục này.</p>
        </div>
      ) : (
        <Table columns={columns} data={orders} />
      )}
    </div>
  )
}

import { useEffect, useState } from 'react'
import { BookOpen, ShoppingBag, Clock, Search, AlertCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import StatCard from '../components/StatCard'
import apiService from '../services/apiService'
import { USER_STATS, USER_RENTALS_CURRENT } from '../constants/api'

export default function UserDashboard() {
  const navigate = useNavigate()
  const username = localStorage.getItem('username') || 'Người dùng'
  const [statsData, setStatsData] = useState<any>(null)
  const [currentRentals, setCurrentRentals] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        const [statsResponse, rentalsResponse] = await Promise.all([
          apiService.get<any>(USER_STATS),
          apiService.get<any[]>(USER_RENTALS_CURRENT)
        ])
        setStatsData(statsResponse)
        setCurrentRentals(rentalsResponse)
      } catch (err: any) {
        console.error('Error fetching dashboard data:', err)
        setError('Không thể tải dữ liệu dashboard. Vui lòng thử lại sau.')
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  const stats = [
    {
      icon: <BookOpen className="w-8 h-8 text-blue-600" />,
      label: 'Sách có sẵn',
      value: statsData?.available_books ?? 0,
      trend: 0,
      color: 'primary' as const,
    },
    {
      icon: <ShoppingBag className="w-8 h-8 text-purple-600" />,
      label: 'Đang thuê',
      value: statsData?.active_rentals ?? 0,
      trend: 0,
      color: 'secondary' as const,
    },
    {
      icon: <Clock className="w-8 h-8 text-orange-600" />,
      label: 'Lịch sử thuê',
      value: statsData?.total_history ?? 0,
      trend: 0,
      color: 'orange' as const,
    },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dữ liệu...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 lg:p-8 bg-gray-100 min-h-screen">
      <div className="mb-8 animate-fade-in">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Xin chào, {username}!</h1>
        <p className="text-gray-600">Chào mừng bạn đến với Thư viện Sách. Hôm nay bạn muốn đọc gì?</p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 flex items-center gap-3 text-red-700">
          <AlertCircle size={20} />
          <p>{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat, idx) => (
          <div key={idx} className="animate-slide-in">
            <StatCard {...stat} />
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Sách bạn đang thuê</h2>
          <div className="space-y-3">
            {currentRentals.length > 0 ? (
              currentRentals.map((order, idx) => (
                <div key={idx} className="flex items-center justify-between p-4 bg-white border border-gray-100 rounded-xl shadow-sm">
                  <div className="flex items-center gap-4">
                    <div className="bg-blue-50 p-3 rounded-lg text-blue-600">
                      <BookOpen size={24} />
                    </div>
                    <div>
                      <p className="font-bold text-gray-900">Đơn hàng: {order.order_code}</p>
                      <p className="text-sm text-gray-500">Hạn trả: {order.expected_return_date ? new Date(order.expected_return_date).toLocaleDateString('vi-VN') : 'N/A'}</p>
                    </div>
                  </div>
                  <button onClick={() => navigate('/user/rentals/history')} className="btn-outline btn-sm">Xem chi tiết</button>
                </div>
              ))
            ) : (
              <div className="text-center py-10 bg-white rounded-xl border border-dashed border-gray-300">
                <p className="text-gray-500">Bạn hiện không thuê cuốn sách nào.</p>
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Hành động nhanh</h2>
          <div className="space-y-3">
            <button onClick={() => navigate('/user/books')} className="w-full flex items-center gap-3 p-4 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-all shadow-md">
              <Search size={20} />
              <span className="font-bold">Tìm kiếm sách</span>
            </button>
            <button onClick={() => navigate('/user/rentals/history')} className="w-full flex items-center gap-3 p-4 bg-white border-2 border-primary-600 text-primary-600 rounded-xl hover:bg-primary-50 transition-all">
              <Clock size={20} />
              <span className="font-bold">Lịch sử thuê sách</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

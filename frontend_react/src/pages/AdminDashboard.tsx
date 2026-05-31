import { BookOpen, Users, ShoppingCart, TrendingUp } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import StatCard from '../components/StatCard'

export default function AdminDashboard() {
  const navigate = useNavigate()
  
  const stats = [
    {
      icon: <BookOpen className="w-8 h-8 text-blue-600" />,
      label: 'Tổng sách',
      value: 150,
      trend: 5,
      color: 'primary' as const,
    },
    {
      icon: <ShoppingCart className="w-8 h-8 text-purple-600" />,
      label: 'Đơn đang thuê',
      value: 45,
      trend: -2,
      color: 'secondary' as const,
    },
    {
      icon: <Users className="w-8 h-8 text-green-600" />,
      label: 'Khách hàng',
      value: 120,
      trend: 8,
      color: 'green' as const,
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-orange-600" />,
      label: 'Doanh thu tháng',
      value: '25,000,000đ',
      trend: 12,
      color: 'orange' as const,
    },
  ]

  return (
    <div className="p-4 lg:p-8 bg-gray-100 min-h-screen">
      <div className="mb-8 animate-fade-in">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
        <p className="text-gray-600">Tổng quan hệ thống dành cho Quản trị viên.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, idx) => (
          <div key={idx} className="animate-slide-in">
            <StatCard {...stat} />
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Hoạt động gần đây</h2>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((_, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900">Đơn #ORD{String(idx + 1).padStart(3, '0')}</p>
                  <p className="text-sm text-gray-500">Trạng thái: Đang xử lý</p>
                </div>
                <span className="badge badge-success">Thành công</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quản lý nhanh</h2>
          <div className="space-y-2">
            <button onClick={() => navigate('/admin/books')} className="w-full btn-primary text-left">➕ Quản lý sách</button>
            <button onClick={() => navigate('/admin/customers')} className="w-full btn-secondary text-left">➕ Quản lý khách hàng</button>
            <button onClick={() => navigate('/admin/orders')} className="w-full btn-outline text-left">📝 Quản lý đơn thuê</button>
            <button onClick={() => navigate('/admin/reports')} className="w-full btn-outline text-left">📊 Báo cáo thống kê</button>
          </div>
        </div>
      </div>
    </div>
  )
}

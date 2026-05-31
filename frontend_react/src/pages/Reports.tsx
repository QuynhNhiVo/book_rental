import { useState, useEffect } from 'react'
import { TrendingUp, BookOpen, Users } from 'lucide-react'
import StatCard from '../components/StatCard'
import apiService from '../services/apiService'
import { ADMIN_STATS } from '../constants/api'

export default function Reports() {
  const [stats, setStats] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setIsLoading(true)
        const data = await apiService.get<any>(ADMIN_STATS)
        setStats(data)
      } catch (error) {
        console.error('Error fetching stats:', error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchStats()
  }, [])

  if (isLoading) return <div className="p-8 text-center">Đang tải báo cáo...</div>

  const statCards = [
    { icon: <BookOpen className="w-8 h-8 text-blue-600" />, label: 'Tổng sách', value: stats?.total_books || 0, color: 'primary' as const },
    { icon: <TrendingUp className="w-8 h-8 text-purple-600" />, label: 'Sách đang thuê', value: stats?.rented_books || 0, color: 'secondary' as const },
    { icon: <Users className="w-8 h-8 text-green-600" />, label: 'Khách hàng', value: stats?.total_customers || 0, color: 'green' as const },
  ]

  return (
    <div className="p-4 lg:p-8 bg-gray-100 min-h-screen">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Báo cáo & Thống kê</h1>
        <p className="text-gray-600">Phân tích hoạt động thư viện.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {statCards.map((stat, idx) => <StatCard key={idx} {...stat} />)}
      </div>

      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Sách được thuê nhiều nhất</h2>
        <div className="py-10 text-center text-gray-400 italic">Tính năng biểu đồ đang được phát triển</div>
      </div>
    </div>
  )
}

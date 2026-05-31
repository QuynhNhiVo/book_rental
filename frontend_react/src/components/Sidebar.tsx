import { useState } from 'react'
import { BookOpen, BarChart3, Users, ShoppingCart, Settings, LogOut, Menu, X, History } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'

interface SidebarProps {
  userRole: 'Admin' | 'Customer'
  onLogout: () => void
}

export default function Sidebar({ userRole, onLogout }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(true)
  const location = useLocation()

  const adminMenuItems = [
    { icon: BarChart3, label: 'Dashboard', path: '/admin/dashboard' },
    { icon: BookOpen, label: 'Quản lý sách', path: '/admin/books' },
    { icon: Users, label: 'Khách hàng', path: '/admin/customers' },
    { icon: ShoppingCart, label: 'Đơn thuê', path: '/admin/orders' },
    { icon: Settings, label: 'Báo cáo', path: '/admin/reports' },
  ]

  const customerMenuItems = [
    { icon: BarChart3, label: 'Dashboard', path: '/user/dashboard' },
    { icon: BookOpen, label: 'Tìm sách', path: '/user/books' },
    { icon: ShoppingCart, label: 'Sách đang thuê', path: '/user/rentals/current' },
    { icon: History, label: 'Lịch sử thuê', path: '/user/rentals/history' },
  ]

  const menuItems = userRole === 'Admin' ? adminMenuItems : customerMenuItems

  const isActive = (path: string) => location.pathname === path

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-40 lg:hidden bg-primary-600 text-white p-2 rounded-lg hover:bg-primary-700"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      <aside
        className={`${
          isOpen ? 'w-64' : 'w-0'
        } bg-primary-800 text-white shadow-lg transition-all duration-300 flex flex-col fixed h-screen lg:static lg:w-64 z-30`}
      >
        <div className="p-6 border-b border-primary-700 flex items-center gap-3">
          <BookOpen className="w-8 h-8 text-yellow-300" />
          <div>
            <h1 className="text-xl font-bold">📚 BookRent</h1>
            <p className="text-xs text-primary-200">{userRole === 'Admin' ? 'Quản trị viên' : 'Khách hàng'}</p>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => window.innerWidth < 1024 && setIsOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive(item.path)
                    ? 'bg-primary-600 text-white shadow-md'
                    : 'text-primary-100 hover:bg-primary-700'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-primary-700 space-y-2">
          <button
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-4 py-3 text-red-300 hover:bg-red-900 rounded-lg transition-all"
          >
            <LogOut size={20} />
            <span>Đăng xuất</span>
          </button>
        </div>
      </aside>

      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 lg:hidden z-20"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}

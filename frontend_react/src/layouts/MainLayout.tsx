import { ReactNode } from 'react'
import Sidebar from '../components/Sidebar'
import { Role } from '../routes/ProtectedRoute'

interface MainLayoutProps {
  children: ReactNode
  userRole: Role
  onLogout: () => void
}

/**
 * MainLayout - Layout chung cho toàn bộ ứng dụng sau khi đăng nhập.
 * Bao gồm Sidebar bên trái và phần nội dung chính bên phải.
 */
const MainLayout = ({ children, userRole, onLogout }: MainLayoutProps) => {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar cố định bên trái */}
      <Sidebar userRole={userRole} onLogout={onLogout} />
      
      {/* Vùng nội dung có thể cuộn bên phải */}
      <main className="flex-1 overflow-y-auto">
        <div className="animate-fade-in">
          {children}
        </div>
      </main>
    </div>
  )
}

export default MainLayout

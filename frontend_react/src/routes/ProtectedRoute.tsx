import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'

// Định nghĩa các Role hợp lệ trong hệ thống
export type Role = 'Admin' | 'Customer'

interface ProtectedRouteProps {
  children: ReactNode
  allowedRoles: Role[]
  userRole: Role | null
  isLoggedIn: boolean
}

/**
 * ProtectedRoute - Thành phần bảo vệ các route yêu cầu đăng nhập và phân quyền.
 * Nếu chưa đăng nhập -> Chuyển về trang Login.
 * Nếu đã đăng nhập nhưng sai Role -> Chuyển về Dashboard tương ứng của Role đó.
 */
const ProtectedRoute = ({ children, allowedRoles, userRole, isLoggedIn }: ProtectedRouteProps) => {
  // 1. Kiểm tra trạng thái đăng nhập
  if (!isLoggedIn) {
    return <Navigate to="/login" replace />
  }

  // 2. Kiểm tra phân quyền (RBAC - Role Based Access Control)
  if (userRole && !allowedRoles.includes(userRole)) {
    // Nếu là Admin nhưng cố tình vào trang User (hoặc ngược lại), đẩy về trang chủ của họ
    const redirectPath = userRole === 'Admin' ? '/admin/dashboard' : '/user/dashboard'
    return <Navigate to={redirectPath} replace />
  }

  // 3. Nếu thỏa mãn mọi điều kiện, render nội dung bên trong (children)
  return <>{children}</>
}

export default ProtectedRoute

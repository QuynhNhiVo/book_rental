import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'

// Layouts & Routes
import MainLayout from './layouts/MainLayout'
import ProtectedRoute, { Role } from './routes/ProtectedRoute'

// Pages
import AdminDashboard from './pages/AdminDashboard'
import UserDashboard from './pages/UserDashboard'
import UserOrders from './pages/UserOrders'
import Books from './pages/Books'
import Customers from './pages/Customers'
import Orders from './pages/Orders'
import Reports from './pages/Reports'
import Login from './pages/Login'
import NotFound from './pages/NotFound'

/**
 * Thành phần chính điều hướng toàn bộ ứng dụng.
 */
function App() {
  // Trạng thái đăng nhập được đồng bộ với localStorage
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(!!localStorage.getItem('token'))
  const [userRole, setUserRole] = useState<Role | null>(localStorage.getItem('role') as Role)

  const handleLogin = (role: Role) => {
    setIsLoggedIn(true)
    setUserRole(role)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('username')
    localStorage.removeItem('customer_id')
    setIsLoggedIn(false)
    setUserRole(null)
  }

  return (
    <Router>
      <Routes>
        {/* TRANG CÔNG KHAI */}
        <Route 
          path="/login" 
          element={
            isLoggedIn 
              ? <Navigate to={userRole === 'Admin' ? '/admin/dashboard' : '/user/dashboard'} replace /> 
              : <Login onLogin={handleLogin} />
          } 
        />

        {/* TRANG YÊU CẦU ĐĂNG NHẬP (PROTECTED) */}
        <Route
          path="/*"
          element={
            <ProtectedRoute allowedRoles={['Admin', 'Customer']} userRole={userRole} isLoggedIn={isLoggedIn}>
              <MainLayout userRole={userRole || 'Customer'} onLogout={handleLogout}>
                <Routes>
                  {/* Routes dành riêng cho Quản trị viên */}
                  <Route path="/admin/dashboard" element={<AdminDashboard />} />
                  <Route path="/admin/books" element={<Books />} />
                  <Route path="/admin/customers" element={<Customers />} />
                  <Route path="/admin/orders" element={<Orders />} />
                  <Route path="/admin/reports" element={<Reports />} />

                  {/* Routes dành riêng cho Khách hàng */}
                  <Route path="/user/dashboard" element={<UserDashboard />} />
                  <Route path="/user/books" element={<Books />} />
                  <Route path="/user/rentals/current" element={<UserOrders mode="current" />} />
                  <Route path="/user/rentals/history" element={<UserOrders mode="history" />} />

                  {/* Điều hướng mặc định */}
                  <Route path="/" element={<Navigate to={userRole === 'Admin' ? '/admin/dashboard' : '/user/dashboard'} replace />} />
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </MainLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  )
}

export default App

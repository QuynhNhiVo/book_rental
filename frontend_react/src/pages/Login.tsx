import React, { useState } from 'react'
import { BookOpen } from 'lucide-react'
import { AUTH_LOGIN } from '../constants/api'

interface LoginProps {
  onLogin: (role: 'Admin' | 'Customer') => void
}

export default function Login({ onLogin }: LoginProps) {
  const [username, setUsername] = useState('admin_vip')
  const [password, setPassword] = useState('123456')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      const response = await fetch(AUTH_LOGIN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.trim(),
          password: password.trim(),
        }),
      })

      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await response.text();
        console.error("Non-JSON login response:", text);
        throw new Error("Server returned an invalid response format. Please ensure Backend is running.");
      }

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || `Đăng nhập thất bại (Error ${response.status})`)
      }

      // Backend returns user role - no need to select manually
      const userRole = data.data?.role as 'Admin' | 'Customer'
      const token = data.data?.token
      
      if (!userRole) {
        throw new Error('Không thể xác định vai trò của người dùng')
      }

      if (token) {
        localStorage.setItem('token', token)
        localStorage.setItem('role', userRole)
        localStorage.setItem('username', data.data?.username || '')
      }

      onLogin(userRole)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Lỗi kết nối tới server. Vui lòng chắc chắn API đang chạy trên port 5000')
      console.error('Login error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-800 via-primary-700 to-secondary-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex justify-center mb-4">
            <div className="bg-yellow-300 p-4 rounded-full">
              <BookOpen size={40} className="text-primary-900" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">📚 Residence</h1>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-2xl shadow-2xl p-8 animate-slide-in">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Tên đăng nhập</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field"
                placeholder="Nhập tên đăng nhập"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Mật khẩu</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field"
                placeholder="Nhập mật khẩu"
                required
              />
            </div>

            {error && (
              <div className="text-sm text-red-600 bg-red-50 border border-red-200 p-3 rounded-md">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn-primary py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Đang đăng nhập...' : 'Đăng nhập'}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-xs font-semibold text-blue-900 mb-2">🔐 Tài khoản demo:</p>
            <p className="text-xs text-blue-800">Username: <span className="font-mono">admin_vip</span></p>
            <p className="text-xs text-blue-800">Password: <span className="font-mono">123456</span></p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-primary-100 text-sm mt-8">
          © 2024 Book Rental Management System. All rights reserved.
        </p>
      </div>
    </div>
  )
}

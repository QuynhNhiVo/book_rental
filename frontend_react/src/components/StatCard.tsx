import React from 'react'

interface StatCardProps {
  icon: React.ReactNode
  label: string
  value: string | number
  trend?: number
  color: 'primary' | 'secondary' | 'green' | 'orange'
}

const colorClasses = {
  primary: 'bg-blue-50 border-blue-200 text-blue-700',
  secondary: 'bg-purple-50 border-purple-200 text-purple-700',
  green: 'bg-green-50 border-green-200 text-green-700',
  orange: 'bg-orange-50 border-orange-200 text-orange-700',
}

export default function StatCard({ icon, label, value, trend, color }: StatCardProps) {
  return (
    <div className={`card border-l-4 ${colorClasses[color]} group hover:shadow-lg`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
          {trend && (
            <p className={`text-xs font-semibold mt-2 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% so với tháng trước
            </p>
          )}
        </div>
        <div className="p-3 rounded-lg group-hover:scale-110 transition-transform">
          {icon}
        </div>
      </div>
    </div>
  )
}

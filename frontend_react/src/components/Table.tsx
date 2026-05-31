import React from 'react'

interface TableProps {
  columns: Array<{
    key: string
    label: string
    render?: (value: any, row: any) => React.ReactNode
  }>
  data: any[]
  actions?: (row: any) => React.ReactNode
}

export default function Table({ columns, data, actions }: TableProps) {
  return (
    <div className="overflow-x-auto card">
      <table className="w-full">
        <thead>
          <tr className="bg-gray-50 border-b-2 border-gray-200">
            {columns.map((col) => (
              <th key={col.key} className="table-header text-gray-900">
                {col.label}
              </th>
            ))}
            {actions && <th className="table-header text-gray-900">Hành động</th>}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length + (actions ? 1 : 0)} className="table-cell text-center py-8 text-gray-500">
                Không có dữ liệu
              </td>
            </tr>
          ) : (
            data.map((row, idx) => (
              <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                {columns.map((col) => (
                  <td key={col.key} className="table-cell">
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </td>
                ))}
                {actions && <td className="table-cell">{actions(row)}</td>}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}


export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-primary-900 mb-4">404</h1>
        <p className="text-xl text-gray-600 mb-6">Trang không được tìm thấy</p>
        <a href="/" className="btn-primary">
          Quay về Trang chủ
        </a>
      </div>
    </div>
  )
}

export const API_BASE_URL = ''

// Auth
export const AUTH_BASE = `${API_BASE_URL}/api/v1/auth`
export const AUTH_LOGIN = `${AUTH_BASE}/login`
export const AUTH_LOGOUT = `${AUTH_BASE}/logout`
export const AUTH_ME = `${AUTH_BASE}/me`

// Admin
export const ADMIN_BASE = `${API_BASE_URL}/api/v1/admin`
export const ADMIN_BOOKS = `${ADMIN_BASE}/books`
export const ADMIN_CUSTOMERS = `${ADMIN_BASE}/customers`
export const ADMIN_ORDERS = `${ADMIN_BASE}/orders`
export const ADMIN_STATS = `${ADMIN_BASE}/reports/statistics`

// User
export const USER_BASE = `${API_BASE_URL}/api/v1/user`
export const USER_BOOKS = `${USER_BASE}/books`
export const USER_RENTALS_CREATE = `${USER_BASE}/rentals/create`
export const USER_RENTALS_CURRENT = `${USER_BASE}/rentals/current`
export const USER_RENTALS_HISTORY = `${USER_BASE}/rentals/history`
export const USER_STATS = `${USER_BASE}/dashboard/stats`

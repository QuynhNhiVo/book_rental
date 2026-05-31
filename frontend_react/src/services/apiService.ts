
interface ApiResponse<T> {
  success: boolean
  message?: string
  data: T
}

const getAuthHeader = (): Record<string, string> => {
  const token = localStorage.getItem('token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

const handleResponse = async <T>(response: Response): Promise<T> => {
  const contentType = response.headers.get("content-type");
  
  if (!response.ok) {
    let errorMessage = `Error ${response.status}: ${response.statusText}`;
    try {
      if (contentType && contentType.includes("application/json")) {
        const errorData = await response.json();
        errorMessage = errorData.message || errorMessage;
      }
    } catch (e) { }
    throw new Error(errorMessage);
  }

  if (response.status === 204) return {} as T;

  try {
    const result: ApiResponse<T> = await response.json();
    if (!result.success) {
      throw new Error(result.message || 'API request failed');
    }
    return result.data;
  } catch (e) {
    throw e;
  }
}

export const apiService = {
  async get<T>(url: string): Promise<T> {
    const response = await fetch(url, {
      headers: getAuthHeader()
    })
    return await handleResponse<T>(response);
  },

  async post<T>(url: string, data: any): Promise<T> {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader()
      },
      body: JSON.stringify(data)
    })
    return await handleResponse<T>(response);
  },

  async put<T>(url: string, data: any): Promise<T> {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader()
      },
      body: JSON.stringify(data)
    })
    return await handleResponse<T>(response);
  },

  async delete(url: string): Promise<void> {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: getAuthHeader()
    })
    await handleResponse<any>(response);
  }
}

export default apiService

import axios from 'axios'

/**
 * API Client for PAZ Backend.
 * Configured to work with FastAPI backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.data)
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request)
    } else {
      // Error setting up request
      console.error('Request Error:', error.message)
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const api = {
  // Health check
  health: () => apiClient.get('/health'),

  // Projects (to be implemented)
  projects: {
    list: () => apiClient.get('/api/v1/projects'),
    get: (id: string) => apiClient.get(`/api/v1/projects/${id}`),
    create: (data: unknown) => apiClient.post('/api/v1/projects', data),
    update: (id: string, data: unknown) => apiClient.put(`/api/v1/projects/${id}`, data),
    delete: (id: string) => apiClient.delete(`/api/v1/projects/${id}`),
  },

  // Analysis (to be implemented)
  analysis: {
    run: (projectId: string, loadCases: string[]) =>
      apiClient.post(`/api/v1/analysis/${projectId}/run`, { load_cases: loadCases }),
    status: (projectId: string) =>
      apiClient.get(`/api/v1/analysis/${projectId}/status`),
    results: (projectId: string) =>
      apiClient.get(`/api/v1/analysis/${projectId}/results`),
  },
}

export default apiClient

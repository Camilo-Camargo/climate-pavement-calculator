export async function apiPost(env: string, path: string, params?: {}) {
  const API_URL = env === "prod" ? "/api" : 'http://localhost:8000/api';
  return await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params)
  });
}

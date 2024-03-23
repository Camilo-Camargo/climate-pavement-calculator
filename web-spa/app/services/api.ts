const API_URL = import.meta.env.WEB_ENV === "prod" ? "/api" : 'http://localhost:8000/api';
console.log(import.meta.env.WEB_ENV);

export async function apiPost(path: string, params?: {}) {
  return await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params)
  });
}

const API_URL = `http://localhost:8000`;

export async function apiPost(path: string, params?: {}) {
  return await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params)
  });
}

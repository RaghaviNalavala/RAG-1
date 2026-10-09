const API_BASE = 'http://localhost:8000/api';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || 'Request failed');
  }

  return response.json() as Promise<T>;
}

export async function fetchHealth() {
  return request<any>('/health');
}

export async function fetchModels() {
  return request<{ models: string[]; default_model: string; embedding_model: string }>('/models');
}

export async function sendChat(payload: Record<string, unknown>) {
  return request<any>('/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function uploadDocument(formData: FormData) {
  const response = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'Upload failed');
  }

  return response.json();
}

export async function listDocuments() {
  return request<any>('/documents');
}

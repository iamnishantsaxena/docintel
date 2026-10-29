// Thin typed wrapper over the FastAPI backend. Types mirror app/main.py + app/fields.py.

export type Status = "queued" | "processing" | "needs_review" | "validated" | "failed";

export interface LineItem {
  description: string | null;
  quantity: string | null;
  unit_price: string | null;
  amount: string | null;
}

export interface Fields {
  document_type: "invoice" | "purchase_order" | "other" | null;
  supplier_name: string | null;
  customer_name: string | null;
  document_number: string | null;
  po_number: string | null;
  document_date: string | null;
  due_date: string | null;
  currency: string | null;
  subtotal: string | null;
  tax: string | null;
  total: string | null;
  line_items: LineItem[];
}

export interface Issue {
  field: string | null;
  code: string;
  severity: "error" | "warning";
  message: string;
}

export interface DocumentSummary {
  id: number;
  filename: string;
  status: Status;
  error: string | null;
  error_count: number;
  warning_count: number;
  supplier_name: string | null;
  document_number: string | null;
  total: string | null;
  created_at: string;
  updated_at: string;
}

export interface DocumentDetail extends DocumentSummary {
  page_count: number | null;
  attempts: number;
  fields: Fields | null;
  extracted: Fields | null;
  issues: Issue[];
  meta: { model?: string | null; llm_used?: boolean; sources?: Record<string, "llm" | "regex">; processing_ms?: number } | null;
  reviewed_at: string | null;
}

export interface UploadResult {
  id: number | null;
  filename: string;
  status: Status | null;
  duplicate: boolean;
  error: string | null;
}

export class ApiError extends Error {
  constructor(public status: number, message: string, public body?: unknown) {
    super(message);
  }
}

let token = localStorage.getItem("token");
export const isLoggedIn = () => !!token;
export function logout() {
  token = null;
  localStorage.removeItem("token");
}

async function request(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch(`/api${path}`, { ...init, headers });
  if (res.status === 401 && token) {
    logout();
    location.hash = "";
    location.reload();
  }
  if (!res.ok) {
    const body = await res.json().catch(() => undefined);
    const detail = body?.detail;
    const msg = typeof detail === "string" ? detail : detail?.message ?? (Array.isArray(detail) ? detail.map((d: { msg: string }) => d.msg).join("; ") : res.statusText);
    throw new ApiError(res.status, msg, body);
  }
  return res;
}

const json = <T,>(path: string, init?: RequestInit) => request(path, init).then((r) => r.json() as Promise<T>);
const send = <T,>(method: string, path: string, body?: unknown) =>
  json<T>(path, { method, headers: { "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body) });

async function setToken(p: Promise<{ access_token: string }>) {
  token = (await p).access_token;
  localStorage.setItem("token", token);
}

export const api = {
  login: (email: string, password: string) =>
    setToken(json("/auth/login", { method: "POST", body: new URLSearchParams({ username: email, password }) })),
  register: (email: string, password: string) => setToken(send("POST", "/auth/register", { email, password })),
  me: () => json<{ id: number; email: string }>("/auth/me"),
  list: () => json<DocumentSummary[]>("/documents"),
  get: (id: number) => json<DocumentDetail>(`/documents/${id}`),
  upload: (files: File[]) => {
    const fd = new FormData();
    files.forEach((f) => fd.append("files", f));
    return json<UploadResult[]>("/documents", { method: "POST", body: fd });
  },
  saveFields: (id: number, fields: Fields) => send<DocumentDetail>("PUT", `/documents/${id}/fields`, fields),
  approve: (id: number) => send<DocumentDetail>("POST", `/documents/${id}/approve`),
  reprocess: (id: number) => send<DocumentDetail>("POST", `/documents/${id}/reprocess`),
  remove: (id: number) => request(`/documents/${id}`, { method: "DELETE" }),
  fileUrl: async (id: number) => URL.createObjectURL(await (await request(`/documents/${id}/file`)).blob()),
  download: async (format: "csv" | "xlsx") => {
    const res = await request(`/export?format=${format}`);
    const name = res.headers.get("Content-Disposition")?.match(/filename="(.+)"/)?.[1] ?? `export.${format}`;
    const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(await res.blob()), download: name });
    a.click();
    URL.revokeObjectURL(a.href);
  },
};

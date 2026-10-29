import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError, DocumentDetail, DocumentSummary, Fields, Issue, isLoggedIn, LineItem, logout, Status, UploadResult } from "./api";

// ponytail: hash routing (#/doc/12) instead of react-router; two screens don't need a router dependency
function useHashRoute() {
  const [hash, setHash] = useState(location.hash);
  useEffect(() => {
    const on = () => setHash(location.hash);
    addEventListener("hashchange", on);
    return () => removeEventListener("hashchange", on);
  }, []);
  const m = hash.match(/^#\/doc\/(\d+)$/);
  return m ? Number(m[1]) : null;
}

export default function App() {
  const [authed, setAuthed] = useState(isLoggedIn());
  const [email, setEmail] = useState("");
  const docId = useHashRoute();

  useEffect(() => {
    if (authed) api.me().then((u) => setEmail(u.email)).catch(() => setAuthed(false));
  }, [authed]);

  if (!authed) return <Login onDone={() => setAuthed(true)} />;
  return (
    <>
      <header className="topbar">
        <a href="#" className="brand">DocIntel</a>
        <span className="muted">{email}</span>
        <button className="link" onClick={() => { logout(); setAuthed(false); }}>Sign out</button>
      </header>
      <main>{docId ? <Review id={docId} key={docId} /> : <DocumentList />}</main>
    </>
  );
}

// ---------------- Login ----------------

function Login({ onDone }: { onDone: () => void }) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await (mode === "login" ? api.login(email, password) : api.register(email, password));
      onDone();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="card login" onSubmit={submit}>
      <h1>DocIntel</h1>
      <p className="muted">Extract, validate and export invoice and purchase-order data.</p>
      <label>Email<input type="email" required autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} /></label>
      <label>Password<input type="password" required minLength={8} autoComplete={mode === "login" ? "current-password" : "new-password"} value={password} onChange={(e) => setPassword(e.target.value)} /></label>
      {error && <p className="error" role="alert">{error}</p>}
      <button className="primary" disabled={busy}>{mode === "login" ? "Sign in" : "Create account"}</button>
      <button type="button" className="link" onClick={() => setMode(mode === "login" ? "register" : "login")}>
        {mode === "login" ? "No account? Register" : "Have an account? Sign in"}
      </button>
    </form>
  );
}

// ---------------- Document list ----------------

const STATUS_LABEL: Record<Status, string> = {
  queued: "Queued", processing: "Processing", needs_review: "Needs review", validated: "Validated", failed: "Failed",
};

function StatusBadge({ status }: { status: Status }) {
  return <span className={`badge ${status}`}>{STATUS_LABEL[status]}</span>;
}

function DocumentList() {
  const [docs, setDocs] = useState<DocumentSummary[] | null>(null);
  const [filter, setFilter] = useState<Status | "all">("all");
  const [uploads, setUploads] = useState<UploadResult[]>([]);
  const [error, setError] = useState("");
  const [dragging, setDragging] = useState(false);
  const input = useRef<HTMLInputElement>(null);

  const load = useCallback(() => api.list().then(setDocs).catch((e) => setError(e.message)), []);
  useEffect(() => { load(); }, [load]);

  // Poll only while something is in flight.
  const inFlight = docs?.some((d) => d.status === "queued" || d.status === "processing");
  useEffect(() => {
    if (!inFlight) return;
    const t = setInterval(load, 2000);
    return () => clearInterval(t);
  }, [inFlight, load]);

  async function upload(files: File[]) {
    if (!files.length) return;
    setError("");
    try {
      setUploads(await api.upload(files));
      load();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  }

  const counts = (docs ?? []).reduce<Record<string, number>>((acc, d) => ({ ...acc, [d.status]: (acc[d.status] ?? 0) + 1 }), {});
  const shown = (docs ?? []).filter((d) => filter === "all" || d.status === filter);

  return (
    <>
      <div
        className={`dropzone ${dragging ? "over" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => { e.preventDefault(); setDragging(false); upload([...e.dataTransfer.files]); }}
        onClick={() => input.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && input.current?.click()}
      >
        <strong>Drop PDFs here</strong> or click to choose. Invoices and purchase orders, up to 10 MB each.
        <input ref={input} type="file" accept="application/pdf,.pdf" multiple hidden onChange={(e) => { upload([...(e.target.files ?? [])]); e.target.value = ""; }} />
      </div>

      {uploads.length > 0 && (
        <ul className="upload-results">
          {uploads.map((u, i) => (
            <li key={i} className={u.error ? "error" : ""}>
              {u.filename}: {u.error ?? (u.duplicate ? `already uploaded (#${u.id})` : "queued")}
            </li>
          ))}
        </ul>
      )}
      {error && <p className="error" role="alert">{error}</p>}

      <div className="toolbar">
        <div className="filters">
          {(["all", "needs_review", "validated", "processing", "queued", "failed"] as const).map((s) => (
            <button key={s} className={filter === s ? "chip active" : "chip"} onClick={() => setFilter(s)}>
              {s === "all" ? "All" : STATUS_LABEL[s]} <span className="count">{s === "all" ? docs?.length ?? 0 : counts[s] ?? 0}</span>
            </button>
          ))}
        </div>
        <div className="export">
          <span className="muted">Export {counts.validated ?? 0} validated:</span>
          <button onClick={() => api.download("csv").catch((e) => setError(e.message))}>CSV</button>
          <button onClick={() => api.download("xlsx").catch((e) => setError(e.message))}>Excel</button>
        </div>
      </div>

      {docs === null ? <p className="muted">Loading…</p> : shown.length === 0 ? <p className="muted empty">No documents yet.</p> : (
        <table className="docs">
          <thead>
            <tr><th>#</th><th>File</th><th>Supplier</th><th>Number</th><th className="num">Total</th><th>Status</th><th>Issues</th></tr>
          </thead>
          <tbody>
            {shown.map((d) => (
              <tr key={d.id} onClick={() => (location.hash = `#/doc/${d.id}`)} className="clickable">
                <td className="muted">{d.id}</td>
                <td><a href={`#/doc/${d.id}`}>{d.filename}</a></td>
                <td>{d.supplier_name ?? <span className="muted">—</span>}</td>
                <td>{d.document_number ?? <span className="muted">—</span>}</td>
                <td className="num">{d.total ?? <span className="muted">—</span>}</td>
                <td><StatusBadge status={d.status} /></td>
                <td>
                  {d.error_count > 0 && <span className="pill err">{d.error_count} error{d.error_count > 1 ? "s" : ""}</span>}
                  {d.warning_count > 0 && <span className="pill warn">{d.warning_count} warning{d.warning_count > 1 ? "s" : ""}</span>}
                  {d.status === "failed" && <span className="muted small">{d.error}</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}

// ---------------- Review ----------------

type ScalarKey = Exclude<keyof Fields, "line_items">;
const FIELD_GROUPS: { title: string; fields: { key: ScalarKey; label: string; type?: string }[] }[] = [
  { title: "Parties", fields: [{ key: "supplier_name", label: "Supplier" }, { key: "customer_name", label: "Customer" }] },
  {
    title: "Document",
    fields: [
      { key: "document_type", label: "Type" }, { key: "document_number", label: "Number" }, { key: "po_number", label: "PO number" },
      { key: "document_date", label: "Date", type: "date" }, { key: "due_date", label: "Due date", type: "date" },
    ],
  },
  {
    title: "Amounts",
    fields: [{ key: "currency", label: "Currency" }, { key: "subtotal", label: "Subtotal" }, { key: "tax", label: "Tax" }, { key: "total", label: "Total" }],
  },
];

const emptyItem: LineItem = { description: "", quantity: null, unit_price: null, amount: null };

function Review({ id }: { id: number }) {
  const [doc, setDoc] = useState<DocumentDetail | null>(null);
  const [fields, setFields] = useState<Fields | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<{ kind: "error" | "ok"; text: string } | null>(null);

  const apply = (d: DocumentDetail) => { setDoc(d); setFields(d.fields); setDirty(false); };

  useEffect(() => {
    api.get(id).then(apply).catch((e) => setMessage({ kind: "error", text: e.message }));
    let url: string | null = null;
    api.fileUrl(id).then((u) => setPdfUrl((url = u))).catch(() => {});
    return () => { if (url) URL.revokeObjectURL(url); };
  }, [id]);

  // Keep polling while the worker still owns the document.
  useEffect(() => {
    if (!doc || (doc.status !== "queued" && doc.status !== "processing")) return;
    const t = setInterval(() => api.get(id).then(apply), 2000);
    return () => clearInterval(t);
  }, [doc, id]);

  async function act(fn: () => Promise<DocumentDetail>, ok: string) {
    setBusy(true);
    setMessage(null);
    try {
      apply(await fn());
      setMessage({ kind: "ok", text: ok });
    } catch (e) {
      const issues = e instanceof ApiError ? (e.body as { detail?: { issues?: Issue[] } })?.detail?.issues : undefined;
      if (issues && doc) setDoc({ ...doc, issues });
      setMessage({ kind: "error", text: e instanceof Error ? e.message : String(e) });
    } finally {
      setBusy(false);
    }
  }

  if (!doc) return message ? <p className="error">{message.text}</p> : <p className="muted">Loading…</p>;

  const set = (key: ScalarKey, value: string) => { setFields((f) => f && { ...f, [key]: value === "" ? null : value }); setDirty(true); };
  const setItem = (i: number, key: keyof LineItem, value: string) => {
    setFields((f) => f && { ...f, line_items: f.line_items.map((li, j) => (j === i ? { ...li, [key]: value === "" ? null : value } : li)) });
    setDirty(true);
  };
  const issuesFor = (key: string) => doc.issues.filter((i) => i.field === key || i.field?.startsWith(`${key}[`));
  const errors = doc.issues.filter((i) => i.severity === "error");
  const editable = doc.status === "needs_review" || doc.status === "validated";

  return (
    <div className="review">
      <section className="pdf">
        {pdfUrl ? <iframe src={pdfUrl} title={doc.filename} /> : <p className="muted">Loading PDF…</p>}
      </section>

      <section className="panel">
        <div className="panel-head">
          <a href="#" className="link">← All documents</a>
          <h2>{doc.filename}</h2>
          <div className="meta">
            <StatusBadge status={doc.status} />
            {doc.page_count != null && <span className="muted">{doc.page_count} page{doc.page_count > 1 ? "s" : ""}</span>}
            {doc.meta && <span className="muted">{doc.meta.llm_used ? `model: ${doc.meta.model}` : "pattern matching only"}{doc.meta.processing_ms != null && ` · ${(doc.meta.processing_ms / 1000).toFixed(1)}s`}</span>}
          </div>
        </div>

        {doc.status === "failed" && <p className="error">{doc.error}</p>}
        {(doc.status === "queued" || doc.status === "processing") && <p className="muted">{STATUS_LABEL[doc.status]}… {doc.error}</p>}

        {doc.issues.length > 0 && (
          <ul className="issues">
            {doc.issues.map((i, k) => (
              <li key={k} className={i.severity}><strong>{i.severity === "error" ? "Error" : "Warning"}</strong> {i.message}</li>
            ))}
          </ul>
        )}

        {fields && (
          <form onSubmit={(e) => { e.preventDefault(); act(() => api.saveFields(id, fields), "Saved and re-validated"); }}>
            <fieldset disabled={!editable || busy}>
              {FIELD_GROUPS.map((g) => (
                <div key={g.title} className="group">
                  <h3>{g.title}</h3>
                  <div className="grid">
                    {g.fields.map(({ key, label, type }) => {
                      const fieldIssues = issuesFor(key);
                      const source = doc.meta?.sources?.[key];
                      const changed = (doc.extracted?.[key] ?? null) !== (fields[key] ?? null);
                      const cls = fieldIssues.some((i) => i.severity === "error") ? "has-error" : fieldIssues.length ? "has-warning" : "";
                      return (
                        <label key={key} className={cls}>
                          <span>
                            {label}
                            {changed ? <em className="tag edited">edited</em> : source && <em className={`tag ${source}`}>{source}</em>}
                          </span>
                          {key === "document_type" ? (
                            <select value={fields[key] ?? ""} onChange={(e) => set(key, e.target.value)}>
                              <option value="">—</option><option value="invoice">Invoice</option><option value="purchase_order">Purchase order</option><option value="other">Other</option>
                            </select>
                          ) : (
                            <input type={type ?? "text"} value={fields[key] ?? ""} onChange={(e) => set(key, e.target.value)}
                              inputMode={["subtotal", "tax", "total"].includes(key) ? "decimal" : undefined} />
                          )}
                          {fieldIssues.map((i, k) => <small key={k}>{i.message}</small>)}
                        </label>
                      );
                    })}
                  </div>
                </div>
              ))}

              <div className="group">
                <h3>Line items</h3>
                <table className="items">
                  <thead><tr><th>Description</th><th className="num">Qty</th><th className="num">Unit price</th><th className="num">Amount</th><th /></tr></thead>
                  <tbody>
                    {fields.line_items.map((li, i) => {
                      const bad = doc.issues.some((x) => x.field?.startsWith(`line_items[${i}]`));
                      return (
                        <tr key={i} className={bad ? "has-error" : ""}>
                          <td><input value={li.description ?? ""} onChange={(e) => setItem(i, "description", e.target.value)} /></td>
                          {(["quantity", "unit_price", "amount"] as const).map((k) => (
                            <td key={k}><input className="num" inputMode="decimal" value={li[k] ?? ""} onChange={(e) => setItem(i, k, e.target.value)} /></td>
                          ))}
                          <td><button type="button" className="link" aria-label="Remove line" onClick={() => { setFields({ ...fields, line_items: fields.line_items.filter((_, j) => j !== i) }); setDirty(true); }}>✕</button></td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
                <button type="button" className="link" onClick={() => { setFields({ ...fields, line_items: [...fields.line_items, { ...emptyItem }] }); setDirty(true); }}>+ Add line</button>
              </div>
            </fieldset>

            <div className="actions">
              {message && <span className={message.kind === "error" ? "error" : "ok"} role="status">{message.text}</span>}
              {editable && <button type="submit" disabled={!dirty || busy}>Save</button>}
              {doc.status === "needs_review" && (
                <button type="button" className="primary" disabled={dirty || busy || errors.length > 0}
                  title={errors.length ? "Resolve errors first" : dirty ? "Save changes first" : ""}
                  onClick={() => act(() => api.approve(id), "Approved")}>Approve</button>
              )}
            </div>
          </form>
        )}

        <div className="danger-zone">
          {(doc.status === "failed" || doc.status === "needs_review") && (
            <button className="link" disabled={busy} onClick={() => (doc.status === "failed" || confirm("Re-running discards your edits. Continue?")) && act(() => api.reprocess(id), "Re-queued")}>Re-run extraction</button>
          )}
          <button className="link danger" disabled={busy} onClick={async () => {
            if (confirm(`Delete ${doc.filename}?`)) { await api.remove(id); location.hash = ""; }
          }}>Delete</button>
        </div>
      </section>
    </div>
  );
}

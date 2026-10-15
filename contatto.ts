// @ts-nocheck
// Supabase Edge Function "contatto": riceve il modulo contatti del sito, lo salva e lo gira per email a Garda Center.
// IMPORTANTE: alla pubblicazione "Verify JWT" va SPENTO. Secret usati: RESEND_API_KEY (già presente), NOTIFICA_EMAIL (facoltativo).
const URL_ = Deno.env.get("SUPABASE_URL")!;
const SERVICE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const RESEND = Deno.env.get("RESEND_API_KEY") || "";
const TO = Deno.env.get("NOTIFICA_EMAIL") || "gardacenter.srl@gmail.com";
const FROM = Deno.env.get("MAIL_FROM") || "Garda Center <rimessaggio@mail.gardacenter.info>";
const SH = { apikey: SERVICE, Authorization: `Bearer ${SERVICE}`, "Content-Type": "application/json" };
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info", "Access-Control-Allow-Methods": "POST, OPTIONS" };
const J = (o: any, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...CORS, "Content-Type": "application/json" } });
const esc = (t: string) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const cut = (v: any, n: number) => String(v ?? "").replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").trim().slice(0, n);
async function sha(s: string) { const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)); return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("").slice(0, 32); }
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return J({ ok: false }, 405);
  let b: any; try { b = await req.json(); } catch { return J({ ok: false }, 400); }
  // trappola per i robot: il campo "sito" deve restare vuoto; finto successo
  if (b.sito) return J({ ok: true });
  if (Number(b.ms) < 2500) return J({ ok: true });
  const nome = cut(b.nome, 120), email = cut(b.email, 160), msg = cut(b.messaggio, 3000);
  if (!nome || !msg || !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return J({ ok: false, err: "dati" }, 400);
  const ip = (req.headers.get("x-forwarded-for") || "").split(",")[0].trim() || "?";
  const h = await sha(ip + "|garda-contatti");
  const da = new Date(Date.now() - 3600_000).toISOString();
  const c = await fetch(`${URL_}/rest/v1/contatti?select=id&ip_hash=eq.${h}&creato=gte.${da}`, { headers: { ...SH, Prefer: "count=exact", Range: "0-0" } });
  const tot = parseInt((c.headers.get("content-range") || "0/0").split("/")[1] || "0");
  if (tot >= 5) return J({ ok: false, err: "troppe" }, 429);
  const row = { nome, email, telefono: cut(b.telefono, 40), motivo: cut(b.motivo, 20), mezzo: cut(b.mezzo, 20), lunghezza: cut(b.lunghezza, 6), asse: !!b.asse, messaggio: msg, lingua: cut(b.lingua, 2), ip_hash: h };
  const r = await fetch(`${URL_}/rest/v1/contatti`, { method: "POST", headers: SH, body: JSON.stringify(row) });
  if (!r.ok) { console.error("db", r.status, (await r.text()).slice(0, 200)); return J({ ok: false }, 500); }
  if (RESEND) {
    const righe = [["Nome", nome], ["Email", email], ["Telefono", row.telefono], ["Motivo", row.motivo], ["Mezzo", row.mezzo + (row.lunghezza ? ` ${row.lunghezza} m` : "") + (row.asse ? " (asse doppio)" : "")], ["Lingua del sito", row.lingua]];
    const txt = righe.filter((x) => x[1]).map((x) => `${x[0]}: ${x[1]}`).join("\n") + `\n\n${msg}`;
    const html = `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.5;color:#222;max-width:620px">${esc(txt).replace(/\n/g, "<br>")}</div>`;
    const m = await fetch("https://api.resend.com/emails", { method: "POST", headers: { Authorization: `Bearer ${RESEND}`, "Content-Type": "application/json" }, body: JSON.stringify({ from: FROM, to: [TO], reply_to: email, subject: `Sito: richiesta da ${nome}`, html, text: txt }) });
    if (!m.ok) console.error("resend", m.status, (await m.text()).slice(0, 200));
  }
  return J({ ok: true });
});

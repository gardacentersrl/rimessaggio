/* Garda Center · comportamento delle pagine. Nessun servizio esterno (la mappa si carica solo al click). */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var LANG = document.documentElement.lang || "it";
  var AREA = "https://app.gardacenter.info/ospiti.html";

  // menu
  var bg = $(".burger"), mn = $("#menu");
  if (bg && mn) bg.addEventListener("click", function () { var on = mn.classList.toggle("on"); bg.setAttribute("aria-expanded", on ? "true" : "false"); });

  // nastro dell'anno
  var rb = $("#ribbon"), now = $("#now"), st = $("#state");
  if (rb && now) {
    var d = new Date(), m = d.getMonth(), dim = new Date(d.getFullYear(), m + 1, 0).getDate();
    now.style.left = (((m + (d.getDate() - 0.5) / dim) / 12) * 100).toFixed(2) + "%"; now.classList.add("on");
    var open = (m >= 3 && m <= 8) || (m === 9 && d.getDate() === 1);
    if (st) st.textContent = open ? st.dataset.o : st.dataset.c;
  }

  // mappe: si caricano solo al click
  $$(".mappa").forEach(function (box) {
    var b = $("button", box); if (!b) return;
    b.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.loading = "lazy"; f.referrerPolicy = "no-referrer-when-downgrade"; f.title = "Google Maps";
      f.src = "https://www.google.com/maps?q=" + encodeURIComponent(box.dataset.q.replace(/\+/g, " ")) + "&output=embed&hl=" + LANG;
      box.innerHTML = ""; box.appendChild(f);
    });
  });

  // calcolatore prezzi
  var cf = $("#calc");
  if (cf && window.GC && window.GCB && GCB[LANG]) {
    var B = GCB[LANG], T = window.GCP || {}, ty = $("#ct"), ln = $("#cl"), dxw = $("#cdxw"), dx = $("#cdx"), out = $("#cout");
    var sync = function () { dxw.style.display = ty.value === "roulotte" ? "flex" : "none"; ln.parentNode.style.display = ty.value === "carrello" ? "none" : ""; };
    ty.addEventListener("change", sync); sync();
    cf.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var type = ty.value, len = parseFloat(String(ln.value).replace(",", "."));
      if (type !== "carrello" && !(len >= 2 && len <= 20)) { out.textContent = T.need || ""; ln.focus(); return; }
      var a = GC.annual(type, len, dx.checked), t = GC.transport(type, len, dx.checked);
      var h = "<div>" + T.r_ann + ": <b>" + B.m(a) + "</b></div>";
      h += t != null ? "<div>" + T.r_tr + ": <b>" + B.m(t) + "</b></div>" : "<div>" + (T.tr_none || "") + "</div>";
      out.innerHTML = h;
    });
  }

  // modulo contatti
  var fm = $("#cform");
  if (fm) {
    var qs = new URLSearchParams(location.search), t0 = Date.now(), M = window.GCF || {};
    if (qs.get("m") && $("#fm [value='" + qs.get("m") + "']")) $("#fm").value = qs.get("m");
    if (qs.get("q")) $("#fg").value = qs.get("q").slice(0, 1000);
    if (qs.get("t")) $("#fy").value = qs.get("t");
    var msg = $("#fmsg"), btn = $("#fs"), say = function (cls, tx) { msg.className = "msg " + cls; msg.textContent = tx; };
    fm.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var bad = [];
      ["fn", "fe", "fg"].forEach(function (id) { var el = $("#" + id), ok = el.value.trim() && (id !== "fe" || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value.trim())); el.style.borderColor = ok ? "" : "var(--ko)"; if (!ok) bad.push(el); });
      if (!$("#fc").checked) bad.push($("#fc"));
      if (bad.length) { say("ko", M.bad); bad[0].focus(); return; }
      btn.disabled = true; var lab = btn.textContent; btn.textContent = M.sending; say("", "");
      var body = { nome: $("#fn").value.trim(), email: $("#fe").value.trim(), telefono: $("#ft").value.trim(), motivo: $("#fm").value, mezzo: $("#fy").value,
        lunghezza: $("#fl").value.trim(), asse: $("#fd").checked, messaggio: $("#fg").value.trim(), lingua: fm.dataset.lang, sito: $("#fw").value, ms: Date.now() - t0 };
      fetch(fm.dataset.url, { method: "POST", headers: { "Content-Type": "application/json", apikey: fm.dataset.key, Authorization: "Bearer " + fm.dataset.key }, body: JSON.stringify(body) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || !j.ok) throw 0; }); })
        .then(function () { say("ok", M.ok); fm.reset(); btn.textContent = lab; btn.disabled = false; })
        .catch(function () { say("ko", M.err); btn.textContent = lab; btn.disabled = false; });
    });
  }

  // assistente
  var fab = $("#botfab"), bot = $("#bot");
  if (fab && bot && window.GC && window.GCB && GCB[LANG]) {
    var B = GCB[LANG], U = B.ui, ctx = GC.newCtx(), lastQ = "", started = false;
    fab.lastChild.textContent = U.fab;
    bot.innerHTML = '<header><img src="../assets/logo-120.png" alt=""><div><b id="bot-t">' + U.title + '</b><small>' + U.sub + '</small></div><button type="button" aria-label="' + U.close + '">×</button></header>' +
      '<div class="log" id="blog" aria-live="polite"></div><p class="nota">' + U.note + '</p><form><input id="bin" autocomplete="off" maxlength="300" placeholder="' + U.ph + '" aria-label="' + U.ph + '"><button type="submit">' + U.send + '</button></form>';
    var log = $("#blog"), inp = $("#bin");
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    var scroll = function () { log.scrollTop = log.scrollHeight; };
    function addMsg(cls, h) { var d = document.createElement("div"); d.className = "m " + cls; d.innerHTML = h; log.appendChild(d); scroll(); }
    function clearChips() { $$(".chips", log).forEach(function (c) { c.remove(); }); }
    function href(h) { return h === "#form" ? U.formpage + "?m=info" + (lastQ ? "&q=" + encodeURIComponent(lastQ) : "") : h === "#where" ? "location.html" : h === "#login" ? AREA : h; }
    function addChips(list) {
      if (!list.length) return; var w = document.createElement("div"); w.className = "chips";
      list.forEach(function (c) {
        var el;
        if (c.href) { el = document.createElement("a"); el.href = href(c.href); if (c.primary) el.className = "p"; }
        else { el = document.createElement("button"); el.type = "button"; el.addEventListener("click", function () { ask(c.send); }); }
        el.textContent = c.label; w.appendChild(el);
      });
      log.appendChild(w); scroll();
    }
    function ask(text) {
      text = String(text || "").trim(); if (!text) return;
      clearChips(); addMsg("u", esc(text)); lastQ = text;
      var r; try { r = GC.respond(text, ctx, B); } catch (e) { r = { msgs: [B.fallback], chips: [], handoff: true }; }
      r.msgs.forEach(function (h) { addMsg("b", h); });
      var ch = r.chips.slice();
      if (r.handoff) ch.push({ label: U.form, href: "#form", primary: true }, { label: U.call, href: "tel:+393475539170" });
      addChips(ch);
    }
    function openBot() {
      bot.classList.add("on"); fab.style.display = "none"; document.body.classList.add("noscroll");
      if (!started) { started = true; addMsg("b", B.hello); addChips(B.chips.map(function (c) { return { label: c[0], send: c[1] }; })); }
      setTimeout(function () { inp.focus(); }, 50);
    }
    function closeBot() { bot.classList.remove("on"); fab.style.display = ""; document.body.classList.remove("noscroll"); fab.focus(); }
    fab.addEventListener("click", openBot);
    $("header button", bot).addEventListener("click", closeBot);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && bot.classList.contains("on")) closeBot(); });
    $("form", bot).addEventListener("submit", function (e) { e.preventDefault(); var v = inp.value; inp.value = ""; ask(v); });
    $$("a[href='#assistente']").forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); openBot(); }); });
  } else if (fab) fab.style.display = "none";
})();

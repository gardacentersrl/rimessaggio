/* Garda Center · tariffe e logica dell'assistente (nessun servizio esterno, nessun costo).
   Funziona nel browser e in Node (per i test). Le frasi delle risposte stanno in bot-data.js. */
(function (root) {
  "use strict";
  // ---------- Tariffe 2026 (da tabella prezzi; trasporti validi tra Peschiera e Garda) ----------
  var P = {
    roulotte: [[6, 600], [7, 700], [8, 800], [Infinity, 1000]], dx: 100,
    barca: [[6, 800], [8, 900], [9, 1200], [Infinity, 1400]],
    carrello: 350,
    sea: { roulotte: { s2: 100, s1: 200, s3: 300 }, barca: { s2: 200, s1: 300, s3: 450 }, carrello: { s2: 100, s1: 200, s3: 300 } },
    tr: { roulotte: [[7, 70], [Infinity, 80]], dx: 20, barca: [[7, 80], [Infinity, 110]] }
  };
  function tier(arr, len) { for (var i = 0; i < arr.length; i++) if (len <= arr[i][0]) return arr[i][1]; return null; }
  function annual(type, len, dx) {
    if (type === "carrello") return P.carrello;
    var p = tier(P[type], len); if (p == null) return null;
    return type === "roulotte" && dx ? p + P.dx : p;
  }
  function transport(type, len, dx) {
    if (!P.tr[type]) return null;
    var p = tier(P.tr[type], len); if (p == null) return null;
    return type === "roulotte" && dx ? p + P.tr.dx : p;
  }

  // ---------- Testo ----------
  function norm(s) {
    return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9.,'’\s]/g, " ").replace(/\s+/g, " ").trim();
  }
  var NUM = "(\\d{1,2}(?:[.,]\\d{1,2})?)";
  var LEN_UNIT = new RegExp(NUM + "\\s*(?:m|mt|mtr|mtrs|metri|metro|metre|metres|meter|meters|metern|mtr\\.)\\b");
  function parseLen(t, expectBare) {
    var m = t.match(LEN_UNIT);
    if (!m && expectBare) m = t.match(new RegExp("^\\D*" + NUM + "\\D*$"));
    if (!m) return null;
    var v = parseFloat(m[1].replace(",", "."));
    return v >= 2 && v <= 20 ? v : null;
  }
  function parseDur(t) {
    var m = t.match(/(\d{1,3})\s*(giorn|day|tag|dag)/); if (m) { var d = +m[1]; return d <= 14 ? "s2" : d <= 31 ? "s1" : d <= 92 ? "s3" : "long"; }
    m = t.match(/(\d{1,2})\s*(settiman|week|woche|weken)/); if (m) { var w = +m[1]; return w <= 2 ? "s2" : w <= 4 ? "s1" : w <= 13 ? "s3" : "long"; }
    m = t.match(/(\d{1,2})\s*(mes|month|monat|maand)/); if (m) { var mo = +m[1]; return mo <= 1 ? "s1" : mo <= 3 ? "s3" : "long"; }
    if (/(un|1|one|ein|een)\s*(mese|month|monat|maand)/.test(t)) return "s1";
    if (/(una|1|one|eine|een)\s*(settimana|week|woche)/.test(t)) return "s2";
    if (/(due|2|two|zwei|twee)\s*(settimane|weeks|wochen|weken)/.test(t)) return "s2";
    return null;
  }
  var RX = {
    roulotte: /roulott|caravan|wohnwagen|woonwagen/,
    barca: /\bbarc|motoscaf|gommon|\bboat|speedboat|motorboat|\bboot|motorboot|schlauchboot|bootje|sloep|rubberboot/,
    carrello: /moto d.?acqua|motodacqua|jet ?ski|jetski|waterscooter|wetbike|personal watercraft|carrello|\bwave ?runner/,
    camper: /\bcamper|wohnmobil|motorhome|motor home|kampeerauto|campervan|\bvan\b|furgon/,
    vela: /\bvela\b|barca a vela|sailboat|sailing|segelboot|zeilboot|zeiljacht/,
    dx: /asse doppio|doppio asse|due assi|2 assi|\btandem|double axle|dual axle|two axle|2 axle|doppelachs|zwei achsen|2 achsen|dubbele as|tweeas|2 assen|twee assen/,
    sx: /asse singolo|singolo asse|un asse|single axle|einachs|enkele as/
  };
  var INT = [
    ["greet", /\b(ciao|buongiorno|buonasera|salve|hello|hi|hey|good (morning|afternoon|evening)|hallo|guten (tag|morgen|abend)|moin|goedemorgen|goedendag)\b/],
    ["thanks", /grazie|thank|danke|bedankt|dank je|dankjewel|merci/],
    ["price", /prezz|quot[ae]|annual[ei]?\b|costo|costa|costi|quanto|tariff|retta|canone|\bprice|\bcost|how much|\bfee\b|annual fee|jahrespreis|jaarprijs|\bfees\b|\brate\b|preis|kosten|wieviel|wie viel|gebuhr|prijs|prijzen|\bkost\b|tarief|hoeveel/],
    ["season", /stagional|seasonal|saison|seizoen|settiman|\bmese\b|\bmesi\b|\bweeks?\b|\bmonths?\b|woche|monat|maand|\bweken\b/],
    ["transport", /trasport|trasferi|navett|transport|shuttle|transfer|abhol|vervoer|ophalen|consegn|delivery|campeggio|camping|campsite|campingplatz|peschiera|\bgarda\b.*(porta|bring)/],
    ["insurance", /assicur|polizza|insur|coverage|versicher|verzeker|furto|theft|diebstahl|diefstal|\bdann[oi]\b|damage|risarc|massimal|schaden|schade|compensation/],
    ["hours", /(?<!all['’ ]?)apert|chius|orari|gennaio|febbraio|marzo|novembre|dicembre|january|february|march|november|december|januar|februar|marz|dezember|januari|februari|maart|\bopen\b|closed|opening|hours|offen|offnet|geschlossen|offnungs|geopend|gesloten|openingstijd|1 ottobre|1 aprile|1 october|1 april|1 oktober|inverno|winter|seasonal opening|periodo|period/],
    ["pickup", /ritir|prelev|uscit|uscire|portar(e)? via|pick ?up|collect|take (it|my|the).{0,12}out|get my|abhol|\bhol(e|en)\b|herausnehm|ophaal|uit de stalling|preavviso|notice|vorlauf|wegbrengen/],
    ["return", /riconsegn|rientr|ripor|consegnar|bring (it )?back|drop ?off|return|zuruck|abgeben|anliefern|terugbrengen|inleveren|binnenbrengen/],
    ["payment", /pagament|pagare|bonifico|\bcarta\b|\biban\b|saldo|acconto|caparra|scadenz|payment|\bpay\b|deposit|balance|bank|\bideal\b|zahlung|bezahl|uberweis|anzahlung|kreditkarte|creditcard|kaart|betal|storting|aanbetaling|saldo|stripe/],
    ["booking", /prenot|riserv|disponibil|\bbook|reserve|reservation|availab|buche|reservier|verfugbar|boeken|reserveer|beschikbaar|diventare cliente|become a customer|nuovo cliente|new customer|posto (per|libero)|space for|spot for|plek voor|platz fur/],
    ["documents", /document|libretto|identita|passaporto|patente|contratto|firma|contract|passport|licen[cs]e|registration|papers|vertrag|ausweis|fahrzeugschein|unterschrift|papieren|identiteitsbewijs|kenteken|kentekenbewijs|handtekening/],
    ["included", /includ|compres|cosa offr|inclus|what do i get|what.s in|enthalt|inklusive|leistung|inbegrepen|diensten|servizi/],
    ["security", /sicurez|sorveglian|allarm|telecamer|security|\bsafe\b|alarm|camera|surveillance|sicherheit|beveiliging|bewaking|veilig/],
    ["gas", /bombol|\bgas\b|infiammab|gasflasche|gasfles|flammable|propane|\blpg\b|gasbottle|gas bottle/],
    ["location", /\bdove\b|indirizz|\bsede\b|\bsedi\b|come arrivare|mappa|raggiung|\bwhere\b|address|location|find you|directions|\bmap\b|\bwo\b|adresse|standort|anfahrt|\bwaar\b|adres|locatie|route|navigat/],
    ["contact", /telefon|chiam|e-?mail|\bmail\b|contatt|numero|whatsapp|\bphone\b|\bcall\b|contact|reach you|kontakt|anrufen|nummer|bellen|contacteren/],
    ["washing", /lavagg|lavare|\bwash|clean|reinig|waschen|wassen|schoonmaak/],
    ["extras", /extra|zusatz|supplement|penale|penalt|late fee|surcharge|zuschlag|aufpreis|toeslag|boete|in ritardo|ritardo/],
    ["indoor", /all['’ ]?aperto|im freien|coperto|\binterno\b|inside|indoor|outdoor|esterno|overdekt|\bbinnen\b|\bbuiten\b|drinnen|\bhalle|\binnen\b|aussen|capannon|shed|warehouse|hangar/],
    ["login", /area clienti|login|accedi|accesso|\bentra|account|password|\bcodice\b|customer area|client area|portal|kundenbereich|anmelden|inloggen|klantenpagina|klantenportaal|my area/],
    ["size", /dimension|altezza|larghezza|massim|height|width|max(imum)? size|how big|how large|largest|\bhohe\b|breite|grosse|maximal|hoogte|breedte|afmeting|\bpeso\b|weight|gewicht/],
    ["about", /chi siete|who are you|about you|uber uns|over ons|chi e garda/]
  ];
  function detect(t) {
    var best = null, bs = 0, hits = {};
    for (var i = 0; i < INT.length; i++) {
      var m = t.match(new RegExp(INT[i][1].source, "g")); var c = m ? m.length : 0;
      hits[INT[i][0]] = c;
      if (c > bs) { bs = c; best = INT[i][0]; }
    }
    return { best: best, hits: hits };
  }

  // ---------- Conversazione ----------
  function newCtx() { return { type: null, len: null, dx: null, dur: null, pend: null, intent: null }; }
  function fill(t, ctx, expect) {
    var ty = null;
    if (RX.carrello.test(t)) ty = "carrello"; else if (RX.roulotte.test(t)) ty = "roulotte"; else if (RX.barca.test(t)) ty = "barca";
    if (ty) { if (ty !== ctx.type) { ctx.len = ty === "carrello" ? null : ctx.len; } ctx.type = ty; }
    var l = parseLen(t, expect === "len"); if (l != null) ctx.len = l;
    if (RX.dx.test(t)) ctx.dx = true; else if (RX.sx.test(t)) ctx.dx = false;
    var d = parseDur(t); if (d) ctx.dur = d;
    return ty;
  }
  /* respond(text, ctx, B) -> { msgs:[{html}], chips:[{label,send}|{label,href,primary}], handoff:bool } */
  function respond(text, ctx, B) {
    var t = norm(text), out = { msgs: [], chips: [], handoff: false };
    function say(h) { out.msgs.push(h); }
    function chips() { for (var i = 0; i < arguments.length; i++) out.chips.push(arguments[i]); }
    function ask(what) { ctx.pend = what; say(B.ask[what]); if (what === "type") chips({ label: B.types.roulotte, send: B.types.roulotte }, { label: B.types.barca, send: B.types.barca }, { label: B.types.carrello, send: B.types.carrello }); if (what === "dur") chips({ label: B.dur.s2, send: B.dur.s2 }, { label: B.dur.s1, send: B.dur.s1 }, { label: B.dur.s3, send: B.dur.s3 }); }
    function handoff(msg) { out.handoff = true; say(msg || B.fallback); }
    if (!t) { say(B.empty); return out; }

    // 1) risposta a una domanda in sospeso
    var pend = ctx.pend; ctx.pend = null;
    var before = JSON.stringify([ctx.type, ctx.len, ctx.dx, ctx.dur]);
    var isNew = detect(t);
    var specific = isNew.best && isNew.best !== "price" && isNew.best !== "season" && isNew.best !== "transport";
    if (pend && !(specific && isNew.hits[isNew.best] > 0 && !/^\d/.test(t))) {
      fill(t, ctx, pend === "len" ? "len" : null);
      if (JSON.stringify([ctx.type, ctx.len, ctx.dx, ctx.dur]) !== before) return answerPrice(ctx.intent || "price");
      if (RX.camper.test(t) || RX.vela.test(t)) { handoff(B.noTariff); return out; }
      // niente di nuovo: continua con l'analisi normale
    }
    var d = detect(t), intent = d.best, h = d.hits;
    if (RX.camper.test(t) && !RX.roulotte.test(t)) { ctx.type = null; handoff(B.noTariff); return out; }
    if (RX.vela.test(t)) { handoff(B.noTariff); return out; }
    var hadType = fill(t, ctx, null);
    var hasData = hadType || parseLen(t, false) != null;
    // intenti di prezzo
    if (h.extras > 0 && h.extras >= (h.price || 0) && !hasData && !(h.season > 0)) intent = "extras";
    else if (h.season > 0 && (h.price > 0 || hasData || ctx.intent === "price")) intent = "season";
    else if (h.transport > 0 && h.transport >= (h.price || 0)) intent = "transport";
    else if (h.price > 0 && (h.price >= (h.insurance || 0)) && !(h.extras > 0 && h.price === h.extras && !hasData)) intent = "price";
    if (!intent && hasData) intent = ctx.intent && /price|season|transport/.test(ctx.intent) ? ctx.intent : "price";
    if (intent === "price" || intent === "season" || intent === "transport") { ctx.intent = intent; return answerPrice(intent); }
    if (!intent) { handoff(); return out; }
    if (intent === "greet") { say(B.hello); chips.apply(null, B.chips.map(function (c) { return { label: c[0], send: c[1] }; })); return out; }
    if (intent === "thanks") { say(B.thanks); return out; }
    var a = B.a[intent];
    if (intent === "size") { handoff(B.a.size); return out; }
    if (!a) { handoff(); return out; }
    say(a);
    var next = B.next[intent] || [];
    next.forEach(function (n) { chips(n[1].charAt(0) === "#" ? { label: n[0], href: n[1], primary: n[1] === "#form" } : { label: n[0], send: n[1] }); });
    return out;

    function answerPrice(kind) {
      var ty = ctx.type, len = ctx.len;
      if (!ty) { ask("type"); return out; }
      var T = B.types[ty];
      if (kind === "season") {
        if (!ctx.dur) { ask("dur"); return out; }
        if (ctx.dur === "long") { say(B.seasonLong); chips({ label: B.chipAnnual, send: B.chipAnnual }); return out; }
        say(B.f.season(T, B.dur[ctx.dur], P.sea[ty][ctx.dur])); chips({ label: B.chipAnnual, send: B.chipAnnual }, { label: B.chipTransport, send: B.chipTransport }); return out;
      }
      if (ty !== "carrello" && len == null) { ask("len"); return out; }
      if (kind === "transport") {
        var tp = transport(ty, len, ctx.dx);
        if (tp == null) { handoff(B.f.noTransport(T)); return out; }
        var extra = ty === "roulotte" && ctx.dx == null ? B.f.dxTr(tp + P.tr.dx) : "";
        say(B.f.transport(T, len, tp, extra)); chips({ label: B.chipAnnual, send: B.chipAnnual }, { label: B.chipOtherRoute, href: "#form", primary: true }); return out;
      }
      var p = annual(ty, len, ctx.dx);
      if (p == null) { handoff(B.fallback); return out; }
      var dxNote = ty === "roulotte" && ctx.dx == null ? B.f.dxAnnual(p + P.dx) : "";
      say(B.f.annual(T, len, p, dxNote)); chips({ label: B.chipTransport, send: B.chipTransport }, { label: B.chipIncluded, send: B.chipIncluded }, { label: B.chipBook, send: B.chipBook });
      return out;
    }
  }
  var api = { P: P, annual: annual, transport: transport, norm: norm, respond: respond, newCtx: newCtx, parseLen: parseLen, detect: detect };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.GC = api;
})(typeof window !== "undefined" ? window : globalThis);

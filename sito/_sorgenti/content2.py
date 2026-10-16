# -*- coding: utf-8 -*-
# Correzioni dopo le indicazioni del titolare + versione olandese. Si applica sopra content.py
import copy
from content import *
import content

SEDI["cam"].update(ind="Via Galileo Galilei", cap="Località Camporengo, 37010 Cavaion Veronese (VR)", q="Via Galileo Galilei, Camporengo, Cavaion Veronese VR")
SEDI["cas"].update(ind="Località Casalmenini, 4", cap="37010 Rivoli Veronese (VR)", q="Località Casalmenini 4, Rivoli Veronese VR")

def faq_set(L, id_, q=None, a=None):
    lst = C[L]["FAQ"]
    for i, (k, qq, aa) in enumerate(lst):
        if k == id_:
            lst[i] = (k, q or qq, a if a is not None else aa); return
    raise KeyError(id_)
def faq_after(L, after, item):
    lst = C[L]["FAQ"]
    for i, (k, _, _) in enumerate(lst):
        if k == after: lst.insert(i + 1, item); return
    raise KeyError(after)

PRIV = {}
TXT = {
 "it": dict(
  lede="Rimessaggio invernale in capannoni chiusi a Cavaion Veronese e Rivoli Veronese. Assicurato, con accessi controllati, gestito da una famiglia.",
  d_index="Rimessaggio invernale al coperto per roulotte, barche e moto d'acqua a Cavaion Veronese e Rivoli Veronese. Assicurato, con controllo degli accessi, a gestione familiare.",
  sec_h="Accessi", sec="Controllo automatizzato degli accessi all'interno della proprietà.",
  iva="Prezzi IVA inclusa.", pfoot="I prezzi sono in euro, IVA inclusa, e valgono per la stagione indicata. Se cambiano, il contratto prevede che ti mandiamo la tabella aggiornata.",
  prsub="Quota annuale per il parcheggio invernale. IVA inclusa.",
  trn=dict(h="Trasporto del mezzo", p="Possiamo organizzare il trasporto del tuo mezzo da e per il deposito. Scrivici dove e quando ti serve e ti rispondiamo con le condizioni.", c="Chiedi un trasporto"),
  ti="Possiamo organizzare il trasporto del tuo mezzo da e per il deposito. Scrivici dove e quando ti serve e ti rispondiamo con le condizioni.",
  camper="Mi dispiace: non ospitiamo camper. Teniamo roulotte, barche e moto d'acqua.",
  f_included="Sono inclusi l'assicurazione, **1 lavaggio standard** e **2 uscite per stagione**. Il posto è sempre al coperto e la proprietà ha un controllo automatizzato degli accessi.",
  f_sec=("Com'è protetto il deposito?", "La proprietà ha un controllo automatizzato degli accessi."),
  f_extras="Sì, in alcuni casi: **100 €** se il saldo arriva dopo il 30 settembre, **50 €** se ci avvisi del ritiro con meno di una settimana di preavviso, **50 €** per ogni uscita oltre le 2 incluse. Il trasporto, se lo richiedi, si concorda a parte.",
  f_tr=("Fate anche il trasporto del mezzo?",),
  f_loc="Abbiamo due sedi: **Camporengo**, Via Galileo Galilei, Cavaion Veronese (VR), e **Casalmenini**, Località Casalmenini 4, Rivoli Veronese (VR). Ti diciamo noi in quale sede si trova il tuo mezzo.",
  f_about=None,
  fannual="function(T,len,p,dx){return '<b>'+B.m(p)+'</b> (IVA inclusa) per la quota annuale di una '+T.toLowerCase()+(len?' di '+B.n(len)+' m':'')+'. Comprende assicurazione, 1 lavaggio e 2 uscite.'+dx}",
  chipTr="Organizzate il trasporto?", chipOther="Chiedi un trasporto",
  priv=["**Chi tratta i tuoi dati.** Garda Center S.r.l., P.IVA 03578820239, sede legale in Via Galileo Galilei, Cavaion Veronese (VR). Email: " + EMAIL + ".",
   "**Quali dati raccogliamo.** Se scrivi dal modulo di contatto: nome, email, telefono (facoltativo), tipo e lunghezza del mezzo, il tuo messaggio e la lingua del sito. Per limitare gli invii automatici conserviamo anche un codice anonimo ricavato dal tuo indirizzo IP (non l'indirizzo stesso). Le domande che scrivi all'assistente restano nel tuo browser: non vengono inviate né salvate da noi.",
   "**Perché li usiamo e su quale base.** Per rispondere alla tua richiesta e, se lo desideri, proporti un posto (art. 6.1.b GDPR, misure precontrattuali su richiesta dell'interessato). Il codice anti-spam serve a proteggere il modulo (art. 6.1.f, legittimo interesse). Dare i dati è facoltativo, ma senza nome, email e messaggio non possiamo risponderti.",
   "**Per quanto tempo.** Le richieste che non diventano un contratto sono cancellate dopo 12 mesi. Se diventi cliente, i dati seguono il contratto e gli obblighi di legge (per esempio quelli fiscali, 10 anni); per i clienti vale l'informativa allegata al contratto.",
   "**Chi li riceve.** Solo fornitori tecnici che li trattano per nostro conto: Supabase (database, che si trova in Italia, e funzioni del sito), Resend (invio delle email) e GitHub (ospita le pagine del sito, può registrare l'indirizzo IP dei visitatori per sicurezza). Alcuni di questi fornitori hanno sede o server fuori dall'Unione europea (Stati Uniti): il trasferimento avviene con le garanzie previste dal GDPR (clausole contrattuali standard o Data Privacy Framework). Non vendiamo né cediamo i dati a terzi per scopi commerciali.",
   "**Cookie e mappe.** Questo sito non usa cookie di profilazione né strumenti di statistica. Le mappe di Google si caricano solo se premi il pulsante: in quel momento Google riceve il tuo indirizzo IP e può usare i propri cookie, secondo la sua informativa.",
   "**I tuoi diritti.** Puoi chiedere accesso, correzione, cancellazione, limitazione o portabilità dei dati e opporti al trattamento scrivendo a " + EMAIL + ". Se pensi che i tuoi dati non siano trattati correttamente puoi presentare reclamo al Garante per la protezione dei dati personali (garanteprivacy.it).",
   "Ultimo aggiornamento: ottobre 2026."]),
 "en": dict(
  lede="Winter storage in closed sheds in Cavaion Veronese and Rivoli Veronese. Insured, with controlled access, run by a family.",
  d_index="Indoor winter storage for caravans, boats and jet skis in Cavaion Veronese and Rivoli Veronese, Lake Garda. Insured, with access control, family run.",
  sec_h="Access", sec="Automated access control inside the property.",
  iva="Prices include VAT.", pfoot="Prices are in euro, VAT included, and apply to the season shown. If they change, the contract says we send you the updated price table.",
  prsub="Annual fee for winter parking. VAT included.",
  trn=dict(h="Vehicle transport", p="We can arrange transport of your vehicle to and from the storage. Tell us where and when you need it and we reply with the terms.", c="Ask for transport"),
  ti="We can arrange transport of your vehicle to and from the storage. Tell us where and when you need it and we reply with the terms.",
  camper="Sorry, we do not store motorhomes. We keep caravans, boats and jet skis.",
  f_included="Included are insurance, **1 standard wash** and **2 exits per season**. The space is always indoors and the property has automated access control.",
  f_sec=("How is the storage protected?", "The property has automated access control."),
  f_extras="In some cases: **100 €** if the balance arrives after 30 September, **50 €** if you tell us about collection with less than one week's notice, **50 €** for each exit beyond the 2 included. Transport, if you ask for it, is agreed separately.",
  f_tr=("Do you also arrange transport?",),
  f_loc="We have two sites: **Camporengo**, Via Galileo Galilei, Cavaion Veronese (VR), and **Casalmenini**, Località Casalmenini 4, Rivoli Veronese (VR). We will tell you which site your vehicle is at.",
  fannual="function(T,len,p,dx){return '<b>'+B.m(p)+'</b> (VAT included) for the annual fee of a '+T.toLowerCase()+(len?' of '+B.n(len)+' m':'')+'. It includes insurance, 1 wash and 2 exits.'+dx}",
  chipTr="Do you arrange transport?", chipOther="Ask for transport",
  priv=["**Who processes your data.** Garda Center S.r.l., VAT no. IT03578820239, registered office at Via Galileo Galilei, Cavaion Veronese (VR), Italy. Email: " + EMAIL + ".",
   "**What we collect.** If you write through the contact form: name, email, phone (optional), type and length of your vehicle, your message and the site language. To limit automated submissions we also keep an anonymous code derived from your IP address (not the address itself). Questions you type to the assistant stay in your browser: we neither receive nor store them.",
   "**Why and on what basis.** To answer your request and, if you wish, offer you a space (art. 6(1)(b) GDPR, steps taken at your request before a contract). The anti-spam code protects the form (art. 6(1)(f), legitimate interest). Providing the data is optional, but without name, email and message we cannot reply.",
   "**How long.** Requests that do not become a contract are deleted after 12 months. If you become a customer, the data follows the contract and legal obligations (for example tax records, 10 years); customers are covered by the notice attached to the contract.",
   "**Who receives it.** Only technical providers processing it on our behalf: Supabase (database, located in Italy, and site functions), Resend (sending emails) and GitHub (hosts the site pages and may log visitors' IP addresses for security). Some of them are based or have servers outside the European Union (United States): transfers rely on the safeguards required by the GDPR (standard contractual clauses or the Data Privacy Framework). We do not sell or pass on data to third parties for marketing.",
   "**Cookies and maps.** This site uses no profiling cookies and no analytics. Google Maps loads only if you press the button: at that point Google receives your IP address and may use its own cookies, under its own policy.",
   "**Your rights.** You can ask for access, correction, deletion, restriction or portability of your data and object to processing by writing to " + EMAIL + ". If you believe your data is not handled correctly you can complain to the Italian data protection authority (Garante per la protezione dei dati personali, garanteprivacy.it).",
   "Last updated: October 2026."]),
 "de": dict(
  lede="Winterstellplätze in geschlossenen Hallen in Cavaion Veronese und Rivoli Veronese. Versichert, mit kontrolliertem Zugang, von einer Familie geführt.",
  d_index="Überdachte Winterstellplätze für Wohnwagen, Boote und Jetskis in Cavaion Veronese und Rivoli Veronese am Gardasee. Versichert, mit Zutrittskontrolle, familiengeführt.",
  sec_h="Zugang", sec="Automatisierte Zutrittskontrolle auf dem Gelände.",
  iva="Preise inklusive MwSt.", pfoot="Alle Preise in Euro, inklusive MwSt., gültig für die angegebene Saison. Bei Änderungen schicken wir Ihnen laut Vertrag die aktualisierte Preistabelle.",
  prsub="Jahrespreis für das Winterparken. Inklusive MwSt.",
  trn=dict(h="Fahrzeugtransport", p="Wir können den Transport Ihres Fahrzeugs zum und vom Lager organisieren. Sagen Sie uns, wohin und wann, und wir antworten mit den Konditionen.", c="Transport anfragen"),
  ti="Wir können den Transport Ihres Fahrzeugs zum und vom Lager organisieren. Sagen Sie uns, wohin und wann, und wir antworten mit den Konditionen.",
  camper="Leider nehmen wir keine Wohnmobile auf. Wir stellen Wohnwagen, Boote und Jetskis ein.",
  f_included="Enthalten sind die Versicherung, **1 Standardwäsche** und **2 Ausfahrten pro Saison**. Der Platz ist immer überdacht und das Gelände hat eine automatisierte Zutrittskontrolle.",
  f_sec=("Wie ist das Lager geschützt?", "Das Gelände hat eine automatisierte Zutrittskontrolle."),
  f_extras="In bestimmten Fällen: **100 €**, wenn die Restzahlung nach dem 30. September eingeht, **50 €**, wenn Sie die Abholung mit weniger als einer Woche Vorlauf melden, **50 €** für jede Ausfahrt über die 2 inklusiven hinaus. Ein Transport wird, wenn Sie ihn wünschen, gesondert vereinbart.",
  f_tr=("Organisieren Sie auch den Transport?",),
  f_loc="Wir haben zwei Standorte: **Camporengo**, Via Galileo Galilei, Cavaion Veronese (VR), und **Casalmenini**, Località Casalmenini 4, Rivoli Veronese (VR). Wir sagen Ihnen, an welchem Standort Ihr Fahrzeug steht.",
  fannual="function(T,len,p,dx){return '<b>'+B.m(p)+'</b> (inkl. MwSt.) Jahrespreis für '+(T==='Boot'?'ein ':'einen ')+T+(len?' mit '+B.n(len)+' m':'')+'. Enthalten sind Versicherung, 1 Wäsche und 2 Ausfahrten.'+dx}",
  chipTr="Organisieren Sie den Transport?", chipOther="Transport anfragen",
  priv=["**Verantwortlicher.** Garda Center S.r.l., USt-IdNr. IT03578820239, Sitz in Via Galileo Galilei, Cavaion Veronese (VR), Italien. E-Mail: " + EMAIL + ".",
   "**Welche Daten wir erfassen.** Wenn Sie das Kontaktformular nutzen: Name, E-Mail, Telefon (optional), Art und Länge Ihres Fahrzeugs, Ihre Nachricht und die Sprache der Seite. Um automatische Absendungen zu begrenzen, speichern wir außerdem einen anonymen Code, der aus Ihrer IP-Adresse abgeleitet wird (nicht die Adresse selbst). Fragen, die Sie dem Assistenten schreiben, bleiben in Ihrem Browser: Wir erhalten oder speichern sie nicht.",
   "**Wozu und auf welcher Grundlage.** Um Ihre Anfrage zu beantworten und Ihnen auf Wunsch einen Platz anzubieten (Art. 6 Abs. 1 lit. b DSGVO, vorvertragliche Maßnahmen auf Ihre Anfrage). Der Spam-Schutzcode sichert das Formular (Art. 6 Abs. 1 lit. f, berechtigtes Interesse). Die Angabe ist freiwillig, aber ohne Name, E-Mail und Nachricht können wir nicht antworten.",
   "**Wie lange.** Anfragen, aus denen kein Vertrag wird, löschen wir nach 12 Monaten. Wenn Sie Kunde werden, folgen die Daten dem Vertrag und den gesetzlichen Pflichten (z. B. steuerlich, 10 Jahre); für Kunden gilt die dem Vertrag beigefügte Erklärung.",
   "**Wer sie erhält.** Nur technische Dienstleister, die sie in unserem Auftrag verarbeiten: Supabase (Datenbank, die sich in Italien befindet, und Funktionen der Seite), Resend (E-Mail-Versand) und GitHub (hostet die Seiten und kann IP-Adressen der Besucher aus Sicherheitsgründen protokollieren). Einige haben ihren Sitz oder Server außerhalb der Europäischen Union (USA): Die Übermittlung stützt sich auf die von der DSGVO vorgesehenen Garantien (Standardvertragsklauseln oder Data Privacy Framework). Wir verkaufen oder geben Daten nicht zu Werbezwecken an Dritte weiter.",
   "**Cookies und Karten.** Diese Website verwendet keine Profiling-Cookies und keine Statistik-Tools. Google Maps wird nur geladen, wenn Sie die Schaltfläche drücken: Dann erhält Google Ihre IP-Adresse und kann eigene Cookies nutzen, gemäß seiner eigenen Erklärung.",
   "**Ihre Rechte.** Sie können Auskunft, Berichtigung, Löschung, Einschränkung oder Übertragbarkeit Ihrer Daten verlangen und der Verarbeitung widersprechen, indem Sie an " + EMAIL + " schreiben. Wenn Sie meinen, dass Ihre Daten nicht korrekt verarbeitet werden, können Sie sich bei der italienischen Datenschutzbehörde beschweren (Garante per la protezione dei dati personali, garanteprivacy.it).",
   "Letzte Aktualisierung: Oktober 2026."]),
}
TR_FAQ = {
 "it": "transport", "en": "transport", "de": "transport"}
TR_ANS = {L: TXT[L]["ti"] for L in TXT}

ALL = {"it": "Tutte le tariffe e le quote stagionali", "en": "All prices and seasonal fees", "de": "Alle Preise und Saisonpreise"}
def patch(L):
    c = C[L]; t = TXT[L]; c["pr"]["all"] = ALL[L]
    c["hero"]["lede"] = t["lede"]; c["desc"]["index"] = t["d_index"]
    c["inc"]["items"] = c["inc"]["items"][:3]; c["inc"]["sec_h"] = t["sec_h"]; c["inc"]["sec"] = t["sec"]
    c["P"]["sub"] = c["P"]["sub"] + " " + t["iva"]; c["P"]["foot"] = t["pfoot"]; c["pr"]["sub"] = t["prsub"]
    c["P"]["trn"] = t["trn"]; c["P"].pop("tr", None)
    c["B"]["transportInfo"] = t["ti"]; c["B"]["camper"] = t["camper"]
    c["B"]["f"] = {"annual": t["fannual"], "dxAnnual": c["B"]["f"]["dxAnnual"], "season": c["B"]["f"]["season"]}
    c["B"]["chips"][1] = (c["B"]["chips"][1][0], t["chipTr"]); c["B"]["chipOtherRoute"] = t["chipOther"]
    faq_set(L, "included", a=t["f_included"]); faq_set(L, "security", q=t["f_sec"][0], a=t["f_sec"][1])
    faq_set(L, "extras", a=t["f_extras"]); faq_set(L, "location", a=t["f_loc"])
    faq_after(L, "extras", ("transport", t["f_tr"][0], t["ti"]))
    c["PV"]["body"] = t["priv"]; c["B"].pop("transportIntro", None)
    c["B"]["next"]["included"] = [x for x in c["B"]["next"]["included"]]
    c["B"]["next"]["extras"] = c["B"]["next"].get("extras", [])
    # rimuove il controllo luci/freni dal calcolatore (stringa in 'calc' non lo cita)
    c["P"]["calc"].pop("r_tr", None); c["P"]["calc"].pop("tr_none", None)
for L in ("it", "en", "de"): patch(L)

# ============================================================ NEDERLANDS
nl = copy.deepcopy(C["en"])
def S(d, **kw):
    d.update(kw); return d
nl["loc"] = "nl_NL"; nl["name"] = "Nederlands"; nl["nums"] = ("nl-NL", ".")
nl["months"] = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
nl["nav"] = dict(prices="Prijzen", how="Vragen", where="Locatie", contact="Contact", login="Klantenzone", menu="Menu", lang="Taal", skip="Naar de inhoud")
nl["brand_sub"] = "Overdekte stalling aan het Gardameer"
nl["title"] = dict(index="Garda Center · Overdekte stalling voor caravans en boten aan het Gardameer", prices="Prijzen 2026 · Garda Center", faq="Veelgestelde vragen · Garda Center", location="Locatie · Garda Center", contact="Contact · Garda Center", privacy="Privacy · Garda Center")
nl["desc"] = dict(
  index="Overdekte winterstalling voor caravans, boten en waterscooters in Cavaion Veronese en Rivoli Veronese aan het Gardameer. Verzekerd, met toegangscontrole, door een familie gerund.",
  prices="Jaar- en seizoensprijzen voor de overdekte stalling van caravans, boten en waterscooters bij Garda Center.",
  faq="Verzekering, openingsdata, ophalen, betaling en documenten: antwoorden op de meest gestelde vragen over Garda Center.",
  location="De twee locaties van Garda Center: Camporengo in Cavaion Veronese en Casalmenini in Rivoli Veronese.",
  contact="Schrijf Garda Center: vraag naar een plek of naar informatie over de overdekte stalling van caravans en boten.",
  privacy="Privacyverklaring van de website van Garda Center.")
nl["hero"] = dict(h1="Caravans en boten onder dak, aan het Gardameer.", lede="Winterstalling in gesloten hallen in Cavaion Veronese en Rivoli Veronese. Verzekerd, met gecontroleerde toegang, door een familie gerund.", c1="Plek aanvragen", c2="Bekijk de prijzen", art="Tekening van een hal met een caravan en een boot")
nl["year"] = dict(h="Wanneer u uw voertuig kunt ophalen",
  sub="Van 1 april tot 1 oktober is de stalling open: u haalt uw voertuig op en brengt het terug wanneer u wilt, met een week van tevoren melden. De rest van het jaar staat het overdekt.",
  o="1 april tot 1 oktober: open. U kunt uw voertuig ophalen en terugbrengen.", c="1 oktober tot 1 april: gesloten. Uw voertuig blijft binnen en kan niet worden opgehaald.",
  now="vandaag", s_open="De stalling is vandaag open. Meld het ons minstens een week van tevoren als u uw voertuig wilt ophalen.", s_closed="De stalling is vandaag gesloten: de voertuigen staan overdekt. Op 1 april gaat zij weer open.", aria="Jaarkalender: de stalling is open van april tot en met september")
nl["indoor"] = dict(h="Alleen overdekte plaatsen", p="Wij hebben geen plaatsen buiten: elk voertuig staat in een gesloten hal, droog en beschermd tegen zon, hagel en vocht. Wij zijn een van de grootste overdekte stallingen voor caravans en boten aan het Gardameer.")
nl["inc"] = dict(h="Inbegrepen in de jaarprijs",
  items=[("Verzekering", "Diefstal, brand, blikseminslag en ontploffing, vandalisme, weersomstandigheden en schade door manoeuvreren op het stallingsterrein."),
         ("1 standaardwasbeurt", "Die doen wij bij het eerste ophalen van elk seizoen."),
         ("2 ritten per seizoen", "U haalt uw voertuig op en brengt het terug tussen april en september. Vanaf de derde rit betaalt u 50 € per keer.")],
  sec_h="Toegang", sec="Geautomatiseerde toegangscontrole op het terrein.")
nl["pr"] = dict(h="Wat het kost", sub="Jaarprijs voor de winterstalling. Inclusief btw.", from_="vanaf",
  rows=[("Caravan", "600 €", "Tot 6 m. Boven 8 m: 1.000 €."), ("Boot", "800 €", "Tot 6 m. Boven 9 m: 1.400 €."), ("Waterscooter op trailer", "350 €", "Vaste prijs.")], all="Alle prijzen en seizoenstarieven")
nl["steps"] = dict(h="Zo wordt u klant", items=[
  ("Schrijf ons", "Vertel welk voertuig u heeft en hoe lang het is. Wij antwoorden met prijs en beschikbaarheid."),
  ("Contract en documenten", "Wij hebben een geldig identiteitsbewijs, het kentekenbewijs van het voertuig en uw ondertekende contract nodig."),
  ("Aanbetaling", "Met de aanbetaling (meestal 50 €) is de plek van u."),
  ("Breng uw voertuig voor de winter", "Restbetaling uiterlijk 30 september, daarna brengt u het voertuig uiterlijk 1 oktober terug."),
  ("Haal het in het voorjaar op", "Meld het ons vanaf 1 april een week van tevoren: u vindt het klaar buiten de hal, vanaf 8:30 uur.")])
nl["sedi"] = dict(h="Twee locaties tussen Cavaion en Rivoli Veronese", p="Wij zeggen u op welke locatie uw voertuig staat.", go="Routebeschrijving")
nl["altre"] = dict(h="Ook deze zijn van de familie", p="Andere bedrijven in de buurt:")
nl["cta"] = dict(h="Heeft u een vraag? Vraag het de assistent of schrijf ons.", c1="Schrijf ons", c2="Klantenzone")
nl["foot"] = dict(c="Contact", s="Locaties", l="Beveiligd gedeelte", gest="Toegang beheer", privacy="Privacy", rights="Garda Center S.r.l. · btw-nr. IT03578820239", social="Volg ons")
nl["P"] = dict(h1="Prijzen 2026", sub="Prijzen per stallingseizoen. Alle plaatsen zijn overdekt. Prijzen inclusief btw.",
  calc=dict(h="Bereken uw prijs", t="Welk voertuig heeft u?", types=[("roulotte", "Caravan"), ("barca", "Boot"), ("carrello", "Waterscooter op trailer")], l="Lengte (m)", dx="Dubbele as (twee assen)", go="Berekenen", r_ann="Jaarprijs (incl. btw)", need="Vul de lengte in meters in (tussen 2 en 20)."),
  ann=dict(cap="Jaarprijs · winterstalling", col=["Voertuig en lengte", "Prijs"],
    rows=[("Caravan tot 6 m", "600 €"), ("Caravan van 6 tot 7 m", "700 €"), ("Caravan van 7 tot 8 m", "800 €"), ("Caravan boven 8 m", "1.000 €"), ("Caravan met dubbele as", "+ 100 €"),
          ("Boot tot 6 m", "800 €"), ("Boot van 6 tot 8 m", "900 €"), ("Boot van 8 tot 9 m", "1.200 €"), ("Boot boven 9 m", "1.400 €"), ("Waterscooter op trailer", "350 €")]),
  sea=dict(cap="Seizoensprijs · maart tot oktober, maximaal 3 maanden", col=["Voertuig", "Tot 2 weken", "Tot 1 maand", "Tot 3 maanden"],
    rows=[("Caravan, waterscooter op trailer", "100 €", "200 €", "300 €"), ("Boot", "200 €", "300 €", "450 €")], note="Langer dan 3 maanden geldt de jaarprijs."),
  inc=dict(h="Wat is inbegrepen"),
  ex=dict(cap="Extra kosten", rows=[("Restbetaling na 30 september", "100 €"), ("Ophalen met minder dan een week van tevoren melden", "50 €"), ("Extra rit (vanaf de derde in een seizoen)", "50 €"), ("Gasfles in het voertuig aangetroffen, per fles", "200 €")]),
  trn=dict(h="Vervoer van het voertuig", p="Wij kunnen het vervoer van uw voertuig van en naar de stalling organiseren. Laat weten waarheen en wanneer, dan antwoorden wij met de voorwaarden.", c="Vervoer aanvragen"),
  foot="Prijzen zijn in euro, inclusief btw, en gelden voor het genoemde seizoen. Bij wijzigingen sturen wij u volgens het contract de bijgewerkte prijslijst.")
nl["W"] = dict(h1="Locatie", sub="Wij hebben twee locaties. Schrijf of bel ons voordat u komt: wij ontvangen op afspraak.", maps="Openen in Google Maps", load="Kaart tonen",
  priv="De kaart komt van Google: bij het laden ontvangt Google uw IP-adres.", note="Ophalen en terugbrengen gebeurt op de afgesproken afspraak: lees in de veelgestelde vragen hoe het werkt.")
nl["K"] = dict(h1="Contact", sub="Schrijf ons: wij antwoorden zo snel mogelijk. Als u de assistent iets heeft gevraagd, staat uw vraag al in het bericht.",
  m="Waarmee kunnen wij helpen?", mopts=[("info", "Informatie"), ("posto", "Een plek aanvragen"), ("ritiro", "Voertuig ophalen of terugbrengen"), ("altro", "Iets anders")],
  n="Voor- en achternaam", e="E-mail", t="Telefoon (optioneel)", ty="Welk voertuig heeft u?", tyopts=[("", "Kies"), ("roulotte", "Caravan"), ("barca", "Boot"), ("carrello", "Waterscooter op trailer"), ("altro", "Anders")],
  len="Lengte (m)", dx="Dubbele as", msg="Uw bericht", priv="Ik heb de <a href=\"privacy.html\">privacyverklaring</a> gelezen en ga ermee akkoord dat Garda Center mijn gegevens gebruikt om mij te antwoorden.",
  send="Bericht versturen", sending="Bezig met versturen…", ok="Bericht verzonden. Wij antwoorden zo snel mogelijk, meestal binnen één werkdag.",
  err="Het bericht is niet verzonden. Controleer uw verbinding en probeer het opnieuw, of schrijf naar " + EMAIL + ".", bad="Controleer de gemarkeerde velden: wij hebben uw naam, een geldig e-mailadres, een bericht en uw toestemming nodig.",
  direct="Liever bellen?", hint="Wij antwoorden op het e-mailadres dat u invult.")
nl["PV"] = dict(h1="Privacyverklaring", body=[
  "**Wie uw gegevens verwerkt.** Garda Center S.r.l., btw-nr. IT03578820239, statutaire zetel in Via Galileo Galilei, Cavaion Veronese (VR), Italië. E-mail: " + EMAIL + ".",
  "**Welke gegevens wij verzamelen.** Als u het contactformulier gebruikt: naam, e-mail, telefoon (optioneel), soort en lengte van uw voertuig, uw bericht en de taal van de site. Om geautomatiseerde verzendingen te beperken bewaren wij ook een anonieme code die is afgeleid van uw IP-adres (niet het adres zelf). Vragen die u aan de assistent schrijft blijven in uw browser: wij ontvangen of bewaren ze niet.",
  "**Waarom en op welke grondslag.** Om uw verzoek te beantwoorden en u, indien gewenst, een plek aan te bieden (art. 6 lid 1 sub b AVG, maatregelen vóór een overeenkomst op uw verzoek). De anti-spamcode beschermt het formulier (art. 6 lid 1 sub f, gerechtvaardigd belang). Het verstrekken van gegevens is vrijwillig, maar zonder naam, e-mail en bericht kunnen wij niet antwoorden.",
  "**Hoe lang.** Verzoeken die geen overeenkomst worden, verwijderen wij na 12 maanden. Als u klant wordt, volgen de gegevens het contract en de wettelijke verplichtingen (bijvoorbeeld fiscaal, 10 jaar); voor klanten geldt de verklaring die bij het contract is gevoegd.",
  "**Wie ze ontvangt.** Alleen technische dienstverleners die ze in onze opdracht verwerken: Supabase (database, die zich in Italië bevindt, en functies van de site), Resend (verzenden van e-mail) en GitHub (host de pagina's en kan IP-adressen van bezoekers om veiligheidsredenen registreren). Sommige hebben hun zetel of servers buiten de Europese Unie (Verenigde Staten): de doorgifte berust op de waarborgen van de AVG (standaardcontractbepalingen of het Data Privacy Framework). Wij verkopen of verstrekken geen gegevens aan derden voor commerciële doeleinden.",
  "**Cookies en kaarten.** Deze site gebruikt geen profileringscookies en geen statistiekprogramma's. Google Maps wordt alleen geladen als u op de knop drukt: dan ontvangt Google uw IP-adres en kan het eigen cookies gebruiken, volgens zijn eigen verklaring.",
  "**Uw rechten.** U kunt vragen om inzage, correctie, verwijdering, beperking of overdraagbaarheid van uw gegevens en bezwaar maken tegen de verwerking door te schrijven naar " + EMAIL + ". Als u denkt dat uw gegevens niet correct worden verwerkt, kunt u een klacht indienen bij de Italiaanse toezichthouder (Garante per la protezione dei dati personali, garanteprivacy.it).",
  "Laatst bijgewerkt: oktober 2026."])
nl["B"] = dict(
  ui=dict(fab="Vraag het de assistent", title="Garda Center-assistent", sub="Beantwoordt veelgestelde vragen direct", ph="Typ uw vraag", send="Versturen", close="Sluiten", note="Automatische assistent: als hij het niet weet, schrijf dan ons team.", form="Schrijf het team", call="Bel", formpage="contact.html"),
  hello="Hallo! Ik ben de assistent van Garda Center. Ik vertel u graag over prijzen, vervoer, verzekering en openingsdata. Waarmee kan ik helpen?",
  thanks="Graag gedaan! Als u nog iets nodig heeft, schrijf gerust.", empty="Typ hieronder uw vraag.",
  fallback="Daar ben ik niet zeker van. Schrijf ons via het formulier: uw vraag staat al in het bericht en wij antwoorden.",
  noTariff="Voor dit soort voertuig heb ik geen vaste prijs. Stuur ons model en afmetingen via het formulier, dan antwoorden wij met een prijs.",
  ask=dict(type="Welk voertuig heeft u?", len="Hoe lang is het? Geef de lengte in meters (bijvoorbeeld 6,5).", dur="Hoe lang heeft u de plek nodig?"),
  types=dict(roulotte="Caravan", barca="Boot", carrello="Waterscooter op trailer"), typeLc=dict(roulotte="caravan", barca="boot", carrello="waterscooter op trailer"),
  dur=dict(s2="Tot 2 weken", s1="Tot 1 maand", s3="Tot 3 maanden"),
  seasonLong="De seizoensprijs geldt tot 3 maanden, van maart tot oktober. Voor langere periodes geldt de jaarprijs.",
  chipAnnual="Jaarprijs", chipTransport="Vervoer", chipOtherRoute="Vervoer aanvragen", chipIncluded="Wat is inbegrepen", chipBook="Hoe boek ik",
  transportInfo="Wij kunnen het vervoer van uw voertuig van en naar de stalling organiseren. Laat weten waarheen en wanneer, dan antwoorden wij met de voorwaarden.",
  camper="Helaas: wij stallen geen campers. Wij nemen caravans, boten en waterscooters.",
  chips=[("Prijzen", "Wat kost het?"), ("Vervoer", "Organiseren jullie vervoer?"), ("Verzekering", "Is mijn voertuig verzekerd?"), ("Openingsdata", "Wanneer zijn jullie open?")],
  size="De maximale afmetingen hangen af van de beschikbare plek. Stuur ons model en afmetingen van uw voertuig via het formulier, dan antwoorden wij.",
  next={
   "insurance": [("Wat is inbegrepen", "Wat is inbegrepen?"), ("Prijzen", "Wat kost het?")], "hours": [("Ophalen", "Hoe haal ik mijn voertuig op?"), ("Prijzen", "Wat kost het?")],
   "pickup": [("Terugbrengen", "Hoe breng ik het terug?"), ("Extra kosten", "Zijn er extra kosten?")], "return": [("Openingsdata", "Wanneer zijn jullie open?")],
   "payment": [("Documenten", "Welke documenten heb ik nodig?"), ("Klantenzone", "Hoe kom ik in de klantenzone?")], "booking": [("Prijzen", "Wat kost het?"), ("Documenten", "Welke documenten heb ik nodig?"), ("Plek aanvragen", "#form")],
   "documents": [("Hoe boek ik", "Hoe boek ik een plek?")], "included": [("Prijzen", "Wat kost het?"), ("Verzekering", "Is mijn voertuig verzekerd?")],
   "security": [("Verzekering", "Is mijn voertuig verzekerd?")], "gas": [("Extra kosten", "Zijn er extra kosten?")], "extras": [("Prijzen", "Wat kost het?")],
   "location": [("Locatie", "#where")], "contact": [("Schrijf ons", "#form")], "indoor": [("Prijzen", "Wat kost het?")], "login": [("Klantenzone", "#login")],
   "washing": [("Wat is inbegrepen", "Wat is inbegrepen?")], "about": [("Prijzen", "Wat kost het?"), ("Waar zijn jullie", "Waar zijn jullie?")]},
  f=dict(
   annual="function(T,len,p,dx){return '<b>'+B.m(p)+'</b> (incl. btw) voor de jaarprijs van een '+T.toLowerCase()+(len?' van '+B.n(len)+' m':'')+'. Inbegrepen: verzekering, 1 wasbeurt en 2 ritten.'+dx}",
   dxAnnual="function(p){return '\\nMet een dubbele as (twee assen) is het '+B.m(p)+'.'}",
   season="function(T,d,p){return 'Seizoensprijs voor een '+T.toLowerCase()+' ('+d.toLowerCase()+', maart tot oktober): <b>'+B.m(p)+'</b>.'}"))
nl["FAQ"] = [
 ("indoor", "Staat het voertuig buiten of overdekt?", "Al onze plaatsen zijn **overdekt**, in gesloten hallen. Plaatsen buiten bieden wij niet aan."),
 ("insurance", "Is mijn voertuig verzekerd?", "Ja. Tijdens de stalling is uw voertuig verzekerd tegen diefstal, brand, blikseminslag en ontploffing, vandalisme, weersomstandigheden en schade door manoeuvreren op het stallingsterrein.\n\nDe vergoeding is beperkt tot **25.000 € per voertuig** (behalve bij opzet of grove schuld) en gaat niet boven de marktwaarde van het voertuig op het moment van de schade. Niet gedekt: schade door gasflessen of brandbare stoffen die in het voertuig zijn achtergelaten, schade op de dag van ophalen of terugbrengen en slijtage (banden, neuswiel, kunststof). De details staan in het contract."),
 ("hours", "Wanneer is de stalling open?", "De stalling is **van 1 april tot 1 oktober** open: in die periode kunt u uw voertuig ophalen en terugbrengen. **Van 1 oktober tot 1 april is zij gesloten**: dan kan het voertuig niet worden opgehaald en is het stallingsterrein niet toegankelijk.\n\nWij ontvangen op afspraak."),
 ("pickup", "Hoe haal ik mijn voertuig op?", "Meld het ons minstens **een week van tevoren** (per e-mail of in de klantenzone) met de gewenste dag. Wij bevestigen en maken het voertuig klaar.\n\nOp de dag zelf vindt u het buiten de hal, op een open en makkelijk bereikbaar terrein, en kunt u het zelf meenemen **vanaf 8:30 uur**. Haalt u het niet voor 17:00 uur op, dan blijft het buiten staan en valt het niet meer onder onze verantwoordelijkheid. Heeft u het voor 8:30 uur nodig, dan maken wij het de dag ervoor klaar.\n\nMeldt u zich met minder dan een week van tevoren, dan kunnen wij niet garanderen dat het klaar staat; lukt het toch, dan geldt een toeslag van 50 €. Twee ritten per seizoen zijn inbegrepen."),
 ("return", "Hoe breng ik het terug?", "Schrijf ons op welke dag u het terugbrengt en zet het in de buitenruimtes: de dissel niet met hangsloten of kettingen vastzetten, geen brandbare stoffen in het voertuig laten, zo parkeren dat andere voertuigen niet worden gehinderd en foto's maken.\n\nWij zetten het dezelfde dag voor 17:00 uur binnen. Komt het na 16:30 uur aan, dan blijft het tot de volgende dag buiten staan en valt het in de tussentijd niet onder onze verantwoordelijkheid. Denk eraan: na 1 oktober is de stalling gesloten."),
 ("payment", "Hoe en wanneer betaal ik?", "Met een **aanbetaling** (meestal 50 €) bevestigt u uw plek. De **restbetaling** is verschuldigd uiterlijk **30 september**, voordat u het voertuig voor de winter terugbrengt; daarna komt er 100 € bij.\n\nU kunt betalen per bankoverschrijving, op kantoor op afspraak of, in de klantenzone, met kaart of iDEAL. Pas na volledige betaling kunt u het voertuig het jaar daarop ophalen."),
 ("booking", "Hoe boek ik een plek?", "Schrijf ons via het contactformulier welk voertuig u heeft en hoe lang het is: wij antwoorden met prijs en beschikbaarheid. Als diensten en prijzen u bevallen, wordt u klant met een identiteitsbewijs, het kentekenbewijs en uw ondertekende contract.\n\nElk jaar in april schrijven wij u om de plek te boeken: de aanbetaling moet binnen de in de e-mail genoemde termijn binnen zijn, anders vervalt de plek."),
 ("documents", "Welke documenten heb ik nodig?", "U heeft een geldig identiteitsbewijs (paspoort, rijbewijs of identiteitskaart), het kentekenbewijs van het voertuig en uw ondertekende contract nodig, met kennisname van de privacyverklaring. Bestaande klanten kunnen documenten uploaden in de klantenzone."),
 ("included", "Wat is inbegrepen in de jaarprijs?", "Inbegrepen zijn de verzekering, **1 standaardwasbeurt** en **2 ritten per seizoen**. De plek is altijd overdekt en het terrein heeft een geautomatiseerde toegangscontrole."),
 ("washing", "Is wassen inbegrepen?", "Ja, in de jaarprijs zit 1 standaardwasbeurt van het voertuig, die wij doen bij het eerste ophalen van het seizoen."),
 ("security", "Hoe is de stalling beschermd?", "Het terrein heeft een geautomatiseerde toegangscontrole."),
 ("gas", "Mag ik gasflessen in het voertuig laten?", "Nee. Brandbare of explosieve stoffen zoals gasflessen mogen niet in het voertuig blijven: als wij er vinden, geldt een boete van **200 € per fles**. Wij bieden geen opslag van gasflessen meer aan."),
 ("extras", "Zijn er extra kosten?", "In sommige gevallen: **100 €** als de restbetaling na 30 september binnenkomt, **50 €** als u het ophalen met minder dan een week van tevoren meldt, **50 €** voor elke rit boven de 2 inbegrepen ritten. Vervoer wordt, als u het wilt, apart afgesproken."),
 ("transport", "Organiseren jullie ook het vervoer?", "Ja, wij kunnen het vervoer van uw voertuig van en naar de stalling organiseren. Laat weten waarheen en wanneer, dan antwoorden wij met de voorwaarden."),
 ("location", "Waar zijn jullie?", "Wij hebben twee locaties: **Camporengo**, Via Galileo Galilei, Cavaion Veronese (VR), en **Casalmenini**, Località Casalmenini 4, Rivoli Veronese (VR). Wij zeggen u op welke locatie uw voertuig staat."),
 ("contact", "Hoe bereik ik jullie?", "Schrijf via het contactformulier of bel **" + PHONE1 + "** of **" + PHONE2 + "**. E-mail: " + EMAIL + "."),
 ("login", "Hoe kom ik in de klantenzone?", "Druk op «Klantenzone» en vul het e-mailadres in waarmee u bent geregistreerd: wij sturen u een code van 6 cijfers. Daar ziet u uw rekening en bonnen, boekt u de rit, uploadt u documenten en betaalt u online. Dit werkt alleen voor klanten die al geregistreerd zijn."),
 ("about", "Wie zijn jullie?", "Garda Center is een familiebedrijf: overdekte stalling voor caravans, boten en waterscooters in Cavaion Veronese en Rivoli Veronese, aan het Gardameer."),
]
C["nl"] = nl
LANGS = ("it", "en", "de", "nl")


# ---------------- lunghezza = con il timone (ovunque compaia la domanda sulla lunghezza)
LENW = {"it": "con il timone", "en": "including the drawbar", "de": "einschließlich der Deichsel", "nl": "inclusief dissel"}
def lenpatch():
    it, en, de, nl = C["it"], C["en"], C["de"], C["nl"]
    for L, c in C.items():
        w = LENW[L]
        K = c["K"]; K["len"] = K["len"].replace("(m)", "(m, " + w + ")")
        cc = c["P"]["calc"]; cc["l"] = cc["l"].replace("(m)", "(m, " + w + ")")
    it["P"]["sub"] += " Le lunghezze si intendono con il timone."; en["P"]["sub"] += " Lengths include the drawbar."
    de["P"]["sub"] += " Die Längenangaben verstehen sich einschließlich der Deichsel."; nl["P"]["sub"] += " Lengtes zijn inclusief dissel."
    it["pr"]["sub"] += " Lunghezze con il timone."; en["pr"]["sub"] += " Lengths include the drawbar."; de["pr"]["sub"] += " Längen einschließlich Deichsel."; nl["pr"]["sub"] += " Lengtes inclusief dissel."
    it["B"]["ask"]["len"] = "Quanto è lungo, con il timone? Scrivi la misura in metri (per esempio 6,5)."
    en["B"]["ask"]["len"] = "How long is it, including the drawbar? Give the length in metres (for example 6.5)."
    de["B"]["ask"]["len"] = "Wie lang ist es, einschließlich der Deichsel? Geben Sie die Länge in Metern an (zum Beispiel 6,5)."
    nl["B"]["ask"]["len"] = "Hoe lang is het, inclusief dissel? Geef de lengte in meters (bijvoorbeeld 6,5)."
    it["B"]["f"]["annual"] = it["B"]["f"]["annual"].replace("' m'", "' m (con il timone)'")
    en["B"]["f"]["annual"] = en["B"]["f"]["annual"].replace("' m'", "' m (including the drawbar)'")
    de["B"]["f"]["annual"] = de["B"]["f"]["annual"].replace("' m'", "' m (einschließlich Deichsel)'")
    nl["B"]["f"]["annual"] = nl["B"]["f"]["annual"].replace("' m'", "' m (inclusief dissel)'")
    it["steps"]["items"][0] = ("Scrivici", "Dicci che mezzo hai e quanto è lungo, con il timone. Ti rispondiamo con prezzo e disponibilità.")
    en["steps"]["items"][0] = ("Write to us", "Tell us what vehicle you have and how long it is, including the drawbar. We reply with price and availability.")
    de["steps"]["items"][0] = ("Schreiben Sie uns", "Sagen Sie uns, welches Fahrzeug Sie haben und wie lang es ist, einschließlich der Deichsel. Wir antworten mit Preis und Verfügbarkeit.")
    nl["steps"]["items"][0] = ("Schrijf ons", "Vertel welk voertuig u heeft en hoe lang het is, inclusief dissel. Wij antwoorden met prijs en beschikbaarheid.")
    for L, a in (("it", "e quanto è lungo"), ("en", "and how long it is"), ("de", "und wie lang es ist"), ("nl", "en hoe lang het is")):
        lst = C[L]["FAQ"]
        for i, (k, q, an) in enumerate(lst):
            if k == "booking":
                assert a in an, (L, a)
                lst[i] = (k, q, an.replace(a, a + ", " + LENW[L], 1))
    for L in C:
        for k in ("size", "noTariff"):
            pass
    it["B"]["size"] = it["B"]["size"].replace("misure del tuo mezzo", "misure del tuo mezzo (lunghezza con il timone)")
    en["B"]["size"] = en["B"]["size"].replace("measurements of your vehicle", "measurements of your vehicle (length including the drawbar)")
    de["B"]["size"] = de["B"]["size"].replace("Maße Ihres Fahrzeugs", "Maße Ihres Fahrzeugs (Länge einschließlich Deichsel)")
    nl["B"]["size"] = nl["B"]["size"].replace("afmetingen van uw voertuig", "afmetingen van uw voertuig (lengte inclusief dissel)")
lenpatch()

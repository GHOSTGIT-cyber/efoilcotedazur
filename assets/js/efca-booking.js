/* =============================================================================
   efca-booking.js — Réservation SANS paiement -> notifications WhatsApp + e-mail
   -----------------------------------------------------------------------------
   100 % navigateur, aucun serveur requis :
     - WhatsApp : CallMeBot (envoi vers le numéro du gérant)        -> CFG.booking.whatsapp*
     - E-mail   : FormSubmit (gratuit, sans inscription)            -> CFG.booking.email
     - (option) POST JSON vers un back Coolify pour stockage/dashboard -> CFG.booking.storeEndpoint
   Dégradation gracieuse : si un canal n'est pas configuré, il est ignoré ;
   la confirmation s'affiche quand même (la demande n'est jamais "perdue" si au
   moins un canal est actif).
   ============================================================================= */
(function () {
  "use strict";

  var CFG = (window.EFCA_CONFIG || {});
  var B = CFG.booking || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };

  var form = $("#efca-booking-form");
  if (!form) { return; } // pas sur la page réservation

  var els = {
    error: $("#efca-form-error"),
    submit: $("#efca-submit"),
    stepForm: $("#efca-step-form"),
    stepSuccess: $("#efca-step-success"),
    ref: $("#efca-ref"),
    date: $("#f-date"),
    slot: $("#f-slot")
  };

  /* ----------- créneaux déjà CONFIRMÉS -> grisés dans le select (évite le double-booking)
     Charge une fois au démarrage depuis l'API publique du dashboard (aucune donnée perso
     exposée : ref/date/slot/status seulement). Best-effort : si l'appel échoue, le
     formulaire reste utilisable normalement (aucun blocage, comme avant). ----------- */
  var takenByDate = {}; // { "2026-08-20": Set("08:00","11:00") }
  var slotOptionsHtml = els.slot ? els.slot.innerHTML : "";

  function loadTakenSlots() {
    if (!B.storeEndpoint || !els.date || !els.slot) { return; }
    var apiUrl = B.storeEndpoint.replace(/\/api\/reservations\/?$/, "/api/reservations");
    fetch(apiUrl, { cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var list = (data && data.reservations) || [];
        list.forEach(function (r) {
          if (r.status !== "confirmed" || !r.date || !r.slot) { return; }
          if (!takenByDate[r.date]) { takenByDate[r.date] = {}; }
          takenByDate[r.date][r.slot] = true;
        });
        refreshSlotOptions();
      })
      .catch(function () { /* silencieux : dégrade proprement, formulaire non bloqué */ });
  }

  function refreshSlotOptions() {
    if (!els.date || !els.slot) { return; }
    var taken = takenByDate[els.date.value] || {};
    var current = els.slot.value;
    els.slot.innerHTML = slotOptionsHtml;
    Array.prototype.forEach.call(els.slot.options, function (opt) {
      if (opt.value && taken[opt.value]) {
        opt.disabled = true;
        opt.textContent = opt.value + " — complet";
      }
    });
    // Si le créneau sélectionné vient d'être complété, on le réinitialise.
    if (taken[current]) { els.slot.value = ""; }
  }

  if (els.date) { els.date.addEventListener("change", refreshSlotOptions); }
  loadTakenSlots();

  function showError(msg) { if (els.error) { els.error.textContent = msg; els.error.hidden = false; } }
  function hideError() { if (els.error) { els.error.hidden = true; } }

  /* ----------- référence lisible : EFCA-AAMMJJ-XXXX ----------- */
  function makeRef() {
    var d = new Date();
    var p = function (n) { return ("0" + n).slice(-2); };
    var stamp = String(d.getFullYear()).slice(2) + p(d.getMonth() + 1) + p(d.getDate());
    var rnd = Math.random().toString(36).slice(2, 6).toUpperCase();
    return "EFCA-" + stamp + "-" + rnd;
  }

  /* ----------- collecte + validation ----------- */
  function collect() {
    var fd = new FormData(form);
    return {
      ref: makeRef(),
      name: (fd.get("name") || "").trim(),
      email: (fd.get("email") || "").trim(),
      phone: (fd.get("phone") || "").trim(),
      formule: fd.get("formule") || "",
      date: fd.get("date") || "",
      slot: fd.get("slot") || "",
      participants: Math.max(1, parseInt(fd.get("participants"), 10) || 1),
      level: fd.get("level") || "",
      message: (fd.get("message") || "").trim(),
      cgv: !!fd.get("cgv"),                       // acceptation des CGV (case obligatoire)
      hp: (fd.get("website") || "").trim(),       // honeypot
      createdAt: new Date().toISOString()
    };
  }

  function validate(d) {
    if (d.hp) { return "spam"; } // honeypot rempli -> bot
    if (!d.name) { return "Indiquez votre nom complet."; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) { return "Indiquez un e-mail valide."; }
    if (!d.phone || d.phone.replace(/\D/g, "").length < 8) { return "Indiquez un téléphone valide."; }
    if (!d.date) { return "Choisissez une date."; }
    if (!d.slot) { return "Choisissez un créneau."; }
    // Re-vérifie que le créneau n'est pas devenu complet entre le chargement et le clic
    // (ex. un autre client vient d'être confirmé sur ce créneau pendant que ce visiteur remplissait).
    if (takenByDate[d.date] && takenByDate[d.date][d.slot]) {
      return "Ce créneau vient d'être complété, merci d'en choisir un autre.";
    }
    // Le formulaire est en novalidate : l'attribut `required` de la case ne bloque rien.
    if (!d.cgv) { return "Vous devez accepter les conditions générales de vente."; }
    return null;
  }

  /* ----------- message texte commun (personnalisable via CFG.booking.whatsappTemplate) ----------- */
  function fillTemplate(tpl, d) {
    return tpl.replace(/\{(\w+)\}/g, function (_, k) { return (d[k] != null ? String(d[k]) : ""); });
  }
  function textMessage(d) {
    if (B.whatsappTemplate) { return fillTemplate(B.whatsappTemplate, d); }
    return "Nouvelle réservation eFoil ✅\n"
      + "Réf : " + d.ref + "\n"
      + "Nom : " + d.name + "\n"
      + "Tél : " + d.phone + "\n"
      + "Formule : " + d.formule + "\n"
      + "Date : " + d.date + " à " + d.slot + "\n"
      + "Participants : " + d.participants + " (" + d.level + ")\n"
      + (d.message ? ("Message : " + d.message + "\n") : "")
      + "CGV acceptées : " + (d.cgv ? "oui (" + d.createdAt + ")" : "non") + "\n";
  }

  /* ----------- canal 1 : WhatsApp (CallMeBot, fire-and-forget) ----------- */
  function sendWhatsApp(d) {
    if (!B.whatsappApiKey || !B.whatsappPhone) { return false; }
    var url = "https://api.callmebot.com/whatsapp.php?phone=" + encodeURIComponent(B.whatsappPhone)
      + "&text=" + encodeURIComponent(textMessage(d))
      + "&apikey=" + encodeURIComponent(B.whatsappApiKey);
    // fetch no-cors (même méthode fiable que l'enregistrement) ; fallback <img>.
    try {
      fetch(url, { mode: "no-cors", cache: "no-store" });
    } catch (e) {
      var img = new Image(); img.referrerPolicy = "no-referrer"; img.src = url;
    }
    return true;
  }

  /* ----------- canal 2 : e-mail (FormSubmit AJAX, CORS OK) ----------- */
  function sendEmail(d) {
    if (!B.email) { return Promise.resolve(false); }
    var payload = {
      _subject: "Réservation eFoil — " + d.ref + " — " + d.name,
      "Référence": d.ref,
      "Nom": d.name,
      "Téléphone": d.phone,
      "E-mail": d.email,
      "Formule": d.formule,
      "Date": d.date,
      "Créneau": d.slot,
      "Participants": d.participants,
      "Niveau": d.level,
      "Message": d.message || "—",
      "CGV acceptées": d.cgv ? "Oui — le " + d.createdAt : "Non",
      _template: "table"
    };
    return fetch("https://formsubmit.co/ajax/" + encodeURIComponent(B.email), {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) { return r.ok; }).catch(function () { return false; });
  }

  /* ----------- canal 3 (option) : stockage back Coolify pour le dashboard ----------- */
  function sendStore(d) {
    if (!B.storeEndpoint) { return Promise.resolve(false); }
    // text/plain => requête "simple", pas de préflight CORS. Réponse non lue.
    return fetch(B.storeEndpoint, {
      method: "POST",
      mode: "no-cors",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(d)
    }).then(function () { return true; }).catch(function () { return false; });
  }

  /* ----------- soumission ----------- */
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    hideError();
    var d = collect();
    var err = validate(d);
    if (err === "spam") { return; }            // bot : on ne fait rien
    if (err) { showError(err); return; }

    if (!B.email && !B.whatsappApiKey && !B.storeEndpoint) {
      showError("Aucun canal de réception n'est configuré (voir reservation-backend/README.md).");
      return;
    }

    els.submit.disabled = true;
    els.submit.textContent = "Envoi en cours…";

    var okWhatsApp = sendWhatsApp(d); // synchrone (fire-and-forget)

    Promise.all([sendEmail(d), sendStore(d)]).then(function (res) {
      var okEmail = res[0], okStore = res[1];
      // succès si au moins un canal a fonctionné
      if (okWhatsApp || okEmail || okStore) {
        if (els.ref) { els.ref.textContent = d.ref; }
        els.stepForm.hidden = true;
        els.stepSuccess.hidden = false;
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        els.submit.disabled = false;
        els.submit.textContent = "Envoyer ma demande de réservation";
        showError("L'envoi a échoué. Réessayez ou appelez-nous au 06 35 30 50 67.");
      }
    });
  });
})();

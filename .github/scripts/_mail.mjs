// Warn-Mail via Resend (https://resend.com).
// Braucht das GitHub-Secret RESEND_API_KEY. Empfaenger kommt aus ALERT_TO.
// Ohne eigene verifizierte Domain erlaubt Resend nur den Versand an die
// Adresse des eigenen Resend-Kontos - das Konto also mit der Empfaenger-
// Adresse (michael.pleus@swiss-ski.ch) anlegen.

export async function warnmail(subject, lines) {
  const key = process.env.RESEND_API_KEY;
  // Mehrere Empfaenger moeglich: Adressen in ALERT_TO mit Komma trennen.
  // Achtung: ohne verifizierte Domain stellt Resend nur an die Adresse des
  // eigenen Resend-Kontos zu - weitere Adressen erst nach Domain-Verifizierung.
  const to = (process.env.ALERT_TO || '').split(',').map(s => s.trim()).filter(Boolean);
  const run = process.env.GITHUB_SERVER_URL && process.env.GITHUB_RUN_ID
    ? `${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID}`
    : '';
  const when = new Date().toLocaleString('de-CH', { timeZone: 'Europe/Zurich' });
  if (!key || !to.length) {
    console.error('Keine Mail verschickt: RESEND_API_KEY oder ALERT_TO fehlt.');
    return false;
  }
  const html =
    `<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.55;color:#1d2630">` +
    `<p><b>my.ftem.swiss-ski.ch &ndash; automatische Pr&uuml;fung</b><br>${when} (Schweizer Zeit)</p>` +
    `<ul>` + lines.map(l => `<li>${String(l).replace(/</g, '&lt;')}</li>`).join('') + `</ul>` +
    (run ? `<p>Details: <a href="${run}">Protokoll des Pr&uuml;flaufs auf GitHub</a></p>` : '') +
    `<p style="color:#667">Diese Mail kommt automatisch von der GitHub-&Uuml;berwachung des FTEM-Projekts. ` +
    `Sie wird bei jedem fehlgeschlagenen Lauf erneut verschickt, bis das Problem behoben ist.</p></div>`;
  const r = await fetch(process.env.RESEND_URL || 'https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'FTEM Ueberwachung <onboarding@resend.dev>',
      to,
      subject,
      html,
    }),
  });
  if (!r.ok) {
    console.error('Mailversand fehlgeschlagen:', r.status, await r.text().catch(() => ''));
    return false;
  }
  console.log('Warn-Mail verschickt an', to.join(', '));
  return true;
}

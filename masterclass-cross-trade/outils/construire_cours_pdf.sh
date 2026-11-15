#!/usr/bin/env bash
# Construit le PDF du cours complet (A4) avec les schémas Mermaid rendus.
# Prérequis : pandoc, node + playwright, et le paquet npm "mermaid" (chemin : MERMAID_JS).
# Usage : MERMAID_JS=/chemin/vers/mermaid.min.js outils/construire_cours_pdf.sh
set -euo pipefail
cd "$(dirname "$0")/.."
: "${MERMAID_JS:?Indiquer le chemin de mermaid.min.js (npm install mermaid)}"
SRC=linkedin/sources
TMP=$(mktemp -d)
cp "$MERMAID_JS" "$SRC/mermaid.min.js"
trap 'rm -rf "$TMP" "$SRC/mermaid.min.js" "$SRC/cours.html"' EXIT

# Concaténation des livrables, sans les liens de navigation entre fichiers
for f in A1-cours-modules-1-a-5.md A2-cours-modules-6-a-10.md A3-cours-modules-11-a-18.md C-etudes-de-cas.md \
         D-exercices-corriges.md E-fiche-revision.md F-glossaire.md G-ressources.md; do
  grep -vE '^(➡️|⬅️) |^# LIVRABLE A — COURS COMPLET' "$f"
  printf '\n\n'
done > "$TMP/cours.md"

cat > "$TMP/avant.html" <<'HTML'
<section class="couverture">
  <div class="k">Masterclass · Commerce international · Transit maritime</div>
  <h1>Un conteneur,<br>trois pays,<br><span>une seule opération.</span></h1>
  <div class="barre"></div>
  <p>Masterclass Cross-Trade International : comprendre, organiser, sécuriser et développer les opérations maritimes entre l'Asie, l'océan Indien et le monde.</p>
  <p>Cours complet · 3 études de cas · exercices corrigés · fiche de révision · glossaire FR-EN · ressources</p>
  <div class="bas"><b>Houzaifah Rassolmian</b> · Sales &amp; Freight Forwarding Coordinator, Cross-Trade · La Réunion<br>
  Entreprises, personnes et chiffres fictifs, à visée pédagogique. Règles vérifiées en novembre 2026, à revérifier à chaque opération.
  Travail personnel : opinions personnelles, pas celles de mon employeur.</div>
</section>
HTML

cat > "$TMP/apres.html" <<'HTML'
<script src="mermaid.min.js"></script>
<script>
window.renderMermaid = async () => {
  document.querySelectorAll('pre.diagramme').forEach(pre => {
    const d = document.createElement('div'); d.className = 'mermaid';
    d.textContent = pre.textContent; pre.replaceWith(d);
  });
  mermaid.initialize({startOnLoad:false, theme:'base', fontFamily:'Inter, sans-serif',
    themeVariables:{primaryColor:'#FFFFFF',primaryBorderColor:'#13678A',primaryTextColor:'#0B2545',
      lineColor:'#13678A',secondaryColor:'#FFF1E3',tertiaryColor:'#E8F1F6',fontSize:'15px',
      cScale0:'#0B2545',cScale1:'#13678A',cScale2:'#F28C28',cScale3:'#2E9E6B'}});
  const errs=[]; for (const d of document.querySelectorAll('div.mermaid')) { try { await mermaid.run({nodes:[d]}); } catch(e) { errs.push(String(e.message||e).slice(0,300)); } } window.__mermaidErrors=errs;
};
</script>
HTML

pandoc "$TMP/cours.md" -f gfm -t html5 -s --toc --toc-depth=1 \
  --metadata title="Masterclass Cross-Trade International" --metadata lang=fr \
  --css cours.css -B "$TMP/avant.html" -A "$TMP/apres.html" \
  -V title= -o "$SRC/cours.html"
# pandoc affiche un titre par défaut : on le retire
sed -i 's#<header id="title-block-header">.*##; /<h1 class="title">/d' "$SRC/cours.html"
# évite le rendu automatique de Mermaid au chargement : on rend nous-mêmes les blocs
sed -i 's#<pre class="mermaid">#<pre class="diagramme">#g' "$SRC/cours.html"

node outils/rendre_pdf.js "$SRC/cours.html" linkedin/Masterclass-Cross-Trade-Cours-complet.pdf a4

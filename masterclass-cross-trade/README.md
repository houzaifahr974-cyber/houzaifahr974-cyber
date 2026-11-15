# 🚢 Masterclass Cross-Trade International
### « Un conteneur, trois pays, une seule opération »

Un cours de niveau Master (accessible aux débutants) sur le **Cross-Trade**, le **commerce triangulaire** et la **coordination maritime FCL** entre l'Asie, l'océan Indien et le reste du monde, vu depuis un transitaire installé à La Réunion.

> 🧪 **Toutes les entreprises, personnes, numéros de documents, tarifs et montants sont fictifs et pédagogiques.** Aucune donnée d'entreprise réelle n'est utilisée. Les règles juridiques citées sont sourcées dans le Livrable G (vérification : novembre 2026) et doivent être revérifiées à la date de chaque opération.

## 📦 Contenu

| Livrable | Fichier | Contenu |
|----------|---------|---------|
| **A — Cours complet** | [A1 — Modules 1 à 5 bis](A1-cours-modules-1-a-5.md) · [A2 — Modules 6 à 10](A2-cours-modules-6-a-10.md) · [A3 — Modules 11 à 18](A3-cours-modules-11-a-18.md) | Titre, objectifs, déroulé, scénario d'ouverture, 19 modules (dont 5 bis et les approfondissements : groupage, assurance et avaries, conteneurs spéciaux, paiement, géographie, environnement, fiches pays, éthique), conclusion |
| **B — Présentation** | [Diapositives + notes](B-presentation-diapositives.md) · [Masterclass-Cross-Trade.pptx](Masterclass-Cross-Trade.pptx) | 47 diapositives : titre, message, contenu, visuel, notes, oral, exemple, transition |
| **C — Études de cas** | [3 cas immersifs](C-etudes-de-cas.md) | Cross-Trade Shanghai → Port-Louis · Import Yantian → Port Réunion · Négoce Chine → Madagascar |
| **D — Exercices** | [Exercices corrigés](D-exercices-corriges.md) | 10 questions, 10 QCM, 9 exercices, 3 simulations, 1 étude de cas notée sur 20 |
| **E — Fiche de révision** | [Fiche](E-fiche-revision.md) | Synthèse de 2 pages + fiche complémentaire d'une page |
| **F — Glossaire** | [Glossaire FR-EN](F-glossaire.md) | 40 termes essentiels + 20 complémentaires |
| **G — Ressources** | [Bibliographie](G-ressources.md) | Sources officielles, textes, organismes |

## 🧭 Fil rouge
Les étudiants « travaillent » au service Cross-Trade de **Lagon Bleu Transit** (fictif, Le Port) sur un dossier 1×40'HC Shanghai → Port-Louis, de l'e-mail de demande de cotation à la clôture.

## 🛠️ Régénérer le PowerPoint
Le fichier `.pptx` est produit à partir du Markdown des diapositives (charte bleu marine / bleu océan / orange, emplacements de visuels, notes du présentateur) :

```bash
pip install python-pptx
python3 outils/generer_pptx.py
```

Ensuite, importer le `.pptx` dans PowerPoint ou Canva et remplacer les emplacements « VISUEL RECOMMANDÉ » par des photos et schémas libres de droits.

## ⏱️ Durée
2 h 30 à 3 h (version courte de 2 h proposée dans le cours, A1).

## 💼 Kit LinkedIn (dossier `linkedin/`)
| Fichier | Usage |
|---|---|
| [Textes-LinkedIn.md](linkedin/Textes-LinkedIn.md) | Textes prêts à coller : section Cours, Projets, Sélection, 3 versions du post, premier commentaire, check-list |
| `Carrousel-LinkedIn-Masterclass-Cross-Trade.pdf` | Carrousel de 16 slides (1080×1350) pour un post « Document » |
| `Masterclass-Cross-Trade-Cours-complet.pdf` | Cours complet mis en page (A4, 106 pages, schémas inclus) pour la section Sélection |
| `Visuel-Selection-1200x627.png` | Vignette pour la section Sélection |

Régénération : `node outils/rendre_pdf.js linkedin/sources/carrousel.html linkedin/Carrousel-LinkedIn-Masterclass-Cross-Trade.pdf carrousel` et `MERMAID_JS=…/mermaid.min.js outils/construire_cours_pdf.sh` (nécessitent Playwright, pandoc et le paquet npm `mermaid`).

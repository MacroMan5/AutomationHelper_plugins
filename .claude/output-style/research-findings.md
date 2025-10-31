# Output Style: Research Findings

Format standardisé pour présenter les résultats de recherche documentation Power Automate.

**Utilisé par:** docs-researcher agent

## 📋 Structure Standard

### 1. Résumé de la Question

```markdown
# 📚 Résultats de Recherche

**Question:** [Question de l'utilisateur]
**Type:** [Limitation/Action/Trigger/Error/BestPractice]
**Connecteur:** [Nom du connecteur si applicable]
```

### 2. Réponse Directe

```markdown
## 🎯 Réponse

[Réponse claire et directe à la question en 2-3 phrases]

**Information Clé:**
- [Point important 1]
- [Point important 2]
- [Point important 3]
```

### 3. Source Documentation

```markdown
## 📖 Source

**Documentation Locale:**
- **Fichier:** `Docs/PowerAutomateDocs/[Connector]/[file].md`
- **Section:** [Nom de la section]
- **Ligne:** [Numéro de ligne si pertinent]

**Extrait:**
> [Citation exacte de la documentation]
```

### 4. Contexte et Contraintes

```markdown
## ⚙️ Contexte

### Limitations Associées
- **[Limitation 1]:** [Description impact]
  - Référence: [lim-XXX](../../Docs/PowerAutomateDocs/[Connector]/overview.md#lim-XXX)
- **[Limitation 2]:** [Description impact]

### API Limits
- Rate limit: **X calls per Y seconds**
- Max size: **Z MB**
- Timeout: **A seconds**

### Contraintes
- [Contrainte 1]
- [Contrainte 2]
```

### 5. Exemples Pratiques

```markdown
## 💡 Exemples

### Cas d'Usage 1: [Nom]
\`\`\`json
{
  "example": "code"
}
\`\`\`
**Résultat:** [Ce qui se passe]

### Cas d'Usage 2: [Nom]
\`\`\`json
{
  "example": "code"
}
\`\`\`
**Résultat:** [Ce qui se passe]
```

### 6. Recommandations

```markdown
## ✅ Recommandations

### Best Practices
1. **[Practice 1]:** [Explication]
2. **[Practice 2]:** [Explication]

### À Éviter
- ❌ [Anti-pattern 1]
- ❌ [Anti-pattern 2]

### Alternatives
Si contraintes bloquantes, considérer:
- [Alternative 1]: [Description]
- [Alternative 2]: [Description]
```

### 7. Ressources Additionnelles

```markdown
## 🔗 Pour Aller Plus Loin

**Documentation Locale:**
- [Actions détaillées](../../Docs/PowerAutomateDocs/[Connector]/actions.md)
- [Triggers](../../Docs/PowerAutomateDocs/[Connector]/triggers.md)

**Documentation Officielle:**
- [Microsoft Learn](https://learn.microsoft.com/connectors/[connector])

**Documentation Manquante:**
- [ ] [Information non trouvée localement]
- Suggestion: Recherche web requise
```

## 🎨 Règles de Formatage

### Emojis Standard

- 📚 Titre recherche
- 🎯 Réponse directe
- 📖 Source documentation
- ⚙️ Contexte
- 💡 Exemples
- ✅ Recommandations
- 🔗 Ressources
- ⚠️ Avertissement
- ❓ Information manquante

### Attribution Sources

**TOUJOURS** indiquer la source:

```markdown
**Source:** Docs/PowerAutomateDocs/SharePoint/overview.md (ligne 23)
```

Pour sources web:
```markdown
**Source Web:** [Microsoft Learn - SharePoint Connector](URL)
**Date:** 2024-10-31
⚠️ Information non vérifiée dans documentation locale
```

### Niveaux de Confiance

Indiquer le niveau de confiance:

```markdown
**Confiance:** ✅ Haute (Documentation locale officielle)
**Confiance:** ⚠️ Moyenne (Documentation web, non vérifiée localement)
**Confiance:** ❌ Basse (Information incomplète, validation requise)
```

## ⚡ Quick Format

Pour recherches simples:

```markdown
# 📚 [Question]

**Réponse:** [1-2 phrases]

**Source:** `Docs/PowerAutomateDocs/[path]`

**Détails:**
- [Point 1]
- [Point 2]

**Limitation:** [Si applicable]
```

## 📊 Exemples

### Exemple 1: Question API Limits

```markdown
# 📚 Résultats de Recherche

**Question:** "Quelles sont les limites API de SharePoint?"
**Type:** API Limits
**Connecteur:** SharePoint

## 🎯 Réponse

SharePoint a une limite de **600 appels API par 60 secondes** par connexion.

**Informations Clés:**
- Throttling scope: Par connexion (pas par flow)
- Comportement: HTTP 429 "Too Many Requests"
- Retry: Automatique avec exponential backoff

## 📖 Source

**Documentation Locale:**
- **Fichier:** `Docs/PowerAutomateDocs/SharePoint/overview.md`
- **Section:** API Limits
- **Ligne:** 18-19

**Extrait:**
> **600 calls per 60 seconds** per connection
> - Max attachment size: **90MB**

## ⚙️ Contexte

### Limitations Associées
- **Throttling Impact:** High-volume flows nécessitent délais
  - Référence: [overview](../../Docs/PowerAutomateDocs/SharePoint/overview.md#api_limits)

### Calcul Impact
Pour flow avec "Apply to each":
- 100 items × 2 actions = 200 calls
- Temps minimum: ~20 secondes (pour rester sous 600/60s)

## 💡 Exemples

### Scénario 1: Loop avec 50 Items
\`\`\`
Apply to each (50 items)
→ Get file properties (50 calls)
→ Update file (50 calls)
Total: 100 calls
Temps safe: 10+ secondes (delay 0.2s/item)
\`\`\`

### Scénario 2: Batch Processing
\`\`\`
Get items (1 call)
→ Filter (0 calls - local)
→ Select (0 calls - local)
→ Create items batch (1 call)
Total: 2 calls → OK même haute fréquence
\`\`\`

## ✅ Recommandations

### Best Practices
1. **Filtrer à la source:** Utiliser OData queries dans triggers/actions
2. **Batch operations:** Grouper opérations quand possible
3. **Monitoring:** Tracker calls/minute dans production

### À Éviter
- ❌ Loops sans délai sur large datasets
- ❌ Nested loops sans concurrency control
- ❌ Refresh fréquents (< 1 minute) de listes entières

### Alternatives
Si throttling bloque:
- HTTP connector avec SharePoint REST API + manuelles retries
- Logic Apps (limites différentes)
- Azure Functions pour processing bulk

## 🔗 Pour Aller Plus Loin

**Documentation Locale:**
- [SharePoint Actions](../../Docs/PowerAutomateDocs/SharePoint/actions.md)
- [Patterns de Performance](../../Docs/PowerAutomateDocs/SharePoint/overview.md#best_practices)

**Documentation Officielle:**
- [Microsoft Learn - SharePoint Limits](https://learn.microsoft.com/connectors/sharepointonline/#limits)
```

### Exemple 2: Information Manquante

```markdown
# 📚 Résultats de Recherche

**Question:** "Comment gérer les pièces jointes > 90MB dans SharePoint?"
**Type:** Limitation/Workaround
**Connecteur:** SharePoint

## 🎯 Réponse

SharePoint connector limite les pièces jointes à **90MB maximum**.

**Confiance:** ✅ Haute (Documentation locale)

## 📖 Source

**Documentation Locale:**
- **Fichier:** `Docs/PowerAutomateDocs/SharePoint/overview.md`
- **Section:** API Limits
- **Ligne:** 19

**Extrait:**
> Max attachment size: **90MB**

## ⚙️ Contexte

### Limitation Identifiée
- **Max attachment:** 90MB (hard limit)
- **Pas de workaround** dans documentation locale

### Documentation Manquante
❓ **Information non trouvée:**
- Chunked upload pour fichiers > 90MB
- Alternative avec Graph API
- Compression avant upload

⚠️ **Recherche web recommandée pour workarounds**

## ✅ Recommandations

### Workarounds Possibles (non documentés localement)
1. **HTTP connector + SharePoint REST API:**
   - Chunked upload (blocks de 10MB)
   - Requiert authentification manuelle

2. **OneDrive intermédiaire:**
   - Upload vers OneDrive (pas de limite 90MB)
   - Puis copy vers SharePoint

3. **Validation en amont:**
   - Rejeter fichiers > 90MB avec message clair
   - Split fichiers si possible (ZIP multi-part)

### Recherche Web Suggérée
\`\`\`
"Power Automate SharePoint upload large files > 90MB chunked"
"SharePoint REST API chunked upload Power Automate"
\`\`\`

## 🔗 Pour Aller Plus Loin

**Action Requise:**
- [ ] Recherche web pour workarounds officiels
- [ ] Mise à jour documentation locale avec findings
- [ ] Test solution HTTP + chunked upload
```

## 🔗 Références

- **Agent docs-researcher:** `../ agents/docs-researcher.md`
- **Templates Documentation:** `../../Docs/PowerAutomateDocs/templates/`
- **Format Documentation:** `../../Docs/PowerAutomateDocs/templates/agent-optimized-format.md`

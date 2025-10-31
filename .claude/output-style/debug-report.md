# Output Style: Debug Report

Format standardisé pour les rapports de débogage d'erreurs Power Automate.

**Utilisé par:** automation-debugger skill, flow-debugger agent

## 📋 Structure Standard

### 1. En-tête

```markdown
# 🔧 Rapport de Débogage

**Flow:** [Nom du flow]
**Erreur:** [Code/Message d'erreur]
**Action problématique:** [Nom de l'action]
**Date:** [Date d'analyse]
```

### 2. Analyse de l'Erreur

```markdown
## 🔍 Analyse

### Type d'Erreur
[Catégorie: Throttling/Authentication/DataFormat/Timeout/NotFound/Permission]

### Symptômes
- [Ce que l'utilisateur voit]
- [Comportement observé]
- [Fréquence: systématique/intermittent]

### Contexte
- **Connecteur:** [Nom]
- **Action:** [Nom de l'action]
- **Données d'entrée:** [Description]
```

### 3. Root Cause

```markdown
## 🎯 Cause Racine

[Explication claire et concise de la cause racine]

**Documentation consultée:**
- Source: Docs/PowerAutomateDocs/[Connector]/[File].md
- Section: [Section spécifique]
- Limitation identifiée: [lim-XXX si applicable]

**Contraintes identifiées:**
- [Limitation 1]
- [Limitation 2]
```

### 4. Solution

```markdown
## ✅ Solution

### Changements Requis

**Dans l'action [Nom]:**
1. [Modification 1 - description]
2. [Modification 2 - description]

### Code Corrigé

\`\`\`json
{
  "action_corrected": {
    "parameter1": "nouvelle_valeur",
    "parameter2": "nouvelle_valeur"
  }
}
\`\`\`

### Fichier fix_bloc.json

\`\`\`json
{
  "bloc_id": "[ID du bloc]",
  "action_name": "[Nom]",
  "fixes": {
    // Code complet prêt à copier-coller
  }
}
\`\`\`
```

### 5. Prévention

```markdown
## 🛡️ Prévention

Pour éviter cette erreur à l'avenir:
1. [Recommandation 1]
2. [Recommandation 2]
3. [Best practice référencée]

**Monitoring:**
- [Métrique à surveiller]
- [Seuil d'alerte]
```

### 6. Tests

```markdown
## 🧪 Plan de Test

1. **Test unitaire:**
   - Input: [Données de test]
   - Expected: [Résultat attendu]

2. **Test d'intégration:**
   - [Scénario complet]

3. **Validation:**
   - [ ] Erreur résolue
   - [ ] Pas de régression
   - [ ] Performance acceptable
```

## 🎨 Règles de Formatage

### Emojis Standard

- 🔧 Titre rapport
- 🔍 Analyse
- 🎯 Cause racine
- ✅ Solution
- 🛡️ Prévention
- 🧪 Tests
- ⚠️ Avertissement
- 📚 Documentation

### Mise en Forme

- **Gras** pour mots-clés importants
- `Code inline` pour noms techniques
- ```Blocs code``` pour JSON/code
- > Citations pour extraits de documentation
- - Listes à puces pour énumérations

### Liens

Toujours référencer documentation:
```markdown
[Voir limitation lim-001](../../Docs/PowerAutomateDocs/SharePoint/overview.md#lim-001)
```

## ⚡ Quick Format

Pour rapports rapides (erreurs simples):

```markdown
# 🔧 Debug: [Action] - [Erreur]

**Problème:** [1 phrase]

**Cause:** [1 phrase]

**Fix:**
\`\`\`json
{fix_code}
\`\`\`

**Source:** Docs/[path]
```

## 📊 Exemples

### Exemple 1: Erreur Throttling

```markdown
# 🔧 Rapport de Débogage

**Flow:** Document Sync Workflow
**Erreur:** 429 Too Many Requests
**Action problématique:** SharePoint - Get files
**Date:** 2024-10-31

## 🔍 Analyse

### Type d'Erreur
Throttling (429)

### Symptômes
- Flow échoue après traitement de ~50 fichiers
- Message: "Rate limit exceeded"
- Survient systématiquement vers 10h00

### Contexte
- **Connecteur:** SharePoint
- **Action:** Get files (properties only)
- **Données d'entrée:** Liste de 200 documents

## 🎯 Cause Racine

Le flow dépasse la limite API de SharePoint: **600 appels par 60 secondes**.

**Documentation consultée:**
- Source: Docs/PowerAutomateDocs/SharePoint/overview.md
- Section: API Limits
- Limitation: 600 calls/60s per connection

L'action "Get files" dans Apply to each génère 1 appel API par fichier.
200 fichiers en 20 secondes = 600 calls/60s → Throttling.

## ✅ Solution

### Changements Requis

**Ajouter délai dans boucle:**
1. Insérer action "Delay" après "Get files"
2. Durée: 1 seconde
3. Active concurrency control: OFF

### Code Corrigé

\`\`\`json
{
  "actions": {
    "Apply_to_each": {
      "foreach": "@triggerBody()?['value']",
      "actions": {
        "Get_file_properties": {...},
        "Delay": {
          "type": "Wait",
          "inputs": {
            "interval": {
              "count": 1,
              "unit": "Second"
            }
          }
        }
      },
      "runtimeConfiguration": {
        "concurrency": {
          "repetitions": 1
        }
      }
    }
  }
}
\`\`\`

## 🛡️ Prévention

1. **Ajouter délai systématique** dans loops intensifs
2. **Monitoring**: Tracker API calls/minute
3. **Filtrage**: Réduire nombre d'items si possible
4. **Batch operations**: Utiliser si disponible

## 🧪 Plan de Test

1. Test avec 10 fichiers → Succès attendu
2. Test avec 100 fichiers → Succès attendu (temps: ~2 min)
3. Test avec 200 fichiers → Succès attendu (temps: ~4 min)
```

## 🔗 Références

- **Templates Documentation:** `../../Docs/PowerAutomateDocs/templates/`
- **Agent automation-debugger:** `../skills/automation-debugger/SKILL.md`
- **Patterns d'erreur:** `../skills/automation-debugger/ERROR-PATTERNS.md`

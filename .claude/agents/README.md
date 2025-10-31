---
name: agents-documentation
description: Documentation for Power Automate specialized agents (not an executable agent)
skip: true
---

# Power Automate Agents

Ce dossier contient les agents spécialisés pour Power Automate.

## flow-builder

**Agent de construction de flows Power Automate**

### Fonctionnalité principale

Cet agent génère des flows Power Automate complets au format JSON prêt à copier-coller directement dans Power Automate via la fonction "Paste code".

### Format de sortie garanti

**Structure JSON exacte**:
```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
      "$connections": {
        "defaultValue": {},
        "type": "Object"
      }
    },
    "triggers": { /* déclencheur du flow */ },
    "actions": { /* toutes les actions */ },
    "outputs": {}
  },
  "schemaVersion": "1.0.0.0"
}
```

### Caractéristiques garanties

- ✅ **JSON valide** - Syntaxe correcte, pas d'erreurs
- ✅ **Structure complète** - Aucun placeholder `{...}`, tout est défini
- ✅ **GUIDs valides** - Tous les `operationMetadataId` sont des UUID correctement formatés
- ✅ **Expressions dynamiques** - Syntaxe Power Automate correcte (`@triggerOutputs()`, `@body('action')`, etc.)
- ✅ **Noms de connexion standards** - `shared_sharepointonline`, `shared_onedrive`, etc.
- ✅ **Dependencies runAfter** - Chaînage correct des actions
- ✅ **Copy-paste ready** - Prêt à coller directement dans Power Automate

### Validation automatique

Avant de renvoyer le JSON, l'agent vérifie:
1. Syntaxe JSON (brackets, quotes, commas)
2. Structure complète (root, definition, schemaVersion)
3. Tous les champs obligatoires présents
4. GUIDs au bon format
5. Expressions Power Automate correctes
6. Pas de texte placeholder

### Utilisation

**Fournir à l'agent**:
- Description détaillée du flow souhaité
- Inputs (sources de données, déclencheurs)
- Outputs (destinations, résultats attendus)
- Logique métier (conditions, boucles, transformations)

**L'agent génère**:
1. Analyse des requirements
2. Architecture du flow
3. **JSON complet prêt à copier-coller**
4. Notes d'implémentation
5. Instructions d'import

### Référence format

Consultez `/PowerAutomateDocs/power-automate-json-format.md` pour la spécification complète du format JSON Power Automate.

### Import dans Power Automate

1. Ouvrir https://make.powerautomate.com
2. Cliquer "My flows" → "New flow" → "Instant cloud flow"
3. Cliquer "..." (menu) → "Paste code"
4. Coller le JSON généré
5. Sauvegarder

Le flow s'importe sans modification nécessaire!

---

## powerautomate-docs-researcher

**Agent de recherche dans la documentation Power Automate**

Utilise la documentation locale dans `PowerAutomateDocs/` pour répondre aux questions sur les connecteurs, actions, triggers, limitations, et best practices.

Consulte automatiquement:
- Limitations API et throttling
- Spécifications des actions/triggers
- Patterns de design
- Stratégies de debugging

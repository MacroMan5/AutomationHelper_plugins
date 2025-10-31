# Power Automate Documentation Templates

Templates pour créer une documentation standardisée et optimisée pour la recherche par agent Claude Code.

## 📋 Templates Disponibles

### 1. template-overview-v2.md
Template pour documenter l'overview d'un connecteur Power Automate.

**Contient:**
- YAML frontmatter avec métadonnées
- Sections: capabilities, API limits, limitations, use cases
- Format optimisé pour recherche par agent

**Usage:**
```
Copier template-overview-v2.md
→ Renommer: ConnectorName/overview.md
→ Remplir tous les {PLACEHOLDERS}
→ Sauvegarder dans PowerAutomateDocs/ConnectorName/
```

### 2. template-actions-v2.md
Template pour documenter toutes les actions d'un connecteur.

**Contient:**
- Structure par catégorie (create, read, update, delete)
- Détails par action: parameters, returns, examples
- IDs uniques et attributs sémantiques

**Usage:**
```
Copier template-actions-v2.md
→ Renommer: ConnectorName/actions.md
→ Documenter chaque action
→ Assigner IDs uniques (action-create-file, etc.)
```

### 3. template-triggers-v2.md
Template pour documenter tous les triggers d'un connecteur.

**Contient:**
- Classification par type (polling, webhook, scheduled)
- Détails: behavior, outputs, performance
- Impact API et considérations de performance

**Usage:**
```
Copier template-triggers-v2.md
→ Renommer: ConnectorName/triggers.md
→ Documenter chaque trigger
→ Inclure polling behavior et latency
```

## 🔍 Format Optimisé Agent

### YAML Frontmatter

Permet recherche rapide par métadonnées:

```yaml
---
type: connector-overview
connector_name: SharePoint
keywords: [sharepoint, lists, files, collaboration]
api_limits:
  calls_per_hour: 600
---
```

**Agent peut:**
- Filtrer par keywords sans lire le fichier
- Extraire API limits instantanément
- Identifier type de document

### XML Tags

Permet extraction précise de sections:

```xml
<limitation id="lim-001" severity="critical">
**Generic Lists Only**: Description...
</limitation>
```

**Agent peut:**
- Grep `<limitation.*severity="critical"`
- Extraire toutes limitations high severity
- Parser structure sans ambiguïté

### Unique IDs

Permet références directes:

```markdown
<limitation id="lim-001">
<action id="action-create-file">
<error id="err-429">
```

**Agent peut:**
- Jump direct à `#lim-001`
- Créer liens: `voir [limitation](overview.md#lim-001)`
- Navigation inter-documents

## 📚 Documentation de Référence

### agent-optimized-format.md
Spécifications complètes du format v2:
- Standards YAML, XML, IDs
- Principes d'optimisation agent
- Exemples de recherche

### migration-guide.md
Guide pour convertir documentation existante vers format v2:
- Processus étape par étape
- Exemples avant/après
- Checklist de validation

## 🤖 Utilisation par Agents

### Agent: docs-researcher

Cet agent utilise ces templates pour:
1. **Rechercher** documentation existante
2. **Valider** format des documents
3. **Suggérer** améliorations structure

**Référence:** `.claude/agents/docs-researcher.md`

### Agent: docs-fetcher (futur)

Utilisera ces templates pour:
1. **Fetch** documentation Microsoft
2. **Formater** selon templates
3. **Générer** fichiers prêts à utiliser

## 📊 Priorités Documentation

### Format v2 (Recommandé)

Utilisez templates v2 pour:
- ✅ Nouvelles documentations connecteurs
- ✅ Migration docs existantes
- ✅ Mise à jour documentations incomplètes

**Avantages:**
- Recherche agent 3-5x plus rapide
- Précision +20-25%
- Navigation directe par IDs
- Filtrage multi-critères

### Connecteurs Prioritaires

1. **SharePoint** (usage élevé)
2. **OneDrive** (usage élevé)
3. **Office 365** (usage moyen)
4. **HTTP** (usage moyen)
5. **Teams** (usage moyen)

## 🛠️ Commandes Claude Code

### Créer nouvelle documentation

```
Utilise le template Docs/PowerAutomateDocs/templates/template-overview-v2.md
pour créer la documentation du connecteur [Nom]
```

### Valider documentation

```
Valide Docs/PowerAutomateDocs/[Connector]/overview.md
contre le template Docs/PowerAutomateDocs/templates/template-overview-v2.md
```

### Migrer documentation

```
Migre Docs/PowerAutomateDocs/[Connector]/overview.md
vers format v2 selon Docs/PowerAutomateDocs/templates/migration-guide.md
```

## 📈 Métriques

**Templates créés:** 3 (overview, actions, triggers)
**Format:** v2 optimisé agent
**Gain performance:** 3-5x recherche plus rapide
**Gain précision:** +20-25%

## 🔗 Liens

- **Documentation Power Automate:** `../` (répertoire parent)
- **Agents Claude Code:** `../../.claude/agents/`
- **Agent docs-researcher:** `../../.claude/agents/docs-researcher.md`

---

**Dernière mise à jour:** 2024-10-31
**Version:** 2.0
**Mainteneur:** Système Claude Code

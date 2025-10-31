# Migration Guide - Vers Format Optimisé Agent

## Objectif

Convertir la documentation existante vers le nouveau format optimisé pour la recherche par agent Claude Code.

## Bénéfices du Nouveau Format

### Pour les Agents
1. **Métadonnées YAML**: Recherche rapide par keywords, type, catégorie
2. **Balises XML**: Extraction précise de sections spécifiques
3. **IDs Uniques**: Références croisées et navigation directe
4. **Structure Prévisible**: Parsing automatique sans ambiguïté
5. **Attributs Sémantiques**: Filtrage par sévérité, complexité, type

### Pour les Humains
1. **Navigation Claire**: Hiérarchie cohérente et table des matières
2. **Recherche Rapide**: Index et références croisées
3. **Exemples Concrets**: Code et configurations réels
4. **Troubleshooting Structuré**: Erreurs documentées avec solutions

## Processus de Migration

### Étape 1: Analyser le Document Existant

**Pour chaque fichier de documentation**:

1. **Identifier le type**:
   - `overview.md` → Utiliser `template-overview-v2.md`
   - `actions.md` → Utiliser `template-actions-v2.md`
   - `triggers.md` → Utiliser `template-triggers-v2.md`

2. **Extraire les informations clés**:
   - Nom du connecteur
   - Nombre d'actions/triggers
   - Limites API
   - Limitations critiques
   - Exemples existants

3. **Identifier les sections manquantes**:
   - Quelles sections du template n'existent pas?
   - Quelles informations devront être ajoutées?

### Étape 2: Créer le Frontmatter YAML

**Template de base**:
```yaml
---
type: connector-overview|connector-actions|connector-triggers
connector_name: NomDuConnecteur
version: 1.0
last_updated: 2024-10-31
keywords: [mot-clé1, mot-clé2, mot-clé3]
---
```

**Extraction des keywords**:
- Nom du connecteur
- Catégorie (sharepoint, office365, data, etc.)
- Types d'opérations (files, lists, users, etc.)
- Cas d'usage (automation, sync, approval, etc.)

**Exemple SharePoint**:
```yaml
keywords: [sharepoint, lists, documents, collaboration, files, permissions]
```

### Étape 3: Structurer avec Balises XML

**Sections Critiques à Baliser**:

#### Pour Overview
```xml
<official_docs>URL</official_docs>
<description>...</description>
<capabilities>...</capabilities>
<api_limits>...</api_limits>
<critical_limitations>
  <limitation id="lim-001" severity="high">...</limitation>
</critical_limitations>
```

#### Pour Actions
```xml
<action id="action-create-file" category="create" complexity="medium">
  <description>...</description>
  <parameters>...</parameters>
  <returns>...</returns>
  <limitations>...</limitations>
  <example>...</example>
</action>
```

#### Pour Triggers
```xml
<trigger id="trigger-when-file-created" type="polling" latency_minutes="5">
  <description>...</description>
  <behavior>...</behavior>
  <outputs>...</outputs>
</trigger>
```

### Étape 4: Ajouter les IDs Uniques

**Schéma de Naming**:

**Limitations**:
- `lim-001`, `lim-002`, etc.
- Optionnel: `lim-auth-001`, `lim-size-001` (par catégorie)

**Actions**:
- `action-create-file`
- `action-get-file-content`
- Format: `action-{operation}-{object}`

**Triggers**:
- `trigger-when-file-created`
- `trigger-when-item-modified`
- Format: `trigger-{event-description}`

**Erreurs**:
- `err-429`, `err-401`, `err-404` (par code HTTP)
- `err-action-001`, `err-trigger-001` (par séquence)

### Étape 5: Enrichir le Contenu

**Éléments à Ajouter**:

1. **Attributs Sémantiques**:
   ```xml
   severity="critical|high|medium|low"
   complexity="low|medium|high"
   throttle_impact="low|medium|high"
   ```

2. **Exemples Concrets**:
   - Code JSON réel (pas de pseudo-code)
   - Expressions Power Automate
   - Résultats attendus

3. **Références Croisées**:
   ```markdown
   - Voir [Action Create File](#action-create-file)
   - Référence: [Limitations](./overview.md#lim-001)
   ```

4. **Troubleshooting**:
   - Messages d'erreur exacts
   - Causes racines
   - Solutions étape par étape

### Étape 6: Valider le Format

**Checklist de Validation**:

- [ ] YAML frontmatter présent et complet
- [ ] Toutes les sections critiques ont des balises XML
- [ ] IDs uniques assignés (limitations, actions, triggers, erreurs)
- [ ] Attributs sémantiques ajoutés
- [ ] Exemples concrets (pas de placeholders)
- [ ] Références croisées utilisent les IDs
- [ ] Hiérarchie markdown correcte (H1, H2, H3, H4)
- [ ] Pas de sections vides
- [ ] Liens officiels Microsoft présents
- [ ] Keywords pertinents et spécifiques

## Exemple de Migration

### Avant (Format Ancien)

```markdown
# SharePoint Connector Overview

## Official Documentation
https://learn.microsoft.com/en-us/connectors/sharepointonline/

## Description
SharePoint connector helps organizations share and collaborate with colleagues.

## API Limits
- 600 calls per 60 seconds per connection
- Max attachment size: 90MB

## Critical Limitations
- Only supported in generic lists
- Lists with periods in names cause errors
```

### Après (Format Optimisé Agent)

```markdown
---
type: connector-overview
connector_name: SharePoint
connector_type: standard
version: 1.0
last_updated: 2024-10-31
keywords: [sharepoint, lists, documents, collaboration, files, permissions, microsoft365]
related_connectors: [OneDrive, Office365Groups]
api_limits:
  calls_per_minute: 10
  calls_per_hour: 600
  max_file_size_mb: 90
official_docs_url: https://learn.microsoft.com/en-us/connectors/sharepointonline/
---

# SharePoint Connector Overview

<official_docs>
https://learn.microsoft.com/en-us/connectors/sharepointonline/
</official_docs>

<description>
SharePoint connector enables automation of document management, list operations, and collaboration workflows. Connects to SharePoint Online or on-premises SharePoint 2016/2019 via On-Premises Data Gateway.
</description>

<capabilities>
## Core Capabilities
- Document library management (upload, download, update, delete)
- List item CRUD operations
- Folder structure management
- Content approval workflows
- Permission and sharing management

## Supported Operations
- File Operations: Create, read, update, delete, copy, move
- List Operations: Get items, create items, update items, delete items
- Folder Operations: Create, list, delete folders
</capabilities>

<api_limits>
## Rate Limits

**Connection-Level Throttling**
- **600 API calls per 60 seconds** per connection
- Throttling scope: per connection
- Retry-After header: yes

**Throttling Behavior**
- HTTP Status: 429 Too Many Requests
- Error message: "Rate limit exceeded"
- Automatic retry: yes (with exponential backoff)

## Size Limits

**File Operations**
- Max file upload size: **90MB**
- Max file download size: **90MB**
- Max attachment size: **90MB**

## Timeout Limits
- Default timeout: **120 seconds**
- Max timeout: **600 seconds**
- Long-running operations: not supported (use chunking)
</api_limits>

<critical_limitations>
## Content Type Support

<limitation id="lim-001" severity="critical">
**Generic Lists Only**: Only generic lists and document libraries are supported

- **Impact**: Cannot use connector with custom list templates
- **Scope**: All SharePoint actions and triggers
- **Affected Templates**:
  - Announcements lists
  - Contacts lists
  - Events/Calendar lists
  - Tasks lists
  - Custom library templates
- **Workaround**: Migrate data to generic list or use HTTP connector with SharePoint REST API

**Example Scenario**: Attempting to create item in Announcements list will fail with "List template not supported" error
</limitation>

<limitation id="lim-002" severity="high">
**List Names with Periods**: Lists with periods in names fail when used dynamically

- **Impact**: Runtime errors when list name contains period (.)
- **Scope**: Dynamic list selection in actions
- **Workaround**:
  1. Rename list to remove periods, OR
  2. Use static list selection (dropdown), OR
  3. Use HTTP connector with list GUID
- **Error**: "The specified list was not found"

**Example**: List named "My.SharePoint.List" works in dropdown but fails with expressions
</limitation>
</critical_limitations>

<authentication>
## Supported Authentication Methods

### OAuth 2.0 (Recommended)
- Flow type: Authorization Code
- Required scopes: AllSites.Read, AllSites.Write (depending on operations)
- Token refresh: automatic

## Required Permissions

### Delegated Permissions (User Context)
- **Sites.Read.All**: Read items in all site collections
- **Sites.ReadWrite.All**: Read and write items in all site collections

### Application Permissions (App-Only Context)
- **Sites.Read.All**: Read items across all site collections
- **Sites.ReadWrite.All**: Create, edit, delete items across all site collections
</authentication>

<common_use_cases>
## 1. Document Approval Workflow

**Description**: Automate document review and approval process

**Typical Flow**:
```
Trigger: When a file is created (properties only)
↓
Action 1: Get file metadata - Retrieve document details
↓
Action 2: Start and wait for approval - Route to approver
↓
Condition: Check approval status
↓ (Approved)
Action 3: Update file properties - Mark as approved
↓ (Rejected)
Action 4: Move file - Move to rejected folder
```

**Key Actions**: [Create file](./actions.md#action-create-file), [Update file properties](./actions.md#action-update-properties), [Move file](./actions.md#action-move-file)

**Best For**: Compliance workflows, contract reviews, document publishing
</common_use_cases>

<!-- Additional sections following same structure -->
```

### Changements Clés

1. **YAML frontmatter** avec métadonnées structurées
2. **Balises XML** autour des sections critiques
3. **IDs uniques** pour limitations (`lim-001`, `lim-002`)
4. **Attributs sémantiques** (`severity="critical"`)
5. **Descriptions enrichies** avec contexte et impact
6. **Exemples concrets** de scénarios d'erreur
7. **Références croisées** vers autres documents
8. **Structure prévisible** et complète

## Priorités de Migration

### Haute Priorité
1. **Connecteurs populaires**:
   - SharePoint ✓ (déjà migré - exemple)
   - OneDrive
   - Office 365 Outlook
   - Teams

2. **Sections critiques**:
   - API Limits
   - Critical Limitations
   - Common Errors

### Moyenne Priorité
3. **Connecteurs standards**:
   - Excel Online
   - SQL Server
   - Dataverse

4. **Sections importantes**:
   - Best Practices
   - Use Cases
   - Examples

### Basse Priorité
5. **Connecteurs spécialisés**:
   - Connecteurs custom
   - Connecteurs premium rares

6. **Sections supplémentaires**:
   - Advanced patterns
   - Performance tuning

## Outils d'Assistance

### Script de Validation (À venir)

```bash
# Valide format d'un fichier doc
./validate-doc.sh Docs/PowerAutomateDocs/SharePoint/overview.md

# Valide tous les fichiers
./validate-doc.sh Docs/PowerAutomateDocs/**/*.md
```

### Template Generator (À venir)

```bash
# Génère template pour nouveau connecteur
./generate-connector-docs.sh "Excel Online"
```

## Support Agent Claude Code

Les agents Claude Code peuvent aider à la migration:

**Commande**:
```
Claude, migre le fichier Docs/PowerAutomateDocs/OneDrive/overview.md vers
le nouveau format agent-optimized en utilisant le template
.claude/output-style/template-overview-v2.md
```

**L'agent va**:
1. Lire le fichier existant
2. Extraire les informations
3. Appliquer le template v2
4. Ajouter YAML frontmatter
5. Structurer avec XML tags
6. Assigner des IDs uniques
7. Enrichir avec exemples
8. Valider contre checklist

## Questions Fréquentes

**Q: Dois-je migrer tous les fichiers immédiatement?**
R: Non, migrez progressivement en commençant par les connecteurs les plus utilisés.

**Q: Le format ancien est-il encore supporté?**
R: Oui, mais le nouveau format améliore significativement la recherche par agent.

**Q: Que faire si des informations manquent?**
R: Laissez des sections TODO ou consultez la documentation officielle Microsoft.

**Q: Les balises XML affectent-elles la lisibilité?**
R: Non, elles sont invisibles dans les readers Markdown standards et améliorent le parsing agent.

**Q: Puis-je mixer ancien et nouveau format?**
R: Oui, mais l'uniformité maximise les bénéfices pour les agents.

## Prochaines Étapes

1. **Migrer SharePoint** (priorité 1) - ✓ EXEMPLE CRÉÉ
2. **Migrer OneDrive** (priorité 1)
3. **Migrer Office 365** (priorité 1)
4. **Créer script de validation** (automatisation)
5. **Documenter nouveaux connecteurs** avec format v2 directement

## Contribution

Pour contribuer à la migration:
1. Choisir un connecteur non migré
2. Suivre ce guide de migration
3. Utiliser la checklist de validation
4. Tester avec recherches agent
5. Documenter les difficultés rencontrées

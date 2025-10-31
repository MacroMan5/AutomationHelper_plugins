# Output Style - Formats de Sortie pour Agents Claude Code

Ce répertoire contient des formats standardisés pour les sorties des agents et skills Claude Code.

## 🎯 Objectif

Définir **comment les agents formatent leurs réponses** pour assurer:
- ✅ Uniformité des sorties
- ✅ Lisibilité optimale
- ✅ Facilité de parsing
- ✅ Expérience utilisateur cohérente

## 📋 Output Styles Disponibles

### debug-report.md
Format pour rapports de débogage (automation-debugger skill)
- Structure d'analyse d'erreur
- Format de solution
- Présentation de fix_bloc.json

### error-analysis.md
Format pour analyses d'erreur Power Automate
- Catégorisation erreurs
- Root cause analysis
- Solutions étape par étape

### flow-documentation.md
Format pour documentation de flows générés
- Structure de présentation
- Explication des choix techniques
- Instructions de déploiement

### research-findings.md
Format pour résultats de recherche (docs-researcher agent)
- Présentation de findings
- Attribution de sources
- Contexte et recommandations

## 🎨 Principe des Output Styles

### Ce que c'est

Instructions pour **formater la sortie** d'un agent:

```markdown
# Output Style: Debug Report

Quand tu débogues une erreur, utilise ce format:

## 🔍 Analyse
[Description problème]

## 🎯 Root Cause
[Cause racine identifiée]

## ✅ Solution
[Solution avec code]
```

### Ce que ce n'est PAS

- ❌ Templates pour créer documentation externe
- ❌ Formats pour fichiers de projet
- ❌ Standards de code

## 🤖 Utilisation par Agents

### Dans les Prompts Agents

```markdown
---
name: mon-agent
description: Description...
---

# Agent Instructions

...

## Output Format

Suis le style défini dans `.claude/output-style/debug-report.md`:
- [Instructions spécifiques]
```

### Référence dans Skills

```markdown
---
name: mon-skill
---

# Skill

Utilise output-style `.claude/output-style/error-analysis.md`
pour formater tes analyses d'erreur.
```

## 📊 Agents Utilisant Output Styles

| Agent/Skill | Output Style | Usage |
|-------------|--------------|-------|
| automation-debugger | debug-report.md | Rapports de débogage |
| docs-researcher | research-findings.md | Résultats de recherche |
| flow-builder | flow-documentation.md | Documentation flows |
| flow-debugger | error-analysis.md | Analyses d'erreur |

## 🔗 Références

**Templates Documentation Connecteurs:**
→ `Docs/PowerAutomateDocs/templates/`

**Agents:**
→ `.claude/agents/`

**Skills:**
→ `.claude/skills/`

---

**Note:** Les templates pour documenter les connecteurs Power Automate
sont dans `Docs/PowerAutomateDocs/templates/`, pas ici.

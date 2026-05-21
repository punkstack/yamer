# Project Configuration

> The Chief of Staff refuses to delegate any real work until every required field below is filled. If you opened a session and saw an interview kick off, this is the file being filled.

## Required

```yaml
product:
  name: "<short name, e.g. 'InvoiceChase'>"
  one_liner: "<one sentence — for whom, doing what, replacing what>"

user:
  who: "<specific. not 'developers'. 'Indian freelance devs chasing late payments from US clients'>"
  current_alternative: "<what they use today — manual spreadsheets, competitor X, nothing>"
  one_pain_quote: "<one sentence in the user's voice if you have it, else write what you'd expect them to say>"

constraints:
  timeline_weeks_to_mvp: 4
  team_size: 1
  budget_usd_per_month: 50
  must_be_mobile_first: true   # true | false
  
tracker:
  type: "clickup"              # clickup | linear | github_projects | none
  workspace: "<workspace name or id>"
  list_or_project: "<list name or project name>"
  statuses: ["Backlog", "Spec", "Building", "Review", "Done"]
  
git:
  repo_url: "<https://github.com/you/yourrepo or local path>"
  default_branch: "main"
  use_worktrees_for_parallel_agents: true
```

## Optional but useful

```yaml
audience:
  geo: ["India", "US"]
  language: ["English"]
  
inspiration:
  - "<URL of a product whose UX you like — frontend agent will study it>"
  - "<URL of a product whose positioning you like — gtm agent will study it>"

guardrails:
  - "Do not call OpenAI or other paid third-party APIs without asking me first"
  - "Default to open-source stacks unless I approve a paid SaaS"
```

## Status: ☐ not yet filled

Chief of Staff: when this top line still says "not yet filled", you run the interview at session start. When every required field has a real value (no placeholders left), change this line to `## Status: ☑ filled` and proceed.

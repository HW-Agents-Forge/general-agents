# Diagram lab (temporary)

A scratch page to see which Mermaid features GitHub renders. Open it on GitHub and note which blocks display a diagram and which show an error. It will be deleted once the diagram style is decided.

## 1. Frontmatter configuration with the hand-drawn look

```mermaid
---
config:
  look: handDrawn
  theme: neutral
---
flowchart LR
    A("agents/*.md") --> B("shuttle") --> C("Claude Code")
```

## 2. Neutral theme through frontmatter

```mermaid
---
config:
  theme: neutral
---
flowchart LR
    A["source"] --> B{"valid?"}
    B -- "yes" --> C["install"]
    B -- "no" --> D["refuse"]
```

## 3. New node shapes (`@{ shape: ... }`)

```mermaid
flowchart LR
    A@{ shape: doc, label: "agents/*.md" } --> B@{ shape: rounded, label: "shuttle" }
    B --> C@{ shape: cyl, label: "~/.claude" }
    B --> D@{ shape: hex, label: "refuse?" }
```

## 4. ELK layout

```mermaid
---
config:
  layout: elk
---
flowchart LR
    A("parse") --> B("resolve") --> C("render")
    A --> C
```

## 5. Architecture diagram with icons

```mermaid
architecture-beta
    group repo(cloud)[Repository]
    service src(disk)[Sources] in repo
    service engine(server)[shuttle] in repo
    service home(database)[Home or project]
    src:R --> L:engine
    engine:R --> L:home
```

## 6. Block diagram

```mermaid
block-beta
    columns 3
    A["agents"] B["skills"] C["config"]
    D["shuttle"]:3
    E["Claude Code"] F["Copilot CLI"] G["planned"]
    A --> D
    B --> D
    C --> D
    D --> E
    D --> F
    D --> G
```

## 7. Kanban

```mermaid
kanban
    todo[To do]
        t1[VS Code target]
        t2[OpenCode target]
    wip[In progress]
        t3[First evaluation]
    done[Done]
        t4[Claude Code target]
```

## 8. Timeline

```mermaid
timeline
    title general-agents
    Preparation : vision : ADRs
    Engine : parser : installer : targets
    Next : evaluation : more targets
```

## 9. Mind map

```mermaid
mindmap
  root((general-agents))
    Agents
      run
      find
      diff
      git
      svn
    Skills
      atomic-tasks
      csh-pro
    Targets
      Claude Code
      Copilot CLI
```

## 10. Quadrant chart

```mermaid
quadrantChart
    title Agents by effort and value
    x-axis Low effort --> High effort
    y-axis Low value --> High value
    quadrant-1 Do next
    quadrant-2 Plan
    quadrant-3 Maybe
    quadrant-4 Skip
    run: [0.4, 0.9]
    find: [0.3, 0.7]
    diff: [0.45, 0.5]
    git: [0.25, 0.4]
```

## 11. Pie

```mermaid
pie title Prompt size (tokens)
    "run" : 800
    "find" : 560
    "diff" : 510
    "git and svn" : 870
```

## 12. Gitgraph

```mermaid
gitGraph
    commit id: "engine"
    branch dev
    commit id: "diagrams"
    checkout main
    merge dev
```

## 13. State diagram, hand-drawn

```mermaid
---
config:
  look: handDrawn
---
stateDiagram-v2
    [*] --> Checking
    Checking --> Running
    Running --> finished
    finished --> [*]
```

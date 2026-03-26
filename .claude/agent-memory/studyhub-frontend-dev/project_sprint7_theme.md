---
name: Sprint 7 color theme — zinc neutral + green accent
description: Complete color theme — zinc near-black backgrounds with green accent (corrected from the all-green-surface approach that looked muddy)
type: project
---

The theme uses near-black zinc neutrals for all surfaces with vibrant green as the sole accent color. The original gray/violet theme was first replaced with an all-green-surface theme (bg-green-900/40 etc.), which looked monochromatic and muddy. This was then corrected to the current zinc+green-accent approach (Linear/Vercel/GitHub Dark style).

**Why:** The all-green surface approach created a monochromatic muddy look. Near-black bases with a single vibrant accent gives higher contrast and looks professional.

**How to apply:** Every new template must use zinc for panels, cards, inputs, borders, and page background. Green is used ONLY for: active nav items, hover states on active items, CTA button gradients, links, accent icons, and the brand logo/wordmark gradient.

## Core rule
- Background / surface → `zinc` family
- Accent (interactive, link, highlight, icon, active state, button gradient) → `green`/`emerald`

## Key token mapping
- Page background: `bg-zinc-950`
- Cards/panels/sidebar/topbar: `bg-zinc-900`
- Input fields: `bg-zinc-800`
- Elevated surfaces: `bg-zinc-800/60`
- Borders (default): `border-zinc-800`
- Borders (hover/elevated): `border-zinc-700`
- Dividers: `divide-zinc-800`
- Primary text: `text-zinc-100` / `text-white`
- Secondary text: `text-zinc-400`
- Muted text: `text-zinc-600`
- Accent text/icon: `text-green-400`
- Accent hover: `text-green-300`
- Active nav bg: `bg-green-500/10`
- Active nav text: `text-green-400`
- Nav hover: `hover:bg-zinc-800 hover:text-zinc-100`
- Primary button: `from-green-500 to-emerald-600` → hover `from-green-400 to-emerald-500`
- Button shadow: `shadow-green-500/20`
- Brand logo gradient: `from-green-400 to-emerald-500`
- Brand text gradient: `from-green-400 to-emerald-400`
- Mobile overlay: `bg-black/70 backdrop-blur-sm`
- Input focus: `focus:ring-green-500/40 focus:border-green-500/50`
- Secondary button: `bg-zinc-800 text-zinc-300 border-zinc-700 hover:bg-zinc-700`
- Topbar: `bg-zinc-900/80 border-zinc-800`
- Count/number badges: `bg-zinc-800/60 text-zinc-400 border-zinc-700`

## Unchanged semantic colors (never modify)
- Status badges: sky (new), amber (in_progress), emerald (completed)
- Content type badges: violet (article), rose (video), orange (podcast), cyan (course), emerald (book), pink (tool), gray (other)
- Error/warning alerts: rose, amber
- Success alerts: emerald
- Category icons: emerald
- Tag icons: amber
- Tag pill chip (accent): `bg-green-500/10 text-green-400 border-green-500/20`

## Dashboard clickable filters (implemented Sprint 7)
- Content type badges in "Content by Type" link to `?content_type={{ item.content_type }}`
- Category links in "Top Categories" link to `?category={{ category.id }}`
- Tag names in "Top Tags" link to `?tag={{ tag.id }}`

## Landing page (implemented Sprint 7)
- Large StudyHub `<h1>` brand heading above the badge (font-black, 6xl–8xl responsive)
- The marketing headline is `<h2 id='hero-heading'>` for correct heading hierarchy

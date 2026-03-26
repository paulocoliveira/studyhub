# Design System

Dark-themed UI using TailwindCSS utility classes in Django Template Language. All pages extend `base.html` (authenticated) or `base_public.html` (public).

## Color Palette

Near-black neutral backgrounds with vibrant green as accent. Rule: if a color is a background/surface → use `zinc` family. If it's an accent (interactive, link, highlight, icon, active state, button gradient) → use `green`/`emerald`.

| Token | TailwindCSS Class | Hex approx | Usage |
|---|---|---|---|
| Background Primary | `bg-zinc-950` | `#09090b` | Page background |
| Background Secondary | `bg-zinc-900` | `#18181b` | Cards, panels, sidebars |
| Background Elevated | `bg-zinc-800/60` | | Inputs, elevated surfaces |
| Border | `border-zinc-800` | `#27272a` | Default borders |
| Border Subtle | `border-zinc-700` | `#3f3f46` | Hover/elevated borders |
| Divider | `divide-zinc-800` | | List dividers |
| Text Primary | `text-zinc-100` | `#f4f4f5` | Headings, primary text |
| Text Secondary | `text-zinc-400` | `#a1a1aa` | Descriptions, labels |
| Text Muted | `text-zinc-600` | `#52525b` | Placeholders, hints |
| Accent | `text-green-400` | `#4ade80` | Links, active states, icons |
| Accent Dim | `text-green-300` | `#86efac` | Accent hover states |
| Active Nav BG | `bg-green-500/10` | | Active sidebar item background |
| Active Nav Text | `text-green-400` | | Active sidebar item text |
| Nav Hover | `hover:bg-zinc-800 hover:text-zinc-100` | | Default nav item hover |
| Input BG | `bg-zinc-800` | | Form inputs |
| Input Border | `border-zinc-700` | | Input borders |
| Input Focus | `focus:ring-green-500/40 focus:border-green-500/50` | | Input focus ring |
| Primary Button | `from-green-500 to-emerald-600` gradient | | CTA buttons |
| Primary Button Hover | `hover:from-green-400 hover:to-emerald-500` | | CTA hover |
| Button Shadow | `shadow-green-500/20` | | Button glow |
| Brand Logo Gradient | `from-green-400 to-emerald-500` | | Logo icon |
| Brand Text Gradient | `from-green-400 to-emerald-400` | | "StudyHub" wordmark |
| Mobile Overlay | `bg-black/70 backdrop-blur-sm` | | Mobile sidebar backdrop |
| Success | `text-emerald-500` | `#10B981` | Completed status |
| Warning | `text-amber-500` | `#F59E0B` | In-progress status |
| Danger | `text-rose-500` | `#F43F5E` | Delete actions, errors |
| Info | `text-sky-500` | `#0EA5E9` | New status |

## Typography

| Element | TailwindCSS Classes |
|---|---|
| Font Family | `font-sans` (Inter, system-ui, sans-serif) |
| Page Title | `text-3xl font-bold text-white` |
| Section Title | `text-xl font-semibold text-white` |
| Card Title | `text-lg font-medium text-zinc-100` |
| Body Text | `text-sm text-zinc-400` |
| Label | `text-sm font-medium text-zinc-400` |
| Helper Text | `text-xs text-zinc-600` |

## Gradient Patterns

```html
<!-- Primary gradient (buttons, hero) -->
<div class="bg-gradient-to-r from-green-500 to-emerald-600">

<!-- Subtle card gradient -->
<div class="bg-gradient-to-br from-zinc-900 via-zinc-900 to-zinc-800/30">

<!-- Text gradient (brand) -->
<span class="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
```

## Buttons

```html
<!-- Primary -->
<button class="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-600
    text-white text-sm font-medium rounded-lg
    hover:from-green-400 hover:to-emerald-500
    transition-all duration-200 shadow-lg shadow-green-500/20">

<!-- Secondary -->
<button class="px-4 py-2 bg-zinc-800 text-zinc-300 text-sm font-medium rounded-lg
    border border-zinc-700 hover:bg-zinc-700 hover:text-white
    transition-all duration-200">

<!-- Danger -->
<button class="px-4 py-2 bg-rose-600/10 text-rose-500 text-sm font-medium rounded-lg
    border border-rose-500/20 hover:bg-rose-600/20
    transition-all duration-200">

<!-- Ghost / Icon -->
<button class="p-2 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-lg
    transition-all duration-200">
```

## Form Inputs

```html
<!-- Text Input -->
<input type="text"
    class="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg
    text-zinc-100 text-sm placeholder-zinc-600
    focus:outline-none focus:ring-2 focus:ring-green-500/40 focus:border-green-500/50
    transition-all duration-200">

<!-- Select -->
<select class="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg
    text-zinc-100 text-sm
    focus:outline-none focus:ring-2 focus:ring-green-500/40 focus:border-green-500/50
    transition-all duration-200">

<!-- Textarea -->
<textarea class="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg
    text-zinc-100 text-sm placeholder-zinc-600
    focus:outline-none focus:ring-2 focus:ring-green-500/40 focus:border-green-500/50
    transition-all duration-200 resize-none" rows="4">

<!-- Label -->
<label class="block text-sm font-medium text-zinc-400 mb-1">

<!-- Error -->
<p class="mt-1 text-xs text-rose-500">This field is required.</p>
```

## Cards

```html
<!-- Standard Card -->
<div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5
    hover:border-zinc-700 transition-all duration-200">

<!-- Stats Card -->
<div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5
    hover:border-zinc-700 transition-all duration-200">
    <p class="text-sm text-zinc-400">Label</p>
    <p class="text-2xl font-bold text-white mt-1">Value</p>
</div>
```

## Content Card (card grid view)

```html
<div class="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden
    hover:border-zinc-700 transition-all duration-200 flex flex-col">

    <!-- Thumbnail -->
    <div class="aspect-video bg-zinc-800 relative overflow-hidden">
        <img src="{{ card_image_url }}" alt=""
            class="w-full h-full object-cover"
            onerror="this.src='{% static 'images/placeholders/' %}{{ content.content_type }}.svg'">
    </div>

    <!-- Body -->
    <div class="p-4 flex flex-col flex-1 gap-2">
        <h3 class="text-sm font-medium text-zinc-100 line-clamp-2">{{ content.title }}</h3>
        <p class="text-xs text-zinc-500 line-clamp-2">{{ content.description }}</p>
        <div class="mt-auto flex items-center justify-between pt-3 border-t border-zinc-800">
            <span class="text-xs text-zinc-600">{{ content.created_at|date:"M d" }}</span>
        </div>
    </div>
</div>
```

## Status Badges

```html
<span class="px-2.5 py-0.5 text-xs font-medium rounded-full bg-sky-500/10 text-sky-400">New</span>
<span class="px-2.5 py-0.5 text-xs font-medium rounded-full bg-amber-500/10 text-amber-400">In Progress</span>
<span class="px-2.5 py-0.5 text-xs font-medium rounded-full bg-emerald-500/10 text-emerald-400">Completed</span>
```

## Content Type Badges

```html
<!-- Article -->
<span class="px-2.5 py-0.5 text-xs font-medium rounded-full bg-violet-500/10 text-violet-400">Article</span>

<!-- Video -->
<span class="px-2.5 py-0.5 text-xs font-medium rounded-full bg-rose-500/10 text-rose-400">Video</span>
```

## Layout

```html
<!-- Page layout (sidebar + main) -->
<div class="flex min-h-screen bg-zinc-950">
    <aside class="w-64 bg-zinc-900 border-r border-zinc-800 min-h-screen p-4">
    <main class="flex-1 p-6">

<!-- Stats grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

<!-- Content cards grid -->
<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">

<!-- Form layout -->
<div class="max-w-2xl mx-auto">
```

## Sidebar Navigation

```html
<!-- Active item -->
<a class="flex items-center gap-3 px-3 py-2 rounded-lg
    bg-green-500/10 text-green-400 text-sm font-medium">

<!-- Default item -->
<a class="flex items-center gap-3 px-3 py-2 rounded-lg
    text-zinc-400 text-sm hover:bg-zinc-800 hover:text-zinc-100
    transition-all duration-200">
```

## View Toggle (card / list)

```html
<div class="flex items-center gap-1 bg-zinc-800/60 rounded-lg p-0.5">
    <button data-view="cards"
        class="p-1.5 rounded-md text-zinc-400 hover:text-white
        transition-all duration-200">
    <button data-view="list"
        class="p-1.5 rounded-md text-zinc-400 hover:text-white
        transition-all duration-200">
</div>
```

The selected view preference is persisted via `localStorage`.

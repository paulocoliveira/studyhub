# Design System

Dark-themed UI using TailwindCSS utility classes in Django Template Language. All pages extend `base.html` (authenticated) or `base_public.html` (public).

## Color Palette

| Token | TailwindCSS Class | Hex | Usage |
|---|---|---|---|
| Background Primary | `bg-gray-950` | `#030712` | Page background |
| Background Secondary | `bg-gray-900` | `#111827` | Cards, panels, sidebars |
| Background Tertiary | `bg-gray-800` | `#1F2937` | Input fields, hover states |
| Border | `border-gray-700` | `#374151` | Borders, dividers |
| Text Primary | `text-gray-100` | `#F3F4F6` | Headings, primary text |
| Text Secondary | `text-gray-400` | `#9CA3AF` | Descriptions, labels |
| Text Muted | `text-gray-500` | `#6B7280` | Placeholders, hints |
| Accent | `text-violet-500` | `#8B5CF6` | Primary actions, active states |
| Gradient From | `from-violet-600` | `#7C3AED` | Gradient start |
| Gradient To | `to-indigo-600` | `#4F46E5` | Gradient end |
| Success | `text-emerald-500` | `#10B981` | Completed status |
| Warning | `text-amber-500` | `#F59E0B` | In-progress status |
| Danger | `text-rose-500` | `#F43F5E` | Delete actions, errors |
| Info | `text-sky-500` | `#0EA5E9` | New status |

## Typography

| Element | TailwindCSS Classes |
|---|---|
| Font Family | `font-sans` (Inter, system-ui, sans-serif) |
| Page Title | `text-3xl font-bold text-gray-100` |
| Section Title | `text-xl font-semibold text-gray-100` |
| Card Title | `text-lg font-medium text-gray-100` |
| Body Text | `text-sm text-gray-300` |
| Label | `text-sm font-medium text-gray-400` |
| Helper Text | `text-xs text-gray-500` |

## Gradient Patterns

```html
<!-- Primary gradient (buttons, hero) -->
<div class="bg-gradient-to-r from-violet-600 to-indigo-600">

<!-- Subtle card gradient -->
<div class="bg-gradient-to-br from-gray-900 via-gray-900 to-violet-950/20">

<!-- Text gradient -->
<h1 class="bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">
```

## Buttons

```html
<!-- Primary -->
<button class="px-4 py-2 bg-gradient-to-r from-violet-600 to-indigo-600
    text-white text-sm font-medium rounded-lg
    hover:from-violet-500 hover:to-indigo-500
    transition-all duration-200 shadow-lg shadow-violet-500/25">

<!-- Secondary -->
<button class="px-4 py-2 bg-gray-800 text-gray-300 text-sm font-medium rounded-lg
    border border-gray-700 hover:bg-gray-700 hover:text-white
    transition-all duration-200">

<!-- Danger -->
<button class="px-4 py-2 bg-rose-600/10 text-rose-500 text-sm font-medium rounded-lg
    border border-rose-500/20 hover:bg-rose-600/20
    transition-all duration-200">

<!-- Ghost / Icon -->
<button class="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg
    transition-all duration-200">
```

## Form Inputs

```html
<!-- Text Input -->
<input type="text"
    class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg
    text-gray-100 text-sm placeholder-gray-500
    focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500
    transition-all duration-200">

<!-- Select -->
<select class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg
    text-gray-100 text-sm
    focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500
    transition-all duration-200">

<!-- Textarea -->
<textarea class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg
    text-gray-100 text-sm placeholder-gray-500
    focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500
    transition-all duration-200 resize-none" rows="4">

<!-- Label -->
<label class="block text-sm font-medium text-gray-400 mb-1">

<!-- Error -->
<p class="mt-1 text-xs text-rose-500">This field is required.</p>
```

## Cards

```html
<!-- Standard Card -->
<div class="bg-gray-900 border border-gray-800 rounded-xl p-5
    hover:border-gray-700 transition-all duration-200">

<!-- Stats Card -->
<div class="bg-gradient-to-br from-gray-900 to-gray-900/50
    border border-gray-800 rounded-xl p-5">
    <p class="text-sm text-gray-400">Label</p>
    <p class="text-2xl font-bold text-gray-100 mt-1">Value</p>
</div>
```

## Content Card (card grid view)

```html
<div class="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden
    hover:border-gray-700 transition-all duration-200 flex flex-col">

    <!-- Thumbnail -->
    <div class="aspect-video bg-gray-800 relative overflow-hidden">
        <img src="{{ card_image_url }}" alt=""
            class="w-full h-full object-cover"
            onerror="this.src='{% static 'images/placeholders/' %}{{ content.content_type }}.svg'">
        <span class="absolute top-2 right-2 px-2 py-0.5 text-xs font-medium rounded-full
            bg-gray-900/80 text-gray-300 backdrop-blur-sm">
            {{ content.get_content_type_display }}
        </span>
    </div>

    <!-- Body -->
    <div class="p-4 flex flex-col flex-1 gap-2">
        <h3 class="text-sm font-medium text-gray-100 line-clamp-2">{{ content.title }}</h3>
        <p class="text-xs text-gray-500 line-clamp-2">{{ content.description }}</p>
        <div class="mt-auto flex items-center justify-between pt-3">
            <!-- status badge -->
            <span class="text-xs text-gray-600">{{ content.created_at|date:"M d" }}</span>
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
<div class="flex min-h-screen bg-gray-950">
    <aside class="w-64 bg-gray-900 border-r border-gray-800 min-h-screen p-4">
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
    bg-violet-600/10 text-violet-400 text-sm font-medium">

<!-- Default item -->
<a class="flex items-center gap-3 px-3 py-2 rounded-lg
    text-gray-400 text-sm hover:bg-gray-800 hover:text-gray-200
    transition-all duration-200">
```

## View Toggle (card / list)

```html
<div class="flex items-center gap-1 bg-gray-800 rounded-lg p-0.5">
    <button data-view="cards"
        class="p-1.5 rounded-md text-gray-400 hover:text-white
        data-[active]:bg-gray-700 data-[active]:text-white transition-all duration-200">
    <button data-view="list"
        class="p-1.5 rounded-md text-gray-400 hover:text-white
        data-[active]:bg-gray-700 data-[active]:text-white transition-all duration-200">
</div>
```

The selected view preference is persisted via `localStorage`.

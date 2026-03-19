# Data Schema

## Models

### User (`users.CustomUser`)

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField | Primary key |
| `email` | EmailField | Unique, used as login credential |
| `first_name` | CharField | — |
| `last_name` | CharField | — |
| `password` | CharField | Hashed by Django |
| `is_active` | BooleanField | — |
| `created_at` | DateTimeField | Auto-set on creation |
| `updated_at` | DateTimeField | Auto-updated |

### Category (`categories.Category`)

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField | Primary key |
| `name` | CharField | Required |
| `description` | TextField | Optional |
| `user` | ForeignKey → User | User-scoped |
| `created_at` | DateTimeField | Auto-set on creation |
| `updated_at` | DateTimeField | Auto-updated |

### Tag (`tags.Tag`)

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField | Primary key |
| `name` | CharField | Unique per user |
| `user` | ForeignKey → User | User-scoped |
| `created_at` | DateTimeField | Auto-set on creation |
| `updated_at` | DateTimeField | Auto-updated |

### Content (`contents.Content`)

| Field | Type | Notes |
|---|---|---|
| `id` | AutoField | Primary key |
| `title` | CharField | Required |
| `url` | URLField | Optional |
| `content_type` | CharField | Choices — see below |
| `description` | TextField | Optional |
| `status` | CharField | Choices — see below |
| `preview_image_url` | URLField | Open Graph image URL |
| `file` | FileField | Optional local file upload |
| `user` | ForeignKey → User | Owner |
| `category` | ForeignKey → Category | Optional, null on category delete |
| `tags` | ManyToManyField → Tag | Via `ContentTags` junction |
| `created_at` | DateTimeField | Auto-set on creation |
| `updated_at` | DateTimeField | Auto-updated |

## Choices

### Content Types

```python
CONTENT_TYPE_CHOICES = [
    ('article', 'Article'),
    ('video', 'Video'),
    ('podcast', 'Podcast'),
    ('social_media_post', 'Social Media Post'),
    ('social_media_profile', 'Social Media Profile'),
    ('pdf', 'PDF'),
    ('course', 'Course'),
    ('other', 'Other'),
]
```

### Statuses

```python
STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]
```

## Relationships

```
User ──< Content         (one user → many contents)
User ──< Category        (one user → many categories)
User ──< Tag             (one user → many tags)
Content >──< Tag         (many-to-many via ContentTags)
Content >──o Category    (many contents → one optional category)
```

## Rules

- Every model must have `created_at` and `updated_at` fields
- Categories and tags are user-scoped — users only see their own
- Deleting a category sets `category` to `null` on its contents (no cascade delete)
- Deleting a tag removes it from all associated contents
- File uploads are stored via `FileField` in local media storage

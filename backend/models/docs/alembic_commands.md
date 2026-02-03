# Alembic Migration Commands

## Creating Migrations
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "migration message"

# Create empty migration manually
alembic revision -m "migration message"
```

**Note:** `import sqlmodel` is automatically included in all migrations via the template.

## Applying Migrations
```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade by specific number of versions
alembic upgrade +2

# Upgrade to specific revision
alembic upgrade <revision_id>
```

## Downgrading Migrations
```bash
# Downgrade one version
alembic downgrade -1

# Downgrade by specific number of versions
alembic downgrade -2

# Downgrade to specific revision
alembic downgrade <revision_id>

# Downgrade all the way back
alembic downgrade base
```

## Viewing Migration History
```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show verbose history with details
alembic history --verbose

# Show specific migration SQL
alembic show <revision_id>
```

## Workflow
1. Create or modify model in `models/` folder
2. Add table model import to `models/__init__.py` (if new model)
3. Run `alembic revision --autogenerate -m "description"`
4. Review generated file in `alembic/versions/`
5. Run `alembic upgrade head`
6. Check Supabase database to verify changes
DB aanmaken:

- pas de setting sqlalchemy.url in alembic.ini aan met de juiste database URL
- voer de volgende commando's uit om de initiële revisie aan te maken en toe te passen:
```bash
alembic revision -m "initinal"
```

Example
```python
def upgrade() -> None:
    """Upgrade schema: create persoon table."""
    op.create_table(
        "persoon",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("voornaam", sa.String(length=255), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema: drop persoon table."""
    op.drop_table("persoon")
```

```bash
alembic upgrade head
```

Nieuwe revisie aanmaken:
```bash
alembic revision -m "Beschrijving van de wijziging"
```

start de development server met reload:
```bash
uv run fastapi dev app/main.py --reload
```
>>>>>>> develop

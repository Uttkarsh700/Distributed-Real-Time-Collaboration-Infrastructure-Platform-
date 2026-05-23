# Scripts

This folder is reserved for automation scripts used during development, setup, maintenance, and future deployment workflows.

## Planned Uses

- Environment bootstrap scripts
- Local development helpers
- Build and deployment utilities
- Maintenance and cleanup helpers

## Seed Database Script

`seed_db.py` creates safe demo data for local development. It checks for existing demo records before creating new ones, so it can be run multiple times without duplicating the seed user, workspace, or project.

### Run it

```bash
cd backend
python ../scripts/seed_db.py
```

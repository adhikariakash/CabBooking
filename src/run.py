"""Implementation of the entry point."""
from src.models.models import db
from src.iam.login import main
db.create_all()
main().login_master(db)


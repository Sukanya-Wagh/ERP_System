from app import app, db
from models import Complaint

with app.app_context():
    c = Complaint.query.get(1)
    if c:
        print(f"Found complaint: id={c.id}, title={c.title}, submitted_by={c.submitted_by}")
        print(f"submitter: {c.submitter}")
        print(f"description: {c.description[:30]}")
        try:
            db.session.delete(c)
            db.session.commit()
            print("DELETE SUCCESS")
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            print(f"DELETE FAILED: {e}")
    else:
        print("Complaint #1 not found")
        all_c = Complaint.query.all()
        print(f"All complaints: {[(c.id, c.title) for c in all_c]}")

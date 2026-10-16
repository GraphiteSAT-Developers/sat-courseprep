"""The review queue: every missed question comes back until the student gets it right twice."""
from ..db import days_from_today, execute, now_iso, query

REVIEW_GAP_DAYS = 3


def mark_right(user_id, item_id):
    """Records a right answer on a review question. Returns its new state, or None if it's gone or cleared."""
    item = query("SELECT * FROM review_items WHERE id = ? AND user_id = ? AND cleared_at IS NULL", (item_id, user_id), one=True)
    if not item:
        return None
    count = item["right_count"] + 1
    if count >= 2:
        execute("UPDATE review_items SET right_count = ?, cleared_at = ? WHERE id = ?", (count, now_iso(), item_id))
        return {"id": item_id, "right_count": count, "cleared": True}
    due = days_from_today(REVIEW_GAP_DAYS)
    execute("UPDATE review_items SET right_count = ?, due_on = ? WHERE id = ?", (count, due, item_id))
    return {"id": item_id, "right_count": count, "cleared": False, "due_on": due}

"""Plans and prices, shared by the parent dashboard and the site build (so the preview shows the same prices).

They match the home page's pricing section. Yearly is ten months' price: two months free.
"""
PLANS = {
    "free": {"name": "Diagnostic", "blurb": "The full diagnostic and a study plan.", "month": 0, "year": 0},
    "daily": {"name": "Daily", "blurb": "Unlimited practice, daily sets and a new practice test every 3 weeks.", "month": 2400, "year": 24000},
    "coached": {"name": "Coached", "blurb": "Everything in Daily, plus a weekly check-in with a human coach.", "month": 11900, "year": 119000},
}
INTERVALS = ("month", "year")
PAUSE_DAYS = 30
ALERT_DAYS = (0, 2, 3, 5, 7)  # quiet days before a parent gets an inactivity alert; 0 turns alerts off

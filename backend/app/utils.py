from datetime import datetime

# Category importance weights
CATEGORY_WEIGHTS = {
    "Health": 5.0,
    "Documents": 4.5,
    "Finance": 4.0,
    "Subscriptions": 3.0,
    "Groceries": 2.5,
    "Vehicle": 2.5,
    "Memberships": 2.0,
    "Others": 1.5,
}


def calculate_urgency(category: str, expiry_date: datetime):
    """
    Urgency Score Formula:
    Score = weight / (days_remaining + 1)
    """

    days_remaining = (expiry_date - datetime.utcnow()).days

    # avoid division by negative or zero
    if days_remaining < 0:
        days_remaining = 0

    weight = CATEGORY_WEIGHTS.get(category, 2.0)

    return weight / (days_remaining + 1)

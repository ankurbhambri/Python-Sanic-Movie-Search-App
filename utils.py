from models import Users


def try_or(fn, default):
    try:
        return fn()
    except Exception:
        return default


async def user_isAdmin(user_id):
    user = await Users.filter(id=user_id).first()
    if user.is_admin:
        return True
    else:
        return False

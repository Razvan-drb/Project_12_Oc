def has_management_permission(user):
    return user.department == "management"

def has_sales_permission(user):
    return user.department == "sales"

def has_support_permission(user):
    return user.department == "support"

def can_access_client(user, client):
    if has_management_permission(user):
        return True
    elif has_sales_permission(user) and client.commercial_contact_id == user.id:
        return True
    return False

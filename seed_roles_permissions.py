# seed_roles_permissions.py

from backend.app import create_app, db
from backend.app.models import Role, Permission

app = create_app()
app.app_context().push()

def seed_data():
    # Define all roles
    roles = [
        'designer',
        'manufacturer',
        'retailer',
        'shopper',
        'creator',
        'government',
        'admin',
        'customer'
    ]

    for role_name in roles:
        if not Role.query.filter_by(role_name=role_name).first():
            db.session.add(Role(role_name=role_name))
    db.session.commit()

    # Define initial permissions (can be extended per module/system)
    permissions = [
        {'role_name': 'admin', 'system': 'dashboard', 'module_access': 'full'},
        {'role_name': 'designer', 'system': 'ai-tools', 'module_access': 'full'},
        {'role_name': 'manufacturer', 'system': 'production', 'module_access': 'predictive'},
        {'role_name': 'retailer', 'system': 'storefront', 'module_access': 'optimize'},
        {'role_name': 'shopper', 'system': 'shopping', 'module_access': 'personalized'},
        {'role_name': 'creator', 'system': 'collections', 'module_access': 'collaborate'},
        {'role_name': 'government', 'system': 'esg-dashboard', 'module_access': 'monitor'},
        {'role_name': 'customer', 'system': 'orders', 'module_access': 'read'}
    ]

    for perm in permissions:
        role = Role.query.filter_by(role_name=perm['role_name']).first()
        if role:
            exists = Permission.query.filter_by(
                role_id=role.id,
                system=perm['system'],
                module_access=perm['module_access']
            ).first()
            if not exists:
                db.session.add(Permission(
                    role_id=role.id,
                    system=perm['system'],
                    module_access=perm['module_access']
                ))
    db.session.commit()
    print("Seeding completed.")

if __name__ == '__main__':
    seed_data()

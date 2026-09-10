"""seed roles and permissions, migrate existing access to user_roles

Revision ID: 1635d497fbdc
Revises: d45e29049933
Create Date: 2026-09-09 21:38:46.013162

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision: str = '1635d497fbdc'
down_revision: Union[str, Sequence[str], None] = 'd45e29049933'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    roles_table = table(
        'roles',
        column('id', UUID(as_uuid=True)),
        column('name', sa.String),
    )
    permissions_table = table(
        'permissions',
        column('id', UUID(as_uuid=True)),
        column('name', sa.String),
    )
    role_permissions_table = table(
        'role_permissions',
        column('id', UUID(as_uuid=True)),
        column('role_id', UUID(as_uuid=True)),
        column('permission_id', UUID(as_uuid=True)),
    )
    user_roles_table = table(
        'user_roles',
        column('id', UUID(as_uuid=True)),
        column('user_id', UUID(as_uuid=True)),
        column('embedded_system_id', UUID(as_uuid=True)),
        column('role_id', UUID(as_uuid=True)),
    )

    # 1. Roller
    role_ids = {name: uuid.uuid4() for name in ["superadmin", "owner", "editor", "viewer"]}
    op.bulk_insert(roles_table, [
        {"id": rid, "name": name} for name, rid in role_ids.items()
    ])

    # 2. Yetkiler
    permission_ids = {name: uuid.uuid4() for name in ["view", "create", "update", "delete", "manage_access"]}
    op.bulk_insert(permissions_table, [
        {"id": pid, "name": name} for name, pid in permission_ids.items()
    ])

    # 3. Rol -> Yetki eşlemeleri
    role_permission_map = {
        "superadmin": ["view", "create", "update", "delete", "manage_access"],
        "owner": ["view", "create", "update", "delete", "manage_access"],
        "editor": ["view", "create", "update", "delete"],
        "viewer": ["view"],
    }
    role_permission_rows = []
    for role_name, permission_names in role_permission_map.items():
        for permission_name in permission_names:
            role_permission_rows.append({
                "id": uuid.uuid4(),
                "role_id": role_ids[role_name],
                "permission_id": permission_ids[permission_name],
            })
    op.bulk_insert(role_permissions_table, role_permission_rows)

    # 4. Mevcut verilerin user_roles'a taşınması
    connection = op.get_bind()

    # 4a. Superadmin kullanıcılar -> global rol (embedded_system_id = NULL)
    superadmin_users = connection.execute(
        sa.text("SELECT id FROM users WHERE is_superadmin = true")
    ).fetchall()
    superadmin_rows = [
        {"id": uuid.uuid4(), "user_id": row.id, "embedded_system_id": None, "role_id": role_ids["superadmin"]}
        for row in superadmin_users
    ]
    if superadmin_rows:
        op.bulk_insert(user_roles_table, superadmin_rows)

    # 4b. Owner'lar (her embedded_system için, mevcut owner_id'den)
    systems = connection.execute(
        sa.text("SELECT id, owner_id FROM embedded_systems")
    ).fetchall()
    owner_rows = [
        {"id": uuid.uuid4(), "user_id": row.owner_id, "embedded_system_id": row.id, "role_id": role_ids["owner"]}
        for row in systems
    ]
    if owner_rows:
        op.bulk_insert(user_roles_table, owner_rows)

    # 4c. Device Access kayıtları (editor/viewer)
    accesses = connection.execute(
        sa.text("SELECT user_id, embedded_system_id, access_level FROM device_access")
    ).fetchall()
    access_rows = [
        {
            "id": uuid.uuid4(),
            "user_id": row.user_id,
            "embedded_system_id": row.embedded_system_id,
            "role_id": role_ids[row.access_level],
        }
        for row in accesses
    ]
    if access_rows:
        op.bulk_insert(user_roles_table, access_rows)


def downgrade() -> None:
    op.execute("DELETE FROM user_roles")
    op.execute("DELETE FROM role_permissions")
    op.execute("DELETE FROM permissions")
    op.execute("DELETE FROM roles")

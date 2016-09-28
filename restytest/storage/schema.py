""" Database Schema """

import sqlalchemy as sa


metadata = sa.MetaData()

groups = sa.Table(
    'groups',
    metadata,
    sa.Column('id', sa.String(35), primary_key=True),
)

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.String(35), primary_key=True),
    sa.Column('first_name', sa.String(35)),
    sa.Column('last_name', sa.String(35)),
)

user_group_associations = sa.Table(
    'users_groups',
    metadata,
    sa.Column('group_id', sa.String(35),
              sa.ForeignKey('groups.id', ondelete='CASCADE')),
    sa.Column('user_id', sa.String(35),
              sa.ForeignKey('users.id', ondelete='CASCADE')),
)

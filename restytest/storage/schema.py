""" Database schema """

import sqlalchemy as sa


metadata = sa.MetaData()

groups = sa.Table(
    'groups',
    metadata,
    sa.Column('id', sa.String(35), primary_key=True),
)

# Feedback on original specification: Why first_name/last_name? Some people don't have both, some might end up having more.
# Wouldn't work so well internationally-speaking.
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
              sa.ForeignKey('groups.id', ondelete='CASCADE')), # Why ondelete='CASCADE'? What is this supposed to do? (Look it up)
    sa.Column('user_id', sa.String(35),
              sa.ForeignKey('users.id', ondelete='CASCADE')),
)

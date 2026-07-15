"""convert goal_questions category to fk

Revision ID: 1ec0ff055dc7
Revises: 7b113e122652
Create Date: 2026-07-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1ec0ff055dc7'
down_revision: Union[str, Sequence[str], None] = '7b113e122652'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('goal_questions', sa.Column('category_id', sa.Uuid(), nullable=True))
    op.execute(
        """
        UPDATE goal_questions gq
        SET category_id = c.id
        FROM categories c
        WHERE c.sort_order = gq.category
        """
    )
    op.drop_column('goal_questions', 'category')
    op.alter_column('goal_questions', 'category_id', new_column_name='category')
    op.create_index(op.f('ix_goal_questions_category'), 'goal_questions', ['category'], unique=False)
    op.create_foreign_key(
        op.f('fk_goal_questions_category_categories'),
        'goal_questions', 'categories', ['category'], ['id'], ondelete='SET NULL',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('fk_goal_questions_category_categories'), 'goal_questions', type_='foreignkey')
    op.drop_index(op.f('ix_goal_questions_category'), table_name='goal_questions')
    op.alter_column('goal_questions', 'category', new_column_name='category_id')
    op.add_column('goal_questions', sa.Column('category', sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE goal_questions gq
        SET category = c.sort_order
        FROM categories c
        WHERE c.id = gq.category_id
        """
    )
    op.drop_column('goal_questions', 'category_id')

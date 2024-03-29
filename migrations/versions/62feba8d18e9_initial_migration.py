"""initial_migration

Revision ID: 62feba8d18e9
Revises: 
Create Date: 2021-12-05 22:24:06.010724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62feba8d18e9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "patent",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patent_number", sa.String(length=8), nullable=False),
        sa.Column("patent_application_number", sa.String(length=10), nullable=False),
        sa.Column("assignee_entity_name", sa.String(length=150), nullable=True),
        sa.Column("filing_date", sa.DateTime(), nullable=True),
        sa.Column("grant_date", sa.DateTime(), nullable=True),
        sa.Column("invention_title", sa.String(length=200), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("patent")
    # ### end Alembic commands ###

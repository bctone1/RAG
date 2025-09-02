"""create initial tables"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "0001_create_initial_tables"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "file",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("original_name", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=50)),
        sa.Column("storage_path", sa.String(length=512), nullable=False),
        sa.Column(
            "uploaded_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_table(
        "document",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "file_id", sa.BigInteger(), sa.ForeignKey("file.id", ondelete="CASCADE")
        ),
        sa.Column("title", sa.String(length=255)),
        sa.Column("doc_meta", sa.JSON()),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_table(
        "chunk",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "document_id",
            sa.BigInteger(),
            sa.ForeignKey("document.id", ondelete="CASCADE"),
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("chunk_order", sa.Integer()),
        sa.Column("chunk_meta", sa.JSON()),
        sa.UniqueConstraint("document_id", "chunk_order", name="uq_chunk_document_order"),
    )
    op.create_table(
        "embedding",
        sa.Column(
            "chunk_id",
            sa.BigInteger(),
            sa.ForeignKey("chunk.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("vector", Vector(1536)),
        sa.Column("model", sa.String(length=100)),
        sa.Column("dim", sa.Integer()),
    )
    op.create_table(
        "chat_history",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_input", sa.Text(), nullable=False),
        sa.Column("llm_output", sa.Text()),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )


def downgrade() -> None:
    op.drop_table("chat_history")
    op.drop_table("embedding")
    op.drop_table("chunk")
    op.drop_table("document")
    op.drop_table("file")

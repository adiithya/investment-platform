
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio


def create_portfolio(
    db: Session,
    user_id: int,
    name: str,
    description: str | None = None,
) -> Portfolio:
    portfolio = Portfolio(
        user_id=user_id,
        name=name.strip(),
        description=description.strip() if description else None,
    )

    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    return portfolio


def get_user_portfolios(
    db: Session,
    user_id: int,
) -> list[Portfolio]:
    statement = (
        select(Portfolio)
        .where(Portfolio.user_id == user_id)
        .order_by(Portfolio.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_portfolio_by_id(
    db: Session,
    portfolio_id: int,
    user_id: int,
) -> Portfolio | None:
    statement = select(Portfolio).where(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == user_id,
    )

    return db.scalar(statement)


def update_portfolio(
    db: Session,
    portfolio: Portfolio,
    name: str | None = None,
    description: str | None = None,
) -> Portfolio:
    if name is not None:
        portfolio.name = name.strip()

    if description is not None:
        portfolio.description = description.strip() or None

    db.commit()
    db.refresh(portfolio)

    return portfolio


def delete_portfolio(
    db: Session,
    portfolio: Portfolio,
) -> None:
    db.delete(portfolio)
    db.commit()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse,
)
from app.services import portfolio_service

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"],
)


@router.post(
    "",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    return portfolio_service.create_portfolio(
        db=db,
        user_id=current_user.id,
        name=portfolio_data.name,
        description=portfolio_data.description,
    )


@router.get(
    "",
    response_model=list[PortfolioResponse],
)
def get_my_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    return portfolio_service.get_user_portfolios(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    portfolio = portfolio_service.get_portfolio_by_id(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    return portfolio


@router.patch(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    portfolio = portfolio_service.get_portfolio_by_id(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    update_data = portfolio_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided",
        )

    return portfolio_service.update_portfolio(
        db=db,
        portfolio=portfolio,
        **update_data,
    )


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    portfolio = portfolio_service.get_portfolio_by_id(
        db=db,
        portfolio_id=portfolio_id,
        user_id=current_user.id,
    )

    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    portfolio_service.delete_portfolio(
        db=db,
        portfolio=portfolio,
    )
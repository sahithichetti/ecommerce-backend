from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.wishlist import WishlistItem
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductResponse
from app.utils.auth import get_required_user

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])


@router.get("", response_model=list[ProductResponse])
def get_wishlist(current_user: User = Depends(get_required_user), db: Session = Depends(get_db)):
    items = db.query(WishlistItem).options(
        joinedload(WishlistItem.product).joinedload(Product.category)
    ).filter(WishlistItem.user_id == current_user.id).all()
    return [ProductResponse.model_validate(item.product) for item in items if item.product]


@router.post("")
def add_to_wishlist(
    product_id: int,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.product_id == product_id,
    ).first()
    if existing:
        return {"message": "Already in wishlist"}

    item = WishlistItem(user_id=current_user.id, product_id=product_id)
    db.add(item)
    db.commit()
    return {"message": "Added to wishlist"}


@router.delete("/{product_id}")
def remove_from_wishlist(
    product_id: int,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    item = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.product_id == product_id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in wishlist")

    db.delete(item)
    db.commit()
    return {"message": "Removed from wishlist"}

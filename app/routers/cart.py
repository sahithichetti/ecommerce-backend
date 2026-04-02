from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartItemResponse, CartResponse
from app.utils.auth import get_required_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
def get_cart(current_user: User = Depends(get_required_user), db: Session = Depends(get_db)):
    items = db.query(CartItem).options(
        joinedload(CartItem.product).joinedload(Product.category)
    ).filter(CartItem.user_id == current_user.id).all()

    total = sum(
        item.quantity * (item.product.discount_price or item.product.price)
        for item in items
    )
    return CartResponse(
        items=[CartItemResponse.model_validate(item) for item in items],
        total=round(total, 2),
    )


@router.post("", response_model=CartItemResponse)
def add_to_cart(
    data: CartItemCreate,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if already in cart
    existing = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == data.product_id,
    ).first()

    if existing:
        existing.quantity += data.quantity
        db.commit()
        db.refresh(existing)
        return CartItemResponse.model_validate(existing)

    item = CartItem(
        user_id=current_user.id,
        product_id=data.product_id,
        quantity=data.quantity,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    # Reload with product relationship
    item = db.query(CartItem).options(
        joinedload(CartItem.product)
    ).filter(CartItem.id == item.id).first()
    return CartItemResponse.model_validate(item)


@router.put("/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if data.quantity <= 0:
        db.delete(item)
        db.commit()
        return CartItemResponse(id=item_id, product_id=item.product_id, quantity=0)

    item.quantity = data.quantity
    db.commit()
    db.refresh(item)
    item = db.query(CartItem).options(
        joinedload(CartItem.product)
    ).filter(CartItem.id == item.id).first()
    return CartItemResponse.model_validate(item)


@router.delete("/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == current_user.id,
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}

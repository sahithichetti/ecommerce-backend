from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.auth import get_required_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse)
def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    # Get cart items
    cart_items = db.query(CartItem).options(
        joinedload(CartItem.product)
    ).filter(CartItem.user_id == current_user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate total
    total = sum(
        item.quantity * (item.product.discount_price or item.product.price)
        for item in cart_items
    )

    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=round(total, 2),
        shipping_address=data.shipping_address,
        payment_method=data.payment_method,
        status="confirmed",
    )
    db.add(order)
    db.flush()

    # Create order items
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.discount_price or cart_item.product.price,
        )
        db.add(order_item)

        # Reduce stock
        cart_item.product.stock = max(0, cart_item.product.stock - cart_item.quantity)

    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()

    db.commit()
    db.refresh(order)

    # Reload with items
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter(Order.id == order.id).first()

    return OrderResponse.model_validate(order)


@router.get("", response_model=list[OrderResponse])
def get_orders(current_user: User = Depends(get_required_user), db: Session = Depends(get_db)):
    orders = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
    return [OrderResponse.model_validate(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter(Order.id == order_id, Order.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse.model_validate(order)

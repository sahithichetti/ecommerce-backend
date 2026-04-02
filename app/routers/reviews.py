from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import Review
from app.models.product import Product
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse
from app.utils.auth import get_required_user

router = APIRouter(prefix="/api/products", tags=["Reviews"])


@router.get("/{product_id}/reviews", response_model=list[ReviewResponse])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).order_by(
        Review.created_at.desc()
    ).all()

    result = []
    for review in reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        data = ReviewResponse.model_validate(review)
        data.user_name = user.name if user else "Anonymous"
        result.append(data)
    return result


@router.post("/{product_id}/reviews", response_model=ReviewResponse)
def create_review(
    product_id: int,
    data: ReviewCreate,
    current_user: User = Depends(get_required_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")

    # Check if user already reviewed
    existing = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.product_id == product_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You already reviewed this product")

    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=data.rating,
        comment=data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    response = ReviewResponse.model_validate(review)
    response.user_name = current_user.name
    return response

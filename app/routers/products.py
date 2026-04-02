from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.database import get_db
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductResponse, ProductListResponse, CategoryResponse
import math

router = APIRouter(prefix="/api", tags=["Products & Categories"])


# ── Categories ──────────────────────────────────────────
@router.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [CategoryResponse.model_validate(c) for c in categories]


@router.get("/categories/{slug}/products", response_model=ProductListResponse)
def get_products_by_category(
    slug: str,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.slug == slug).first()
    if not category:
        return ProductListResponse(products=[], total=0, page=page, pages=0)

    query = db.query(Product).filter(Product.category_id == category.id)
    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 0
    products = query.options(joinedload(Product.category)).offset((page - 1) * limit).limit(limit).all()
    return ProductListResponse(
        products=[ProductResponse.model_validate(p) for p in products],
        total=total, page=page, pages=pages,
    )


# ── Products ────────────────────────────────────────────
@router.get("/products", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = "newest",  # newest, price_asc, price_desc, name
    db: Session = Depends(get_db),
):
    query = db.query(Product).options(joinedload(Product.category))

    # Search
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Category filter
    if category:
        cat = db.query(Category).filter(Category.slug == category).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)

    # Price filter
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Sorting
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "name":
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())

    total = query.count()
    pages = math.ceil(total / limit) if total > 0 else 0
    products = query.offset((page - 1) * limit).limit(limit).all()

    return ProductListResponse(
        products=[ProductResponse.model_validate(p) for p in products],
        total=total, page=page, pages=pages,
    )


@router.get("/products/featured", response_model=list[ProductResponse])
def get_featured_products(db: Session = Depends(get_db)):
    products = db.query(Product).options(joinedload(Product.category)).filter(
        Product.is_featured == True
    ).limit(8).all()
    return [ProductResponse.model_validate(p) for p in products]


@router.get("/products/best-sellers", response_model=list[ProductResponse])
def get_best_sellers(db: Session = Depends(get_db)):
    products = db.query(Product).options(joinedload(Product.category)).filter(
        Product.is_best_seller == True
    ).limit(8).all()
    return [ProductResponse.model_validate(p) for p in products]


@router.get("/products/latest", response_model=list[ProductResponse])
def get_latest_products(db: Session = Depends(get_db)):
    products = db.query(Product).options(joinedload(Product.category)).order_by(
        Product.created_at.desc()
    ).limit(8).all()
    return [ProductResponse.model_validate(p) for p in products]


@router.get("/products/deals", response_model=list[ProductResponse])
def get_deal_products(db: Session = Depends(get_db)):
    products = db.query(Product).options(joinedload(Product.category)).filter(
        Product.discount_price.isnot(None),
        Product.discount_price < Product.price,
    ).limit(12).all()
    return [ProductResponse.model_validate(p) for p in products]


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).options(joinedload(Product.category)).filter(
        Product.id == product_id
    ).first()
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.model_validate(product)

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, RoleChecker
from app.models.user import User
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
def list_products(
    only_active: bool = Query(True, description="Show only products available for sale"),
    db: Session = Depends(get_db)
):
    """
    Cash register and menu query: list all products available at the school.
    The iPad fetches this list on startup to display the cash register grid.
    """
    query = db.query(Product)
    if only_active:
        query = query.filter(Product.is_active == True)
    return query.order_by(Product.name.asc()).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details for a single product.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt mit ID {product_id} nicht gefunden."
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(RoleChecker(["admin"]))
):
    """
    Create a new product (e.g. "Water 0.5L" for 150 cents).
    Available to admins only.
    """
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(RoleChecker(["admin"]))
):
    """
    Update a product's name, price in cents, or active status.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt mit ID {product_id} nicht gefunden."
        )

    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", response_model=ProductResponse)
def deactivate_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(RoleChecker(["admin"]))
):
    """
    Deactivate a product ("soft delete") to preserve historical transaction logs
    while removing the product from the cash register grid.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produkt mit ID {product_id} nicht gefunden."
        )

    product.is_active = False
    db.commit()
    db.refresh(product)
    return product
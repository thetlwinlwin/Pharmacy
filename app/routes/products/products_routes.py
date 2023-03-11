from fastapi import APIRouter, Depends, status

from app.db.models import products
from app.schema import products_schema

products_router = APIRouter(
    prefix="/product",
    tags=["Products"],
)


# Products


@products_router.post(
    "/",
    description="Create products",
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    new_obj: products_schema.ProductCreate,
    product_service: products.ProductCrud = Depends(products.get_product_crud),
):
    product_service.create(new_obj)


@products_router.post(
    "/batch",
    description="Create products in bulk",
    status_code=status.HTTP_201_CREATED,
)
def create_products(
    new_objs: list[products_schema.ProductCreate],
    product_service: products.ProductCrud = Depends(products.get_product_crud),
):
    product_service.create_in_bulk(new_objs)


@products_router.get(
    "/name/all",
    description="get all product names",
    response_model=list[products_schema.ProductNames],
)
def get_all_product_names(
    product_service: products.ProductCrud = Depends(products.get_product_crud),
):
    return product_service.get_all_product_names()


@products_router.get(
    "/all",
    description="get all products",
    response_model=list[products_schema.ProductResponse],
)
def get_all_products(
    product_service: products.ProductCrud = Depends(products.get_product_crud),
):
    return product_service.get_all_products()


# @products_router.get(
#     "/{id}",
#     description="get product by id",
#     response_model=products_schema.ProductResponse,
# )
# def get_product_by_id(
#     id: int,
#     product_service: products.ProductCrud = Depends(products.get_product_crud),
# ):
#     return product_service.get_by_id(id)


@products_router.put(
    "/{id}",
    description="update product by id",
    status_code=status.HTTP_200_OK,
)
def update_product_by_id(
    id: int,
    new_obj: products_schema.ProductUpdate,
    product_service: products.ProductCrud = Depends(products.get_product_crud),
):
    product_service.update_by_id(id, new_obj)


@products_router.delete(
    "/{id}",
    description="Delete product by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_by_id(
    id: int,
    product_service: products.ProductCrud = Depends(products.get_product_crud),
):
    product_service.delete_by_id(id)


# Types


@products_router.post(
    "/types",
    description="Create product type",
    status_code=status.HTTP_201_CREATED,
)
def create_product_type(
    new_obj: products_schema.ProductTypeCreate,
    product_service: products.ProductTypeCrud = Depends(products.get_product_type_crud),
):
    product_service.create(new_obj)


@products_router.post(
    "/types/batch",
    description="Create product types in bulk",
    status_code=status.HTTP_201_CREATED,
)
def create_product_types(
    new_objs: list[products_schema.ProductTypeCreate],
    product_service: products.ProductTypeCrud = Depends(products.get_product_type_crud),
):
    product_service.create_in_bulk(new_objs)


@products_router.get(
    "/types/all",
    description="get all the names of product types",
    response_model=list[products_schema.ProductTypeResponse],
)
def get_all_product_type_name(
    product_service: products.ProductTypeCrud = Depends(products.get_product_type_crud),
):
    return product_service.get_all_product_types()


@products_router.put(
    "/types/{id}",
    description="update product type by id",
    status_code=status.HTTP_200_OK,
)
def update_product_type_by_id(
    id: int,
    new_obj: products_schema.ProductTypeCreate,
    product_service: products.ProductTypeCrud = Depends(products.get_product_type_crud),
):
    print("here")
    product_service.update_by_id(id, new_obj)


@products_router.delete(
    "/types/{id}",
    description="Delete product types by id",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_type_by_id(
    id: int,
    product_service: products.ProductTypeCrud = Depends(products.get_product_type_crud),
):
    product_service.delete_by_id(id)

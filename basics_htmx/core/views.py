from math import ceil

from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import Product

PRODUCTS_PER_PAGE = 3


def _read_page(value, default=1):
    try:
        return max(int(value), 1)
    except (TypeError, ValueError):
        return default


def _products_context(page=1):
    total = Product.objects.count()
    last_page = max(1, ceil(total / PRODUCTS_PER_PAGE))
    page = min(max(page, 1), last_page)
    return {
        "products": Product.objects.all()[: page * PRODUCTS_PER_PAGE],
        "total_products": total,
        "page": page,
        "next_page": page + 1,
        "has_more": total > page * PRODUCTS_PER_PAGE,
    }


@require_GET
def index(request):
    template = "partials/index-content.html" if request.headers.get("HX-Request") == "true" else "index.html"
    return render(request, template, _products_context())


@require_GET
def about(request):
    template = "partials/about-content.html" if request.headers.get("HX-Request") == "true" else "about.html"
    return render(request, template)


@require_GET
def products(request):
    context = _products_context(_read_page(request.GET.get("page"), default=2))
    template = "partials/products-region.html" if request.headers.get("HX-Request") == "true" else "products.html"
    return render(request, template, context)


@require_POST
def product_create(request):
    product_name = request.POST.get("product", "").strip()
    if not product_name:
        message = "Give your product a name before adding it."
    elif len(product_name) > 120:
        message = "Product names can be up to 120 characters."
    else:
        Product.objects.create(name=product_name)
        if request.headers.get("HX-Request") == "true":
            total = Product.objects.count()
            page = max(_read_page(request.POST.get("page")), ceil(total / PRODUCTS_PER_PAGE))
            context = _products_context(page)
            context["message"] = f'"{product_name}" is in your collection now.'
            return render(request, "partials/product-response.html", context)
        return redirect("index")

    if request.headers.get("HX-Request") == "true":
        return render(request, "partials/product-feedback.html", {"message": message})
    context = _products_context()
    context["form_error"] = message
    return render(request, "index.html", context, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Sum, Q, Avg
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from sierra_luxe.decorators import login_admin_required, admin_required
from sierra_luxe.utils import get_breadcrumbs
from catalog.models import Category, Product, ProductImage
from orders.models import Order
from users.models import User
from cart.models import Cart
from reviews.models import Review, Like

User = get_user_model()

def get_bool_from_post(request, field_name):
    """Helper to convert checkbox POST value to boolean"""
    return request.POST.get(field_name) == 'on'

def delete_model_instance(request, model_class, instance_id, redirect_url, name_field='name'):
    """Helper function for deleting model instances with consistent messaging"""
    instance = get_object_or_404(model_class, id=instance_id)
    instance_name = getattr(instance, name_field)
    instance.delete()
    messages.success(request, f'{model_class.__name__} "{instance_name}" deleted successfully.')
    return redirect(redirect_url)

@login_admin_required
def dashboard(request):
    """Admin dashboard home with statistics"""
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.filter(role='CUSTOMER').count()
    total_orders = Order.objects.count()
    
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]
    recent_users = User.objects.filter(role='CUSTOMER').order_by('-date_joined')[:5]
    low_stock_products = Product.objects.filter(stock__lt=10).order_by('stock')[:5]
    
    # Sales stats
    total_sales = Order.objects.filter(status__in=['SHIPPED', 'DELIVERED']).aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0')
    
    pending_orders = Order.objects.filter(status='PENDING').count()
    
    # Reviews and Likes stats
    total_reviews = Review.objects.count()
    approved_reviews = Review.objects.filter(is_approved=True).count()
    pending_reviews = Review.objects.filter(is_approved=False).count()
    total_likes = Like.objects.count()
    
    # Recent reviews
    recent_reviews = Review.objects.select_related('customer', 'product').filter(is_approved=True).order_by('-created_at')[:5]
    
    # Top rated products
    top_rated_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
    
    # Most liked products
    most_liked_products = Product.objects.annotate(
        like_count=Count('likes')
    ).filter(like_count__gt=0).order_by('-like_count')[:5]
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'low_stock_products': low_stock_products,
        'total_reviews': total_reviews,
        'approved_reviews': approved_reviews,
        'pending_reviews': pending_reviews,
        'total_likes': total_likes,
        'recent_reviews': recent_reviews,
        'top_rated_products': top_rated_products,
        'most_liked_products': most_liked_products,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', None, 'fas fa-tachometer-alt')
        ),
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

@login_admin_required
def product_list(request):
    """List all products with search and filter"""
    products = Product.objects.select_related('category').all()
    
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    status = request.GET.get('status')
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Products', None, 'fas fa-box')
        ),
    }
    return render(request, 'admin_dashboard/product_list.html', context)

@login_admin_required
def product_create(request):
    """Create new product"""
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price') or None
        stock = request.POST.get('stock', 0)
        sizes = request.POST.get('sizes', '')
        colors = request.POST.get('colors', '')
        material = request.POST.get('material', '')
        care_instructions = request.POST.get('care_instructions', '')
        main_image = request.FILES.get('main_image')
        video = request.POST.get('video', '')
        is_featured = get_bool_from_post(request, 'is_featured')
        is_active = get_bool_from_post(request, 'is_active')
        
        try:
            product = Product.objects.create(
                name=name,
                category_id=category_id,
                description=description,
                price=price,
                discount_price=discount_price,
                stock=stock,
                sizes=sizes,
                colors=colors,
                material=material,
                care_instructions=care_instructions,
                main_image=main_image,
                video=video,
                is_featured=is_featured,
                is_active=is_active
            )
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('admin_dashboard:product_images', product_id=product.id)
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    
    context = {
        'categories': categories,
        'action': 'Create',
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Products', reverse('admin_dashboard:product_list'), 'fas fa-box'),
            ('Create Product', None, 'fas fa-plus')
        ),
    }
    return render(request, 'admin_dashboard/product_form.html', context)

@login_admin_required
def product_edit(request, product_id):
    """Edit product"""
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.discount_price = request.POST.get('discount_price') or None
        product.stock = request.POST.get('stock', 0)
        product.sizes = request.POST.get('sizes', '')
        product.colors = request.POST.get('colors', '')
        product.material = request.POST.get('material', '')
        product.care_instructions = request.POST.get('care_instructions', '')
        main_image = request.FILES.get('main_image')
        video = request.POST.get('video', '')
        if main_image:
            product.main_image = main_image
        if video:
            product.video = video
        product.is_featured = get_bool_from_post(request, 'is_featured')
        product.is_active = get_bool_from_post(request, 'is_active')
        
        try:
            product.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('admin_dashboard:product_list')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    context = {
        'product': product,
        'categories': categories,
        'action': 'Edit',
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Products', reverse('admin_dashboard:product_list'), 'fas fa-box'),
            (f'Edit {product.name}', None, 'fas fa-edit')
        ),
    }
    return render(request, 'admin_dashboard/product_form.html', context)

@login_admin_required
@require_POST
def product_delete(request, product_id):
    """Delete product"""
    return delete_model_instance(request, Product, product_id, 'admin_dashboard:product_list')

@login_admin_required
@require_POST
def product_bulk_delete(request):
    """Bulk delete products"""
    product_ids = request.POST.getlist('product_ids')
    if product_ids:
        products = Product.objects.filter(id__in=product_ids)
        count = products.count()
        # Iterate through products to trigger custom delete method for Cloudinary cleanup
        for product in products:
            product.delete()
        messages.success(request, f'{count} product(s) deleted successfully.')
    else:
        messages.warning(request, 'No products selected for deletion.')
    return redirect('admin_dashboard:product_list')

@login_admin_required
def product_images(request, product_id):
    """Manage product images and video"""
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_images':
            image_files = request.FILES.getlist('images')
            is_primary = request.POST.get('is_primary') == 'on'
            
            if is_primary:
                product.images.update(is_primary=False)
            
            for image_file in image_files:
                ProductImage.objects.create(
                    product=product,
                    image=image_file,
                    is_primary=is_primary,
                    alt_text=request.POST.get('alt_text', '')
                )
            
            if is_primary and image_files:
                product.main_image = image_files[0]
                product.save()
            
            messages.success(request, f'{len(image_files)} image(s) added successfully.')
            
        elif action == 'update_video':
            video_url = request.POST.get('video', '')
            if video_url:
                product.video = video_url
                product.save()
                messages.success(request, 'Video updated successfully.')
            
        elif action == 'delete_image':
            image_id = request.POST.get('image_id')
            image = get_object_or_404(ProductImage, id=image_id, product=product)
            image.delete()
            messages.success(request, 'Image deleted successfully.')
            
        elif action == 'set_primary':
            image_id = request.POST.get('image_id')
            image = get_object_or_404(ProductImage, id=image_id, product=product)
            product.images.update(is_primary=False)
            image.is_primary = True
            image.save()
            product.main_image = image.image
            product.save()
            messages.success(request, 'Primary image updated successfully.')
            
        return redirect('admin_dashboard:product_images', product_id=product.id)
    
    context = {
        'product': product,
        'images': images,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Products', reverse('admin_dashboard:product_list'), 'fas fa-box'),
            (f'{product.name} - Images', None, 'fas fa-images')
        ),
    }
    return render(request, 'admin_dashboard/product_images.html', context)

@login_admin_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.annotate(product_count=Count('products'))
    context = {
        'categories': categories,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Categories', None, 'fas fa-tags')
        ),
    }
    return render(request, 'admin_dashboard/category_list.html', context)

@login_admin_required
def category_create(request):
    """Create category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        image = request.FILES.get('image')
        is_active = get_bool_from_post(request, 'is_active')
        
        try:
            category = Category.objects.create(
                name=name,
                description=description,
                image=image,
                is_active=is_active
            )
            messages.success(request, f'Category "{category.name}" created successfully.')
            return redirect('admin_dashboard:category_list')
        except Exception as e:
            messages.error(request, f'Error creating category: {str(e)}')
    
    context = {
        'action': 'Create',
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Categories', reverse('admin_dashboard:category_list'), 'fas fa-tags'),
            ('Create Category', None, 'fas fa-plus')
        ),
    }
    return render(request, 'admin_dashboard/category_form.html', context)

@login_admin_required
def category_edit(request, category_id):
    """Edit category"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description', '')
        image = request.FILES.get('image')
        if image:
            category.image = image
        category.is_active = get_bool_from_post(request, 'is_active')
        
        try:
            category.save()
            messages.success(request, f'Category "{category.name}" updated successfully.')
            return redirect('admin_dashboard:category_list')
        except Exception as e:
            messages.error(request, f'Error updating category: {str(e)}')
    
    context = {
        'category': category,
        'action': 'Edit',
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Categories', reverse('admin_dashboard:category_list'), 'fas fa-tags'),
            (f'Edit {category.name}', None, 'fas fa-edit')
        ),
    }
    return render(request, 'admin_dashboard/category_form.html', context)

@login_admin_required
@require_POST
def category_delete(request, category_id):
    """Delete category"""
    return delete_model_instance(request, Category, category_id, 'admin_dashboard:category_list')

def get_available_permissions():
    """Get permissions grouped by app for user management"""
    permissions = Permission.objects.select_related('content_type').all()
    grouped = {}
    for perm in permissions:
        app_label = perm.content_type.app_label
        if app_label not in grouped:
            grouped[app_label] = []
        grouped[app_label].append(perm)
    return grouped

@login_admin_required
def user_list(request):
    """List all users"""
    users = User.objects.all().order_by('-date_joined')
    
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    context = {
        'users': users,
        'role_choices': User.ROLE_CHOICES,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Users', None, 'fas fa-users')
        ),
    }
    return render(request, 'admin_dashboard/user_list.html', context)

@login_admin_required
def user_create(request):
    """Create new user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        role = request.POST.get('role', 'CUSTOMER')
        is_active = get_bool_from_post(request, 'is_active')
        is_staff = get_bool_from_post(request, 'is_staff')
        is_superuser = get_bool_from_post(request, 'is_superuser')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            
            # Assign selected permissions
            selected_perms = request.POST.getlist('permissions')
            if selected_perms:
                user.user_permissions.set(selected_perms)
            
            messages.success(request, f'User "{user.username}" created successfully.')
            return redirect('admin_dashboard:user_list')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    context = {
        'action': 'Create',
        'role_choices': User.ROLE_CHOICES,
        'permissions': get_available_permissions(),
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Users', reverse('admin_dashboard:user_list'), 'fas fa-users'),
            ('Create User', None, 'fas fa-plus')
        ),
    }
    return render(request, 'admin_dashboard/user_form.html', context)

@login_admin_required
def user_edit(request, user_id):
    """Edit user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.role = request.POST.get('role', 'CUSTOMER')
        user.is_active = get_bool_from_post(request, 'is_active')
        user.is_staff = get_bool_from_post(request, 'is_staff')
        user.is_superuser = get_bool_from_post(request, 'is_superuser')
        
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        
        try:
            user.save()
            
            # Update permissions
            selected_perms = request.POST.getlist('permissions')
            user.user_permissions.set(selected_perms)
            
            messages.success(request, f'User "{user.username}" updated successfully.')
            return redirect('admin_dashboard:user_list')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    context = {
        'user': user,
        'action': 'Edit',
        'role_choices': User.ROLE_CHOICES,
        'permissions': get_available_permissions(),
        'selected_permissions': set(user.user_permissions.values_list('id', flat=True)),
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Users', reverse('admin_dashboard:user_list'), 'fas fa-users'),
            (f'Edit {user.username}', None, 'fas fa-edit')
        ),
    }
    return render(request, 'admin_dashboard/user_form.html', context)

@login_admin_required
@require_POST
def user_delete(request, user_id):
    """Delete user"""
    return delete_model_instance(request, User, user_id, 'admin_dashboard:user_list', 'username')

@login_admin_required
def order_list(request):
    """List all orders"""
    orders = Order.objects.select_related('customer').order_by('-created_at')
    
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    search_query = request.GET.get('search')
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(customer__username__icontains=search_query) |
            Q(customer__email__icontains=search_query)
        )
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Orders', None, 'fas fa-shopping-bag')
        ),
    }
    return render(request, 'admin_dashboard/order_list.html', context)

@login_admin_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Orders', reverse('admin_dashboard:order_list'), 'fas fa-shopping-bag'),
            (f'Order #{order.order_number}', None, 'fas fa-file-invoice')
        ),
    }
    return render(request, 'admin_dashboard/order_detail.html', context)

@login_admin_required
@require_POST
def order_status_update(request, order_id):
    """Update order status"""
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f'Order #{order.order_number} status updated to {order.get_status_display()}.')
    else:
        messages.error(request, 'Invalid status.')
    
    return redirect('admin_dashboard:order_detail', order_id=order.id)


@login_admin_required
def featured_products(request):
    """Manage featured products"""
    featured = Product.objects.filter(is_featured=True, is_active=True).order_by('-created_at')
    all_products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'featured': featured,
        'all_products': all_products,
    }
    return render(request, 'admin_dashboard/featured_products.html', context)


@login_admin_required
@require_POST
def add_featured(request, product_id):
    """Add product to featured"""
    product = get_object_or_404(Product, id=product_id)
    
    if product.is_featured:
        messages.warning(request, f'{product.name} is already featured.')
    else:
        product.is_featured = True
        product.save()
        messages.success(request, f'{product.name} has been added to featured products.')
    
    return redirect('admin_dashboard:featured_products')


@login_admin_required
@require_POST
def remove_featured(request, product_id):
    """Remove product from featured"""
    product = get_object_or_404(Product, id=product_id)
    
    if not product.is_featured:
        messages.warning(request, f'{product.name} is not featured.')
    else:
        product.is_featured = False
        product.save()
        messages.success(request, f'{product.name} has been removed from featured products.')
    
    return redirect('admin_dashboard:featured_products')


# ============ REVIEWS MANAGEMENT ============

@login_admin_required
def review_list(request):
    """List all reviews with search and filter"""
    reviews = Review.objects.select_related('customer', 'product').all()
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        reviews = reviews.filter(
            Q(customer__username__icontains=search_query) |
            Q(product__name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(comment__icontains=search_query)
        )
    
    # Filter by product
    product_id = request.GET.get('product')
    if product_id:
        reviews = reviews.filter(product_id=product_id)
    
    # Filter by rating
    rating = request.GET.get('rating')
    if rating:
        reviews = reviews.filter(rating=rating)
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'approved':
        reviews = reviews.filter(is_approved=True)
    elif status == 'pending':
        reviews = reviews.filter(is_approved=False)
    
    # Pagination
    paginator = Paginator(reviews, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_reviews = Review.objects.count()
    approved_reviews = Review.objects.filter(is_approved=True).count()
    pending_reviews = Review.objects.filter(is_approved=False).count()
    
    context = {
        'page_obj': page_obj,
        'products': Product.objects.all(),
        'total_reviews': total_reviews,
        'approved_reviews': approved_reviews,
        'pending_reviews': pending_reviews,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Reviews', None, 'fas fa-star')
        ),
    }
    return render(request, 'admin_dashboard/review_list.html', context)


@login_admin_required
def review_detail(request, review_id):
    """View review details"""
    review = get_object_or_404(Review.objects.select_related('customer', 'product'), id=review_id)
    
    context = {
        'review': review,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Reviews', reverse('admin_dashboard:review_list'), 'fas fa-star'),
            ('Review Detail', None, 'fas fa-eye')
        ),
    }
    return render(request, 'admin_dashboard/review_detail.html', context)


@login_admin_required
@require_POST
def review_approve(request, review_id):
    """Approve a review"""
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()
    messages.success(request, f'Review by {review.customer.username} has been approved.')
    return redirect('admin_dashboard:review_list')


@login_admin_required
@require_POST
def review_reject(request, review_id):
    """Reject a review"""
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = False
    review.save()
    messages.success(request, f'Review by {review.customer.username} has been rejected.')
    return redirect('admin_dashboard:review_list')


@login_admin_required
@require_POST
def review_delete(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, 'Review deleted successfully.')
    return redirect('admin_dashboard:review_list')


@login_admin_required
@require_POST
def review_bulk_action(request):
    """Bulk action for reviews (approve, reject, delete)"""
    action = request.POST.get('action')
    review_ids = request.POST.getlist('review_ids')
    
    if not review_ids:
        messages.warning(request, 'No reviews selected.')
        return redirect('admin_dashboard:review_list')
    
    reviews = Review.objects.filter(id__in=review_ids)
    
    if action == 'approve':
        reviews.update(is_approved=True)
        messages.success(request, f'{reviews.count()} review(s) approved successfully.')
    elif action == 'reject':
        reviews.update(is_approved=False)
        messages.success(request, f'{reviews.count()} review(s) rejected successfully.')
    elif action == 'delete':
        count = reviews.count()
        reviews.delete()
        messages.success(request, f'{count} review(s) deleted successfully.')
    else:
        messages.error(request, 'Invalid action.')
    
    return redirect('admin_dashboard:review_list')


# ============ LIKES MANAGEMENT ============

@login_admin_required
def like_list(request):
    """List all likes with search and filter"""
    likes = Like.objects.select_related('user', 'product').all()
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        likes = likes.filter(
            Q(user__username__icontains=search_query) |
            Q(product__name__icontains=search_query)
        )
    
    # Filter by product
    product_id = request.GET.get('product')
    if product_id:
        likes = likes.filter(product_id=product_id)
    
    # Pagination
    paginator = Paginator(likes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_likes = Like.objects.count()
    
    context = {
        'page_obj': page_obj,
        'products': Product.objects.all(),
        'total_likes': total_likes,
        'breadcrumbs': get_breadcrumbs(
            ('Dashboard', reverse('admin_dashboard:dashboard'), 'fas fa-tachometer-alt'),
            ('Likes', None, 'fas fa-heart')
        ),
    }
    return render(request, 'admin_dashboard/like_list.html', context)


@login_admin_required
@require_POST
def like_delete(request, like_id):
    """Delete a like"""
    like = get_object_or_404(Like, id=like_id)
    like.delete()
    messages.success(request, 'Like deleted successfully.')
    return redirect('admin_dashboard:like_list')


@login_admin_required
@require_POST
def like_bulk_delete(request):
    """Bulk delete likes"""
    like_ids = request.POST.getlist('like_ids')
    
    if not like_ids:
        messages.warning(request, 'No likes selected.')
        return redirect('admin_dashboard:like_list')
    
    likes = Like.objects.filter(id__in=like_ids)
    count = likes.count()
    likes.delete()
    messages.success(request, f'{count} like(s) deleted successfully.')
    
    return redirect('admin_dashboard:like_list')

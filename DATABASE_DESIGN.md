# Sierra Luxe - Database Design & ERD

## Entity Relationship Diagram (ERD)

### Models Overview
1. **User** (Extended from Django's AbstractUser)
2. **UserProfile**
3. **Category**
4. **Product**
5. **ProductImage**
6. **Order**
7. **OrderItem**
8. **Review**
9. **Wishlist**

---

## Model Relationships

```
User (1) ----< (Many) Order
User (1) ----< (Many) Review
User (1) ----< (Many) Wishlist
User (1) ---- (1) UserProfile

Category (1) ----< (Many) Product

Product (1) ----< (Many) ProductImage
Product (1) ----< (Many) OrderItem
Product (1) ----< (Many) Review
Product (1) ----< (Many) Wishlist

Order (1) ----< (Many) OrderItem
```

---

## Detailed Model Specifications

### 1. User (Extended)
**App**: users  
**Inherits**: AbstractUser  
**Purpose**: Authentication and role-based access control

| Field | Type | Description |
|-------|------|-------------|
| username | CharField | Unique username |
| email | EmailField | User email |
| password | CharField | Hashed password |
| role | CharField | CUSTOMER or ADMIN |
| is_active | BooleanField | Account status |
| date_joined | DateTimeField | Registration date |

**Relationships**:
- One-to-One with UserProfile
- One-to-Many with Order
- One-to-Many with Review
- One-to-Many with Wishlist

---

### 2. UserProfile
**App**: users  
**Purpose**: Extended user information

| Field | Type | Description |
|-------|------|-------------|
| user | OneToOneField | Link to User |
| phone | CharField | Phone number |
| address | TextField | Shipping address |
| city | CharField | City |
| country | CharField | Country |
| postal_code | CharField | Postal/ZIP code |
| profile_image | ImageField | User avatar |

**Relationships**:
- One-to-One with User

---

### 3. Category
**App**: catalog  
**Purpose**: Product categorization

| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Category name (Women, Men, Kids) |
| slug | SlugField | URL-friendly name |
| description | TextField | Category description |
| image | ImageField | Category banner |
| is_active | BooleanField | Display status |
| created_at | DateTimeField | Creation date |

**Relationships**:
- One-to-Many with Product

---

### 4. Product
**App**: catalog  
**Purpose**: Product information

| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Product name |
| slug | SlugField | URL-friendly name |
| description | TextField | Product description |
| category | ForeignKey | Link to Category |
| price | DecimalField | Product price |
| discount_price | DecimalField | Sale price (optional) |
| stock | IntegerField | Available quantity |
| sizes | CharField | Available sizes (S,M,L,XL) |
| colors | CharField | Available colors |
| material | CharField | Fabric/material type |
| care_instructions | TextField | Care guide |
| is_featured | BooleanField | Featured product |
| is_active | BooleanField | Display status |
| created_at | DateTimeField | Creation date |
| updated_at | DateTimeField | Last update |

**Relationships**:
- Many-to-One with Category
- One-to-Many with ProductImage
- One-to-Many with OrderItem
- One-to-Many with Review
- One-to-Many with Wishlist

---

### 5. ProductImage
**App**: catalog  
**Purpose**: Multiple product images

| Field | Type | Description |
|-------|------|-------------|
| product | ForeignKey | Link to Product |
| image | ImageField | Product image |
| is_primary | BooleanField | Main display image |
| alt_text | CharField | Image description |
| created_at | DateTimeField | Upload date |

**Relationships**:
- Many-to-One with Product

---

### 6. Order
**App**: orders  
**Purpose**: Customer orders

| Field | Type | Description |
|-------|------|-------------|
| customer | ForeignKey | Link to User |
| order_number | CharField | Unique order ID |
| total_amount | DecimalField | Total price |
| status | CharField | PENDING/PROCESSING/SHIPPED/DELIVERED/CANCELLED |
| shipping_address | TextField | Delivery address |
| shipping_city | CharField | City |
| shipping_country | CharField | Country |
| shipping_postal_code | CharField | Postal code |
| phone | CharField | Contact number |
| notes | TextField | Order notes |
| created_at | DateTimeField | Order date |
| updated_at | DateTimeField | Last update |

**Relationships**:
- Many-to-One with User
- One-to-Many with OrderItem

---

### 7. OrderItem
**App**: orders  
**Purpose**: Individual items in an order

| Field | Type | Description |
|-------|------|-------------|
| order | ForeignKey | Link to Order |
| product | ForeignKey | Link to Product |
| quantity | IntegerField | Number of items |
| size | CharField | Selected size |
| color | CharField | Selected color |
| price | DecimalField | Price at purchase |
| subtotal | DecimalField | quantity × price |

**Relationships**:
- Many-to-One with Order
- Many-to-One with Product

---

### 8. Review
**App**: reviews  
**Purpose**: Product ratings and reviews

| Field | Type | Description |
|-------|------|-------------|
| product | ForeignKey | Link to Product |
| customer | ForeignKey | Link to User |
| rating | IntegerField | 1-5 stars |
| title | CharField | Review title |
| comment | TextField | Review text |
| is_verified_purchase | BooleanField | Purchased product |
| is_approved | BooleanField | Moderation status |
| created_at | DateTimeField | Review date |
| updated_at | DateTimeField | Last update |

**Relationships**:
- Many-to-One with Product
- Many-to-One with User

---

### 9. Wishlist
**App**: catalog  
**Purpose**: Saved items for later

| Field | Type | Description |
|-------|------|-------------|
| customer | ForeignKey | Link to User |
| product | ForeignKey | Link to Product |
| added_at | DateTimeField | Date added |

**Relationships**:
- Many-to-One with User
- Many-to-One with Product

**Unique Constraint**: (customer, product) - prevent duplicates

---

## Database Indexes
- User.email (unique)
- User.username (unique)
- Product.slug (unique)
- Category.slug (unique)
- Order.order_number (unique)
- Product.category (foreign key index)
- Order.customer (foreign key index)
- Review.product (foreign key index)

## Field Validations
- Email: Valid email format
- Phone: Valid phone format
- Price: Positive decimal (max 10 digits, 2 decimal places)
- Rating: Integer between 1-5
- Stock: Non-negative integer
- Postal codes: Alphanumeric

## Cascade Behaviors
- User deleted → UserProfile deleted (CASCADE)
- Category deleted → Products set to NULL (SET_NULL)
- Product deleted → OrderItems preserved (PROTECT)
- Product deleted → Reviews deleted (CASCADE)
- Product deleted → Wishlist items deleted (CASCADE)
- Order deleted → OrderItems deleted (CASCADE)

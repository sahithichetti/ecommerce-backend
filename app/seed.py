"""
Seed script to populate the database with sample data.
Run with: python -m app.seed
"""
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.review import Review
from app.utils.auth import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed():
    print("🌱 Seeding database...")

    # Clear existing data
    db.query(Review).delete()
    db.query(Product).delete()
    db.query(Category).delete()
    db.query(User).delete()
    db.commit()

    # ── Admin User ──────────────────────────────────────
    admin = User(
        name="Admin",
        email="admin@focopet.com",
        password_hash=hash_password("admin123"),
        role="admin",
    )
    db.add(admin)

    # ── Demo Customer ───────────────────────────────────
    customer = User(
        name="Keira Rodriguez",
        email="keira@example.com",
        password_hash=hash_password("customer123"),
        phone="+91 98765 43210",
        role="customer",
    )
    db.add(customer)
    db.commit()

    # ── Categories ──────────────────────────────────────
    categories_data = [
        {"name": "Dog", "slug": "dog", "description": "Premium food and accessories for your loyal companion", "image_url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400"},
        {"name": "Cat", "slug": "cat", "description": "Nutritious meals and fun toys for your feline friend", "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400"},
        {"name": "Bird", "slug": "bird", "description": "Seeds, feed, and cages for your feathered friends", "image_url": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400"},
        {"name": "Rabbit", "slug": "rabbit", "description": "Hay, pellets, and treats for your fluffy bunny", "image_url": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400"},
        {"name": "Fish", "slug": "fish", "description": "Fish food, tanks, and aquarium supplies", "image_url": "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=400"},
        {"name": "Reptile", "slug": "reptile", "description": "Specialized food and habitat supplies for reptiles", "image_url": "https://images.unsplash.com/photo-1504450874802-0ba2bcd659e3?w=400"},
    ]

    categories = {}
    for cat_data in categories_data:
        cat = Category(**cat_data)
        db.add(cat)
        db.flush()
        categories[cat_data["slug"]] = cat.id

    db.commit()
    print(f"  ✅ Created {len(categories)} categories")

    # ── Products ────────────────────────────────────────
    products_data = [
        # Dog Products
        {"name": "FocoPet Premium Dog Food - Salmon", "slug": "focopet-premium-dog-food-salmon", "description": "High-quality salmon-based dog food rich in Omega-3 fatty acids for a healthy coat and strong immune system. Made with real salmon as the first ingredient.", "price": 82.99, "discount_price": 69.99, "stock": 50, "category_id": categories["dog"], "is_featured": True, "is_best_seller": True, "image_url": "https://images.unsplash.com/photo-1568640347023-a616a30bc3bd?w=400"},
        {"name": "FocoPet Premium Dog Food - Chicken", "slug": "focopet-premium-dog-food-chicken", "description": "Wholesome chicken recipe packed with protein and essential nutrients. Perfect for active dogs who need sustained energy throughout the day.", "price": 32.99, "stock": 100, "category_id": categories["dog"], "is_featured": True, "image_url": "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400"},
        {"name": "FocoPet Premium Dog Food - Beef", "slug": "focopet-premium-dog-food-beef", "description": "Rich beef formula with added vegetables and vitamins. A complete and balanced meal for dogs of all sizes and life stages.", "price": 92.99, "discount_price": 79.99, "stock": 30, "category_id": categories["dog"], "is_featured": True, "image_url": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400"},
        {"name": "Organic Dog Treats - Peanut Butter", "slug": "organic-dog-treats-peanut-butter", "description": "Delicious organic peanut butter treats made with natural ingredients. No artificial colors, flavors, or preservatives.", "price": 18.99, "discount_price": 12.99, "stock": 200, "category_id": categories["dog"], "image_url": "https://images.unsplash.com/photo-1582798358481-d199fb7347bb?w=400"},
        {"name": "Dog Grooming Essentials Kit", "slug": "dog-grooming-essentials-kit", "description": "Complete grooming kit including brush, nail clipper, shampoo, and conditioner. Keep your furry friend looking their best.", "price": 45.99, "discount_price": 35.99, "stock": 40, "category_id": categories["dog"], "image_url": "https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?w=400"},
        {"name": "Interactive Dog Toy Bundle", "slug": "interactive-dog-toy-bundle", "description": "Set of 5 interactive toys including rope toys, squeakers, and puzzle feeders to keep your dog entertained for hours.", "price": 29.99, "stock": 80, "category_id": categories["dog"], "image_url": "https://images.unsplash.com/photo-1535294435445-d7249524ef2e?w=400"},
        {"name": "Premium Dog Harness - Adjustable", "slug": "premium-dog-harness-adjustable", "description": "Comfortable, adjustable no-pull harness with reflective strips for safe walks. Available in multiple sizes.", "price": 38.99, "stock": 60, "category_id": categories["dog"], "image_url": "https://images.unsplash.com/photo-1567612529009-afe25413cc54?w=400"},

        # Cat Products
        {"name": "Super Cat Premium Tuna Feast", "slug": "super-cat-premium-tuna-feast", "description": "Gourmet tuna recipe made with real fish. Rich in protein and essential nutrients for indoor and outdoor cats.", "price": 27.99, "discount_price": 22.99, "stock": 120, "category_id": categories["cat"], "is_featured": True, "is_best_seller": True, "image_url": "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400"},
        {"name": "Golden Paws Cat Salmon Delicacies", "slug": "golden-paws-cat-salmon-delicacies", "description": "Premium salmon cat food with added taurine for heart health. Grain-free formula for cats with sensitive stomachs.", "price": 34.99, "stock": 70, "category_id": categories["cat"], "is_best_seller": True, "image_url": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400"},
        {"name": "Cat Scratching Post Tower", "slug": "cat-scratching-post-tower", "description": "Multi-level scratching post with cozy perches, dangling toys, and sisal rope. Perfect for climbing and lounging.", "price": 89.99, "discount_price": 69.99, "stock": 25, "category_id": categories["cat"], "image_url": "https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=400"},
        {"name": "Interactive Cat Laser Toy", "slug": "interactive-cat-laser-toy", "description": "Automatic rotating laser toy that keeps your cat active and engaged. Multiple speed settings and auto-off timer.", "price": 24.99, "stock": 90, "category_id": categories["cat"], "image_url": "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=400"},
        {"name": "Premium Cat Litter - Clumping", "slug": "premium-cat-litter-clumping", "description": "Ultra-absorbent clumping cat litter with odor control technology. Dust-free formula for a cleaner home.", "price": 19.99, "discount_price": 15.99, "stock": 150, "category_id": categories["cat"], "image_url": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400"},

        # Bird Products
        {"name": "Premium Bird Seed Mix", "slug": "premium-bird-seed-mix", "description": "Nutritious blend of sunflower seeds, millet, and safflower for parakeets, finches, and canaries.", "price": 15.99, "stock": 200, "category_id": categories["bird"], "is_featured": True, "image_url": "https://images.unsplash.com/photo-1522926193341-e9ffd686c60f?w=400"},
        {"name": "Parrot Food - Tropical Mix", "slug": "parrot-food-tropical-mix", "description": "Specially formulated tropical fruit and nut mix for parrots and macaws. Rich in vitamins and minerals.", "price": 28.99, "discount_price": 23.99, "stock": 60, "category_id": categories["bird"], "is_best_seller": True, "image_url": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400"},
        {"name": "Spacious Bird Cage - Large", "slug": "spacious-bird-cage-large", "description": "Large cage with multiple perches, feeding cups, and easy-clean tray. Ideal for medium to large birds.", "price": 129.99, "discount_price": 99.99, "stock": 15, "category_id": categories["bird"], "image_url": "https://images.unsplash.com/photo-1520808663317-647b476a81b9?w=400"},

        # Rabbit Products
        {"name": "Timothy Hay Premium Bundle", "slug": "timothy-hay-premium-bundle", "description": "Fresh, hand-selected timothy hay. Essential fiber source for rabbits and guinea pigs. Sun-dried for maximum nutrition.", "price": 22.99, "stock": 100, "category_id": categories["rabbit"], "is_featured": True, "image_url": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400"},
        {"name": "Rabbit Pellet Food - Organic", "slug": "rabbit-pellet-food-organic", "description": "USDA organic rabbit pellets with added vitamins. No artificial ingredients, just pure nutrition for your bunny.", "price": 18.99, "discount_price": 14.99, "stock": 80, "category_id": categories["rabbit"], "image_url": "https://images.unsplash.com/photo-1535241749838-299277c6fc1e?w=400"},
        {"name": "Bunny Treat Variety Pack", "slug": "bunny-treat-variety-pack", "description": "Assorted dried fruit and vegetable treats. Includes apple, carrot, and banana chips your rabbit will love.", "price": 12.99, "stock": 150, "category_id": categories["rabbit"], "image_url": "https://images.unsplash.com/photo-1452857297128-d9c29adba80b?w=400"},

        # Fish Products
        {"name": "Tropical Fish Flakes - Premium", "slug": "tropical-fish-flakes-premium", "description": "Color-enhancing formula for tropical freshwater fish. Rich in vitamins and easily digestible for vibrant, healthy fish.", "price": 11.99, "stock": 250, "category_id": categories["fish"], "is_featured": True, "image_url": "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=400"},
        {"name": "Betta Fish Pellets", "slug": "betta-fish-pellets", "description": "Specially sized floating pellets for betta fish. High protein formula to support vibrant colors and active behavior.", "price": 8.99, "stock": 300, "category_id": categories["fish"], "image_url": "https://images.unsplash.com/photo-1520990547781-9c2e4c7e3b6d?w=400"},
        {"name": "Aquarium Starter Kit - 20 Gallon", "slug": "aquarium-starter-kit-20-gallon", "description": "Complete aquarium setup with filter, LED light, heater, and thermometer. Everything you need to start your fish-keeping journey.", "price": 159.99, "discount_price": 129.99, "stock": 10, "category_id": categories["fish"], "image_url": "https://images.unsplash.com/photo-1535591273668-578e31182c4f?w=400"},

        # Reptile Products
        {"name": "Reptile Calcium Supplement", "slug": "reptile-calcium-supplement", "description": "Essential calcium powder with vitamin D3 for healthy bone development. Suitable for all reptiles and amphibians.", "price": 14.99, "stock": 100, "category_id": categories["reptile"], "image_url": "https://images.unsplash.com/photo-1504450874802-0ba2bcd659e3?w=400"},
        {"name": "Freeze-Dried Crickets", "slug": "freeze-dried-crickets", "description": "High-protein freeze-dried crickets. Convenient and mess-free alternative to live insects for insectivorous reptiles.", "price": 16.99, "discount_price": 13.99, "stock": 180, "category_id": categories["reptile"], "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400"},
        {"name": "Reptile Heat Lamp Kit", "slug": "reptile-heat-lamp-kit", "description": "Complete basking lamp setup with adjustable fixture and UVB bulb. Provides essential heat and UV light for reptile health.", "price": 49.99, "discount_price": 39.99, "stock": 35, "category_id": categories["reptile"], "image_url": "https://images.unsplash.com/photo-1504450874802-0ba2bcd659e3?w=400"},
    ]

    for prod_data in products_data:
        product = Product(**prod_data)
        db.add(product)

    db.commit()
    print(f"  ✅ Created {len(products_data)} products")

    # ── Sample Reviews ──────────────────────────────────
    reviews_data = [
        {"user_id": customer.id, "product_id": 1, "rating": 5, "comment": "My golden retriever absolutely loves this salmon food! His coat is shinier than ever. Highly recommend!"},
        {"user_id": customer.id, "product_id": 2, "rating": 4, "comment": "Great quality chicken food. My dog enjoys every meal. Would love a larger bag option."},
        {"user_id": customer.id, "product_id": 8, "rating": 5, "comment": "My cats can't get enough of this tuna feast! They meow at me until I serve it. Five stars!"},
    ]

    for rev_data in reviews_data:
        review = Review(**rev_data)
        db.add(review)

    db.commit()
    print(f"  ✅ Created {len(reviews_data)} reviews")

    print("\n🎉 Database seeded successfully!")
    print(f"  Admin: admin@focopet.com / admin123")
    print(f"  Customer: keira@example.com / customer123")


if __name__ == "__main__":
    seed()
    db.close()

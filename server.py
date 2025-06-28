from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app) # Enable CORS for all origins, allowing your frontend to access this backend

# Mock Product Database with fixed data
PRODUCTS = [
{"id":1,"name":"iPhone 13","category":"phone","price":69999,"description":"Latest model with powerful chip and stunning display.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=iPhone"},
{"id":2,"name":"Redmi Note 12","category":"phone","price":17999,"description":"Budget-friendly smartphone with great features and long battery life.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Redmi"},
{"id":3,"name":"HP Laptop","category":"laptop","price":45999,"description":"Reliable laptop for everyday use, perfect for students and professionals.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=HP"},
{"id":4,"name":"Samsung Galaxy S22","category":"phone","price":59999,"description":"Flagship Android phone with stunning camera and powerful performance.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=SamG"},
{"id":5,"name":"Dell XPS 15","category":"laptop","price":120000,"description":"High-performance laptop for professionals, known for its sleek design and strong specs.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Dell"},
{"id":6,"name":"Sony WH-1000XM4","category":"headphones","price":24999,"description":"Industry-leading noise-canceling headphones for immersive audio.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Sony"},
{"id":7,"name":"Apple MacBook Air M1","category":"laptop","price":92999,"description":"Ultra-portable laptop with amazing battery life and silent operation.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Mac"},
{"id":8,"name":"Google Pixel 7","category":"phone","price":49999,"description":"Pure Android experience with a smart camera and seamless integration.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Pixl"},
{"id":9,"name":"JBL Flip 6","category":"speaker","price":8999,"description":"Portable Bluetooth speaker with rich sound and durable, waterproof design.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=JBL"},
{"id":10,"name":"Acer Aspire 5","category":"laptop","price":38999,"description":"Value-for-money laptop for students and everyday tasks.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Acer"},
{"id":11,"name":"OnePlus 10 Pro","category":"phone","price":66999,"description":"Fast and smooth smartphone experience with a great display and camera.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=OneP"},
{"id":12,"name":"Bose QuietComfort 45","category":"headphones","price":29999,"description":"Comfortable over-ear headphones with advanced noise cancellation.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Bose"},
{"id":13,"name":"Lenovo IdeaPad","category":"laptop","price":52999,"description":"Versatile laptop for work and entertainment, offering a balance of performance and portability.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Lenovo"},
{"id":14,"name":"Oppo Reno 8","category":"phone","price":28999,"description":"Sleek design and great photography features for capturing stunning moments.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Oppo"},
{"id":15,"name":"Marshall Stanmore II","category":"speaker","price":34999,"description":"Classic design with powerful, balanced audio, perfect for home use.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Mars"},
{"id":16,"name":"Asus ROG Zephyrus","category":"laptop","price":150000,"description":"High-end gaming laptop with powerful graphics and fast refresh rates.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Asus"},
{"id":17,"name":"Vivo V25 Pro","category":"phone","price":32999,"description":"Stylish phone with vibrant display and impressive camera capabilities.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Vivo"},
{"id":18,"name":"Sennheiser Momentum 3","category":"headphones","price":31999,"description":"Premium sound quality with comfortable fit and elegant design.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Senn"},
{"id":19,"name":"Microsoft Surface Laptop","category":"laptop","price":78999,"description":"Elegant design with touchscreen capabilities, ideal for productivity and creativity.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Surf"},
{"id":20,"name":"Realme GT Neo 3","category":"phone","price":26999,"description":"Gaming-focused phone with incredibly fast charging and smooth performance.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Real"},
{"id":21,"name":"Basmati Rice (1kg)","category":"grocery","price":129,"description":"Premium long-grain rice with a fragrant aroma, perfect for biryanis and pulao.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Rice"},
{"id":22,"name":"Extra Virgin Olive Oil (500ml)","category":"grocery","price":599,"description":"Cold-pressed olive oil rich in antioxidants, ideal for salads and cooking.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=OliveOil"},
{"id":23,"name":"Almonds (200g)","category":"grocery","price":299,"description":"Crunchy and nutritious almonds, great for snacking or adding to desserts.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Almonds"},
{"id":24,"name":"Whole Wheat Bread","category":"grocery","price":55,"description":"Healthy bread made from whole grains, free from artificial preservatives.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Bread"},
{"id":25,"name":"Greek Yogurt (200g)","category":"grocery","price":89,"description":"Creamy and protein-rich yogurt, perfect for smoothies or breakfast bowls.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Yogurt"},
{"id":26,"name":"Free-Range Eggs (6pcs)","category":"grocery","price":99,"description":"Farm-fresh eggs from free-range chickens, rich in omega-3.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Eggs"},
{"id":27,"name":"Organic Spinach (100g)","category":"grocery","price":49,"description":"Fresh, leafy greens packed with iron and vitamins.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Spinach"},
{"id":28,"name":"Dark Chocolate (85% Cocoa)","category":"grocery","price":149,"description":"Bitter-sweet chocolate with high cocoa content for a guilt-free treat.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Chocolate"},
{"id":29,"name":"Quinoa (500g)","category":"grocery","price":349,"description":"Protein-packed superfood, gluten-free and great for salads.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Quinoa"},
{"id":30,"name":"Organic Tomatoes (1kg)","category":"grocery","price":79,"description":"Juicy and flavorful tomatoes grown without synthetic pesticides.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Tomatoes"},
{"id":31,"name":"Himalayan Pink Salt (200g)","category":"grocery","price":129,"description":"Mineral-rich salt with a distinct flavor, sourced from the Himalayas.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=HimalayanSalt"},
{"id":32,"name":"Coconut Oil (500ml)","category":"grocery","price":249,"description":"Cold-pressed virgin oil for cooking, haircare, and skincare.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=CoconutOil"},
{"id":33,"name":"Green Tea Bags (25pcs)","category":"grocery","price":199,"description":"Antioxidant-rich tea for metabolism boost and relaxation.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=GreenTea"},
{"id":34,"name":"Fresh Strawberries (250g)","category":"grocery","price":179,"description":"Sweet and tangy berries, rich in vitamin C and fiber.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Strawberries"},
{"id":35,"name":"Peanut Butter (Crunchy, 500g)","category":"grocery","price":279,"description":"100% natural peanut butter with no added sugar or palm oil.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=PeanutButter"},
{"id":36,"name":"Oats (1kg)","category":"grocery","price":119,"description":"Whole grain oats for a fiber-rich breakfast or baking.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Oats"},
{"id":37,"name":"Avocados (2pcs)","category":"grocery","price":159,"description":"Creamy and nutrient-dense, perfect for toast or guacamole.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Avocado"},
{"id":38,"name":"Almond Milk (1L)","category":"grocery","price":189,"description":"Dairy-free milk alternative, low in calories and lactose-free.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=AlmondMilk"},
{"id":39,"name":"Whole Chicken (1kg)","category":"grocery","price":349,"description":"Farm-raised chicken, antibiotic-free and vacuum-packed for freshness.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Chicken"},
{"id":40,"name":"Organic Honey (500g)","category":"grocery","price":399,"description":"Pure, unfiltered honey with natural antibacterial properties.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Honey"},
{"id":41,"name":"Classic White T-Shirt","category":"clothing","price":599,"description":"100% cotton crew neck t-shirt, perfect for casual wear.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=White+T"},
{"id":42,"name":"Slim Fit Jeans","category":"clothing","price":1299,"description":"Stretch denim jeans with modern slim fit design.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Slim+Jeans"},
{"id":43,"name":"Hooded Sweatshirt","category":"clothing","price":899,"description":"Warm fleece-lined hoodie with front pocket.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Hoodie"},
{"id":44,"name":"Formal Dress Shirt","category":"clothing","price":799,"description":"Premium cotton dress shirt with button-down collar.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Dress+Shirt"},
{"id":45,"name":"Athletic Shorts","category":"clothing","price":499,"description":"Lightweight quick-dry shorts for sports and workouts.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Shorts"},
{"id":46,"name":"Winter Parka","category":"clothing","price":2999,"description":"Insulated waterproof jacket for extreme cold weather.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Parka"},
{"id":47,"name":"Silk Scarf","category":"clothing","price":699,"description":"Luxurious pure silk scarf with elegant print.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Scarf"},
{"id":48,"name":"Yoga Pants","category":"clothing","price":649,"description":"High-waisted stretchy leggings for yoga and exercise.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Yoga+Pants"},
{"id":49,"name":"Denim Jacket","category":"clothing","price":1499,"description":"Classic medium wash denim jacket with button front.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Denim+Jacket"},
{"id":50,"name":"Cashmere Sweater","category":"clothing","price":2499,"description":"Ultra-soft 100% cashmere crew neck sweater.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Cashmere"},
{"id":51,"name":"Linen Blouse","category":"clothing","price":899,"description":"Breathable linen blouse with button-down front.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Linen+Blouse"},
{"id":52,"name":"Cargo Pants","category":"clothing","price":1099,"description":"Utility pants with multiple pockets for storage.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Cargo+Pants"},
{"id":53,"name":"Leather Gloves","category":"clothing","price":1299,"description":"Genuine leather gloves with fleece lining.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Leather+Gloves"},
{"id":54,"name":"Swim Trunks","category":"clothing","price":599,"description":"Quick-dry swim shorts with built-in mesh lining.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Swim+Trunks"},
{"id":55,"name":"Wool Socks","category":"clothing","price":299,"description":"Warm merino wool socks for cold weather.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Wool+Socks"},
{"id":56,"name":"Trench Coat","category":"clothing","price":3499,"description":"Classic beige trench coat with belt and water-resistant finish.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Trench+Coat"},
{"id":57,"name":"Graphic Tee","category":"clothing","price":499,"description":"Cotton t-shirt with unique printed design.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Graphic+Tee"},
{"id":58,"name":"Pajama Set","category":"clothing","price":799,"description":"Comfortable cotton pajama set with button-up top.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Pajamas"},
{"id":59,"name":"Baseball Cap","category":"clothing","price":349,"description":"Adjustable cotton cap with curved brim.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Baseball+Cap"},
{"id":60,"name":"Evening Gown","category":"clothing","price":4999,"description":"Elegant floor-length gown for special occasions.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Evening+Gown"},
{"id":61,"name":"Ceramic Vase Set","category":"decoration","price":1299,"description":"Set of 3 handcrafted ceramic vases in neutral tones.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Ceramic+Vases"},
{"id":62,"name":"Wall Art Canvas","category":"decoration","price":1999,"description":"Modern abstract painting on high-quality canvas.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Wall+Art"},
{"id":63,"name":"Decorative Throw Pillow","category":"decoration","price":599,"description":"Soft velvet pillow with geometric pattern.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Throw+Pillow"},
{"id":64,"name":"Tabletop Fountain","category":"decoration","price":2499,"description":"Relaxing water fountain with LED lights.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Fountain"},
{"id":65,"name":"Crystal Candle Holders","category":"decoration","price":899,"description":"Set of 2 faceted glass candle holders.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Candle+Holders"},
{"id":66,"name":"Macrame Wall Hanging","category":"decoration","price":1299,"description":"Bohemian-style handwoven cotton wall decor.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Macrame"},
{"id":67,"name":"Decorative Bookends","category":"decoration","price":749,"description":"Marble-effect resin bookends with gold accents.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Bookends"},
{"id":68,"name":"Artificial Potted Plant","category":"decoration","price":499,"description":"Lifelike faux fiddle leaf fig tree in ceramic pot.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Faux+Plant"},
{"id":69,"name":"Mirrored Tray","category":"decoration","price":1099,"description":"Rectangular mirrored serving tray with handles.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Mirror+Tray"},
{"id":70,"name":"Decorative Bowl Set","category":"decoration","price":899,"description":"Set of 3 hammered metal decorative bowls.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Decorative+Bowls"},
{"id":71,"name":"Wall Clock","category":"decoration","price":1499,"description":"Minimalist round wall clock with wooden frame.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Wall+Clock"},
{"id":72,"name":"Glass Terrarium","category":"decoration","price":1799,"description":"Geometric glass terrarium for succulents or air plants.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Terrarium"},
{"id":73,"name":"Decorative Lantern","category":"decoration","price":699,"description":"Metal lantern with cut-out design for candles.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Lantern"},
{"id":74,"name":"Photo Display Shelf","category":"decoration","price":1199,"description":"Floating wooden shelf for displaying photos and small items.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Photo+Shelf"},
{"id":75,"name":"Decorative Figurines","category":"decoration","price":499,"description":"Set of 3 ceramic animal figurines.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Figurines"},
{"id":76,"name":"Wall Mirror","category":"decoration","price":2299,"description":"Round wall mirror with rustic wooden frame.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Wall+Mirror"},
{"id":77,"name":"Decorative Tray","category":"decoration","price":799,"description":"Marble-look serving tray with gold handles.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Marble+Tray"},
{"id":78,"name":"String Lights","category":"decoration","price":399,"description":"20-foot LED fairy lights with remote control.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Fairy+Lights"},
{"id":79,"name":"Decorative Plates","category":"decoration","price":999,"description":"Set of 3 hand-painted wall plates.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Decorative+Plates"},
{"id":80,"name":"Scented Candle Set","category":"decoration","price":899,"description":"Set of 3 soy wax candles in different fragrances.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Scented+Candles"},
{"id":81,"name":"Modern Sofa","category":"furniture","price":24999,"description":"3-seater contemporary sofa with wooden legs and premium fabric upholstery.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Modern+Sofa"},
{"id":82,"name":"Coffee Table","category":"furniture","price":8999,"description":"Rectangular wooden coffee table with tempered glass top.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Coffee+Table"},
{"id":83,"name":"Dining Table Set","category":"furniture","price":18999,"description":"6-seater dining table with matching chairs in walnut finish.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Dining+Set"},
{"id":84,"name":"Bookshelf","category":"furniture","price":7499,"description":"5-tier wooden bookshelf with adjustable shelves.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Bookshelf"},
{"id":85,"name":"King Size Bed","category":"furniture","price":22999,"description":"Solid wood king size bed frame with upholstered headboard.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=King+Bed"},
{"id":86,"name":"Study Desk","category":"furniture","price":6999,"description":"Ergonomic study desk with built-in drawers and cable management.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Study+Desk"},
{"id":87,"name":"Recliner Chair","category":"furniture","price":14999,"description":"Premium leather recliner with footrest and adjustable back.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Recliner"},
{"id":88,"name":"TV Cabinet","category":"furniture","price":10999,"description":"Modern TV stand with open shelves and closed storage compartments.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=TV+Cabinet"},
{"id":89,"name":"Wardrobe","category":"furniture","price":17999,"description":"3-door sliding wardrobe with mirror and internal drawers.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Wardrobe"},
{"id":90,"name":"Bar Stool","category":"furniture","price":3999,"description":"Adjustable height bar stool with cushioned seat and metal frame.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Bar+Stool"},
{"id":91,"name":"Console Table","category":"furniture","price":7999,"description":"Slim entryway table with drawer and lower shelf.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Console+Table"},
{"id":92,"name":"Lounge Chair","category":"furniture","price":12999,"description":"Mid-century modern lounge chair with walnut legs.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Lounge+Chair"},
{"id":93,"name":"Shoe Rack","category":"furniture","price":3499,"description":"5-tier shoe organizer with ventilated design.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Shoe+Rack"},
{"id":94,"name":"Dressing Table","category":"furniture","price":11999,"description":"Vanity table with large mirror and multiple storage compartments.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Dressing+Table"},
{"id":95,"name":"Office Chair","category":"furniture","price":8999,"description":"Ergonomic office chair with lumbar support and adjustable arms.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Office+Chair"},
{"id":96,"name":"Side Table","category":"furniture","price":4999,"description":"Nesting side tables set of 2 in matte black finish.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Side+Table"},
{"id":97,"name":"Bookshelf Chair","category":"furniture","price":15999,"description":"Combination chair and bookshelf in one innovative design.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Bookshelf+Chair"},
{"id":98,"name":"Futon Sofa","category":"furniture","price":13999,"description":"Convertible sofa that transforms into a guest bed.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Futon"},
{"id":99,"name":"Display Cabinet","category":"furniture","price":14999,"description":"Glass-front display cabinet with LED lighting.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Display+Cabinet"},
{"id":100,"name":"Accent Chair","category":"furniture","price":10999,"description":"Velvet upholstered accent chair with gold metal legs.","imageUrl":"https://placehold.co/60x60/random_hex/FFFFFF?text=Accent+Chair"}
 ]+ [
    {
        "id": i,
        "name": f"Product {i} Name",
        "category": random.choice(['Gadget', 'Accessory', 'Home Appliance', 'Wearable', 'Audio','decoration','clothing','furniture']),
        "price": round(random.uniform(1000, 50000), 2),
        "description": f"Detailed description for product {i}, highlighting its benefits and uses.",
        "imageUrl": f"https://placehold.co/60x60/random_hex/FFFFFF?text=P{i}"
    } for i in range(101, 106) # Adds enough products to exceed 100 easily, adjusted range
]

# --- RESTful API Endpoints ---

@app.route('/')
def home():
    """Home route for the server."""
    return "Mock E-commerce Inventory Backend is Running!"

@app.route('/products', methods=['GET'])
def get_all_products():
    """Returns all products in the inventory."""
    return jsonify(PRODUCTS)

@app.route('/products/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """Returns a single product by its ID."""
    try:
        # Assuming product IDs in PRODUCTS are integers
        product_id_int = int(product_id)
        product = next((p for p in PRODUCTS if p['id'] == product_id_int), None)
    except ValueError:
        # If product_id cannot be converted to an integer
        product = None 

    if product:
        return jsonify(product)
    return jsonify({'message': 'Product not found'}), 404

@app.route('/products/search', methods=['GET'])
def search_products():
    """Searches products based on a query parameter."""
    user_query = request.args.get('query', '').lower()
    print(f"Received search query: '{user_query}'") # Debugging print
    if not user_query:
        # Return all products if query is empty, or an error if preferred
        return jsonify(PRODUCTS) # Or jsonify({'message': 'Please provide a search query'}), 400

    # Split the query into keywords for a more flexible search
    keywords = user_query.split()

    results = []
    for p in PRODUCTS:
        # Combine relevant text fields for searching, using .get() for safety
        product_text = (p['name'] + " " + p.get('description', '') + " " + p['category']).lower()

        # Check if all keywords from the user's query are present in the product's combined text
        if all(keyword in product_text for keyword in keywords):
            results.append(p)
    
    print(f"Found {len(results)} results for query '{user_query}': {results}") # Debugging print
    time.sleep(0.5) # Simulate network delay
    return jsonify(results)

if __name__ == '__main__':
    # Run the Flask app on port 5000
    # In a production environment, you would use a more robust WSGI server like Gunicorn or uWSGI
    app.run(port=5000, debug=True)
from pathlib import Path
import shutil, zipfile, textwrap, json

base = Path("/mnt/data/amrushort-shop")
assets = base / "assets"
assets.mkdir(parents=True, exist_ok=True)

# Copy the three uploaded product images into the project.
srcs = [
    Path("/mnt/data/b49ea2ca-a0e8-4f75-a806-87b11477bd00.png"),
    Path("/mnt/data/9e2a2799-f1d5-4790-b47f-4bc1ff5902ab.png"),
    Path("/mnt/data/fb8e7503-962b-4ac6-993a-454d036de425.png"),
]
for i, src in enumerate(srcs, 1):
    shutil.copy2(src, assets / f"product-{i}.png")

index_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="AmruShop - modern online shopping store" />
  <title>AmruShop — Smart Shopping</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header class="topbar">
    <div class="container nav">
      <a class="brand" href="#"><span class="brand-mark">A</span> AmruShop</a>
      <div class="search-wrap">
        <span>⌕</span>
        <input id="searchInput" type="search" placeholder="Search products..." aria-label="Search products">
      </div>
      <button class="cart-btn" id="cartBtn" aria-label="Open cart">
        🛒 <span>Cart</span><b id="cartCount">0</b>
      </button>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="container hero-grid">
        <div>
          <span class="eyebrow">NEW • SMART AUDIO COLLECTION</span>
          <h1>Better sound.<br><span>Better everyday.</span></h1>
          <p>Discover stylish wireless earbuds and everyday tech at simple, transparent prices.</p>
          <a class="primary-btn" href="#products">Shop now <span>→</span></a>
        </div>
        <div class="hero-card">
          <div class="hero-glow"></div>
          <img src="assets/product-1.png" alt="Wireless earbuds" />
          <div class="floating-badge">⚡ Trending</div>
        </div>
      </div>
    </section>

    <section class="container categories">
      <button class="category active" data-category="All">All</button>
      <button class="category" data-category="Earbuds">Earbuds</button>
      <button class="category" data-category="Wireless Audio">Wireless Audio</button>
      <button class="category" data-category="Deals">Deals</button>
    </section>

    <section class="container products-section" id="products">
      <div class="section-head">
        <div>
          <span class="eyebrow">OUR PICKS</span>
          <h2>Popular products</h2>
        </div>
        <span id="resultCount" class="result-count"></span>
      </div>
      <div id="productGrid" class="product-grid"></div>
      <div id="emptyState" class="empty-state hidden">
        <div>🔎</div>
        <h3>No products found</h3>
        <p>Try another search or category.</p>
      </div>
    </section>

    <section class="trust">
      <div class="container trust-grid">
        <div><strong>🚚</strong><span><b>Fast delivery</b><small>Quick shipping options</small></span></div>
        <div><strong>🔒</strong><span><b>Secure checkout</b><small>Safe shopping experience</small></span></div>
        <div><strong>↩</strong><span><b>Easy returns</b><small>Simple return process</small></span></div>
        <div><strong>💬</strong><span><b>Support</b><small>We're here to help</small></span></div>
      </div>
    </section>
  </main>

  <div class="overlay hidden" id="overlay"></div>
  <aside class="cart-drawer" id="cartDrawer">
    <div class="drawer-head">
      <div><h2>Your cart</h2><span id="drawerCount">0 items</span></div>
      <button id="closeCart" class="icon-btn">×</button>
    </div>
    <div id="cartItems" class="cart-items"></div>
    <div class="cart-footer">
      <div class="subtotal"><span>Subtotal</span><strong id="cartTotal">₹0</strong></div>
      <button class="checkout-btn" id="checkoutBtn">Proceed to checkout</button>
      <p class="checkout-note">Checkout is a demo. Connect your payment/order backend later.</p>
    </div>
  </aside>

  <footer>
    <div class="container footer-inner">
      <span>© 2026 AmruShop</span>
      <span>Built for GitHub Pages</span>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>
"""

style_css = r"""*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#101114;--muted:#70747d;--line:#e8e9ec;--soft:#f5f6f8;--accent:#111;--white:#fff}
html{scroll-behavior:smooth}
body{font-family:Inter,Arial,sans-serif;color:var(--ink);background:#fff}
button,input{font:inherit}
button{cursor:pointer}
a{text-decoration:none;color:inherit}
.container{width:min(1180px,92%);margin:auto}
.topbar{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.9);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.nav{height:76px;display:flex;align-items:center;gap:28px}
.brand{font-size:21px;font-weight:800;display:flex;align-items:center;gap:10px;white-space:nowrap}
.brand-mark{width:34px;height:34px;border-radius:11px;background:#111;color:#fff;display:grid;place-items:center;font-size:16px}
.search-wrap{height:44px;max-width:520px;flex:1;margin:auto;display:flex;align-items:center;gap:10px;background:#f4f5f7;border:1px solid transparent;border-radius:13px;padding:0 14px;color:#8a8d94}
.search-wrap:focus-within{background:#fff;border-color:#d7d9dd}
.search-wrap input{border:0;outline:0;background:transparent;width:100%;font-size:14px}
.cart-btn{border:0;background:#111;color:#fff;border-radius:12px;height:44px;padding:0 15px;display:flex;align-items:center;gap:8px;font-weight:700}
.cart-btn b{min-width:21px;height:21px;border-radius:99px;background:#fff;color:#111;font-size:11px;display:grid;place-items:center}
.hero{background:#f5f5f2;padding:72px 0 62px;overflow:hidden}
.hero-grid{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:60px}
.eyebrow{font-size:11px;font-weight:800;letter-spacing:.16em;color:#73777e}
.hero h1{font-size:clamp(46px,6vw,78px);line-height:.98;letter-spacing:-.055em;margin:18px 0}
.hero h1 span{color:#777}
.hero p{max-width:510px;color:#646870;font-size:17px;line-height:1.7;margin-bottom:28px}
.primary-btn{display:inline-flex;gap:22px;align-items:center;background:#111;color:#fff;padding:15px 20px;border-radius:13px;font-weight:700}
.primary-btn span{font-size:20px}
.hero-card{height:420px;border-radius:34px;background:linear-gradient(135deg,#e8e8e4,#fff);position:relative;display:grid;place-items:center;box-shadow:inset 0 0 0 1px rgba(0,0,0,.04)}
.hero-card img{height:90%;max-width:90%;object-fit:contain;filter:drop-shadow(0 25px 25px rgba(0,0,0,.2));position:relative;z-index:2}
.hero-glow{position:absolute;width:260px;height:260px;background:#fff;border-radius:50%;filter:blur(35px)}
.floating-badge{position:absolute;right:22px;top:22px;background:#111;color:#fff;padding:10px 13px;border-radius:99px;font-size:12px;font-weight:700;z-index:3}
.categories{display:flex;gap:10px;padding:30px 0 10px;overflow:auto}
.category{border:1px solid var(--line);background:#fff;border-radius:99px;padding:10px 17px;color:#62666e;white-space:nowrap}
.category.active,.category:hover{background:#111;color:#fff;border-color:#111}
.products-section{padding:48px 0 80px}
.section-head{display:flex;align-items:end;justify-content:space-between;margin-bottom:24px}
.section-head h2{font-size:32px;letter-spacing:-.04em;margin-top:7px}
.result-count{font-size:13px;color:#8b8e95}
.product-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.product-card{border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff;transition:.25s;position:relative}
.product-card:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.08)}
.product-img{height:310px;background:#f5f6f7;display:grid;place-items:center;position:relative;padding:20px}
.product-img img{width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply}
.wish{position:absolute;right:14px;top:14px;width:36px;height:36px;border-radius:50%;border:1px solid var(--line);background:#fff}
.product-info{padding:19px}
.tag{display:inline-block;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:#777;margin-bottom:9px}
.product-info h3{font-size:17px;margin-bottom:7px}
.product-info p{font-size:13px;color:#777;line-height:1.5;min-height:39px}
.price-row{display:flex;align-items:center;justify-content:space-between;margin-top:16px;gap:12px}
.price{font-weight:800;font-size:18px}
.add-btn{border:0;background:#111;color:#fff;border-radius:10px;padding:11px 14px;font-size:12px;font-weight:700}
.view-btn{border:1px solid #ddd;background:#fff;color:#111;border-radius:10px;padding:11px 13px;font-size:12px;font-weight:700}
.actions{display:flex;gap:7px}
.trust{background:#f7f7f7;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.trust-grid{display:grid;grid-template-columns:repeat(4,1fr);padding:28px 0;gap:20px}
.trust-grid>div{display:flex;align-items:center;gap:13px}
.trust-grid strong{font-size:22px}
.trust-grid span{display:flex;flex-direction:column;gap:3px}
.trust-grid b{font-size:13px}.trust-grid small{font-size:11px;color:#858991}
footer{padding:24px 0;color:#858991;font-size:12px}
.footer-inner{display:flex;justify-content:space-between}
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.38);z-index:29}
.hidden{display:none!important}
.cart-drawer{position:fixed;z-index:30;right:0;top:0;height:100vh;width:min(430px,100%);background:#fff;transform:translateX(100%);transition:.3s;display:flex;flex-direction:column;box-shadow:-20px 0 60px rgba(0,0,0,.12)}
.cart-drawer.open{transform:translateX(0)}
.drawer-head{padding:25px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}
.drawer-head h2{font-size:21px}.drawer-head span{font-size:11px;color:#858991}
.icon-btn{border:0;background:#f3f4f5;border-radius:50%;width:36px;height:36px;font-size:24px}
.cart-items{padding:18px 22px;overflow:auto;flex:1}
.cart-item{display:grid;grid-template-columns:74px 1fr auto;gap:12px;align-items:center;padding:13px 0;border-bottom:1px solid var(--line)}
.cart-item img{width:74px;height:74px;object-fit:contain;background:#f4f5f6;border-radius:12px}
.cart-item h4{font-size:13px;margin-bottom:5px}.cart-item p{font-size:12px;color:#777}
.qty{display:flex;align-items:center;gap:7px;margin-top:9px}.qty button{border:1px solid #ddd;background:#fff;width:25px;height:25px;border-radius:7px}.qty span{font-size:12px}
.remove{border:0;background:transparent;color:#a1a3a8;font-size:18px}
.cart-footer{padding:20px 22px;border-top:1px solid var(--line)}
.subtotal{display:flex;justify-content:space-between;margin-bottom:14px}.subtotal strong{font-size:20px}
.checkout-btn{width:100%;border:0;background:#111;color:#fff;padding:15px;border-radius:12px;font-weight:700}
.checkout-note{text-align:center;font-size:10px;color:#9699a0;margin-top:10px}
.empty-state{text-align:center;padding:60px;color:#777}.empty-state div{font-size:34px;margin-bottom:10px}.empty-state h3{color:#111;margin-bottom:6px}
@media(max-width:800px){
 .nav{gap:10px}.brand{font-size:17px}.search-wrap{order:3;flex-basis:100%;max-width:none}.nav{height:auto;padding:12px 0;flex-wrap:wrap}.cart-btn span{display:none}
 .hero{padding:45px 0}.hero-grid{grid-template-columns:1fr;gap:35px}.hero-card{height:330px}.hero h1{font-size:52px}
 .product-grid{grid-template-columns:1fr 1fr}.product-img{height:250px}.trust-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:520px){
 .product-grid{grid-template-columns:1fr}.product-img{height:300px}.section-head h2{font-size:27px}.hero-card{height:300px}
 .trust-grid{grid-template-columns:1fr}.footer-inner{flex-direction:column;gap:8px}
}
"""

script_js = r"""// AmruShop product data.
// Replace `buyLink` with the real product-page URL when you have it.
const products = [
  {
    id: 1,
    name: "Premium Wireless Earbuds",
    category: "Earbuds",
    price: 999,
    image: "assets/product-1.png",
    description: "Modern black earbuds with a compact charging case.",
    buyLink: "https://rukminim1.flixcart.com/image/1536/1536/xif0q/headphone/a/t/k/-original-imahhdjmcezffgwc.jpeg?q=90"
  },
  {
    id: 2,
    name: "Classic White Wireless Earbuds",
    category: "Wireless Audio",
    price: 1499,
    image: "assets/product-2.png",
    description: "Clean white design for everyday listening.",
    buyLink: "https://rukminim1.flixcart.com/image/1536/1536/xif0q/headphone/1/z/k/-original-imah4jvftvzjn8zv.jpeg?q=90"
  },
  {
    id: 3,
    name: "boAt Style Wireless Earbuds",
    category: "Deals",
    price: 799,
    image: "assets/product-3.png",
    description: "Stylish black wireless earbuds with charging case.",
    buyLink: "https://rukminim1.flixcart.com/image/1536/1536/xif0q/headphone/z/r/n/-original-imahfczvrftznu58.jpeg?q=90"
  }
];

let cart = JSON.parse(localStorage.getItem("amruCart") || "[]");
let activeCategory = "All";

const grid = document.getElementById("productGrid");
const search = document.getElementById("searchInput");
const resultCount = document.getElementById("resultCount");
const emptyState = document.getElementById("emptyState");
const cartDrawer = document.getElementById("cartDrawer");
const overlay = document.getElementById("overlay");

function money(value) {
  return "₹" + value.toLocaleString("en-IN");
}

function saveCart() {
  localStorage.setItem("amruCart", JSON.stringify(cart));
  renderCart();
}

function filteredProducts() {
  const q = search.value.trim().toLowerCase();
  return products.filter(p => {
    const matchesCategory = activeCategory === "All" || p.category === activeCategory;
    const matchesSearch = !q || `${p.name} ${p.category} ${p.description}`.toLowerCase().includes(q);
    return matchesCategory && matchesSearch;
  });
}

function renderProducts() {
  const list = filteredProducts();
  resultCount.textContent = `${list.length} product${list.length !== 1 ? "s" : ""}`;
  emptyState.classList.toggle("hidden", list.length !== 0);
  grid.innerHTML = list.map(p => `
    <article class="product-card">
      <div class="product-img">
        <button class="wish" aria-label="Wishlist" onclick="this.textContent=this.textContent==='♡'?'♥':'♡'">♡</button>
        <img src="${p.image}" alt="${p.name}">
      </div>
      <div class="product-info">
        <span class="tag">${p.category}</span>
        <h3>${p.name}</h3>
        <p>${p.description}</p>
        <div class="price-row">
          <span class="price">${money(p.price)}</span>
          <div class="actions">
            <a class="view-btn" href="${p.buyLink}" target="_blank" rel="noopener">View</a>
            <button class="add-btn" onclick="addToCart(${p.id})">Add</button>
          </div>
        </div>
      </div>
    </article>
  `).join("");
}

function addToCart(id) {
  const existing = cart.find(i => i.id === id);
  if (existing) existing.qty += 1;
  else cart.push({ id, qty: 1 });
  saveCart();
  openCart();
}

function changeQty(id, amount) {
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.qty += amount;
  if (item.qty <= 0) cart = cart.filter(i => i.id !== id);
  saveCart();
}

function removeItem(id) {
  cart = cart.filter(i => i.id !== id);
  saveCart();
}

function renderCart() {
  const count = cart.reduce((sum, i) => sum + i.qty, 0);
  const total = cart.reduce((sum, i) => {
    const p = products.find(x => x.id === i.id);
    return sum + (p ? p.price * i.qty : 0);
  }, 0);

  document.getElementById("cartCount").textContent = count;
  document.getElementById("drawerCount").textContent = `${count} item${count !== 1 ? "s" : ""}`;
  document.getElementById("cartTotal").textContent = money(total);

  const box = document.getElementById("cartItems");
  if (!cart.length) {
    box.innerHTML = `<div class="empty-state"><div>🛒</div><h3>Your cart is empty</h3><p>Add something you like.</p></div>`;
    return;
  }

  box.innerHTML = cart.map(i => {
    const p = products.find(x => x.id === i.id);
    return `
      <div class="cart-item">
        <img src="${p.image}" alt="${p.name}">
        <div>
          <h4>${p.name}</h4>
          <p>${money(p.price)} each</p>
          <div class="qty">
            <button onclick="changeQty(${p.id}, -1)">−</button>
            <span>${i.qty}</span>
            <button onclick="changeQty(${p.id}, 1)">+</button>
          </div>
        </div>
        <button class="remove" onclick="removeItem(${p.id})" aria-label="Remove">×</button>
      </div>
    `;
  }).join("");
}

function openCart() {
  cartDrawer.classList.add("open");
  overlay.classList.remove("hidden");
}
function closeCart() {
  cartDrawer.classList.remove("open");
  overlay.classList.add("hidden");
}

document.querySelectorAll(".category").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".category").forEach(x => x.classList.remove("active"));
    btn.classList.add("active");
    activeCategory = btn.dataset.category;
    renderProducts();
  });
});

search.addEventListener("input", renderProducts);
document.getElementById("cartBtn").addEventListener("click", openCart);
document.getElementById("closeCart").addEventListener("click", closeCart);
overlay.addEventListener("click", closeCart);

document.getElementById("checkoutBtn").addEventListener("click", () => {
  if (!cart.length) return alert("Your cart is empty.");
  alert("Demo checkout: connect your payment/order backend here.");
});

renderProducts();
renderCart();
"""

readme = r"""# AmruShop

A responsive, static e-commerce shopping website built with HTML, CSS and JavaScript.

## Files

- `index.html` — main page
- `style.css` — design and responsive layout
- `script.js` — products, search, filters and cart
- `assets/` — product images

## Important: product links

The three URLs supplied initially are **image URLs**, so the `View` buttons currently open those image URLs.

When you have the actual product-page URLs, edit `script.js` and replace each `buyLink` value.

You can also change product names, prices, categories and descriptions in the same file.

## Run locally

Open `index.html` in a browser.

For the best local development experience, use VS Code + Live Server.

## GitHub Pages deployment

1. Create a new GitHub repository, for example `amrushort-shop`.
2. Upload `index.html`, `style.css`, `script.js`, `README.md` and the entire `assets` folder.
3. On GitHub, open **Settings → Pages**.
4. Under **Build and deployment**, select:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
5. Click Save.
6. Wait for GitHub Pages to publish the site.

Your site will normally be available at:

`https://YOUR-USERNAME.github.io/amrushort-shop/`

## If the repository is named YOUR-USERNAME.github.io

If you create a repository named exactly `YOUR-USERNAME.github.io`, your website can be served from:

`https://YOUR-USERNAME.github.io/`

## Before publishing

- Replace demo prices with your real prices.
- Replace the three `buyLink` values with actual product-page links.
- Replace `AmruShop` with your final store name if needed.
- For real orders/payments, connect a backend/payment provider; GitHub Pages alone is static hosting.
"""

# Add a simple .gitignore.
gitignore = """# OS / editor
.DS_Store
Thumbs.db
.vscode/
"""

for path, content in [
    (base/"index.html", index_html),
    (base/"style.css", style_css),
    (base/"script.js", script_js),
    (base/"README.md", readme),
    (base/".gitignore", gitignore),
]:
    path.write_text(content, encoding="utf-8")

zip_path = Path("/mnt/data/amrushort-shop-github-pages.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in base.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(base))

print(f"Created project: {base}")
print(f"ZIP: {zip_path}")
print("Files:", [str(p.relative_to(base)) for p in sorted(base.rglob("*")) if p.is_file()])

# ---------------------------------------------------------------
# Furniture Cost Calculator  |  Python Programming for Business Students
# A Streamlit website that helps a furniture store customer find the
# TOTAL price of an order (discounts, add-ons, delivery and GST)
# before visiting the store.
# Run with:  streamlit run app.py
# ---------------------------------------------------------------

import streamlit as st  # Streamlit turns our Python script into a website

# ---------------------------------------------------------------
# 1. STORE DATA (dictionaries store "name -> value" pairs)
# ---------------------------------------------------------------

STORE_NAME = "Urban Nest Furniture"   # change this to your own store name

# Base price (in rupees) of ONE piece of each furniture type
furniture_prices = {
    "Sofa (3-Seater)": 25000,
    "Double Bed": 30000,
    "Dining Table (6-Seater)": 22000,
    "Wardrobe": 18000,
    "Study Table": 8000,
    "Office Chair": 6000,
    "Bookshelf": 7500,
    "TV Unit": 9500,
}

# An emoji for each furniture type (used only to make the bill look nice)
furniture_icons = {
    "Sofa (3-Seater)": "🛋️", "Double Bed": "🛏️", "Dining Table (6-Seater)": "🍽️",
    "Wardrobe": "🚪", "Study Table": "📚", "Office Chair": "🪑",
    "Bookshelf": "📖", "TV Unit": "📺",
}

# Material multiplier: premium materials make the base price higher
material_multipliers = {
    "Engineered Wood": 1.0,   # standard price
    "Metal Frame": 1.2,       # 20% costlier
    "Sheesham Wood": 1.4,     # 40% costlier
    "Teak Wood": 1.8,         # 80% costlier
}

# Delivery options and their charges (in rupees)
delivery_charges = {
    "Store Pickup (Free)": 0,
    "Standard Delivery (3-5 days)": 1500,
    "Express Delivery (1-2 days)": 3000,
}

# Fixed business rules (constants are written in CAPITAL LETTERS)
ASSEMBLY_COST_PER_ITEM = 800      # fitting/assembly at home
WARRANTY_COST_PER_ITEM = 1000     # 2-year extended warranty
GST_RATE = 0.18                   # 18% GST on the final taxable amount
FREE_DELIVERY_LIMIT = 75000       # delivery is free above this amount


# ---------------------------------------------------------------
# 2. FUNCTION: does all the business calculation
# ---------------------------------------------------------------
def calculate_bill(item, material, quantity, customer, delivery, assembly, warranty):
    """Takes the customer's choices and returns a dictionary of all amounts."""

    # Price of one piece = base price x material multiplier
    unit_price = furniture_prices[item] * material_multipliers[material]

    # Base cost of the whole order
    base_cost = unit_price * quantity

    # Bulk discount: more pieces = bigger discount (if / elif / else)
    if quantity >= 10:
        bulk_discount_pct = 15
    elif quantity >= 5:
        bulk_discount_pct = 10
    elif quantity >= 3:
        bulk_discount_pct = 5
    else:
        bulk_discount_pct = 0

    # Customer-type discount (loyal customers and students save extra)
    if customer == "Loyalty Member":
        customer_discount_pct = 8
    elif customer == "Student":
        customer_discount_pct = 5
    else:
        customer_discount_pct = 0

    # Total discount = bulk + customer discount, applied on the base cost
    total_discount_pct = bulk_discount_pct + customer_discount_pct
    discount_amount = base_cost * total_discount_pct / 100
    cost_after_discount = base_cost - discount_amount

    # Optional add-ons are charged per piece (bool checkboxes decide)
    addon_cost = 0
    if assembly:
        addon_cost += ASSEMBLY_COST_PER_ITEM * quantity
    if warranty:
        addon_cost += WARRANTY_COST_PER_ITEM * quantity

    # Delivery is free if the discounted order is big enough
    if cost_after_discount >= FREE_DELIVERY_LIMIT:
        delivery_cost = 0
    else:
        delivery_cost = delivery_charges[delivery]

    # GST is charged on everything the customer pays for
    taxable_amount = cost_after_discount + addon_cost + delivery_cost
    gst = taxable_amount * GST_RATE
    total = taxable_amount + gst

    # Send all the numbers back as one dictionary
    return {
        "unit_price": unit_price,
        "base_cost": base_cost,
        "bulk_discount_pct": bulk_discount_pct,
        "customer_discount_pct": customer_discount_pct,
        "discount_amount": discount_amount,
        "cost_after_discount": cost_after_discount,
        "addon_cost": addon_cost,
        "delivery_cost": delivery_cost,
        "gst": gst,
        "total": total,
    }


# ---------------------------------------------------------------
# 3. LOOK AND FEEL (page settings + CSS styling)
# ---------------------------------------------------------------
st.set_page_config(page_title=f"{STORE_NAME} | Cost Calculator",
                   page_icon="🛋️", layout="wide")

# CSS = the "paint" of a website. Here we colour the banner, bill and total box.
st.markdown("""
<style>
#MainMenu, footer, .stDeployButton, [data-testid="stToolbar"] {visibility: hidden;}
.block-container {padding-top: 3.5rem; max-width: 1150px;}
button[data-testid="stBaseButton-primary"] {background: #6D4C41; border: none; color: #FFF8F0;
            font-weight: 600; padding: 0.7rem 1rem; border-radius: 12px;}
button[data-testid="stBaseButton-primary"]:hover {background: #4E342E; color: #FFCA28;}
.hero {background: linear-gradient(135deg, #3E2723 0%, #6D4C41 60%, #A1887F 100%);
       padding: 2.2rem 2.2rem; border-radius: 18px; margin-bottom: 1.4rem;
       box-shadow: 0 6px 18px rgba(62,39,35,0.25);}
.hero h1 {color: #FFF8F0; margin: 0; font-size: 2.3rem; line-height: 1.2;}
.hero p {color: #EBD9C8; margin: 0.5rem 0 0 0; font-size: 1.05rem;}
.hero .tag {display: inline-block; background: rgba(255,248,240,0.15); color: #FFF8F0;
            padding: 0.25rem 0.8rem; border-radius: 999px; font-size: 0.8rem;
            margin: 0.8rem 0.4rem 0 0;}
.bill-card {background: #FFFFFF; color: #2B2118; border-radius: 16px;
            padding: 1.4rem 1.6rem; border: 1px solid #E7DACB;
            box-shadow: 0 4px 14px rgba(62,39,35,0.12);}
.bill-card h3 {margin: 0 0 0.2rem 0; color: #3E2723; font-size: 1.25rem;}
.bill-card .sub {color: #7A6A5C; font-size: 0.92rem; margin-bottom: 0.8rem;}
.bill-row {display: flex; justify-content: space-between; padding: 0.6rem 0;
           border-bottom: 1px dashed #E0D2C2; font-size: 1rem;}
.bill-row.green span:last-child {color: #2E7D32; font-weight: 600;}
.total-box {background: #3E2723; border-radius: 16px; padding: 1.5rem 1.6rem;
            text-align: center; box-shadow: 0 6px 18px rgba(62,39,35,0.3);}
.total-box .label {color: #EBD9C8; font-size: 0.95rem; letter-spacing: 0.08em;
                   text-transform: uppercase;}
.total-box .amount {color: #FFCA28; font-size: 2.4rem; font-weight: 700; margin-top: 0.3rem;}
.badge {display: inline-block; background: #E8F5E9; color: #2E7D32; padding: 0.35rem 0.9rem;
        border-radius: 999px; font-size: 0.9rem; font-weight: 600; margin-top: 0.9rem;}
.price-row {display: flex; justify-content: space-between; padding: 0.35rem 0;
            border-bottom: 1px solid rgba(128,128,128,0.25); font-size: 0.92rem;}
</style>
""", unsafe_allow_html=True)

# Top banner (HTML inside Python)
st.markdown(f"""
<div class="hero">
<h1>🛋️ {STORE_NAME}</h1>
<p>Furniture Cost Calculator - know your exact price before you walk in.</p>
<span class="tag">✔ Instant total</span><span class="tag">✔ Bulk &amp; member discounts</span><span class="tag">✔ GST included</span>
</div>
""", unsafe_allow_html=True)

# Sidebar: a loop prints the price list so customers can compare
with st.sidebar:
    st.header("📋 Price List")
    st.caption("Base price per piece (Engineered Wood)")
    for name, price in furniture_prices.items():
        st.markdown(f'<div class="price-row"><span>{furniture_icons[name]} {name}</span>'
                    f'<b>₹{price:,}</b></div>', unsafe_allow_html=True)
    st.caption("Material changes the price: Metal x1.2, Sheesham x1.4, Teak x1.8")
    st.info("Buy 3+ pieces to unlock bulk discounts. Orders above ₹75,000 get free delivery!")

# ---------------------------------------------------------------
# 4. USER INPUTS (7 different widgets, grouped in two cards)
# ---------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("1️⃣ Choose your furniture")
        # Input 1 (str): furniture type from a dropdown
        item = st.selectbox("Furniture Type", list(furniture_prices.keys()))
        # Input 2 (str): material from a dropdown
        material = st.selectbox("Material", list(material_multipliers.keys()))
        # Input 3 (int): number of pieces (0 is allowed so we can show a warning)
        quantity = st.number_input("Quantity", min_value=0, max_value=100, value=1, step=1)
        # Live price preview for one piece (updates as the customer chooses)
        live_price = furniture_prices[item] * material_multipliers[material]
        st.caption(f"Price per piece: **₹{live_price:,.2f}**")

with col2:
    with st.container(border=True):
        st.subheader("2️⃣ Your details & services")
        # Input 4 (str): customer type for the discount
        customer = st.selectbox("Customer Type", ["Regular", "Student", "Loyalty Member"])
        # Input 5 (str): how the furniture reaches the customer
        delivery = st.radio("Delivery Option", list(delivery_charges.keys()))
        # Input 6 (bool): assembly service
        assembly = st.checkbox(f"🔧 Home Assembly (+₹{ASSEMBLY_COST_PER_ITEM}/piece)")
        # Input 7 (bool): extended warranty
        warranty = st.checkbox(f"🛡️ 2-Year Extended Warranty (+₹{WARRANTY_COST_PER_ITEM}/piece)")

# Big button that triggers the calculation
clicked = st.button("Calculate My Total", type="primary", use_container_width=True)

# ---------------------------------------------------------------
# 5. CALCULATE AND SHOW RESULT (with error handling)
# ---------------------------------------------------------------
if clicked:
    # Input validation: quantity must be at least 1
    if quantity <= 0:
        st.warning("Please enter a quantity of at least 1.")
    else:
        try:
            # Call our function with the customer's choices
            bill = calculate_bill(item, material, int(quantity), customer,
                                  delivery, assembly, warranty)

            # Tell the customer if delivery became free
            if bill["delivery_cost"] == 0 and delivery != "Store Pickup (Free)":
                delivery_text = "₹0.00 (free on large orders!)"
            else:
                delivery_text = f"₹{bill['delivery_cost']:,.2f}"

            # Each bill line = (label, value, css class). A loop turns them into HTML rows.
            lines = [
                ("Base cost", f"₹{bill['base_cost']:,.2f}", ""),
                (f"Discount ({bill['bulk_discount_pct']}% bulk + "
                 f"{bill['customer_discount_pct']}% customer)",
                 f"-₹{bill['discount_amount']:,.2f}", "green"),
                ("Add-ons (assembly / warranty)", f"₹{bill['addon_cost']:,.2f}", ""),
                ("Delivery", delivery_text, ""),
                ("GST (18%)", f"₹{bill['gst']:,.2f}", ""),
            ]
            rows_html = ""
            for label, value, style in lines:
                rows_html += (f'<div class="bill-row {style}"><span>{label}</span>'
                              f'<span>{value}</span></div>')

            st.markdown("### 🧾 Your Bill")
            left, right = st.columns([3, 2])

            with left:
                st.markdown(
                    f'<div class="bill-card"><h3>{furniture_icons[item]} {item}</h3>'
                    f'<div class="sub">{material} &middot; ₹{bill["unit_price"]:,.2f} each '
                    f'&times; {int(quantity)} piece(s)</div>{rows_html}</div>',
                    unsafe_allow_html=True)

            with right:
                # Final amount in a big dark box
                st.markdown(
                    f'<div class="total-box"><div class="label">Total Amount Payable</div>'
                    f'<div class="amount">₹{bill["total"]:,.2f}</div></div>',
                    unsafe_allow_html=True)
                # Show a savings badge only if the customer actually got a discount
                if bill["discount_amount"] > 0:
                    st.markdown(f'<span class="badge">🎉 You saved ₹{bill["discount_amount"]:,.2f}</span>',
                                unsafe_allow_html=True)
                else:
                    st.caption("Tip: buy 3 or more pieces to unlock a bulk discount.")

        except Exception as error:
            # If anything unexpected happens, show a friendly message (no crash)
            st.error(f"Sorry, something went wrong: {error}")

st.caption(f"© {STORE_NAME} · Prices are for estimation only · Built with Python & Streamlit")

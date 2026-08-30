import re

import pandas as pd
import streamlit as st

from scraper import scrape_product

from database import (
    DATABASE_NAME,
    create_database,
    save_product,
    save_price,
    get_products,
    get_latest_price
)

from alerts import (
    check_price_drop,
    calculate_savings
)


# ==========================================
# FUNCTIONS
# ==========================================

def extract_price(price_text):
    """Convert price text into a numeric value."""

    if not price_text:
        return None

    match = re.search(
        r"\d+(?:,\d{3})*(?:\.\d+)?",
        price_text
    )

    if match:
        return float(
            match.group(0).replace(",", "")
        )

    return None


def get_all_price_history():
    """Load all product price history."""

    connection = None

    try:
        connection = __import__("sqlite3").connect(
            str(DATABASE_NAME)
        )

        query = """
            SELECT
                products.name AS product,
                price_history.price AS price,
                price_history.recorded_at AS recorded_at
            FROM price_history
            JOIN products
            ON price_history.product_id = products.id
            ORDER BY price_history.recorded_at ASC
        """

        dataframe = pd.read_sql_query(
            query,
            connection
        )

        return dataframe

    finally:
        if connection:
            connection.close()


def check_all_products():
    """Check the latest price for every tracked product."""

    products = get_products()

    results = []

    for product in products:

        product_id = product[0]
        product_name = product[1]
        product_url = product[2]

        try:

            product_data = scrape_product(
                product_url
            )

            current_price = extract_price(
                product_data["price"]
            )

            if current_price is None:
                continue

            save_price(
                product_id,
                current_price
            )

            results.append(
                {
                    "name": product_name,
                    "price": current_price
                }
            )

        except Exception as error:

            results.append(
                {
                    "name": product_name,
                    "price": None,
                    "error": str(error)
                }
            )

    return results


# ==========================================
# DATABASE
# ==========================================

create_database()


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="E-Commerce Price Tracker",
    page_icon="🛒",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("🛒 E-Commerce Price Tracker")

st.caption(
    "Automated product price monitoring with "
    "price history and email alerts."
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🛒 Price Tracker")

st.sidebar.subheader("Add Product")

product_url = st.sidebar.text_input(
    "Product URL",
    placeholder="Paste product URL..."
)

target_price = st.sidebar.number_input(
    "Target Price (£)",
    min_value=0.01,
    value=40.00,
    step=1.00
)


if st.sidebar.button(
    "➕ Track Product",
    use_container_width=True
):

    if not product_url:

        st.sidebar.error(
            "Please enter a product URL."
        )

    else:

        with st.spinner(
            "Fetching product information..."
        ):

            try:

                product = scrape_product(
                    product_url
                )

                price = extract_price(
                    product["price"]
                )

                if price is None:

                    st.sidebar.error(
                        "Could not find product price."
                    )

                else:

                    product_id = save_product(
                        product["name"],
                        product["url"],
                        target_price
                    )

                    if product_id is not None:

                        save_price(
                            product_id,
                            price
                        )

                        st.sidebar.success(
                            "Product tracked successfully!"
                        )

                        st.rerun()

                    else:

                        st.sidebar.error(
                            "Could not save product."
                        )

            except Exception as error:

                st.sidebar.error(
                    f"Error: {error}"
                )


st.sidebar.divider()

st.sidebar.info(
    "💡 The scheduler can automatically "
    "check prices every hour."
)


# ==========================================
# LOAD DATA
# ==========================================

products = get_products()

history = get_all_price_history()


# ==========================================
# TOP METRICS
# ==========================================

total_products = len(products)

total_records = len(history)

current_prices = []

for product in products:

    latest = get_latest_price(
        product[0]
    )

    if latest is not None:
        current_prices.append(latest)


if current_prices:

    lowest_price = min(current_prices)

else:

    lowest_price = None


metric1, metric2, metric3 = st.columns(3)


with metric1:

    st.metric(
        "📦 Tracked Products",
        total_products
    )


with metric2:

    st.metric(
        "📊 Price Records",
        total_records
    )


with metric3:

    if lowest_price is not None:

        st.metric(
            "💰 Lowest Current Price",
            f"£{lowest_price:.2f}"
        )

    else:

        st.metric(
            "💰 Lowest Current Price",
            "—"
        )


st.divider()


# ==========================================
# MANUAL PRICE CHECK
# ==========================================

check_col1, check_col2 = st.columns(
    [4, 1]
)

with check_col1:

    st.subheader(
        "🔄 Price Monitoring"
    )

    st.write(
        "Manually check all tracked products "
        "for the latest prices."
    )


with check_col2:

    if st.button(
        "🔄 Check Prices",
        use_container_width=True
    ):

        with st.spinner(
            "Checking prices..."
        ):

            results = check_all_products()

        if results:

            st.success(
                "Price check completed!"
            )

            for result in results:

                if result["price"] is not None:

                    st.write(
                        f"**{result['name']}** — "
                        f"£{result['price']:.2f}"
                    )

                elif "error" in result:

                    st.error(
                        f"{result['name']}: "
                        f"{result['error']}"
                    )

        st.rerun()


st.divider()


# ==========================================
# PRODUCT CARDS
# ==========================================

st.subheader("🛍️ Your Products")


if products:

    for product in products:

        product_id = product[0]
        product_name = product[1]
        product_url = product[2]
        target = product[3]
        alert_sent = product[4]

        current_price = get_latest_price(
            product_id
        )

        with st.container(
            border=True
        ):

            st.markdown(
                f"### 🛒 {product_name}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                if current_price is not None:

                    st.metric(
                        "Current Price",
                        f"£{current_price:.2f}"
                    )

                else:

                    st.metric(
                        "Current Price",
                        "—"
                    )

            with col2:

                st.metric(
                    "Target Price",
                    f"£{target:.2f}"
                )

            with col3:

                if current_price is not None:

                    difference = (
                        current_price - target
                    )

                    if difference <= 0:

                        st.metric(
                            "Status",
                            "🎉 Target Reached"
                        )

                    else:

                        st.metric(
                            "Above Target",
                            f"£{difference:.2f}"
                        )

                else:

                    st.metric(
                        "Status",
                        "Waiting"
                    )

            if current_price is not None:

                if check_price_drop(
                    current_price,
                    target
                ):

                    savings = calculate_savings(
                        current_price,
                        target
                    )

                    st.success(
                        f"🎉 Target price reached! "
                        f"Save up to £{max(savings, 0):.2f}."
                    )

                else:

                    difference = (
                        current_price - target
                    )

                    st.info(
                        f"£{difference:.2f} "
                        "above your target price."
                    )

            if alert_sent:

                st.caption(
                    "📧 Price alert has already been sent."
                )

            else:

                st.caption(
                    "🔔 Alert is active."
                )

            st.link_button(
                "🔗 Open Product",
                product_url
            )

else:

    st.info(
        "No products tracked yet. "
        "Add one using the sidebar."
    )


st.divider()


# ==========================================
# PRICE HISTORY
# ==========================================

st.subheader("📈 Price History")


if not history.empty:

    selected_product = st.selectbox(
        "Select product",
        history["product"].unique()
    )

    product_history = history[
        history["product"] == selected_product
    ].copy()

    product_history["recorded_at"] = pd.to_datetime(
        product_history["recorded_at"]
    )

    st.line_chart(
        product_history.set_index(
            "recorded_at"
        )["price"]
    )

    st.dataframe(
        product_history,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Price history will appear here "
        "after products are checked."
    )


st.divider()


# ==========================================
# FOOTER
# ==========================================

st.caption(
    "E-Commerce Price Tracker • "
    "Python • Streamlit • SQLite • "
    "Web Scraping • Email Alerts"
)
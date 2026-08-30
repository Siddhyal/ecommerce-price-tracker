import re

from scraper import scrape_product

from database import (
    create_database,
    get_products,
    save_price,
    set_alert_sent
)

from alerts import (
    check_price_drop,
    send_price_alert
)


def extract_price(price_text):
    """Convert price text into a numeric value."""

    if not price_text:
        return None

    match = re.search(
        r"\d+(?:,\d{3})*(?:\.\d+)?",
        price_text
    )

    if match:
        number = match.group(0).replace(",", "")
        return float(number)

    return None


def check_all_products(receiver_email):
    """Check all products and send alerts only once per price drop."""

    create_database()

    products = get_products()

    if not products:
        print("No products are being tracked.")
        return

    print("\n================================")
    print("     PRICE CHECK STARTED")
    print("================================")

    for product in products:

        product_id = product[0]
        product_name = product[1]
        product_url = product[2]
        target_price = product[3]
        alert_sent = product[4]

        print(f"\nChecking: {product_name}")

        try:

            product_data = scrape_product(
                product_url
            )

            current_price = extract_price(
                product_data["price"]
            )

            if current_price is None:

                print("❌ Price could not be found.")
                continue

            save_price(
                product_id,
                current_price
            )

            print(
                f"Current Price: £{current_price:.2f}"
            )

            print(
                f"Target Price: £{target_price:.2f}"
            )

            # ==========================
            # TARGET PRICE REACHED
            # ==========================

            if check_price_drop(
                current_price,
                target_price
            ):

                print(
                    "🎯 Target price reached!"
                )

                # Send email only if we haven't
                # already sent one
                if alert_sent == 0:

                    try:

                        send_price_alert(
                            product_name,
                            current_price,
                            target_price,
                            receiver_email
                        )

                        set_alert_sent(
                            product_id,
                            1
                        )

                        print(
                            "📧 Email alert sent!"
                        )

                    except Exception as email_error:

                        print(
                            f"❌ Email failed: "
                            f"{email_error}"
                        )

                else:

                    print(
                        "📧 Alert already sent. "
                        "No duplicate email."
                    )

            # ==========================
            # PRICE ABOVE TARGET
            # ==========================

            else:

                print(
                    "Price is above target."
                )

                # Reset alert so that if the
                # price drops again later,
                # another email can be sent.
                if alert_sent == 1:

                    set_alert_sent(
                        product_id,
                        0
                    )

                    print(
                        "🔄 Alert reset."
                    )

        except Exception as error:

            print(
                f"❌ Error checking product: "
                f"{error}"
            )

    print("\n================================")
    print("     PRICE CHECK FINISHED")
    print("================================")


if __name__ == "__main__":

    receiver = input(
        "Enter email for price alerts: "
    )

    check_all_products(
        receiver
    )
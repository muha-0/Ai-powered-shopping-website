from http.server import BaseHTTPRequestHandler, HTTPServer
import re
from datetime import datetime

orders = [
    {
        "id": 0,
        "Status": "Delivered",
        "Quantity": "1",
        "Cost": "50.00$",
        "From": "Ahmed Sameh",
        "Address": "SURPRISHIP INC\n123 TECH PARK BLVD STE 500\nMINNEAPOLIS MN 55401",
        "Products": "Cereal",
        "SurpriShip Product": "Milk",
        "Order Time": datetime.now().isoformat(),
        "Shipping": "Ground",
        "Notes": "Left at front door as requested",
    },
    {
        "id": 1,
        "Status": "Shipped",
        "Quantity": "1",
        "Cost": "75.00$",
        "From": "Daniel Kluver",
        "Address": "7420 WASHINGTON AVE APT 3B\nSAINT PAUL MN 55102",
        "Products": "Pencil Eraser",
        "SurpriShip Product": "Notebook",
        "Order Time": datetime.now().isoformat(),
        "Shipping": "Ground",
        "Notes": "",
    },
    {
        "id": 2,
        "Status": "Shipped",
        "Quantity": "1",
        "Cost": "100.00$",
        "From": "Justin Yun",
        "Address": "85 RIVERSIDE DR FL 2\nALLENTOWN PA 18104",
        "Products": "Monitor Mouse Mouse Pad",
        "SurpriShip Product": "Keyboard",
        "Order Time": datetime.now().isoformat(),
        "Shipping": "Ground",
        "Notes": "",
    },
        {
        "id": 3,
        "Status": "Delivered",
        "Quantity": "1",
        "Cost": "50.00$",
        "From": "Mr. X",
        "Address": "SURPRISHIP INC\n123 COMO PARK BLVD STE 500\nMINNEAPOLIS MN 55445",
        "Products": "Burger",
        "SurpriShip Product": "Fries",
        "Order Time": datetime.now().isoformat(),
        "Shipping": "Ground",
        "Notes": "Sorry I lost it in the way",
    }
]

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.


def escape_html(s):
    s = s.replace("&", "&amp;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&#39;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    # you need more.

    return s


def unescape_url(url_str):
    import urllib.parse

    # NOTE -- this is the only place urllib is allowed on this assignment.
    return urllib.parse.unquote_plus(url_str)


def parse_query_parameters(query: str) -> dict:
    params = {}

    if not query:
        return params  

    if query.startswith("?"):
        query = query[1:]

    
    pairs = query.split("&")
    for pair in pairs:
        if "=" in pair:
            key, value = pair.split("=", 1)
            key = unescape_url(key)
            value = unescape_url(value)
            params[key] = value
        else:
            params[unescape_url(pair)] = "" 

    return params  

def render_tracking(order):
    order_id = escape_html(str(order['id']))
    product = escape_html(order['Products'])
    status = escape_html(order['Status'])
    cost = escape_html(order['Cost'])
    address = escape_html(order['Address'])
    shipping = escape_html(order['Shipping'])
    order_time = escape_html(order['Order Time'])
    quantity = escape_html(order['Quantity'])
    # Status text
    if status == "Placed":
        main_msg = "Your Order is Placed"
        sec_msg = "Confirmed and will ship soon!"
    elif status == "Shipped":
        main_msg = "Your Order is Being Shipped"
        sec_msg = "On its way!"
    elif status == "Cancelled":
        main_msg = "Your Order has Been Cancelled"
        sec_msg = "This order will not be processed further."
    else:
        main_msg = "Your Order was Delivered"
        sec_msg = "Go grab it!"

    # because buttons shouldn't be visible for anything else
    show_actions = status == "Placed"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Knewave&display=swap" rel="stylesheet">
        <script src="/js/update.js" defer></script>
        <link rel="stylesheet" href="/main.css">
        <title>SurpriShip</title>
    </head>
    <body>
        <header>
            <a href="/about">About</a>
            <a href="/admin/orders">Orders (Admin Only)</a>
            <a href="/order">Place Order</a>
        </header>

        <div class="main-container">
            <nav>
            </nav>
            <main>
                <h1>Order Tracking</h1>
                <div class = "sub-tracking-container">
                    <div class = "tracking-left-container">
                        

                        <section class="status-box">
                            <h2>{main_msg}</h2>
                            <p>{sec_msg}</p>
                        </section>

                        <section class="details-box">
                            <h3>Order Details</h3>
                            <table class="order-details">
                                <tr><td><strong>Order ID:</strong></td><td>{order_id}</td></tr>
                                <tr><td><strong>Product:</strong></td><td>{product}</td></tr>
                                <tr><td><strong>Status:</strong></td><td>{status}</td></tr>
                                <tr><td><strong>Cost:</strong></td><td>{cost}</td></tr>
                                <tr><td><strong>Shipping:</strong></td><td>{shipping}</td></tr>
                                <tr><td><strong>Address:</strong></td><td>{address}</td></tr>
                                <tr><td><strong>Order Time:</strong></td><td id="order-time">{order_time}</td></tr>
                                <tr><td><strong>Quantity:</strong></td><td>{quantity}</td></tr>
                            </table>
                        </section>
                    </div>
                    <div class = "tracking-right-container">
                        <section class="status-box">
                            <h2>Order Management</h2>
                            {"<p id='countdown'></p>" if show_actions else "<p>Order was Cancelled</p>" if status == "Cancelled" else "<p>Order already Shipped</p>"}
                        </section>
                        {f"""
                        <h1>You can't update or cancel your order</h1>
                         """
                        if not show_actions else
                        f"""
                        <section class='details-box'>
                            <form action='/cancel_order' method='POST' style = 'display:inline;'>
                                <input type='hidden' name='id' value='{order_id}'>
                                <button type='submit'>Cancel Order</button>
                            </form>

                            <button id='toggle-update'>Update Shipping</button>

                            <form id='update-form' action='/update_shipping' method='POST' style='display:none;'>
                                <input type='hidden' name='id' value='{order_id}'>
                                <label for='address'>New Address:</label>
                                <textarea id='address' name='address' required></textarea>
                                <div class='shipping-options'>
                                    <label><input type='radio' name='shipping' value='Flat Rate' checked> Flat Rate</label>
                                    <label><input type='radio' name='shipping' value='Ground'> Ground</label>
                                    <label><input type='radio' name='shipping' value='Expedited'> Expedited</label>
                                </div>
                                <button type='submit'>Confirm Update</button>
                            </form>
                        </section>
                        """}
                    </div>
                </div>
            </main>
            <aside>
            </aside>
        </div>

        <footer>
        </footer>
        
    </body>
    </html>
    """
    return html



# def render_tracking(order):
    
#     order_id = escape_html(str(order['id']))
#     product = escape_html(order['Products'])
#     status = escape_html(order['Status'])
#     cost = escape_html(order['Cost'])
#     main_msg = ""; sec_msg =""
#     if status == "Placed":
#         main_msg = "Your Order is Placed"
#         sec_msg = "Confirmed!!"
#     elif status == "Shipped":
#         main_msg = "Your Order is Being Shipped"
#         sec_msg = "On its Way!!"
#     elif status == "Cancelled":
#         main_msg = "Your Order has Been Cancelled"
#         sec_msg = "Either it was cancelled by you or it violated our policy"
#     else:
#         main_msg = "Your Order was Delivered"
#         sec_msg = "Go Grab it!!"
    
#     html = f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <link href="https://fonts.googleapis.com/css2?family=Knewave&display=swap" rel="stylesheet">
#         <link rel="stylesheet" href="/main.css">
#         <title>SurpriShip - Order Tracking</title>
#     </head>
#     <body>
#         <header>
#             <a href="/about">About</a>
#             <a href="/admin/orders">Orders (Admin Only)</a>
#             <a href="/order">Place Order</a>
#         </header>
#         <div class="main-container">
#             <nav></nav>
#             <main class="tracking-container">
#                 <h1>Order Tracking</h1>
                
#                 <!-- Order status box -->
#                 <section class="status-box">
#                     <h2>{main_msg}</h2>
#                     <p>{sec_msg}</p>
#                 </section>

#                 <!-- Order details -->
#                 <section class="details-box">
#                     <h3>Order Details</h3>
#                     <table class="order-details">
#                         <tr>
#                             <td><strong>Order ID:</strong></td>
#                             <td>{order_id}</td>
#                         </tr>
#                         <tr>
#                             <td><strong>Product:</strong></td>
#                             <td>{product}</td>
#                         </tr>
#                         <tr>
#                             <td><strong>Status:</strong></td>
#                             <td>{status}</td>
#                         </tr>
#                         <tr>
#                             <td><strong>Cost:</strong></td>
#                             <td>{cost}</td>
#                         </tr>
#                     </table>
#                 </section>
#             </main>
#             <aside></aside>
#         </div>
#         <footer>
#             <!--Cool items to be added in the footer soon :)-->
#         </footer>
#     </body>
#     </html>
#     """
#     return html


def render_orders(order_filters: dict[str, str]):
    query = order_filters.get("query", "").lower() 
    status_filter = order_filters.get("status", "all").lower()
    filtered_orders = []
    for order in orders:
        
        if status_filter != "all" and order["Status"].lower() != status_filter:
            continue

        
        if query and query not in order["From"].lower():
            continue
        
        filtered_orders.append(order)

    # Start the HTML content for the orders page
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Knewave&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="/main.css">
        <title>SurpriShip - Orders Management</title>
    </head>
    <body>
        <header>
            <a href="/about">About</a>
            <a href="/admin/orders">Orders (Admin Only)</a>
            <a href="/order">Place Order</a>
        </header>
        <div class="main-container">
            <nav></nav>
            <main class="orders-container">
                <h1>Order Management</h1>
                <!-- Search form -->
                <form action="/admin/orders" method="GET">
                    <input type="text" id="query" name="query" placeholder="Search order-placer..." value="{query}">
                    <select id="status" name="status">
                        <option value="all" {"selected" if status_filter == 'all' else ""}>All Statuses</option>
                        <option value="placed" {"selected" if status_filter == 'placed' else ""}>Placed</option>
                        <option value="shipped" {"selected" if status_filter == 'shipped' else ""}>Shipped</option>
                        <option value="delivered" {"selected" if status_filter == 'delivered' else ""}>Delivered</option>
                    </select>
                    <button type="submit">Search</button>
                </form>

                <!-- Table -->
                <table>
                    <tr>
                        <th>id</th>
                        <th>Status</th>
                        <th>Cost</th>
                        <th>From</th>
                        <th>Address</th>
                        <th>Products</th>
                        <th>SurpriShip Product</th>
                        <th>Notes</th>
                        <th>Track</th>
                    </tr>
    """

    # Generate the rows for each order
    for order in filtered_orders:
        html += f"""
        
        <tr>
            <td>{order['id']}</td>
            <td>{order['Status']}</td>
            <td>{order['Cost']}</td>
            <td>{order['From']}</td>
            <td>{order['Address']}</td>
            <td>{order['Products']}</td>
            <td>{order['SurpriShip Product']}</td>
            <td>{order['Notes']}</td>
            <td><a href = "/tracking/{order['id']}">Go Track</td>
        </tr>
        """

    # If no orders were found
    if not filtered_orders:
        html += "<tr><td colspan='9'>No orders found</td></tr>"

    # End the table and other HTML structure
    html += """
                </table>
            </main>
            <aside></aside>
        </div>
        <footer></footer>
    </body>
    </html>
    """
    
    return html



# Provided function -- converts numbers like 42 or 7.347 to "$42.00" or "$7.35"
def typeset_dollars(number):
    return f"${number:.2f}"

def render_order_success(order_id):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/main.css">
        <link href="https://fonts.googleapis.com/css2?family=Knewave&display=swap" rel="stylesheet">
        <title>SurpriShip</title>
    </head>

    <body>
        <header>
            <a href="/about">About</a>
            <a href="/admin/orders">Orders (Admin Only)</a>
            <a href="/order">Place Another Order</a>
        </header>
        <div class="main-container">
            <nav>
            </nav>
            <main class="order-status-container">
                <h1>Order Success</h1>
                <section class="status-box">
                    <h2>Wohooo! Your order has been placed successfully</h2>
                    <p>You can track it here</p>
                    <a href = "/tracking/{order_id}">Track My Order</a>
                </section>
            </main>
            <aside>
            </aside>
        </div>
        <footer>
            <!--Cool items to be added in the footer soon :)-->
        </footer>
    </body>

    </html>
    """
    return html



def add_new_order(params):
    required_fields = ["buyer", "address", "product", "quantity", "shipping"]
    
    # Check all required fields are filled
    for field in required_fields:
        if field not in params or not params[field].strip():
            print(f"Missing field: {field}")
            return None

    # Validate product
    valid_products = ["apples", "eggs", "milk"]
    if params["product"].lower() not in valid_products:
        print("Invalid product selected.")
        return None

    # Compute cost
    prices = {"apples": 2.5, "eggs": 3.0, "milk": 4.0}
    quantity = int(params["quantity"])
    cost = prices[params["product"].lower()] * quantity

    
    new_id = max(order["id"] for order in orders) + 1 if orders else 0

    # Create order entry
    new_order = {
        "id": new_id,
        "Status": "Placed",
        "Quantity": params["quantity"],
        "Cost": f"{cost:.2f}$",
        "From": params["buyer"],
        "Address": params["address"],
        "Products": params["product"],
        "SurpriShip Product": "",  # Will be Computed with an Ai model later ;)
        "Order Time": params.get("date", datetime.now().isoformat()),
        "Shipping": params["shipping"],
        "Notes": ""
    }

    orders.append(new_order)
    print(f"Added new order: {new_order}")
    return new_id

def cancel_order(params):
    if "id" not in params:
        print("Missing order ID.")
        return False

    order_id = int(params["id"])
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        print("Order not found.")
        return False

    if order["Status"] in ["Shipped", "Delivered", "Cancelled"]:
        print("Cannot cancel this order.")
        return False

    order["Status"] = "Cancelled"
    print(f"Order {order_id} cancelled.")
    return True


def update_shipping_info(params):
    required = ["id", "address", "shipping"]
    for field in required:
        if field not in params or not params[field].strip():
            print(f"Missing field: {field}")
            return False

    order_id = int(params["id"])
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        print("Order not found.")
        return False

    if order["Status"] in ["Shipped", "Delivered", "Cancelled"]:
        print("Cannot update this order.")
        return False

    order["Address"] = params["address"]
    order["Shipping"] = params["shipping"]
    print(f"Order {order_id} updated successfully.")
    return True


def server_GET(url: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    path = url.split("?")[0]  
    query = url.split("?")[1] if "?" in url else ""  


    query_params = parse_query_parameters(query)

    if path == "/about" or path == "/":
        return open("static/html/about.html", "r").read(), "text/html", 200
    
    elif path == "/admin/orders":
        return render_orders(query_params), "text/html", 200
    
    elif path == "/main.css":
        return open("static/css/main.css", "r").read(), "text/css", 200
    
    elif path == "/images/main":
        return open("static/images/logo.png", "rb").read(), "image/png", 200
    
    elif path == "/images/me":
        return open("static/images/me.jpg", "rb").read(), "image/jpeg", 200
    
    elif path == "/order":
        return open("static/html/order.html", "r").read(), "text/html", 200
    
    elif path == "/js/order.js":
        return open("static/js/order.js", "r").read(), "text/javascript", 200
    
    elif path == "/js/update.js":
        return open("static/js/update.js", "r").read(), "text/javascript", 200
    
    elif path.startswith("/tracking/"):
        order_id = path.split("/")[-1]
        order = next((o for o in orders if str(o['id']) == order_id), None)
        if order:
            return render_tracking(order), "text/html", 200
        else:
            return open("static/html/404.html", "r").read(), "text/html", 404
    
    else:
        return open("static/html/404.html", "r").read(), "text/html", 404
    


def server_POST(url: str, body: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a POST request to this website.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """

    # The path here is the url :)

    params = parse_query_parameters(body)
    if url == "/order":
        new_order_id = add_new_order(params)
        if new_order_id is not None:
            return render_order_success(new_order_id), "text/html", 201
        else:
            return open("static/html/order_fail.html", "r").read(), "text/html", 400
        
    elif url == "/cancel_order":
        success = cancel_order(params)
        if success:
            return render_order_success(params["id"]), "text/html", 200
        else:
            return open("static/html/order_fail.html", "r").read(), "text/html", 400

    elif url == "/update_shipping":
        success = update_shipping_info(params)
        if success:
            return render_order_success(params["id"]), "text/html", 200
        else:
            return open("static/html/order_fail.html", "r").read(), "text/html", 400
    else:
        return open("static/html/404.html", "r").read(), "text/html", 404
    

# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")

        message, content_type, response_code = server_POST(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, response_code = server_GET(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()


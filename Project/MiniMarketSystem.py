import json
import os
import time
from datetime import datetime


# === data ===

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")

# === Json fayllari ucun yukleme ve saxlama funksiyalari ===

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# === fayl yollarini dinamik olaraq yaradan funksiyalar ===
def history_file(username): return os.path.join(DATA_DIR, f"history_{username}.log")
def card_file(username): return os.path.join(DATA_DIR, f"basket_{username}.json")
def favorites_file(username): return os.path.join(DATA_DIR, f"favorites_{username}.json")
def purchases_file(username): return os.path.join(DATA_DIR, f"purchases_{username}.json")

# Default Data
DEFAULT_USERS = [
    {"username": "enver", "password": "0611", "balance": 407.9, "failed_attempts": 0, "lock_until": None}
]

DEFAULT_PRODUCTS = {
    "CLOTHES": [
        {"id": 1, "name": "Socks", "price": 3.99},
        {"id": 2, "name": "Shirt", "price": 19.99},
        {"id": 3, "name": "Jacket", "price": 29.99}
    ],
    "ELECTRONICS": [
        {"id": 1, "name": "Headphones", "price": 55.00},
        {"id": 2, "name": "Charger", "price": 25.00},
        {"id": 3, "name": "Keyboard", "price": 35.00}
    ],
    "TOOLS": [
        {"id": 1, "name": "Screwdriver", "price": 5.00},
        {"id": 2, "name": "Hammer", "price": 9.00},
        {"id": 3, "name": "Wrench", "price": 7.00}
    ],
    "DRINKS": [
        {"id": 1, "name": "Water", "price": 0.99},
        {"id": 2, "name": "Soda", "price": 1.50},
        {"id": 3, "name": "Juice", "price": 2.00}
    ]
}

def init_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, DEFAULT_USERS)
    if not os.path.exists(PRODUCTS_FILE):
        save_json(PRODUCTS_FILE, DEFAULT_PRODUCTS)

#-----------------
# Log Sistemi
#-----------------
def log_event(username, message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}\n"
    with open(history_file(username), "a", encoding="utf-8") as f:
        f.write(line)

def show_history(username):
    path = history_file(username)
    if not os.path.exists(path):
        print("\n-- Empty --")
        return
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    last = lines[-20:]
    print("\n── History ──────────")
    for line in last:
        print(line.rstrip())

#-----------------
# Login Sistemi
#-----------------
def login():
    init_data()
    users = load_json(USERS_FILE, DEFAULT_USERS)
    
    print("\n" + "="*40)
    print("      MİNİ MARKET LOGİN")
    print("="*40)

    while True:
        username = input("\nUsername: ").strip()
        user = next((u for u in users if u["username"] == username), None)

        if not user:
            print("ERROR: User not found!")
            continue

        # Lock check
        if user["lock_until"] and time.time() < user["lock_until"]:
            remaining = int(user["lock_until"] - time.time())
            print(f"ERROR: Account locked. Wait {remaining} seconds...")
            for i in range(remaining, 0, -1):
                print(f"Please wait: {i}s", end="\r")
                time.sleep(1)
            print("\nYou can try again now.")
            user["lock_until"] = None
            user["failed_attempts"] = 0
            save_json(USERS_FILE, users)

        password = input("Password: ").strip()

        if password == user["password"]:
            print(f"\nWelcome, {username}!")
            user["failed_attempts"] = 0
            user["lock_until"] = None
            save_json(USERS_FILE, users)
            log_event(username, "SUCCESSFUL_LOGIN")
            return user
        else:
            user["failed_attempts"] += 1
            log_event(username, f"LOGIN_FAIL (Attempt {user['failed_attempts']})")
            
            if user["failed_attempts"] >= 3:
                user["lock_until"] = time.time() + 10
                print("ERROR: 3 failed attempts! You are locked for 10 seconds.")
                save_json(USERS_FILE, users)
            else:
                print(f"ERROR: Incorrect password! (Remaining attempts: {3 - user['failed_attempts']})")
            save_json(USERS_FILE, users)

#-----------------
# Market funksiyalari
#-----------------

def browse_products(user):
    products_data = load_json(PRODUCTS_FILE, DEFAULT_PRODUCTS)
    categories = list(products_data.keys())

    print("\n── Categories ──────────")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat}")
    print("0. Back")

    choice = input("\nYour choice: ")
    if choice == "0" or not choice.isdigit() or int(choice) > len(categories):
        return

    cat_name = categories[int(choice)-1]
    items = products_data[cat_name]

    print(f"\n── {cat_name} ──────────")
    for p in items:
        print(f"[{p['id']}] {p['name']} - {p['price']} AZN")
    
    p_id = input("\nProduct ID: ")
    product = next((p for p in items if str(p['id']) == p_id), None)

    if product:
        try:
            qty = int(input(f"{product['name']} for quantity: "))
            if qty <= 0: raise ValueError
        except ValueError:
            print("ERROR: Quantity must be a positive integer!")
            return

        print(f"\nChoice: {product['name']} x{qty} | Total: {product['price']*qty} AZN")
        opt = input("[B] Add to Cart | [F] Add to Favorites | [X] Cancel: ").upper()

        if opt == "B":
            basket = load_json(card_file(user['username']), [])
            basket.append({
                "category": cat_name,
                "product": product['name'],
                "unit_price": product['price'],
                "qty": qty,
                "line_total": product['price'] * qty
            })
            save_json(card_file(user['username']), basket)
            log_event(user['username'], f"BASKET_ADD ({cat_name}/{product['name']} x{qty})")
            print("Added to cart!")
        
        elif opt == "F":
            favs = load_json(favorites_file(user['username']), [])
            if not any(f['name'] == product['name'] for f in favs):
                favs.append({"category": cat_name, "id": product['id'], "name": product['name'], "price": product['price']})
                save_json(favorites_file(user['username']), favs)
                log_event(user['username'], f"FAVORITE_ADD ({product['name']})")
                print("Added to favorites!")
            else:
                print("This product is already in your favorites.")

def manage_basket(user):
    while True:
        basket = load_json(card_file(user['username']), [])
        total = sum(item['line_total'] for item in basket)
        
        print("\n── My Card ────────────────")
        if not basket:
            print("The card is empty.")
        else:
            for i, item in enumerate(basket):
                print(f"{i}. {item['product']} ({item['category']}) | {item['unit_price']} x {item['qty']} = {item['line_total']} AZN")
            print(f"\nTotal Amount: {total} AZN")
            print(f"Your Balance: {user['balance']} AZN")

        cmd = input("\nCommands: list | qty <id> <val> | remove <id> | clear | checkout | back\n> ").lower().split()
        if not cmd or cmd[0] == "back": break

        if cmd[0] == "clear":
            save_json(card_file(user['username']), [])
            print("Card cleared.")
        
        elif cmd[0] == "remove" and len(cmd) > 1:
            idx = int(cmd[1])
            if 0 <= idx < len(basket):
                removed = basket.pop(idx)
                save_json(card_file(user['username']), basket)
                print(f"{removed['product']} removed.")

        elif cmd[0] == "qty" and len(cmd) > 2:
            idx, new_q = int(cmd[1]), int(cmd[2])
            if 0 <= idx < len(basket) and new_q > 0:
                basket[idx]['qty'] = new_q
                basket[idx]['line_total'] = basket[idx]['unit_price'] * new_q
                save_json(card_file(user['username']), basket)
                print("Quantity updated.")

        elif cmd[0] == "checkout":
            if not basket:
                print("The card is empty!")
                continue
            
            if user['balance'] >= total:
                user['balance'] -= total
                purchases = load_json(purchases_file(user['username']), [])
                purchases.append({"ts": datetime.now().isoformat(), "items": basket, "total": total})
                save_json(purchases_file(user['username']), purchases)
                users = load_json(USERS_FILE, [])
                for u in users:
                    if u['username'] == user['username']:
                        u['balance'] = user['balance']
                save_json(USERS_FILE, users)
                save_json(card_file(user['username']), [])
                log_event(user['username'], f"CHECKOUT_SUCCESS total={total} | new_balance={user['balance']}")
                print(f"Checkout Successful! New Balance: {user['balance']} AZN")
            else:
                log_event(user['username'], f"CHECKOUT_FAIL (insufficient balance: {total} > {user['balance']})")
                print("ERROR: Insufficient balance!")

def manage_favorites(user):
    favs = load_json(favorites_file(user['username']), [])
    print("\n── Favorites ───────────")
    if not favs:
        print("No favorites found.")
        return
    
    for i, f in enumerate(favs):
        print(f"{i}. {f['name']} - {f['price']} AZN")
    
    choice = input("\nTo add to cart, enter ID (or 'X' to go back): ").upper()
    if choice != 'X' and choice.isdigit():
        idx = int(choice)
        if 0 <= idx < len(favs):
            item = favs[idx]
            qty = int(input(f"{item['name']} for quantity: "))
            basket = load_json(card_file(user['username']), [])
            basket.append({
                "category": item['category'], "product": item['name'],
                "unit_price": item['price'], "qty": qty, "line_total": item['price'] * qty
            })
            save_json(card_file(user['username']), basket)
            print("Added to cart!")

def change_password(user):
    old_p = input("Old password: ")
    if old_p == user['password']:
        new_p = input("New password (min 4 characters): ")
        if len(new_p) >= 4:
            user['password'] = new_p
            users = load_json(USERS_FILE, [])
            for u in users:
                if u['username'] == user['username']:
                    u['password'] = new_p
            save_json(USERS_FILE, users)
            log_event(user['username'], "PASSWORD_CHANGED")
            print("Password changed successfully!")
        else:
            print("ERROR: New password is too short.")
    else:
        print("ERROR: Old password is incorrect.")

#-----------------
# main menu
#-----------------
def main():
    user = login()
    if not user: return

    while True:
        print("\n" + "="*30)
        print(f"   MENU - Balance: {user['balance']} AZN")
        print("="*30)
        print("1. Categories")
        print("2. My Cart")
        print("3. My Favorites")
        print("4. History")
        print("5. Settings (Change Password)")
        print("6. Show Balance")
        print("0. Exit")

        choice = input("\nYour Choice: ")

        if choice == "1": browse_products(user)
        elif choice == "2": manage_basket(user)
        elif choice == "3": manage_favorites(user)
        elif choice == "4": show_history(user['username'])
        elif choice == "5": change_password(user)
        elif choice == "6": print(f"\nCurrent Balance: {user['balance']} AZN")
        elif choice == "0":
            print("Exiting the system...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

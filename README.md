# Mini Market System

A file-based mini market system built with Python. No database — all data is stored in JSON files.

## How to Run

Make sure Python is installed, then run:

## Login

Default account:
- Username: `enver`
- Password: `1106`

## Menu Options
1 Categories
2 My Cart
3 My Favorites
4 History
5 Settings (Change Password)
6 Show Balance
0 Exit

## File Structure

data/
├── users.json              # User accounts and login info
├── products.json           # Categories and products
├── basket_enver.json       # Cart items
├── favorites_enver.json    # Favorite products
├── purchases_enver.json    # Completed orders
└── history_enver.log       # Activity log

## Sample Usage

### Scenario 1: Add to cart and checkout
1. Run the program: `python main.py`
2. Login with username `enver`, password `0611`
3. Select `1. Categories` → `CLOTHES`
4. Select product ID 1 (Socks), quantity 2
5. Press `B` to add to cart
6. Select `2. My Cart`
7. Type `checkout` — balance is deducted, purchase saved

### Scenario 2: Favorites to cart
1. Login with username `enver`, password `0611`
2. Select `1. Categories` → `ELECTRONICS`
3. Select Headphones, quantity 1, press `F` to add to favorites
4. Select `3. My Favorites`
5. Enter ID `0` → quantity 1 → added to cart
6. Select `2. My Cart` → type `checkout`

## Login Security

- 3 wrong password attempts → 10 second cooldown
- Cooldown countdown shown in terminal
- All login attempts logged with timestamp

## Note

I would like to note that this project was not created by artificial intelligence, but received help. I was able to build this system by learning and applying what I didn't know

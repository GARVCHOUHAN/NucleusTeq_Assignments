# Product Inventory Dashboard

This is my mini app assignment made using **HTML, CSS, and JavaScript**.  
The main idea of this project is to create a simple product inventory dashboard where products can be displayed, searched, filtered, sorted, added, edited, and deleted dynamically.

I have used **Vanilla JavaScript only** for this project and did not use any framework or library. The product data is stored in **localStorage**, so changes remain saved even after refreshing the page.

---

## Project Objective

The objective of this project was to practice core front-end concepts like:

- DOM manipulation
- event handling
- array methods
- form validation
- localStorage
- asynchronous JavaScript
- responsive UI design

This project helped me understand how a dashboard works and how different features like analytics, filters, and CRUD operations can be connected together in one application.

---

## Features Implemented

The following features are implemented in this project:

- Dynamic rendering of product cards using JavaScript
- Search product by name
- Filter products by category
- Low stock filter (`stock < 5`)
- Sort by:
  - Price low to high
  - Price high to low
  - Alphabetically A-Z
  - Alphabetically Z-A
- Inventory analytics:
  - Total number of products
  - Total inventory value
  - Out of stock count
  - Category-wise product count
- Add new product
- Edit existing product
- Delete product
- Save product data in localStorage
- Loading state using Promise and setTimeout
- Initial product loading using DummyJSON API
- Empty state handling when no product matches the filters
- Responsive design for mobile, tablet, and desktop

---

## Technologies Used

- HTML
- CSS
- JavaScript
- DummyJSON API
- localStorage

---

## Folder Structure

```text
mini_app/
    ├── index.html
    ├── style.css
    ├── script.js
    └── README.md


How the Project Works

When the app loads, it first shows a loading state.
After that, it checks if product data is already saved in localStorage.

If localStorage already has data, it uses that data.
If localStorage is empty, it fetches product data from DummyJSON API.
If API fetch fails for any reason, default products are used.

After loading the products, the app displays them in the product grid and also updates the analytics section.

All product cards are rendered dynamically using JavaScript, so no product card is hardcoded in HTML.

Product Features
1. Search

The user can search products by product name.
The search is case-insensitive and updates the product list in real time.

2. Filter

The app supports:

category filter
low stock filter

These filters also work together with search and sorting.

3. Sorting

Products can be sorted by:

price low to high
price high to low
name A-Z
name Z-A
4. Add Product

A form is given to add a new product.
The form checks all fields properly before adding the product.

5. Edit Product

Any existing product can be edited using the Edit button.
When edit is clicked, the selected product data comes into the form and can be updated.

6. Delete Product

Each product card has a Delete button.
When clicked, the product is removed from the dashboard and localStorage is updated.

7. Analytics

The dashboard shows:

total products
total inventory value
out of stock count
category-wise product count

These values update automatically whenever any product is added, edited, or deleted.

API Used

For initial product data, I used the DummyJSON products API:

https://dummyjson.com/products?limit=12

The API gives product data like title, category, price, and stock.
In my project, I mapped the API field title to name so that it matches my product object structure.

Validation Rules

The add/edit product form checks the following:

Product name should not be empty
Price should be greater than 0
Stock should not be negative
Category must be selected

If any input is invalid, an error message is shown below that field.

How to Run This Project
Download or clone the repository
Open the product_inventory_dashboard folder
Open index.html in browser
The products will load after a short loading delay
Learning Outcome

By making this project, I got better understanding of:

how to render data dynamically
how filters and sorting can work together
how to handle add, edit, and delete operations
how to use localStorage properly
how to fetch and use API data in JavaScript
how to build a clean and responsive UI without frameworks
Screenshots

I can add screenshots here of:

![alt text](<Screenshot 2026-03-22 235650.png>) ![alt text](<Screenshot 2026-03-22 235424.png>) ![alt text](<Screenshot 2026-03-22 235438.png>) ![alt text](<Screenshot 2026-03-22 235449.png>) ![alt text](<Screenshot 2026-03-22 235459.png>) ![alt text](<Screenshot 2026-03-22 235525.png>) ![alt text](<Screenshot 2026-03-22 235538.png>) ![alt text](<Screenshot 2026-03-22 235553.png>) ![alt text](<Screenshot 2026-03-22 235603.png>) ![alt text](<Screenshot 2026-03-22 235634.png>)
const defaultProducts = [
  { id: 1001, name: "Laptop", price: 55000, stock: 5, category: "laptops" },
  { id: 1002, name: "Headphones", price: 2500, stock: 12, category: "mobile-accessories" },
  { id: 1003, name: "T-Shirt", price: 800, stock: 3, category: "mens-shirts" },
  { id: 1004, name: "Sunglasses", price: 1800, stock: 7, category: "sunglasses" },
  { id: 1005, name: "Face Wash", price: 650, stock: 0, category: "beauty" },
  { id: 1006, name: "Handbag", price: 1500, stock: 4, category: "womens-bags" },
  { id: 1007, name: "Watch", price: 3200, stock: 2, category: "mens-watches" },
  { id: 1008, name: "Table Lamp", price: 1200, stock: 6, category: "home-decoration" }
];

let products = [];
let editingProductId = null;

const storageKey = "inventoryProducts";

const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const sortOption = document.getElementById("sortOption");
const lowStockOnly = document.getElementById("lowStockOnly");
const resetFiltersBtn = document.getElementById("resetFiltersBtn");

const totalProducts = document.getElementById("totalProducts");
const totalInventoryValue = document.getElementById("totalInventoryValue");
const outOfStockCount = document.getElementById("outOfStockCount");
const categoryCounts = document.getElementById("categoryCounts");

const loadingState = document.getElementById("loadingState");
const emptyState = document.getElementById("emptyState");
const productGrid = document.getElementById("productGrid");

const productForm = document.getElementById("productForm");
const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");
const cancelEditBtn = document.getElementById("cancelEditBtn");

const productName = document.getElementById("productName");
const productPrice = document.getElementById("productPrice");
const productStock = document.getElementById("productStock");
const productCategory = document.getElementById("productCategory");

const nameError = document.getElementById("nameError");
const priceError = document.getElementById("priceError");
const stockError = document.getElementById("stockError");
const categoryError = document.getElementById("categoryError");

function saveProductsToStorage() {
  localStorage.setItem(storageKey, JSON.stringify(products));
}

function loadProductsFromStorage() {
  const savedProducts = localStorage.getItem(storageKey);
  return savedProducts ? JSON.parse(savedProducts) : null;
}

async function fetchProductsFromAPI() {
  const response = await fetch("https://dummyjson.com/products?limit=12");

  if (!response.ok) {
    throw new Error("Failed to fetch products from API");
  }

  const data = await response.json();

  return data.products.map((item) => ({
    id: item.id,
    name: item.title,
    price: Math.round(item.price * 83),
    stock: item.stock,
    category: item.category
  }));
}


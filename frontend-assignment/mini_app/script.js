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

function fetchProductsWithDelay() {
  return new Promise((resolve, reject) => {
    setTimeout(async () => {
      try {
        const savedProducts = loadProductsFromStorage();

        if (savedProducts && savedProducts.length > 0) {
          resolve(savedProducts);
          return;
        }

        const apiProducts = await fetchProductsFromAPI();
        resolve(apiProducts);
      } catch (error) {
        reject(error);
      }
    }, 1500);
  });
}

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(amount);
}

function capitalizeWord(text) {
  return text
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function getStockStatus(stock) {
  if (stock === 0) {
    return { text: "Out of Stock", className: "out-of-stock" };
  }

  if (stock < 5) {
    return { text: "Low Stock", className: "low-stock" };
  }

  return { text: "In Stock", className: "in-stock" };
}

function populateCategoryFilter() {
  const categories = [...new Set(products.map((product) => product.category))].sort();
  const currentSelectedValue = categoryFilter.value;

  categoryFilter.innerHTML = `<option value="all">All Categories</option>`;

  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = capitalizeWord(category);
    categoryFilter.appendChild(option);
  });

  const optionExists = [...categoryFilter.options].some(
    (option) => option.value === currentSelectedValue
  );

  categoryFilter.value = optionExists ? currentSelectedValue : "all";
}

function updateAnalytics() {
  totalProducts.textContent = products.length;

  const inventoryValue = products.reduce((total, product) => {
    return total + product.price * product.stock;
  }, 0);

  totalInventoryValue.textContent = formatCurrency(inventoryValue);

  const outOfStockProducts = products.filter((product) => product.stock === 0).length;
  outOfStockCount.textContent = outOfStockProducts;

  const countsByCategory = products.reduce((accumulator, product) => {
    accumulator[product.category] = (accumulator[product.category] || 0) + 1;
    return accumulator;
  }, {});

  categoryCounts.innerHTML = "";

  Object.keys(countsByCategory)
    .sort()
    .forEach((category) => {
      const badge = document.createElement("span");
      badge.className = "category-badge";
      badge.textContent = `${capitalizeWord(category)}: ${countsByCategory[category]}`;
      categoryCounts.appendChild(badge);
    });
}

function getFilteredAndSortedProducts() {
  const searchTerm = searchInput.value.trim().toLowerCase();
  const selectedCategory = categoryFilter.value;
  const selectedSort = sortOption.value;
  const showLowStockOnly = lowStockOnly.checked;

  let filteredProducts = [...products];

  filteredProducts = filteredProducts.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm);
    const matchesCategory =
      selectedCategory === "all" || product.category === selectedCategory;
    const matchesLowStock = !showLowStockOnly || product.stock < 5;

    return matchesSearch && matchesCategory && matchesLowStock;
  });

  switch (selectedSort) {
    case "priceLowToHigh":
      filteredProducts.sort((a, b) => a.price - b.price);
      break;
    case "priceHighToLow":
      filteredProducts.sort((a, b) => b.price - a.price);
      break;
    case "nameAToZ":
      filteredProducts.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case "nameZToA":
      filteredProducts.sort((a, b) => b.name.localeCompare(a.name));
      break;
    default:
      break;
  }

  return filteredProducts;
}

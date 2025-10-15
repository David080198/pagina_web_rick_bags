// RickBags Main JavaScript

document.addEventListener("DOMContentLoaded", function () {
  // Initialize all components
  initMobileNav();
  initSearchFunctionality();
  initCartUpdates();
  initFormValidation();
  initImageLazyLoading();
  initSmoothScrolling();
});

// Mobile Navigation Toggle
function initMobileNav() {
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      navMenu.classList.toggle("active");
      this.classList.toggle("active");
    });

    // Close menu when clicking outside
    document.addEventListener("click", function (e) {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove("active");
        navToggle.classList.remove("active");
      }
    });
  }
}

// Search Functionality
function initSearchFunctionality() {
  const searchInput = document.querySelector(".search-input");
  const searchResults = document.querySelector(".search-results");
  let searchTimeout;

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout);
      const query = this.value.trim();

      if (query.length >= 2) {
        searchTimeout = setTimeout(() => {
          performSearch(query);
        }, 300);
      } else if (searchResults) {
        searchResults.style.display = "none";
      }
    });

    // Hide results when clicking outside
    document.addEventListener("click", function (e) {
      if (!searchInput.contains(e.target) && searchResults) {
        searchResults.style.display = "none";
      }
    });
  }
}

function performSearch(query) {
  fetch(`/api/products/search?q=${encodeURIComponent(query)}&limit=5`)
    .then((response) => response.json())
    .then((data) => {
      displaySearchResults(data);
    })
    .catch((error) => {
      console.error("Search error:", error);
    });
}

function displaySearchResults(results) {
  let searchResults = document.querySelector(".search-results");

  if (!searchResults) {
    searchResults = document.createElement("div");
    searchResults.className = "search-results";
    document.querySelector(".search-box").appendChild(searchResults);
  }

  if (results.length === 0) {
    searchResults.innerHTML =
      '<div class="search-no-results">No se encontraron productos</div>';
  } else {
    const resultsHTML = results
      .map(
        (product) => `
            <div class="search-result-item">
                <img src="${product.image}" alt="${
          product.name
        }" class="search-result-image">
                <div class="search-result-info">
                    <div class="search-result-name">${product.name}</div>
                    <div class="search-result-price">$${product.price.toFixed(
                      2
                    )}</div>
                </div>
                <a href="${product.url}" class="search-result-link">Ver</a>
            </div>
        `
      )
      .join("");

    searchResults.innerHTML = resultsHTML;
  }

  searchResults.style.display = "block";
}

// Cart Updates
function initCartUpdates() {
  // Update cart count in real-time
  updateCartDisplay();

  // Listen for cart changes
  document.addEventListener("cartUpdated", function (e) {
    updateCartDisplay();
    if (e.detail && e.detail.message) {
      showNotification("success", e.detail.message);
    }
  });
}

function updateCartDisplay() {
  fetch("/api/cart/count")
    .then((response) => response.json())
    .then((data) => {
      const cartCount = document.querySelector(".cart-count");
      const cartIcon = document.querySelector(".cart-icon");

      if (data.count > 0) {
        if (cartCount) {
          cartCount.textContent = data.count;
        } else {
          const countElement = document.createElement("span");
          countElement.className = "cart-count";
          countElement.textContent = data.count;
          cartIcon.appendChild(countElement);
        }
      } else if (cartCount) {
        cartCount.remove();
      }
    })
    .catch((error) => {
      console.error("Cart update error:", error);
    });
}

// Form Validation
function initFormValidation() {
  const forms = document.querySelectorAll("form[data-validate]");

  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      if (!validateForm(this)) {
        e.preventDefault();
      }
    });

    // Real-time validation
    const inputs = form.querySelectorAll("input, textarea, select");
    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        validateField(this);
      });
    });
  });
}

function validateForm(form) {
  let isValid = true;
  const inputs = form.querySelectorAll(
    "input[required], textarea[required], select[required]"
  );

  inputs.forEach((input) => {
    if (!validateField(input)) {
      isValid = false;
    }
  });

  return isValid;
}

function validateField(field) {
  const value = field.value.trim();
  const type = field.type;
  let isValid = true;
  let message = "";

  // Remove existing error
  clearFieldError(field);

  // Required validation
  if (field.hasAttribute("required") && !value) {
    isValid = false;
    message = "Este campo es requerido";
  }

  // Email validation
  else if (type === "email" && value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      isValid = false;
      message = "Ingresa un email válido";
    }
  }

  // Password validation
  else if (type === "password" && value) {
    if (value.length < 8) {
      isValid = false;
      message = "La contraseña debe tener al menos 8 caracteres";
    }
  }

  // Phone validation
  else if (field.name === "phone" && value) {
    const phoneRegex = /^[+]?[\d\s\-()]+$/;
    if (!phoneRegex.test(value)) {
      isValid = false;
      message = "Ingresa un teléfono válido";
    }
  }

  if (!isValid) {
    showFieldError(field, message);
  }

  return isValid;
}

function showFieldError(field, message) {
  field.classList.add("error");

  const errorElement = document.createElement("div");
  errorElement.className = "field-error";
  errorElement.textContent = message;

  field.parentNode.appendChild(errorElement);
}

function clearFieldError(field) {
  field.classList.remove("error");
  const errorElement = field.parentNode.querySelector(".field-error");
  if (errorElement) {
    errorElement.remove();
  }
}

// Image Lazy Loading
function initImageLazyLoading() {
  const images = document.querySelectorAll("img[data-src]");

  if ("IntersectionObserver" in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove("lazy");
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach((img) => imageObserver.observe(img));
  } else {
    // Fallback for older browsers
    images.forEach((img) => {
      img.src = img.dataset.src;
      img.classList.remove("lazy");
    });
  }
}

// Smooth Scrolling
function initSmoothScrolling() {
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href").substring(1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// Notification System
function showNotification(type, message, duration = 5000) {
  const notification = document.createElement("div");
  notification.className = `flash-message flash-${type}`;
  notification.innerHTML = `
        <i class="fas fa-times flash-close" onclick="this.parentElement.remove()"></i>
        ${message}
    `;

  const container = document.querySelector(".flash-messages");
  container.appendChild(notification);

  // Auto-remove
  setTimeout(() => {
    if (notification.parentElement) {
      notification.style.opacity = "0";
      setTimeout(() => notification.remove(), 300);
    }
  }, duration);
}

// Utility Functions
function formatCurrency(amount) {
  return new Intl.NumberFormat("es-ES", {
    style: "currency",
    currency: "EUR",
  }).format(amount);
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function throttle(func, limit) {
  let inThrottle;
  return function () {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Global error handler
window.addEventListener("error", function (e) {
  console.error("Global error:", e.error);
  // Could send to error reporting service
});

// Handle unhandled promise rejections
window.addEventListener("unhandledrejection", function (e) {
  console.error("Unhandled promise rejection:", e.reason);
  e.preventDefault();
});

// Export functions for use in other scripts
window.RickBags = {
  showNotification,
  updateCartDisplay,
  formatCurrency,
  debounce,
  throttle,
};

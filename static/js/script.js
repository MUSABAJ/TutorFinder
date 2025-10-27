//registration page navigator  func 
const nextbtn = document.getElementById('next')
const prevbtn = document.getElementById('prev')
const formSteps = document.querySelectorAll(".form-info")
const togglebttns = document.querySelectorAll(".role-btn")

let stepCount = 0;
if (nextbtn) {
  nextbtn.addEventListener("click", () => {
    const roleEl = document.getElementById("role")
    const role = roleEl ? roleEl.value : undefined

    stepCount++;
    if ((role === 'tutor' && stepCount == 1) || (role === 'student' && stepCount == 2)) {
      stepCount++
    }
    if (typeof updateFormstep === 'function') updateFormstep()  
    if (typeof updateProgressbar === 'function') updateProgressbar() 
  });
}

if (prevbtn) {
  prevbtn.addEventListener('click', () => {
    const roleEl = document.getElementById("role")
    const role = roleEl ? roleEl.value : undefined
    stepCount--;
    if ((role === 'tutor' && stepCount == 1) || (role === 'student' && stepCount == 2)) {
      stepCount--
    }
    if (typeof updateFormstep === 'function') updateFormstep()
    if (typeof updateProgressbar === 'function') updateProgressbar() 
  })
}

function updateFormstep() {
  togglebttns.forEach(togglebttn => {
    if (stepCount >= 1) {
      togglebttn.style.opacity = 0.8;
      togglebttn.removeAttribute('onclick')
     }
     if (stepCount < 1){
      togglebttn.style.opacity = 1;
      let fucRole = (togglebttn.getAttribute("data-role") === 'student') ? 'student' : 'tutor'
      togglebttn.setAttribute('onclick', `switchRole('${fucRole}')`)
    }
  });

  formSteps.forEach(formstep => {
    formstep.classList.remove("step-active")
  });
  
  if (!formSteps[stepCount + 1]) {
    if (nextbtn) {
      nextbtn.style.opacity = 0;
      nextbtn.style.cursor = 'default';
    }
  } else {
    if (nextbtn) {
      nextbtn.style.opacity = 1;
      nextbtn.style.cursor = 'pointer';
    }
  }

  if (!formSteps[stepCount - 1]) {
    if (prevbtn) {
      prevbtn.style.opacity = 0;
      prevbtn.style.cursor = 'default';
    }
  } else {
    if (prevbtn) {
      prevbtn.style.opacity = 1;
      prevbtn.style.cursor = 'pointer';
    }
  }
  if (formSteps[stepCount]) {
    formSteps[stepCount].classList.add("step-active")
  }
}

function updateProgressbar(){
  const progresSteps = document.querySelectorAll(".progress-step") 
  switch (stepCount) {
    case 0:
      if (progresSteps[1]) progresSteps[1].classList.remove("active")     
      if (progresSteps[2]) progresSteps[2].classList.remove("active") 
      if (progresSteps[0] && progresSteps[0].nextElementSibling) {
        progresSteps[0].nextElementSibling.classList.remove("active")
      }
    break;
    case 1:
    case 2:
      if (progresSteps[1]) progresSteps[1].classList.add("active")      
      if (progresSteps[2]) progresSteps[2].classList.remove("active")      
      if (progresSteps[1] && progresSteps[1].previousElementSibling) {
        progresSteps[1].previousElementSibling.classList.add("active")
      }
      if (progresSteps[1] && progresSteps[1].nextElementSibling) {
        progresSteps[1].nextElementSibling.classList.remove("active")
      }
      break;
    case 3:
    case 4:
      if (progresSteps[2]) progresSteps[2].classList.add("active")
      if (progresSteps[2] && progresSteps[2].previousElementSibling) {
        progresSteps[2].previousElementSibling.classList.add("active")
      }
    default:
      break;
  }
}

// Role switching functionality

function switchRole(role) {
  const roleButtons = document.querySelectorAll(".role-btn")
  const roleInput = document.getElementById("role")
  const studentFields = document.getElementById("student-fields")
  const tutorFields = document.getElementById("tutor-fields")

  // Update button states
  roleButtons.forEach((btn) => {
    btn.classList.remove("active")
    if (btn.dataset.role === role) {
      btn.classList.add("active")
    }
  })

  // Update hidden input
  if (roleInput) {
    roleInput.value = role
    
  }

  // Show/hide role-specific fields
  if (studentFields && tutorFields) {
    if (role === "student") {
      studentFields.style.display = "block"
      tutorFields.style.display = "none"
    } else {
      studentFields.style.display = "none"
      tutorFields.style.display = "block"
    }
  }
 
}

// Password strength checker
function checkPasswordStrength(password) {
  const strengthIndicator = document.getElementById("password-strength")
  if (!strengthIndicator) return

  let strength = 0
  const feedback = []

  if (password.length >= 8) strength++
  else feedback.push("At least 8 characters")

  if (/[a-z]/.test(password)) strength++
  else feedback.push("Lowercase letter")

  if (/[A-Z]/.test(password)) strength++
  else feedback.push("Uppercase letter")

  if (/[0-9]/.test(password)) strength++
  else feedback.push("Number")

  if (/[^A-Za-z0-9]/.test(password)) strength++
  else feedback.push("Special character")

  const strengthLevels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
  const strengthColors = ["#ef4444", "#f59e0b", "#eab308", "#22c55e", "#10b981"]

  strengthIndicator.textContent = `Password strength: ${strengthLevels[strength] || "Very Weak"}`
  strengthIndicator.style.color = strengthColors[strength] || strengthColors[0]

  if (feedback.length > 0) {
    strengthIndicator.textContent += ` (Missing: ${feedback.join(", ")})`
  }
}

// Form validation
function validateForm(form) {
  const inputs = form.querySelectorAll("input[required], select[required], textarea[required]")
  let isValid = true

  inputs.forEach((input) => {
    const errorElement = document.getElementById(input.name + "-error")

    if (!input.value.trim()) {
      if (errorElement) {
        errorElement.textContent = "This field is required"
      }
      input.style.borderColor = "var(--error-color)"
      isValid = false
    } else {
      if (errorElement) {
        errorElement.textContent = ""
      }
      input.style.borderColor = "var(--border-color)"
    }

    // Email validation
    if (input.type === "email" && input.value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(input.value)) {
        if (errorElement) {
          errorElement.textContent = "Please enter a valid email address"
        }
        input.style.borderColor = "var(--error-color)"
        isValid = false
      }
    }

    // Password confirmation
    if (input.name === "confirmPassword") {
      const password = form.querySelector('input[name="password"]')
      if (password && input.value !== password.value) {
        if (errorElement) {
          errorElement.textContent = "Passwords do not match"
        }
        input.style.borderColor = "var(--error-color)"
        isValid = false
      }
    }
  })

  return isValid
}

// Mobile menu toggle
function toggleMobileMenu() {
  const navLinks = document.querySelector(".nav-links")
  const toggle = document.querySelector(".mobile-menu-toggle")
  if (!navLinks || !toggle) return
  navLinks.classList.toggle("active")
  toggle.classList.toggle("active")
  const expanded = toggle.getAttribute('aria-expanded') === 'true'
  toggle.setAttribute('aria-expanded', (!expanded).toString())
}

// Language switching functionality
function switchLanguage(lang) {
  const langButtons = document.querySelectorAll(".lang-btn, .footer-lang-btn")

  langButtons.forEach((btn) => {
    btn.classList.remove("active")
    if (btn.dataset.lang === lang || btn.textContent.includes(getLanguageName(lang))) {
      btn.classList.add("active")
    }
  })

  // Store language preference
  localStorage.setItem("preferred-language", lang)

  // Here you would typically load language-specific content
  // For demo purposes, we'll just show a notification
  showNotification(`Language switched to ${getLanguageName(lang)}`, "success")
}

function getLanguageName(code) {
  const languages = {
    en: "English",
    ar: "العربية",
    am: "አማርኛ",
  }
  return languages[code] || "English"
}

function performSearch(query) {
  if (!query || !query.trim()) return

  // Show loading state
  const searchBtn = document.querySelector(".search-btn")
  if (!searchBtn) return
  const originalText = searchBtn.textContent
  searchBtn.textContent = "Searching..."
  searchBtn.disabled = true

  // Simulate search (in real app, this would be an API call)
  setTimeout(() => {
    searchBtn.textContent = originalText
    searchBtn.disabled = false

    // Redirect to search results
    window.location.href = `tutor-search.html?q=${encodeURIComponent(query)}`
  }, 1000)
}

function searchByTag(subject) {
  const searchInput = document.querySelector(".search-input")
  if (searchInput) {
    searchInput.value = subject
    performSearch(subject)
  }
}

// Enhanced password toggle functionality
function togglePassword(inputId) {
  const input = document.getElementById(inputId)
  if (!input) return
  const toggle = input.parentElement ? input.parentElement.querySelector(".password-toggle i") : null
  if (!toggle) return

  if (input.type === "password") {
    input.type = "text"
    toggle.classList.remove("fa-eye")
    toggle.classList.add("fa-eye-slash")
  } else {
    input.type = "password"
    toggle.classList.remove("fa-eye-slash")
    toggle.classList.add("fa-eye")
  }
}

// Enhanced subject tag functionality
function initializeSubjectTags() {
  const subjectTags = document.querySelectorAll(".subject-tag")

  subjectTags.forEach((tag) => {
    tag.addEventListener("click", function (e) {
      e.preventDefault()
      this.classList.toggle("active")
      updateSelectedSubjects()
    })
  })
}

function updateSelectedSubjects() {
  const activeTags = document.querySelectorAll(".subject-tag.active")
  const subjects = Array.from(activeTags).map((tag) => tag.dataset.subject)

  // Update hidden inputs
  const subjectsInput = document.getElementById("subjects")
  const specialtiesInput = document.getElementById("specialties")

  if (subjectsInput) {
    subjectsInput.value = subjects.join(",")
  }

  if (specialtiesInput) {
    specialtiesInput.value = subjects.join(",")
  }
}

// Enhanced form validation with better error handling
function validateRegistrationForm(form) {
  const inputs = form.querySelectorAll("input[required], select[required], textarea[required]")
  let isValid = true
  const errors = []

  inputs.forEach((input) => {
    const errorElement = document.getElementById(input.name + "-error")
    let errorMessage = ""

    // Clear previous errors
    if (errorElement) {
      errorElement.textContent = ""
    }
    input.style.borderColor = "var(--border-color)"

    // Required field validation
    if (!input.value.trim()) {
      errorMessage = "This field is required"
      isValid = false
    } else {
      // Specific validations
      switch (input.type) {
        case "email":
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
          if (!emailRegex.test(input.value)) {
            errorMessage = "Please enter a valid email address"
            isValid = false
          }
          break

        case "tel":
          const phoneRegex = /^[+]?[^\s][\d\s-]{6,}$/
          if (input.value && !phoneRegex.test(input.value.replace(/\s/g, ""))) {
            errorMessage = "Please enter a valid phone number"
            isValid = false
          }
          break

        case "password":
          if (input.value.length < 8) {
            errorMessage = "Password must be at least 8 characters long"
            isValid = false
          }
          break

        case "number":
          if (input.name === "hourlyRate") {
            const rate = Number.parseFloat(input.value)
            if (rate < 10 || rate > 200) {
              errorMessage = "Hourly rate must be between $10 and $200"
              isValid = false
            }
          }
          break
      }

      // Password confirmation
      if (input.name === "confirmPassword") {
        const password = form.querySelector('input[name="password"]')
        if (password && input.value !== password.value) {
          errorMessage = "Passwords do not match"
          isValid = false
        }
      }
    }

    // Display error
    if (errorMessage) {
      if (errorElement) {
        errorElement.textContent = errorMessage
      }
      input.style.borderColor = "var(--error-color)"
      errors.push(errorMessage)
    }
  })

  // Check terms acceptance
  const termsCheckbox = form.querySelector('input[name="terms"]')
  if (termsCheckbox && !termsCheckbox.checked) {
    showNotification("Please accept the Terms of Service and Privacy Policy", "error")
    isValid = false
  }

  return isValid
}

// Initialize page functionality
// Theme init (used by toggle later)
const savedTheme = localStorage.getItem("theme") || "light"
if (savedTheme === 'dark') {
  document.documentElement.classList.add('dark')
}

document.addEventListener("DOMContentLoaded", () => {
  // Set initial role from URL parameter
  const urlParams = new URLSearchParams(window.location.search)
  const roleParam = urlParams.get("role")
  if (roleParam && (roleParam === "student" || roleParam === "tutor")) {
    switchRole(roleParam)
  }

  // Password strength checking
  const passwordInput = document.getElementById("password")
  if (passwordInput) {
    passwordInput.addEventListener("input", function () {
      checkPasswordStrength(this.value)
    })
  }

  // Form submission handling
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      if (!validateForm(this)) {
        e.preventDefault()
      }
    })
  })

  // Mobile menu toggle
  const mobileToggle = document.querySelector(".mobile-menu-toggle")
  if (mobileToggle) {
    mobileToggle.addEventListener("click", toggleMobileMenu)
  }

  // Smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]')
  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href")
      if (!href || href === "#") return
      e.preventDefault()
      const target = document.querySelector(href)
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Auto-refresh dashboard data every 30 seconds
  if (window.location.pathname.includes("dashboard")) {
    setInterval(() => {
      // Trigger HTMX refresh for dynamic content
      const dynamicElements = document.querySelectorAll("[hx-get]")
      dynamicElements.forEach((element) => {
        if (element.getAttribute("hx-trigger") === "load") {
          if (window.htmx) {
            window.htmx.trigger(element, "load")
          }
        }
      })
    }, 30000)
  }

  // Language switcher
  const langButtons = document.querySelectorAll(".lang-btn")
  langButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.dataset.lang) switchLanguage(btn.dataset.lang)
    })
  })

  // Load saved language preference
  const savedLang = localStorage.getItem("preferred-language") || "en"
  switchLanguage(savedLang)

  // Search functionality
  const searchInput = document.querySelector(".search-input")
  const searchBtn = document.querySelector(".search-btn")

  if (searchBtn && searchInput) {
    searchBtn.addEventListener("click", () => {
      performSearch(searchInput.value)
    })
  }

  if (searchInput) {
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        performSearch(searchInput.value)
      }
    })
  }

  // Popular search tags
  const tagButtons = document.querySelectorAll(".tag-btn")
  tagButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      searchByTag(btn.textContent)
    })
  })

  // Smooth animations on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1"
        entry.target.style.transform = "translateY(0)"
      }
    })
  }, observerOptions)

  // Observe elements for animation
  const animateElements = document.querySelectorAll(".feature-card, .tutor-card, .testimonial-card")
  animateElements.forEach((el) => {
    el.style.opacity = "0"
    el.style.transform = "translateY(20px)"
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease"
    observer.observe(el)
  })

  // Initialize subject tags
  initializeSubjectTags()

  // Enhanced form validation for registration
  const registerForm = document.querySelector('form[hx-post="/api/register"]')
  if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
      if (!validateRegistrationForm(this)) {
        e.preventDefault()
      }
    })
  }

  // Phone number formatting
  const phoneInput = document.getElementById("phone")
  if (phoneInput) {
    phoneInput.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, "")
      if (value.length >= 10) {
        value = value.replace(/(\d{3})(\d{3})(\d{4})/, "($1) $2-$3")
      }
      e.target.value = value
    })
  }

  // Add theme toggle if not present
  const navContainer = document.querySelector(".nav-container")
  if (navContainer && !navContainer.querySelector(".theme-toggle")) {
    const toggleBtn = document.createElement("button")
    toggleBtn.type = "button"
    toggleBtn.className = "theme-toggle"
    toggleBtn.setAttribute("aria-label", "Toggle dark mode")
    const iconSpan = document.createElement("span")
    const labelSpan = document.createElement("span")
    labelSpan.textContent = savedTheme === "dark" ? "Dark" : "Light"
    iconSpan.textContent = savedTheme === "dark" ? "🌙" : "☀️"
    toggleBtn.append(iconSpan, labelSpan)

    navContainer.appendChild(toggleBtn)

    const updateToggleUi = () => {
      const isDark = document.documentElement.classList.contains("dark")
      labelSpan.textContent = isDark ? "Dark" : "Light"
      iconSpan.textContent = isDark ? "🌙" : "☀️"
    }

    toggleBtn.addEventListener("click", () => {
      document.documentElement.classList.toggle("dark")
      const mode = document.documentElement.classList.contains("dark") ? "dark" : "light"
      localStorage.setItem("theme", mode)
      updateToggleUi()
    })
  }
})

// HTMX event handlers
if (typeof document !== 'undefined') {
  document.addEventListener("htmx:beforeRequest", (event) => {
    // Show loading state
    const target = event.target
    if (target && target.classList && target.classList.contains("btn")) {
      target.style.opacity = "0.7"
      target.style.pointerEvents = "none"
    }
  })

  document.addEventListener("htmx:afterRequest", (event) => {
    // Hide loading state
    const target = event.target
    if (target && target.classList && target.classList.contains("btn")) {
      target.style.opacity = "1"
      target.style.pointerEvents = "auto"
    }

    // Handle form responses
    if (event.detail && event.detail.xhr && event.detail.xhr.status === 200) {
      const response = event.detail.xhr.responseText
      if (response.includes("success")) {
        // Redirect or show success message
        const form = target && target.closest ? target.closest("form") : null
        if (form) {
          if (form.getAttribute("hx-post") === "/api/login") {
            window.location.href = "dashboard-student.html"
          } else if (form.getAttribute("hx-post") === "/api/register") {
            window.location.href = "login.html"
          }
        }
      }
    }
  })
}

// Utility functions
function showNotification(message, type = "info") {
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`
  notification.textContent = message

  document.body.appendChild(notification)

  setTimeout(() => {
    notification.remove()
  }, 5000)
}

function formatDate(date) {
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date))
}

function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Declare htmx variable
const htmx = window.htmx


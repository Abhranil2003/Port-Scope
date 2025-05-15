document.addEventListener("DOMContentLoaded", () => {
  // Dark mode toggle with enhanced functionality
  const darkModeToggle = document.getElementById("darkModeToggle")
  const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)")

  // Function to set theme
  function setTheme(isDark) {
    if (isDark) {
      document.documentElement.classList.add("dark")
      localStorage.setItem("darkMode", "true")
    } else {
      document.documentElement.classList.remove("dark")
      localStorage.setItem("darkMode", "false")
    }
  }

  // Initialize theme based on saved preference or system preference
  function initializeTheme() {
    const savedTheme = localStorage.getItem("darkMode")

    if (savedTheme === "true") {
      setTheme(true)
    } else if (savedTheme === "false") {
      setTheme(false)
    } else {
      // No saved preference, use system preference
      setTheme(prefersDarkScheme.matches)
    }
  }

  // Call on page load
  initializeTheme()

  // Listen for theme toggle click
  darkModeToggle.addEventListener("click", () => {
    const isDarkMode = document.documentElement.classList.contains("dark")
    setTheme(!isDarkMode)
  })

  // Listen for system preference changes
  prefersDarkScheme.addEventListener("change", (e) => {
    // Only update if user hasn't set a preference
    if (!localStorage.getItem("darkMode")) {
      setTheme(e.matches)
    }
  })

  // Add a class to show the page after theme is set to prevent flash
  document.body.classList.add("theme-loaded")

  // Collapsible sections
  const sectionHeaders = document.querySelectorAll(".section-header")

  sectionHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const content = this.nextElementSibling
      const icon = this.querySelector(".fa-chevron-down")

      // Toggle the section
      if (content.style.maxHeight) {
        content.style.maxHeight = null
        icon.style.transform = "rotate(0deg)"
      } else {
        content.style.maxHeight = content.scrollHeight + "px"
        icon.style.transform = "rotate(180deg)"
      }
    })

    // Open all sections by default
    const content = header.nextElementSibling
    const icon = header.querySelector(".fa-chevron-down")
    content.style.maxHeight = content.scrollHeight + "px"
    icon.style.transform = "rotate(180deg)"
  })

  // Table sorting functionality
  const tableHeaders = document.querySelectorAll("th[data-sort]")

  tableHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const sortBy = this.getAttribute("data-sort")
      const table = this.closest("table")
      const tbody = table.querySelector("tbody")
      const rows = Array.from(tbody.querySelectorAll("tr"))

      // Get current sort direction
      const currentDir = this.getAttribute("data-direction") || "asc"
      const newDir = currentDir === "asc" ? "desc" : "asc"

      // Update sort direction
      tableHeaders.forEach((th) => th.setAttribute("data-direction", ""))
      this.setAttribute("data-direction", newDir)

      // Update sort icons
      tableHeaders.forEach((th) => {
        const icon = th.querySelector("i")
        icon.className = "fas fa-sort ml-1"
      })

      const icon = this.querySelector("i")
      icon.className = `fas fa-sort-${newDir === "asc" ? "up" : "down"} ml-1`

      // Sort the rows
      const columnIndex = Array.from(this.parentNode.children).indexOf(this)

      rows.sort((a, b) => {
        const aValue = a.children[columnIndex].textContent.trim()
        const bValue = b.children[columnIndex].textContent.trim()

        // Handle numeric sorting for port column
        if (sortBy === "port") {
          return newDir === "asc"
            ? Number.parseInt(aValue) - Number.parseInt(bValue)
            : Number.parseInt(bValue) - Number.parseInt(aValue)
        }

        // String comparison for other columns
        return newDir === "asc" ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
      })

      // Re-append rows in the new order
      rows.forEach((row) => tbody.appendChild(row))
    })
  })

  // Print functionality
  const printBtn = document.getElementById("printBtn")

  printBtn.addEventListener("click", () => {
    window.print()
  })
})

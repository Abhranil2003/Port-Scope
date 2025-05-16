document.addEventListener('DOMContentLoaded', function() {
  // Dark mode toggle
  const darkModeToggle = document.getElementById('darkModeToggle');
  
  // Check for saved theme preference or use system preference
  if (localStorage.getItem('darkMode') === 'true' || 
      (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  }
  
  darkModeToggle.addEventListener('click', function() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
  });
  
  // Collapsible sections
  const sectionHeaders = document.querySelectorAll('.section-header');
  
  sectionHeaders.forEach(header => {
    header.addEventListener('click', function() {
      const content = this.nextElementSibling;
      const icon = this.querySelector('.fa-chevron-down');
      
      // Toggle the section
      if (content.style.maxHeight) {
        content.style.maxHeight = null;
        icon.style.transform = 'rotate(0deg)';
      } else {
        content.style.maxHeight = content.scrollHeight + 'px';
        icon.style.transform = 'rotate(180deg)';
      }
    });
    
    // Open all sections by default
    const content = header.nextElementSibling;
    const icon = header.querySelector('.fa-chevron-down');
    content.style.maxHeight = content.scrollHeight + 'px';
    icon.style.transform = 'rotate(180deg)';
  });
  
  // Table sorting functionality
  const tableHeaders = document.querySelectorAll('th[data-sort]');
  
  tableHeaders.forEach(header => {
    header.addEventListener('click', function() {
      const sortBy = this.getAttribute('data-sort');
      const table = this.closest('table');
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      
      // Get current sort direction
      const currentDir = this.getAttribute('data-direction') || 'asc';
      const newDir = currentDir === 'asc' ? 'desc' : 'asc';
      
      // Update sort direction
      tableHeaders.forEach(th => th.setAttribute('data-direction', ''));
      this.setAttribute('data-direction', newDir);
      
      // Update sort icons
      tableHeaders.forEach(th => {
        const icon = th.querySelector('i');
        icon.className = 'fas fa-sort ml-1';
      });
      
      const icon = this.querySelector('i');
      icon.className = `fas fa-sort-${newDir === 'asc' ? 'up' : 'down'} ml-1`;
      
      // Sort the rows
      const columnIndex = Array.from(this.parentNode.children).indexOf(this);
      
      rows.sort((a, b) => {
        const aValue = a.children[columnIndex].textContent.trim();
        const bValue = b.children[columnIndex].textContent.trim();
        
        // Handle numeric sorting for port column
        if (sortBy === 'port') {
          return newDir === 'asc' 
            ? parseInt(aValue) - parseInt(bValue)
            : parseInt(bValue) - parseInt(aValue);
        }
        
        // String comparison for other columns
        return newDir === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      });
      
      // Re-append rows in the new order
      rows.forEach(row => tbody.appendChild(row));
    });
  });
  
  // Print functionality
  const printBtn = document.getElementById('printBtn');
  
  printBtn.addEventListener('click', function() {
    window.print();
  });

  // Add simple row highlighting on hover
  const tableRows = document.querySelectorAll('tbody tr');
  
  tableRows.forEach(row => {
    row.addEventListener('mouseover', function() {
      this.classList.add('bg-blue-50');
    });
    
    row.addEventListener('mouseout', function() {
      this.classList.remove('bg-blue-50');
    });
  });
  
  // Add print button functionality
  const printButton = document.createElement('button');
  printButton.textContent = 'Print Report';
  printButton.className = 'mt-4 mx-auto block bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded';
  
  printButton.addEventListener('click', function() {
    window.print();
  });
  
  document.querySelector('.container').appendChild(printButton);
});
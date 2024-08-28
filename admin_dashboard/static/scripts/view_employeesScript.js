function searchEmployees() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let table = document.getElementById("employeeTable");
  let rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    let cells = rows[i].getElementsByTagName("td");
    let name = cells[1].textContent.toLowerCase();
    if (name.indexOf(input) > -1) {
      rows[i].style.display = "";
    } else {
      rows[i].style.display = "none";
    }
  }
}

function sortTable(columnIndex) {
  let table = document.getElementById("employeeTable");
  let rows = Array.from(table.getElementsByTagName("tr")).slice(1);
  let ascending = table.getAttribute("data-sort-order") === "asc";

  rows.sort((a, b) => {
    let cellA = a.getElementsByTagName("td")[columnIndex].textContent.trim();
    let cellB = b.getElementsByTagName("td")[columnIndex].textContent.trim();

    // Check if the column contains numeric values
    if (!isNaN(cellA) && !isNaN(cellB)) {
      cellA = parseFloat(cellA);
      cellB = parseFloat(cellB);
      return ascending ? cellA - cellB : cellB - cellA;
    }

    // Default to string comparison for non-numeric values
    if (cellA < cellB) return ascending ? -1 : 1;
    if (cellA > cellB) return ascending ? 1 : -1;
    return 0;
  });

  for (let row of rows) {
    table.getElementsByTagName("tbody")[0].appendChild(row);
  }

  table.setAttribute("data-sort-order", ascending ? "desc" : "asc");
}
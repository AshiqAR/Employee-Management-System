function searchEmployee() {
    var input, filter, table, rows, cells, i, j, txtValue;
    input = document.getElementById("employee_search");
    filter = input.value.toLowerCase();
    table = document.getElementById("employee-list");
    rows = table.getElementsByTagName("tr");

    for (i = 0; i < rows.length; i++) {
      cells = rows[i].getElementsByTagName("td");
      for (j = 0; j < cells.length; j++) {
        if (cells[j]) {
          txtValue = cells[j].textContent || cells[j].innerText;
          if (txtValue.toLowerCase().indexOf(filter) > -1) {
            rows[i].style.display = "";
            break;
          } else {
            rows[i].style.display = "none";
          }
        }
      }
    }
  }

  function saveAttendance(employeeId) {
    employeeId = parseInt(employeeId);
    console.log("Saving attendance for employee ID:", employeeId);
    console.log("data : ", {
      attendance_status: document.querySelector(
        `select[name="attendance_status_${employeeId}"]`
      ).value,
      overtime_hours: document.querySelector(
        `input[name="overtime_hours_${employeeId}"]`
      ).value,
    });
    // You can use AJAX or a form submission to handle the save action
  }
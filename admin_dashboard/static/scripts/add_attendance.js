function createAttendanceForm(employee, attendance) {
  const date = document.getElementById('attendance_date').value;
  const form = document.getElementById('attendance-forms-container').appendChild(document.createElement('form'));
  console.log(form);
  form.setAttribute('class', 'attendance-form');
  form.setAttribute('method', 'POST');
  form.innerHTML = `
      <h3>${employee.first_name} ${employee.last_name}</h3>
      <p>ID: ${employee.employee_id}</p>
      <p>Designation: ${employee.designation}</p>
      <p>Department: ${employee.department.department_name}</p>

      <div class="attendance-form">
          <label for="attendance_type_${employee.employee_id}">Attendance Type:</label>
          <select id="attendance_type_${employee.employee_id}" name="attendance_type_${employee.employee_id}">
              <option value="Present" ${attendance.attendance_type === 'Present' ? 'selected' : ''}>Present</option>
              <option value="Absent" ${attendance.attendance_type === 'Absent' ? 'selected' : ''}>Absent</option>
              <option value="Leave" ${attendance.attendance_type === 'Leave' ? 'selected' : ''}>Leave</option>
          </select>
      </div>
  `;
  return form;
}

function getAttendance() {
  const date = document.getElementById('attendance_date').value;

  const baseUrl = '{% url "apis:get_attendance_by_date" date="DATE_PLACEHOLDER" %}';
  const fetchUrl = baseUrl.replace('DATE_PLACEHOLDER', date);

  fetch(fetchUrl)
      .then(response => response.json())
      .then(data => {
          if (data.length > 0) {
              data.forEach(attendance_data => {
                  const employee = attendance_data.employee;
                  const attendance = attendance_data.attendance;

                  const form = createAttendanceForm(employee, attendance);
                  container.appendChild(form);
              });
          } else {
              alert('No attendance data found for the selected date.');
          }
      })
      .catch(error => {
          console.error('Error fetching attendance data:', error);
      });
}

document.addEventListener('DOMContentLoaded', () => {
  getAttendance();
  document.getElementById('attendance_date').addEventListener('change', getAttendance);
});
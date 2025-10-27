
//Profile Dropdown 
const avatar = document.getElementById("user-avatar")
avatar.addEventListener("click",()=>{
  drodw = document.getElementById("profile-dropdown")
 
  console.log(drodw.classList.toggle('show'))
  console.log(drodw.classList)
})
// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}


function openUploadModal() {
    document.getElementById('uploadModal').style.display = 'block';
}

function closeUploadModal() {
    document.getElementById('uploadModal').style.display = 'none';
}

// Show/hide student selection based on visibility choice
document.addEventListener('change', function(e) {
    if (e.target.matches('select[class="form-input"]') && e.target.previousElementSibling.textContent === 'Visibility') {
        const studentSelection = document.getElementById('studentSelection');
        if (e.target.value === 'private') {
            studentSelection.style.display = 'block';
        } else {
            studentSelection.style.display = 'none';
        }
    }
});
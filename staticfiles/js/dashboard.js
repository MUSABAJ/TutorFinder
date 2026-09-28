checkDevice()

function checkDevice(){ 
  const isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent)
  const isPortrait = window.innerHeight > window.innerWidth

  if (isMobile && isPortrait) {
    const overlay = document.createElement('div')
    overlay.innerHTML = `
    <style>
        #rotatePrompt {
            position: fixed;
            top:0; left:0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            color: whitesmoke;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 99999;
            text-align: center;
            padding: 1rem;
        }
            .rotateIcon{
            color: white;
            }
        
    </style>
    <div class='rotateIcon'><i class="fa-solid fa-computer"></i></div>
    <h1>Screen width too small</h1>
    <h3>Plsease increase the window size or rotate to load.</h3>
    <p>If you are on a mobile phone, please open on a desktop.</p>
    
    `
    overlay.id='rotatePrompt';
    document.body.appendChild(overlay);
    function checkOrientation(){
      if (window.innerHeight < innerWidth){
        overlay.remove();
        window.removeEventListener('resize', checkOrientation)
      }
    }
        window.addEventListener('resize', checkOrientation)
  
  }
}


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
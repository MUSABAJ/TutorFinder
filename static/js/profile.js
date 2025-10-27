
function showTutorTab(tabName) {
         const tabContetns = document.querySelectorAll('.profile-view-tab')
        tabContetns.forEach(content => content.classList.remove('active'))

        const tabBtns = document.querySelectorAll('.profile-tab');
        tabBtns.forEach(btn => btn.classList.remove('active'));

        document.getElementById(tabName).classList.add('active')
        event.target.classList.add('active')

}

function showProfileTab(tabName, evt) {
 
        const tabContetns = document.querySelectorAll('.tab-content')
        tabContetns.forEach(content => content.classList.remove('active'))

        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => btn.classList.remove('active'));

        const target = document.getElementById(tabName)
        
        document.getElementById(tabName).classList.add('active')
        event.target.classList.add('active')}
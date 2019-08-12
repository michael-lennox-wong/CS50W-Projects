document.addEventListener('DOMContentLoaded', () => {
  // Get display name
  const username = localStorage.getItem('display_name');

  // Display the user at bottom of page
  document.querySelector('#user_display').innerHTML = username;

  // Set value in hidden form to be the user, in case we need to send this
  // info to the server
  document.querySelector('#user_id').value = username;
  document.querySelector('#my_msgs').value = username;

  // Default the submit button to be disabled
  document.querySelector('#ncnsub').disabled=true;

  // Enable button only if there is text in field
  document.querySelector('#ncn').onkeyup = () => {
    if (document.querySelector('#ncn').value.length > 0)
      document.querySelector('#ncnsub').disabled=false;
    else
      document.querySelector('#ncnsub').disabled=true;
  };
  // logout procedure
  document.querySelector('#logout').onclick = () => {
    localStorage.removeItem('display_name');
    localStorage.removeItem('last_channel');
    window.location.href="/";
  };

})

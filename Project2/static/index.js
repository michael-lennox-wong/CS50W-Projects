document.addEventListener('DOMContentLoaded', () => {
  // Here we check if there is a username in localStorage.  If so, then we go to
  // to the list of channels, otherwise we go to the login page
  // urls are hard-coded, this should be changed later
  if (localStorage.getItem('display_name') === null) {
    document.write('It looks like you are not yet signed in.<br><a href="/get_display_name">Choose a display name</a>');
  }
  else {
    const disp_name = localStorage.getItem('display_name');
    if (localStorage.getItem('last_channel') === null) {
      document.write(`It looks like you are already signed in as ${disp_name}.<br><a href="/channels">Go to the list of channels</a>`);
    }
    else {
      window.location.href="/channels/"+localStorage.getItem('last_channel');
    }
  }
})

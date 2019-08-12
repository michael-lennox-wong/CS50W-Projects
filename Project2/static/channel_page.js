document.addEventListener('DOMContentLoaded', () => {
  // Set a variable with the user's display name
  const user_j = localStorage.getItem('display_name');

  // Display the display name
  document.querySelector('#user_display').innerHTML = user_j;

  // Set a variable with the channel name
  const chan_name_j = document.querySelector('#channel_name').innerHTML;

  // Store channel name so that one is redirected when one goes back to app
  localStorage.setItem('last_channel', chan_name_j)

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // By default, submit button is disabled
  document.querySelector('#task_submit').disabled = true;

  // Enable button only if there is text in the input field
  document.querySelector('#task').onkeyup = () => {
    if (document.querySelector('#task').value.length > 0)
      document.querySelector('#task_submit').disabled = false;
    else
      document.querySelector('#task_submit').disabled = true;
  };

  // procedure for transmitting a message
  document.querySelector('#new-task').onsubmit = () => {

    // When a message is submitted, we must take it and emit it to the
    // relevant function in application.py
    const msg_j = document.querySelector('#task').value;
    const time_j = Math.round(Date.now()/1000);
    const msg_bdl_j = {'msg': msg_j,
                       'time': time_j,
                       'user': user_j,
                       'chan': chan_name_j }
    socket.emit('task_msg', msg_bdl_j);

    // clean up THE message field
    document.querySelector('#task').value = '';
    document.querySelector('#task_submit').disabled = true;

    // We need the following so that we don't have a post request
    return false;
  };

  // procedure for when message is received
  socket.on('get_msg', sent_msg => {
    const new_msg_chan_j = sent_msg.chan;
    // Only want message to appear in this channel if it was sent from the
    // same channel
    if (new_msg_chan_j === chan_name_j) {
      const new_msg_j = sent_msg.msg;
      const new_msg_user_j = sent_msg.user;
      const new_msg_time_j = sent_msg.time;

      // create new list item, write the broadcasted message to that item and
      // append that list item to the lsit of messages
      const li = document.createElement('li');
      li.innerHTML = new_msg_j + "<br><small>" + new_msg_user_j + ", " + new_msg_time_j + "</small>";
      document.querySelector('#msg_list').append(li);
    }
  });

  document.querySelector('#logout').onclick = () => {
    localStorage.removeItem('display_name');
    localStorage.removeItem('last_channel');
    window.location.href="/";
  };

  document.getElementById('go_back').onclick = () => {
    localStorage.removeItem('last_channel');
  }
});

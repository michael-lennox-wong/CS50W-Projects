import os

from flask import Flask, url_for, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channel_list = []
channels = {}

channel_list.append('Test')
# We store messages in triples:  first element is text of message, second is the
# user, third is the timestamp
channels['Test'] = [ ('First test message', 'user1', 555), ('Reply to first test message', 'user2', 565)]

messages = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/channels", methods = ["post", "get"])
def ch_list():
    """ This displays the list of channels.  A 'post' request should be coming
    from the page itself, when one creates a channel.  In this case, we need to
    update the list of channels above.  A 'get' request should just display the
    list of channels
    """
    if request.method == "GET":
        return render_template("channel_list.html", chan_list=channel_list)

    if request.method == "POST":
        new_ch = request.form.get("new_chan_name")
        if not( new_ch in channel_list ):
            channel_list.append(new_ch)
            channels[new_ch] = []
            return render_template("channel_list.html", chan_list=channel_list)
        else:
            err_msg = 'That channel name already exists'
            return render_template("channel_list.html", chan_list=channel_list, err=err_msg)

@app.route("/get_display_name", methods = ["post", "get"])
def get_disp_name():
    return render_template("get_disp_name.html")

@app.route("/channels/<string:channel_name>")
def go_to_channel(channel_name):
    """This is the page for a given channel:  it will contain the list of
    messages as well as a link to return to the list of channels
    """
    return render_template("channel_page.html", channel = channel_name, msg_list_pj = channels[channel_name])

def get_messages(user):
    msg_dict = {}
    for ch in channel_list:
        msg_dict[ch] = []
        for m in channels[ch]:
            if m[1] == user:
                msg_dict[ch].append(m)
    return(msg_dict)

@app.route("/my_messages", methods = ["post"])
def see_my_messages():
    """ This retrieves the complete list of the messages the user has submitted
    """
    user = request.form.get("name_in_storage")
    msg_bdl = get_messages(user)
    return render_template("my_messages.html", user_msgs_j = msg_bdl, channels=channel_list)


#@app.route("/testchannel")
#def tc():
#    return render_template("testchannel.html")

@socketio.on('task_msg')
def relay_msg(msg_p):
    new_msg_p = (msg_p["msg"], msg_p["user"], msg_p["time"])
    ch = msg_p["chan"]
    channels[ch].append(new_msg_p)
    emit('get_msg', msg_p, broadcast=True)

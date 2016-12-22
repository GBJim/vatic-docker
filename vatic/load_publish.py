from subprocess import call, check_output
import json
import re
import jinja2
users = ["Debbie", "Wen-Ling"]


def generate_admin(users, URLS, URL_padding=16 ):
    template_loader = jinja2.FileSystemLoader( searchpath="/root/vatic/public/admin/" )
    template_env = jinja2.Environment( loader=template_loader)
    template = template_env.get_template("template.html")
    print("\n\nHi!\n\n")
    w = open("/root/vatic/public/admin/index.html", 'w')
    w.write(template.render(hi="Y"))
    #print(template_env.render(hi="May the force be with you"))
    w.close()

    #Environment().from_string(HTML).render(user_map=user_map)



def generate_JS(user_map, URL_padding=16, output_path="./public/URL_map.js"):
    URL_profiles = []

    for user in user_map:
        for assignment in user_map[user]:
            for url in user_map[user][assignment]:

                profile = {"user":user, "assignment":assignment, "url":url}
                URL_profiles.append(profile)

    next_URL = {}
    previous_URL = {}
    #print(URL_profiles)
    for i, profile in enumerate(URL_profiles):
        url_id = re.search(r'\d+', profile["url"]).group()
        last_profile = None if i==0 else URL_profiles[i-1]
        next_profile = None if i>=len(URL_profiles)-1 else URL_profiles[i+1]

        if last_profile and last_profile["user"] == profile["user"]:
            previous_URL[url_id] = last_profile["url"][URL_padding:]
        else:
            previous_URL[url_id] = "head"

        if next_profile and next_profile["user"] == profile["user"]:
            next_URL[url_id] = next_profile["url"][URL_padding:]
        else:
            previous_URL[url_id] = "end"

    w = open(output_path, "w")
    w.write("var previous_URL = {};\n".format(json.dumps(previous_URL)))
    w.write("var next_URL = {};\n".format(json.dumps(next_URL)))
    w.close()



def render_template(user_map,URL_padding=16 ,output_path="./public/directory/index.html"):


    for user in user_map:
        counter = 0
        for assignment in user_map[user]:
            for i,url in enumerate(user_map[user][assignment]):
                counter += 1
                print(url)
                user_map[user][assignment][i] = {"url":url[URL_padding:], "count":counter}





    HTML = """
    <html>
    <head>
    <title>Iron Yun Vatic Server</title>
    </head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
     <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css">
    <body>

    <div class="text-center panel list-group">
        {% for user in user_map %}

            <a href="#" data-parent="#menu" class="list-group-item" data-toggle="collapse" data-target="#{{user}}"><h2>{{  user }} <span class = "glyphicon glyphicon-collapse-down" /></h2></a>
            <div id={{user}} class="panel collapse">
                {%for assignment in user_map[user]%}
                    <a href="#" data-toggle="collapse" data-target="#{{user}}-{{assignment | replace("_","-") | replace(".","-")}}"><h3>{{assignment}} <span class = "glyphicon glyphicon-collapse-down" /></h3></a>
                    <div id="{{user}}-{{assignment | replace("_","-") | replace(".","-")}}" class="collapse" data-parent="#{{user}}">
                        <ul class="list-group">
                        {% for url in user_map[user][assignment] %}
                            <li><a href={{url.url}}>{{user}}'s Segment:{{url.count}} </a></li>
                        {% endfor %}
                        </ul>
                    </div>
                {% endfor %}
            </div>
            {% endfor %}
    </div>

    </body>
    </html>


    """

    w = open(output_path, "w")
    w.write(jinja2.Environment().from_string(HTML).render(user_map=user_map))
    w.close()









for user in users:
    command = ["bash", "/root/vatic/load_video.sh", user]
    print(" ".join(command))
    call(command)

#publsh the video
command = ["turkic", "publish", "--offline"]
check_output(command)
command = ["turkic", "list", "--detail"]
call(command)
user_map = json.load(open("data/user_map.json"))


for user in user_map:
    print(user)
    for assignment in user_map[user]:
        print("\t" + assignment)


generate_JS(user_map)
render_template(user_map)

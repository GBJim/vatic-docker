from subprocess import call, check_output
import json

import jinja2
users = ["Debbie", "Wen-Ling", "John-Doe", "Yeah-yeah","Da-Da"]


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



def generate_JS(users, URLs, URL_padding=16, output_path="./public/URL_map.js"):
    K = len(URLs)/len(users)
    next_URL = {}
    previous_URL = {}

    for i, _ in enumerate(URLs):
        if i % K == 0:

            previous_URL[i+1] = "head"
            next_URL[i+1] = URLs[i+1][URL_padding:]

        elif i % K == K-1:
            previous_URL[i+1] = URLs[i-1][URL_padding:]
            next_URL[i+1] = "end"
        else:
            previous_URL[i+1] = URLs[i-1][URL_padding:]
            next_URL[i+1] = URLs[i+1][URL_padding:]
        #print(previous_URL[1])


    w = open(output_path, "w")
    w.write("var previous_URL = {};\n".format(json.dumps(previous_URL)))
    w.write("var next_URL = {};\n".format(json.dumps(next_URL)))
    w.close()

def render_template(user_map,output_path="./public/directory/index.html"):
    HTML = """
    <html>
    <head>
    <title>Iron Yun Vatic Server</title>
    </head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css">
    <body>
    <div class="text-center">
    {% for single_map in user_map %}

    <h2>{{  single_map.user }}</h2>
    <ul class="list-group">
    {% for URL in single_map.URLs %}
      <li><a href={{URL.URL}}>{{ single_map.user}}'s Segment: {{URL.count}}</a>
      </li>

    {% endfor %}

    </ul>

    {% endfor %}
    </div>
    </body>
    </html>


    """

    w = open(output_path, "w")
    w.write(jinja2.Environment().from_string(HTML).render(user_map=user_map))
    w.close()

def get_user_map(users, URLs, URL_padding = 16):

    K = len(URLs)/len(users)
    user_map = []
    for i, user in enumerate(users):
        single_map = {"user":user}
        URL_map = []
        for URL_count, URL in enumerate(URLs[i*K:(i+1)*K]):
            URL_map.append({"count":URL_count+1, "URL": URL[URL_padding :]})
        single_map["URLs"] = URL_map

        user_map.append({"user":user, "URLs":URL_map})
    return user_map





    URL_map_flat = [{"URL":URL, "user":URL_map[URL]} for URL in sorted(URL_map.keys()) ]
    print(URL_map_flat)
    w = open(output_path, "w")
    w.write(Environment().from_string(HTML).render(URL_maps=URL_map_flat))
    w.close()


for user in users:
    command = ["bash", "/root/vatic/load_video.sh", user]
    print(" ".join(command))
    call(command)

#publsh the video
command = ["turkic", "publish", "--offline"]
URLs = check_output(command).strip().split("\n")

if len(URLs) == 0 or (len(URLs) % len(users)) != 0:
    print("Dman son, something is wrong!")
    print("URLs: {}, Users:{}".format(len(URLs), len(users)))
    raise()



#K is the number of video per user


user_map = get_user_map(users, URLs)
generate_JS(users, URLs)
render_template(user_map)
generate_admin(users, URLs)

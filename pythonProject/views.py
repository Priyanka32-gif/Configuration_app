'''from flask import Flask, render_template, request, jsonify
from pythonProject.config_data import get_json_data

app = Flask(__name__)

@app.route('/')
def index():
    pass_data = get_json_data()
    pass_data.get_file_path()
    load_config = pass_data.load_server_config()
    terminal_name_list = pass_data.terminal_names
    return render_template('index.html', terminal_name_list=terminal_name_list)

@app.route('/get_content', methods=['POST'])
def get_content():
    terminal_name = request.form.get('terminal_name')
    # Fetch content based on the selected terminal_name (modify as needed)
    content = f"Content for {terminal_name}"
    return jsonify(content)

@app.route('/main', methods=['GET','POST'])
def main():
    if request.method == 'POST':
        name = request.form.get('name')
        server = request.form.get('server')
        share = request.form.get('share')
        dest = request.form.get('destination')
        path = request.form.get('path')
        progress = request.form.get('progress')
        tmp_path = request.form.get('temporary_path')
        file_pattern = request.form.get('file_pattern')
        root = request.form.get('root')
        terminal_name = request.form.get('terminal_name')

        username = request.form.get('username') or None
        password = request.form.get('password') or None
        ftp_username = request.form.get('ftp_username') or None
        ftp_password = request.form.get('ftp_password') or None
        ftp_host = request.form.get('ftp_host') or None

        pass_data = get_json_data()
        pass_data.get_data(name,server,share,dest,path,progress,tmp_path,file_pattern,root, terminal_name,username,password,ftp_username,ftp_password,ftp_host)
        pass_data.save_config()
        terminal_name_list = pass_data.terminal_names
        return render_template('index.html', terminal_name_list=terminal_name_list)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=7000)
    '''
# myapp/views.py
import os
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from pythonProject.config_data import get_json_data
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file


def index(request):
    pass_data = get_json_data()
    pass_data.get_file_path()
    pass_data.load_server_config()
    terminal_name_list = pass_data.terminal_names
    return render(request, 'index.html', {'terminal_name_list': terminal_name_list})


def get_content(request):
    if request.method == 'POST':
        with open(os.path.join(BASE_DIR, 'config.json'), 'r') as file:
            data = json.load(file)

        # Get terminal_names and server_configs from JSON data
        terminal_names = data.get('terminal_names', [])
        server_configs = data.get('server_configs', [])

        # Get terminal_name from request
        terminal_name = request.POST.get('terminal_name')

        # Find index of terminal_name in terminal_names
        try:
            index = terminal_names.index(terminal_name)
        except ValueError:
            return HttpResponse(status=404, content='Terminal name not found')

        # Get server config based on index
        if 0 <= index < len(server_configs):
            content = server_configs[index]
            return JsonResponse({'content': content})
        else:
            return HttpResponse(status=404, content='Server config not found')

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def removeTerminal(request):
    if request.method == "POST":
        try:
            terminal_name = request.POST.get('terminal_name')

            # Open and load the config file
            with open(os.path.join(BASE_DIR, 'config.json'), 'r') as file:
                data = json.load(file)

            terminal_names = data.get('terminal_names', [])
            server_configs = data.get('server_configs', [])

            # Find index of terminal_name in terminal_names
            try:
                index = terminal_names.index(terminal_name)
            except ValueError:
                return HttpResponse(status=404, content='Terminal name not found')

            # Remove the corresponding configuration
            del terminal_names[index]
            del server_configs[index]

            # Save the updated dictionary back to the JSON file
            with open(os.path.join(BASE_DIR, 'config.json'), 'w') as file:
                json_data = {"server_configs": server_configs,
                             "terminal_names": terminal_names}
                json.dump(json_data, file, indent=2)

            # Return success response
            return redirect('main', {'success': 'Terminal removed successfully'})

        except FileNotFoundError:
            # Handle file not found error
            return JsonResponse({'error': 'Config file not found'}, status=400)

        except json.decoder.JSONDecodeError:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid JSON format in config file'}, status=400)

        except Exception as e:
            # Handle other exceptions
            print("Error:", str(e))
            return JsonResponse({'error': 'Internal server error'}, status=500)

    else:
        # Return error response for invalid request method
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def main(request):

    if request.method=="GET":
        with open(os.path.join(BASE_DIR, 'config.json'), 'r') as file:
            data = json.load(file)

        # Get terminal_names and server_configs from JSON data
        terminal_names = data.get('terminal_names', [])
        return render(request, 'index.html', {'terminal_name_list': terminal_names})

    elif request.method == 'POST':
        if (request.POST.get('add_edit_btn')) or (request.POST.get('saveConfig')):

            name = request.POST.get('name')
            server = request.POST.get('server')
            share = request.POST.get('share')
            dest = request.POST.get('destination')
            path = request.POST.get('path')
            progress = request.POST.get('progress')
            tmp_path = request.POST.get('temporary_path')
            file_pattern = request.POST.get('file_pattern')
            root = request.POST.get('root')
            terminal_name = request.POST.get('terminal_name')

            username = request.POST.get('username') or None
            password = request.POST.get('password') or None
            ftp_username = request.POST.get('ftp_username') or None
            ftp_password = request.POST.get('ftp_password') or None
            ftp_host = request.POST.get('ftp_host') or None

            pass_data = get_json_data()
            pass_data.get_data(name, server, share, dest, path, progress, tmp_path, file_pattern, root, terminal_name,
                               username, password, ftp_username, ftp_password, ftp_host)
            pass_data.save_config()
            terminal_name_list = pass_data.terminal_names
            return render(request, 'index.html', {'terminal_name_list': terminal_name_list})

        elif (request.POST.get('removeTerminal')):
            pass_data = get_json_data()
            terminal_name_list = pass_data.terminal_names
            return render(request, 'index.html', {'terminal_name_list': terminal_name_list})

    return (index(request))













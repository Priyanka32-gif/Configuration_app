import json
import os
from django.http import JsonResponse

class get_json_data:

     def get_data (self, name=None, server=None, share=None, dest=None, path=None, progress=None, tmp_path=None,
                   file_pattern=None, root=None, terminal_name=None, username=None, password=None, ftp_username=None,
                   ftp_password=None, ftp_host=None):

         self.name = name
         self.server = server
         self.share = share
         self.dest = dest
         self.path = path
         self.progress = progress
         self.tmp_path = tmp_path
         self.file_pattern = file_pattern
         self.root = root

         self.terminal_name = terminal_name

         self.username = username
         self.password = password
         self.ftp_username = ftp_username
         self.ftp_password = ftp_password
         self.ftp_host = ftp_host

         self.config_data = {
             "name": self.name,
             "server": self.server,
             "share": self.share,
             "dest": self.dest,
             "path": self.path,
             "progress": self.progress,
             "tmp_path": self.tmp_path,
             "file_pattern": self.file_pattern,
             "root": self.root
             }

     def get_file_path(self):
         script_dir = os.path.dirname(os.path.realpath(__file__))
         self.json_file_path = os.path.join(script_dir, 'config.json')

     def save_config(self):
         self.get_file_path()
         self.load_server_config()
         self.append_terminal_data(self.config_data, self.terminal_name)
         self.save_to_json()

     def load_server_config(self):
         try:
             with open(self.json_file_path, 'r') as file:
                 data = json.load(file)
                 self.server_configs = data.get('server_configs', [])
                 self.terminal_names = data.get('terminal_names', [])
         except FileNotFoundError:
             self.server_configs = []
             self.terminal_names = []

         return self

     def append_terminal_data(self, terminal_data, terminal_name):
         if terminal_name in self.terminal_names:
             # Find index of terminal_name in terminal_names
             try:
                 index = self.terminal_names.index(terminal_name)
                 # Update server config based on index
                 if 0 <= index < len(self.server_configs):
                     self.server_configs[index] = terminal_data
             except ValueError:
                 return JsonResponse({'error': 'Invalid terminal name'}, status=400)
         else:
             self.server_configs.append(terminal_data)
             self.terminal_names.append(terminal_name)

     def save_to_json(self):
         with open(self.json_file_path, 'w') as file:
             json_data = {"server_configs": self.server_configs,
                          "terminal_names": self.terminal_names}
             if (
                     self.username is not None and
                     self.password is not None and
                     self.ftp_username is not None and
                     self.ftp_password is not None and
                     self.ftp_host is not None
             ):
                 json_data.update({
                     "username": self.username,
                     "password": self.password,
                     "ftp_username": self.ftp_username,
                     "ftp_password": self.ftp_password,
                     "ftp_host": self.ftp_host
                 })
             else:
                 # Add default values if any of the fields is None
                 json_data.update({
                     "username": self.username or "PCBLCard",
                     "password": self.password or "*123456#PCBL",
                     "ftp_username": self.ftp_username or "Gokyo",
                     "ftp_password": self.ftp_password or "Goky0#2023@",
                     "ftp_host": self.ftp_host or "10.20.101.12:2121"
                 })

             json.dump(json_data,file, indent=2)

     def load_config_data(self,selected_index):
             if 0 <= selected_index < len(self.server_configs):
                 config = self.server_configs[selected_index]
                 return config










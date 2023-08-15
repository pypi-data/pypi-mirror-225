import bobj


r = bobj.BOValidation("bobj_url", username = "R", password="pass",auth_type = "SecLDAP")

user_list = r.list_users()
folder_list = r.list_folders()
group_list = r.list_groups()
server_list = r.list_server()


import base64
with open("./imageBack\default-avatar.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string)
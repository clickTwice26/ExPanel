def server_create(token):
    print("")
    print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Hosting</title>
</head>
<body>
    <form enctype="multipart/form-data" method="post" action="/cgi-bin/server.py">
        <label for="port">Port:</label>
        <input type="text" name="port" id="" placeholder="Enter your port"><br>
        <label for="server_selection">Select Your Server</label>
        <select name="server_selection" id="">
            <option value="NodeJs">NodeJs</option>
            <option value="Apache">Apache</option>
            <option value="Python">Python</option>
            <option value="Others">Others</option>
        </select>
        <br>
        <label for="files">Upload your server files:</label>
        <input type="file" name="file" id="">
        <br>
        <label for="">Nickname:</label>
        <input type="text" name="nickname" id="">
        <br>
          <input type="text" name="token" value="{token}" hidden>
        <input type="submit" value="Create a Server">
    </form>
</body>
</html>










""")
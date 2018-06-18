import urllib.parse
import urllib.request
 
url = "http://pastebin.com/api/api_post.php"
values = {'api_option' : 'paste',
          'api_dev_key' : 'e6b82cd9075ca0aa6971f40c7c6dde26',
          'api_paste_code' : 'dank python create paste test kappa',
          'api_paste_private' : '0',
          'api_paste_name' : '\'Tis a paste.',
          'api_paste_expire_date' : 'N',
          'api_paste_format' : 'python',
          }
 
data = urllib.parse.urlencode(values)
data = data.encode('utf-8') # data should be bytes
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
   the_page = response.read()
print(the_page)

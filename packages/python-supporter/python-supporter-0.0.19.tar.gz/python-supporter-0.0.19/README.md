# python-supporter

https://pypi.org/project/python-supporter
<pre>
pip install python-supporter
</pre>

```
from python_supporter import logging

logging.basicConfig(logging.ERROR)
#logging.basicConfig(logging.INFO)
#logging.basicConfig(logging.DEBUG)
#logging.basicConfig()
#logging.basicConfig(logging.ERROR, filename='log.txt')
#logging.basicConfig(logging.INFO, filename='log.txt')
#logging.basicConfig(logging.DEBUG, filename='log.txt')
#logging.basicConfig(filename='log.txt')

logging.error('This is error message') #2023-03-19 22:36:47: ERROR: This is error message
logging.info('This is info message')
logging.debug('This is debug message')
```

```
import python_supporter

text = python_supporter.file.read_file(file)
python_supporter.file.write_file(file, text)
```

```
import python_supporter

chrome_debugger_address = "127.0.0.1:1001"
li = chrome_debugger_address.split(":")
remote_debugging_port = int(li[1])
remote_debugging_address = li[0]

port_opened = python_supporter.socket.check_port_open(remote_debugging_address, remote_debugging_port)
```

```
from python_supporter.file import read_binary_file
from python_supporter.file import write_binary_file

source_image = read_binary_file("./assets/source.png")
driving_video = read_binary_file("./assets/driving.mp4")

source_image = "source_image.png"
write_binary_file(source_image, inputs["source_image"])
driving_video = "driving_video.mp4"
write_binary_file(driving_video, inputs["driving_video"])
```

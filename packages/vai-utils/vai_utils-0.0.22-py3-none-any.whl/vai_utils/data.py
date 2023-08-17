import requests
import json
import sys

python_base_url = "http://199.88.191.194:5007"
node_base_url = "http://199.88.191.194:5008"

# TODO missing return schemas for all the functions
# For instance:

# >>> from vai_utils import data
# >>> html = '<h1>Hello World</h1>'
# >>> data.html_to_json(html)
# <<< {
# <<<    "header": "Hello World"
# <<< }

# or equivalent, based on whatever the function actually returns

def eprint(content):
    print(content, flush=True)
    return True

def html_to_json(html):
    """
    Convert html format into json format.
    To use this method we are calling "http://199.88.191.194:5008" server. 
    It will convert the html format into json format.
    
    :param html: The html passed in the function is a string representing
        html format from which you want to retrieve the json content.
    :type html: str
    :returns: JSON represented as a Python dict.

    :example:

    >>> from vai_utils import data
    >>> html = '<h1>Hello World</h1>'
    >>> data.html_to_json(html)
    """
    request_url = node_base_url + "/html-to-json"
    headers = {"Authorization": "25hD6Fpava"}
    payload = json.dumps({ 
        "html": html
    })
    response = requests.post(request_url, data=payload, headers=headers)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res

def json_to_html(jsonData):
    """
    Convert json format into html format.
    To use this method we are calling "http://199.88.191.194:5008" server.
    It will convert the json format into html format.
    
    :param jsonData: A string representing json format from which you want to
        retrieve the html content.
    :type jsonData: str
    :returns: HTML corresponding to the input.

    :example:

    >>> from vai_utils import data
    >>> json = {
            'age':22
        }
    >>> data.json_to_html(json)
    """
    request_url = node_base_url + "/json-to-html"
    headers = {"Authorization": "25hD6Fpava"}
    payload = json.dumps({ 
        "json": jsonData
    })
    response = requests.post(request_url, data=payload, headers=headers)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def get_url_to_html(url):
    """
    Get html of a given url.
    To use this method we are calling "http://199.88.191.194:5008" server.
    It will convert the given url's html into our html format.

    :param url: Web URL from which you want to retrieve the HTML content.
    :type url: str
    :returns: HTML off the URL.

    :example:
    
    >>> from vai_utils import data
    >>> URL= 'https://dev-cloud.virtuousai.com/meta.json'
    >>> data.get_url_to_html(URL)
    """
    request_url = node_base_url + "/convert?url="+url
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def get_url_to_json(url):
    """
    This method is used to get json of given url.
    To use this method we are calling "http://199.88.191.194:5008" server.
    It will convert the given url's json into our json format.

    :param url: A web URL from which you want to retrieve the JSON content.
    :type url: str
    :returns: JSON off the URL.

    :example:

    >>> from vai_utils import data
    >>> URL = 'https://www.google.com'
    >>> data.get_url_to_json(URL)
    """
    request_url = node_base_url + "/convert?url="+url+"&json=true"
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res

def list_corrupted(path):
    """
    Get a list of corrupted files.
    To use this method we are calling "http://199.88.191.194:5007" server.
    :param path: The directory path where you want to list the corrupted files
    :type path: str

    :example:

    >>> from vai_utils import data
    >>> path = '../list/'
    >>> data.list_corrupted(path)
    """
    request_url = python_base_url + "/list_corrupted?path="+path
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def list_duplicate(path):
    """
    List duplicate files.
    To use this method we are calling "http://199.88.191.194:5007" server.
    :param path: Directory path for which you want to list duplicate files.
    :type path: str

    :example:

    >>> from vai_utils import data
    >>> path = '../list/'
    >>> data.list_duplicate(path)
    """
    request_url = python_base_url + "/list_duplicate?path="+path
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def remove_corrupted(images):
    """
    Remove corrupted files.
    To use this method we are calling "http://199.88.191.194:5007" server.
    The files passed in the function represent a list of file paths that are
    identified as corrupted or damaged, typically obtained using the
    `data.list_corrupted()` function.

    :param files: Directory path for which you want to remove corrupted files.
    :type files: List[File]

    :example:

    >>> from vai_utils import data
    >>> path = '../list/'
    >>> files = data.list_corrupted(path)   #Result return by list_corrupted 
    >>> data.remove_corrupted(files)
    """
    request_url = python_base_url + "/list_corrupted"
    payload =json.dumps({
        "images":images
    })
    response = requests.post(request_url,data=payload)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res

def crop_images(path,height, width):
    # TODO is `crop_images` singular or plural when it takes one path?
    # please clarify, alongside the return type
    """
    Crop an image.
    It will crop images, given that path of image, and height of width of that
    image. To use this method we are calling "http://199.88.191.194:5008"
    server.

    :param path: Path of the image to crop.
    :type path: str
    :param height: Desired height of the cropped image
    :type path: int
    :param width: Desired width of the cropped image
    :type width: int

    :example:

    >>> from vai_utils import data
    >>> path = '../image/dog.png'
    >>> height = 300
    >>> width = 500
    >>> data.crop_images(path,height, width)
    """
    request_url = node_base_url + "/crop?path="+path+'&width='+width+'&height='+height
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def collage_images(path,height, width):
    # TODO why does this take one image path in the example when the function 
        # collates multiple images?
    # TODO is `collage_images` singular or plural? please clarify
    """
    Collage images.
    It will college images, given that path of image, and height of width of
    that image. To use this method we are calling "http://199.88.191.194:5007"
    server.
    
    :param path: Path of the image to collage.
    :type path: str
    :param height: The desired height of each image in the collage
    :type path: int
    :param width: The desired height of each image in the collage
    :type width: int

    :example:

    >>> from vai_utils import data
    >>> path = '../image/cat.png'
    >>> height = 300
    >>> width = 500
    >>> data.collage_images(path,height, width)
    """
    request_url = python_base_url + "/collage_images?path="+path+'&width='+width+'&height='+height
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def store_url_to_html(url,output):
    """
    Store HTML of the given url. It will store html return by url into
    `output_dir`. To use this method we are calling "http://199.88.191.194:5008"
    server.

    :param url: A web URL from which you want to retrieve the HTML content.
    :type url: str
    :param output_dir: The directory where you want to store the HTML file
        obtained from the URL.
    :type output_dir: str

    :example:

    >>> from vai_utils import data
    >>> url = 'https://dev-cloud.virtuousai.com/meta.json'
    >>> input_dir = ./html/vai.html
    >>> data.store_url_to_html(url, input_dir)
    """
    request_url = node_base_url + "/store-url-to-html?url="+url+'&output='+output
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def store_url_files_to_html(input,output,chunk_size, generate ):
    """
    Store html of stored urls json file on given path. It will store html return
    by url given in input_dir and store in output_dir. To use this method we are
    calling "http://199.88.191.194:5007" server.

    :param input_dir: The directory where the stored URLs JSON file is located.
    :type input_dir: str
    :param output_dir: string representing the directory where you want to store
        the HTML files obtained from the URLs specified in the JSON file.
    :type output_dir: str
    :param chunk_size: The number of URLs to process per batch.
    :type chunk_size: int

    :example:

    >>> from vai_utils import data
    >>> input_dir = './file/vai.txt'
    >>> output_dir = ./html/vai.html
    >>> data.store_url_files_to_html(input_dir, output_dir)
    """
    request_url = python_base_url + "/store-url-files-to-html?file_path="+input+'&output='+output+'&chunk_size='+str(chunk_size) +"&html_json="+generate 
    response = requests.get(request_url) 
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def convert_text_to_json(input,output ):
    """
    convert text file into json file.
    To use this method we are calling "http://199.88.191.194:5007" server.
    It will convert text file into json file.

    :param input: The directory where the stored URLs JSON file is located.
    :type input: str
    :param output: The JSON file name you want to store.
    :type output: str

    :example:

    >>> from vai_utils import data
    >>> input = "./input.txt"
    >>> output = "./input.json"
    >>> data.convert_text_to_json(input,output)
    """
    request_url = python_base_url + "/convert-text-to-json?input="+input+'&output='+output 
    response = requests.get(request_url)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
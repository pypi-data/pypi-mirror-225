# Sub_Funcs 
import os
import requests

def image_downloader(url, **kwargs):
    """
        Downloads a file from a given url.
        Args:
            url: Url For The File You Wanna Download.
        Kwargs:
            name: Enter The Name Of The Image.
            chunk: Chunck_Size For Iter_Content.
            location: Where To Save The Image.
        Returns:
            The Downloaded Image
    """
    if 'extension' in kwargs:
        extension = kwargs['extension']
        if extension.startswith('.'):
            extension = extension.replace('.', '')
    else:
        extension = '.png'

    if 'name' in kwargs:
        name = kwargs['name'] + extension
    else:
        name = 'default' + extension 
    
    if 'chunk' in kwargs:
        chunk = kwargs['chunk']
    else:
        chunk = 500

    if 'location' in kwargs:
        location = kwargs['location']
    else:
        location = ''

    try:
        os.chdir(location)
    except OSError:
        pass
    request = requests.get(url, stream=True)
    with open(f"{name}", 'wb') as file:
        for i in request.iter_content(chunk_size=chunk):
            file.write(i)



def image_check(url):
    valid_extensions = ('png', 'jpg', 'jpeg', 'webp', 'svg')
    valid_domains = ('encrypted-tbn0.gstatic.com', 'unsplash', 'pexels', 'image')
    check = None

    for i in valid_extensions:
        if url.split('/')[1] != '' and url.split('/')[1].startswith(i):
            check = True
        elif url.split('/')[1] != '' and url.split('/')[2].startswith(i):
            check = True
        else:
            check = False

    if any(url.endswith(ext) for ext in valid_extensions) or any(domain in url for domain in valid_domains) or check == True:
        return True
    return False
    
# CivitaiDownloader
A tool to auto download all your favorite models from civitai. It's extremely helpful if you want to run your models on the cloud or colab, etc. Just keep a list of urls to your model pages and then it will save your day copying and pasting wget commands.
# Usage
### Dependencies
```
pip install playwright
playwright install
```
### Save login cookie
You have to do this on your machine with a screen. 
```
python civitai_login.py
```
login your civitai account in the browser that shows up, the window should automatically close if you are successfully logged in.

This will generate a file named `cookies.json` in the current directory. If you plan to download on a remote machine you have to upload this file and then run the following steps remotely. 
### prepare urls
put the urls you are interested in a text file, one in each line, see example file [urls.txt](urls.txt])

### retreive url info
```
python civitai.py --info --url_file [your_file_containing_links]
```
to get the title of the links, this will generate a file 'model_info.json' containing the titles.

### download models
```
python civitai.py --download --url_file [your_file_containing_links] --download_dir [download_directory]
```
to batch download the models in your specified links, wait and enjoy.
#!/usr/bin/env python

import logging.config
import os , re, unicodedata
from bs4 import BeautifulSoup

# Logging config
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging.conf'))
# logger = logging.getLogger("logger_console_info")
logger = logging.getLogger("logger_console_debug")


# Global var
site_src = "/Users/sgendrot/Dropbox/Velocipaide/site_web/www.velocipaide.fr"
site_dst = "/Users/sgendrot/Dropbox/Velocipaide/site_web/old-extract-to-jekyll"

def process_html(path, name):
    '''
    Process a html file (read the file, extract data, create jekyll post and write it)

    :param html_file: the cpath + name of the file
    :type html_file: basestring
    :return: xxxx
    '''
    html_file = path+"/"+name
    logger.info("Let process html file: %s" % html_file)

    try:
        html_data = open(html_file,"r", encoding="utf-8").read()
    except:
        html_data = open(html_file,"r", encoding="latin-1").read()



    soup = BeautifulSoup(html_data)

    # logger.info(soup.title.string)

    div_post = soup.find('div',attrs={"class":"post"})

    if div_post is None:
        logger.info ("Not a post page - %s" % soup.title.string)
        # exit(1)
    else:

        date_extracted = re.search(".*/www.velocipaide.fr/([0-9]+)/([0-9]+)/([0-9]+)/.*", path)
        if (date_extracted is not None): # re.search returns None if regex doesn't match
            # extract article name
            article_name = div_post.find('h1',attrs={"class":"title"}).a.text
            # some characters are not UTF8, I normalize the string to use it in the file name
            article_name = unicodedata.normalize('NFKD', article_name).encode('ASCII', 'ignore').decode("utf-8")
            # build jekyll file name ( YYYY-MM-DD-article-name.md )
            # re.group => # 1=year; 2=month; 3=day
            jekyll_file_name = date_extracted.group(1)+"-"+date_extracted.group(2)+"-"+date_extracted.group(3)+"-"
            # 1/change space to hyphen; 2/ remove non alphabetic or hyphen characters
            jekyll_file_name = jekyll_file_name + re.sub("[^a-zA-Z\-]+", "", article_name.replace(" ", "-"))+".md"

            logger.info ("%s is a post page" % soup.title.string)
            logger.info ("it will transform to %s" % jekyll_file_name)

            jekyll_file_data = "---\n"
            jekyll_file_data = jekyll_file_data + "layout: post\n"
            jekyll_file_data = jekyll_file_data + "title: \"" + article_name + "\"\n"
            jekyll_file_data = jekyll_file_data + "---\n\n"
            jekyll_file_data = jekyll_file_data + str(div_post.find('div', attrs={"class": "entry"})).split("<div class=\"entry\">")[1].split("<!-- Start Sociable -->")[0]


            logger.debug (jekyll_file_data)
            jekyll_file_stream = open(site_dst + "/" + jekyll_file_name, "w")
            jekyll_file_stream.write(jekyll_file_data)
            jekyll_file_stream.close()


        else:
            logger.info ("%s is almost a post page" % soup.title.string)

       # exit(1)



###########    MAIN    ###########

if __name__ == "__main__":
    # print (os.getcwd())
    for root, dirs, files in os.walk(site_src):
            logger.debug ("root %s" % root)
            # for adir in dirs:
            #     print ("dir %s" % adir)
            for afile in files:
                logger.debug ("file %s" % afile)
                if afile.lower().endswith("index.html"):
                    logger.debug ("html: %s" % afile)
                    process_html(root,afile)
                elif afile.lower().endswith(('.png', '.jpg', '.jpeg')):
                    logger.debug ("img: %s" % afile)
                else:
                    logger.debug ("other type for: %s" % afile)



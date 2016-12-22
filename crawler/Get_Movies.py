__author__ = '47217_000'
# get Andrew Ng's lessons from WangYi cloud class
# 2016.7.10
import urllib2
import re
import urllib
def Get_Url():
    src='http://open.163.com/special/opencourse/machinelearning.html'
    content=urllib2.urlopen(src).read()
    dest=re.findall(r"http://open.163.com/movie/.*\.html",content)
    return list(set(dest))
def Get_Lesson(src,num):
    content=urllib2.urlopen(src).read()
    l_pattern=re.compile(r"http.*\.m3u8")
    lesson=re.findall(l_pattern,content)
    lesson_src=lesson[0].replace("m3u8","mp4")
    urllib.urlretrieve(lesson_src,"Machine_Learning%s.mp4"%(num))

if __name__ == "__main__":
    Lesson_src=Get_Url()
    num=0
    for item in Lesson_src:
        Get_Lesson(item,num)
        num+=1
        print "%s ok"%num
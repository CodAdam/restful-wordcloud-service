#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from os import path  
from scipy.misc import imread  
import matplotlib.pyplot as plt  
import jieba  
import json
import urllib.parse

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  

app = Flask(__name__)

global stopwords 
        
def importStopword(filename=''):  
    
    global stopwords  
    
    f = open(filename, 'r', encoding='utf-8')  
    line = f.readline().rstrip()  
  
    while line:  
        stopwords.setdefault(line, 0)  
        stopwords[line] = 1  
        line = f.readline().rstrip()  
  
    f.close()  
  
def processChinese(text):  
    seg_generator = jieba.cut(text)   
  
    seg_list = [i for i in seg_generator if i not in stopwords]  
  
    seg_list = [i for i in seg_list if i != u' ']  
  
    seg_list = r' '.join(seg_list)  
  
    return seg_list 


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/getWordCloudPng/<string:wordtext>', methods=['POST','GET'])
def get_word_cloud_png_by_text(wordtext):
    
    global stopwords
    
    stopwords={} 
    importStopword(filename='./stopwords.txt') 
    # __file__  
    d = path.dirname('.')   
      

    #text = open(path.join(d, 'love.txt'),encoding ='utf-8').read()  
      
    text = wordtext

    text = processChinese(text)      
    # read the mask / color image  
    # taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010  

    back_coloring = imread(path.join(d, "./image/alice_color.png"))  
      
    wc = WordCloud( #font_path=' C:/Users/Windows/fonts/msyh.ttf',
                    #font_path='./font/cabin-sketch.bold.ttf',
                    font_path='./font/叶立群几何体.ttf', 
                    background_color="white",  
                    max_words=2000,  
                    mask=back_coloring,  
                    max_font_size=100,   
                    random_state=42,  
                    )
      
    
    wc.generate(text)  
    # wc.generate_from_frequencies(txt_freq)  


    image_colors = ImageColorGenerator(back_coloring)  
      
    plt.figure()  
  
    #plt.imshow(wc)  
    #plt.axis("off")  
    #plt.show()  
 
      
     
    #wc.to_file(path.join(d, "name")) 
    print((path.join(d, "./wordcloud/test.png")))
    wc.to_file((path.join(d, "./wordcloud/test.png"))) 
    host="http://127.0.0.1:8090/"
    #dir="/wordcloud/"
    dir = "wordcloud/"
    name="test.png"
    picurl=host+dir+name
    return jsonify(
                    {
                            "code": "10000",
                            "message": "成功",
                            "data": picurl
                    })



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

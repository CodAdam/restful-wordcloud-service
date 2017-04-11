#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

#�ִ����
from os import path  
from scipy.misc import imread  
import matplotlib.pyplot as plt  
import jieba  
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  

app = Flask(__name__)

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
    seg_generator = jieba.cut(text)  # ʹ�ý�ͷִʣ�Ҳ���Բ�ʹ��  
  
    seg_list = [i for i in seg_generator if i not in stopwords]  
  
    seg_list = [i for i in seg_list if i != u' ']  
  
    seg_list = r' '.join(seg_list)  
  
    return seg_list 


@app.route('/getWordCloudPng/<string:text>', methods=['GET'])
def get_word_cloud_png_by_text(wordtext):
    
    stopwords = {}  
    importStopword(filename='./stopwords.txt') 
    # ��ȡ��ǰ�ļ�·��  
    # __file__ Ϊ��ǰ�ļ�, ��ide�����д��лᱨ��,�ɸ�Ϊ  
    # d = path.dirname('.')  
    d = path.dirname(__file__)  
      
    # Դ��˴�����txt�ı�
    #text = open(path.join(d, 'love.txt'),encoding ='utf-8').read()  
      
    # ��Ŀ��Ҫ��Ϊ���񴫲�
    text = wordtext
      
    #���������  
    text = processChinese(text) #���Ĳ��÷ִʣ�ʹ��Jieba�ִʽ���  
      
    # read the mask / color image  
    # taken from http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010  
    # ���ñ���ͼƬ  
    back_coloring = imread(path.join(d, "./image/love.jpg"))  
      
    wc = WordCloud( font_path='./font/cabin-sketch.bold.ttf',#��������  
                    background_color="black", #������ɫ  
                    max_words=2000,# ������ʾ��������  
                    mask=back_coloring,#���ñ���ͼƬ  
                    max_font_size=100, #�������ֵ  
                    random_state=42,  
                    )  
    # ���ɴ���, ������generate����ȫ���ı�(���Ĳ��÷ִ�),Ҳ�������Ǽ���ô�Ƶ��ʹ��generate_from_frequencies����  
    wc.generate(text)  
    # wc.generate_from_frequencies(txt_freq)  
    # txt_freq����Ϊ[('��a', 100),('��b', 90),('��c', 80)]  
    # �ӱ���ͼƬ������ɫֵ  
    image_colors = ImageColorGenerator(back_coloring)  
      
    plt.figure()  
    # ���´�����ʾͼƬ  
    plt.imshow(wc)  
    plt.axis("off")  
    plt.show()  
    # ���ƴ���  
      
    # ����ͼƬ  
    wc.to_file(path.join(d, "����.png")) 
    return jsonify({'result': "����.png"})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

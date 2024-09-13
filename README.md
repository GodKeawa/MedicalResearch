# MedicalResearch
本项目是**FDU特色**思政-践行平台课题——医保、医疗、医药协同发展和治理研究的数据库子项目   
项目数据均来自政府主动公开的建议提案答复函[国家医疗保障局 建议提案 (nhsa.gov.cn)](https://www.nhsa.gov.cn/col/col110/index.html?uid=2464&pageNum=1)  
项目使用100%的python技术栈（本人太菜），十分简单易懂  
项目仍在完善中  

# 使用方法
## 项目下载
个人建议不要使用GitHub的下载ZIP方法，这将会让你下载接近一个G的内容，因为本项目包含了大量的图片文件，且后续项目更新时，你又要下一个G；建议了解git的基本使用方式，然后将本项目clone下来，后续有更新直接拉取下来即可，git可能会让你处理冲突，但是你可以通过命令行参数强制覆盖，这样你就不用下载非常大的图片资源文件了，它们总是不变的。

当然如果有需要的话我也可以在release里发布不包含图片文件的更新包，只是这样显得很蠢  
## 基本功能及项目使用
如果你有一定的python基础，有能力配置好一个python环境，那么最好根据下面的项目概要了解项目的相关接口，既可以通过源文件方便的打开本人设计的简单的用户界面，又可以自行编写代码来调用接口进行一定的自定义操作，另外最好给编辑器安排一个json格式化插件
(如果需要python虚拟环境也可以直接联系我，我把虚拟环境打包发给你)

如果你完全不懂python，那么你可以先自学一些内容，然后跟着项目日志一步步做，也可以直接使用exe启动本人写的用户界面`viewer.exe`，注意外部的资源文件是必要的，所以请下载完整项目，GUI的使用方式及功能请看项目日志中的GUI设计部分

记住，按钮提供的操作永远是有限的，GUI只是迎合大众，但是大众往往做不到所有事情

# 项目介绍及日志

## 项目概要
**Tips: 使用python版本为3.12.2-64bit**
### 代码文件
* `processer.py` - 提供数据抓取和部分数据预处理功能函数
	* requirements: 查看import的python库即可，都能一键安装
* `analyzer.py` - 提供文本分析函数
	* requirements: 库同上，注意文件的相对位置，如果找不到文件就调一下路径
* `viewer.py` - 提供词云生成函数和简单的GUI
	* requirements: 同上，需要绝大部分资源文件运行GUI
### 资源文件
* 通过网络抓包获取网站返回的文章列表，存放在`datastore.txt`中
* 自定义词典`custom_words.txt`
* 停用词典`stop_words.txt`
* IDF列表`IDF.txt`
* 字体`font/`
### 数据文件
* 解析后的列表为`datalist.json`，目前包括以下字段：
	* 查询序号`index`
	- 标题`title`
	- 文章原链接`url`
	- 文章序号`number`
	- 文章发布时间`time`
	- 文章的高频词`hotwords`
	- 通过TF-IDF算法得到的主题词`theme`
- 每篇文章的数据存放在`articles`文件夹中
	- 文件夹命名使用查询序号字段
	- 爬取的全部图片文件，编号有效
	- ocr识别后的文本及直接爬取到的文本在`text.txt`
	- 分词后的词表在`word_dict.json`
- `full_datalist.json`是添加了相关文本分析数据的列表文件，相对更大，读取可能更慢，所以单独写成一个文件
- `overal_dict.json`是整个数据库文章的全部词频列表

## 项目日志
### 网页链接列表获取

之前写过几次爬虫，直接上通用技术栈，浏览器网络监测看看服务器都发了点什么过来，这次还真的有惊喜，按了半天下一页，最后居然只向服务发了一个post请求，看来信息应该是发到前端处理了，估计网站后端也是一个小数据库，但是只保存了网页的链接

拿几个链接试了一下，不大行，纯自动化估计是做不了了，干脆抓个包好了，反正一次post后端就能发120条数据过来，剩下的翻页其实都是前端做的，所以完全不用加载，抓包7次就全拿下了，全部放在`datastore.txt`里

数据有了就轻车熟路，正则表达式加BeautifulSoup简单生成一个json列表`datalist.json`,后续直接用json读成字典，非常好用，代码在`processer.py - get_datalist()`  
在json里提供了一些有用的字段，包括原网站列表提供的所有信息以及目标网址的url，后续这个json还可以不断扩充，然后载入数据库就行  

### 网页数据爬取
虽然不禁想要吐槽这程序员为了防止复制居然这么偷懒，就搞了个图片上去，自家人也复制不了了，但是看了一下网页的组织结构，就发现这网页的结构算是我爬过的网站里相当整洁的了，虽然一部分是文字，一部分是图片，但是整个的结构都一样，还特意写了两个标签表示正文开始和结束，我哭死，依旧用BeautifulSoup解析，配合正则轻松把内容获取逻辑写了  

之前的代码经常要爬一会睡一会，还必须要cookies，政府的网站没人敢攻击，确实皮实，光速爬完，中间一点小瑕疵无伤大雅，最后用检索序号作文件夹名，直接分区存储了，后续方便处理，现在整个数据结构已经有数据库的样子了，全部文件存储在`articles`文件夹里  
代码在`processer.py - get_articles()`

### 图片ocr转文字
比较折磨，技术路线太少，倒腾了半天才找到一个好用的，识别精度非常不错，更重要的是我的轻薄本没有独显，就装不了cuda，最后都是用cpu跑模型，肯定慢

最后选了PaddleOCR，也算是近期还相当活跃的python OCR库了，python的东西用起来都很轮椅，但是这个确实是电动轮椅，后续打算给自己本地部署一个  
[PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

做了一点小小的格式控制，后续也许有用，代码跑了不到半个小时就好了，确实快  
代码在`processer.py - ocr_process()`

增加了一个图片切分模块，网站的格式又变了，现在只有一张长图，还好变化不大，切分一下正常用

### jieba文本分析
用了python，就不可能不用jieba了，也就它能用，不过jieba本身是支持非常多技术栈的  
[fxsjy/jieba: 结巴中文分词 (github.com)](https://github.com/fxsjy/jieba)  
#### 文本分词
长文本总是逃不掉分词的，毕竟这文本我也没读，不可能知道它的关键词或者话题等是什么，这时就只能分词然后进行数据分析了  
在完成分词后，我们直接进行统计，作为一个字典写进json里，占据`words`字段。同时也统计整个数据库的词频表，放在`overal_dict.json`里  
功能实现在`analyzer.py - article_cut()`  

这里有一些可以商讨的地方，在分词上jieba提供了几种不同的方式，针对不同的应用场景和目的，其中精确模式等同于在句子之间进行切分，所有次按顺序加起来就是原句，而全模式和浏览器模式都提供一定程度的词提取功能，比如复旦大学就会被“分”成三个词：复旦、大学和复旦大学，如果其中的“词”并非原意，但仍然是一个词，那么后者依旧会讲这个词提取出来，比如“我们中出了一个叛徒”中的“中出"，虽然是某种程度上的外来词汇，但是模型依旧能够识别，这可以提取出更多的信息，也能部分解决模式识别精度不足的问题，但目前我还是偏向于使用精确模式，并辅以一定的自定义词典，对于我们的数据库而言，严格遵照原文才是最正确的选项，我们也不需要发散出来的内容  

#### 设置自定义词典
由于中文的语言特色，我们必须删除一些无用的连接词，助词等，统称为停用词  
同时对于一些专有名词，我们也可以设置为单独的词加入词典  

停用词使用开源项目以及个人动态调整  
[elephantnose/characters: 中文停用词/常用汉字/生僻字集合 (github.com)](https://github.com/elephantnose/characters)  
文件为`stop_words.txt`  

自定义词典由个人动态调整得到  
文件为`custom_words.txt`  

#### 添加文章的分析字段
##### 热门词
添加一个`hot_words`字段，就使用最简单的排序取前面十个  
功能实现集成在`analyzer.py - article_cut()`里，非常简单  

##### 关键词
很显然热门词很容易被一些频繁出现在医保这样一个大主题下的热门词干扰，导致几乎每篇文章的热门词里都有医保之类的词，而无法展现这篇文章自身的主题，因此我们引入关键词提取技术`TF-IDF算法`  
[【机器学习】TF-IDF算法：深入解析与应用实践_tfidf实践-CSDN博客](https://blog.csdn.net/g310773517/article/details/139703038)  
简单来说就是通过将词频乘以一个表征词语稀有度的量，再取最大值  
在这里，词“医保”的稀有度将会降到非常低，这样每篇文章的主题里词“医保”的权重也会随之降低，进而展现出文章独特的主题  

同样使用jieba的集成功能实现，`analyzer.py - theme_extract()`  
当然语料库肯定是要自己生成的，功能实现在`analyzer.py - IDF_gen()`  
为了方便存放在`IDF.txt`中  

**Tips: 在代码中我取消了数字的权重，如果有需要可以打开**

## 词云生成及GUI制作
### 词云生成
万能python库  
[amueller/word_cloud: A little word cloud generator in Python (github.com)](https://github.com/amueller/word_cloud)  
注意word_cloud默认不支持中文显示（matplotlib也不支持）  
所以需要自己设置字体，这里最好使用开源字体，避免版权问题  
可以使用adobe的开源字体库，随便选择  
[Adobe Fonts (github.com)](https://github.com/adobe-fonts)  

提供了两个词云生成函数，输入是索引或索引的列表，输出是根据其中内容的词生成的词云，由于一些底层的问题生成词云后GUI的dpi会被修改，导致整个界面等比缩小，目前无法简单修复，但是我将界面都改成了可缩放的，总有办法把界面显示全的
### GUI设计
根据我过往的技术设计，使用`PySimpleGUI`，个人使用是免费的，可能会要求你去官网申请一个license，跟着过去就行  
过往项目[GodKeawa/ics-labs: FDU-ICS-labs (github.com)](https://github.com/GodKeawa/ics-labs)  

GUI的功能实现很简单，首先用户指定一个搜索方式，这将决定搜索在什么内容上进行
* 查询序号：从所有查询序号中寻找
* 标题：从所有标题中寻找
* 时间：从发布时间中寻找
* 单词：从全文的单词中寻找，可以输入`overal_dict.json`中的大部分单词，也可以输入单字，但是不要输入超过单词的内容，因为这里是逐单词比对
* 热门词、关键词：同单词，但是搜索范围缩小到了`hotwords`字段和`theme`字段
* 全文：全文搜索

然后输入搜索的内容点击查询即可，后面的列表将会更新为查询到的文章列表  
注意由于效率问题，**模糊搜索尚未实现**，目前的搜索方式下，只要你的输入是搜索基的子集，那么代码是可以搜索到的，但这个确实不是很好用，后续得直接上数据库

生成词云按钮在什么都没设置或者设置无效时将默认生成全部文章的词云，当文章选择栏有一篇文章时，将生成那篇文章的词云，当文章列表有效，且还未选择文章时，生成的是文章列表中全部文章的词云，详细表现请查看源码的简单if逻辑

查询数据可以查询单篇文章的基本数据，本人提供这个方法只是为了方便复制，如果你有一定的编程能力，那么可以直接使用json自行处理，或者直接查看项目的数据文件  
所有内容均可复制，但是**不提供右键菜单**，请使用`Ctrl+CV`

查看原始图片功能基于基本信息的查询序号生成，所以请保证基本信息里的查询序号有效且是你想要的，**按钮一直都在右下角，只是因为渲染问题可能不显示**，你把鼠标挪开，就会发现又显示了，当然上面的字是显示不了了

### 代码接口汇总
里面提供了多个接口，接口的输入都是查询序号
* `word_cloud_gen_simple(s: str)`
	* 接收一个查询序号的字符串，根据这篇文章生成一个词云并直接弹出
* `word_cloud_gen_list(l: list)`
	* 接收一个查询序号的字符串列表，根据这个列表中的全部文章生成一个词云
* `show_img(s:str)`
	* 接收一个查询序号的字符串，播放对应目录下文章的全部图片
* `updatelist(method: str, key: str)`
	* 接收一个查询方法字符串与查询字段字符串，根据查询方法选取查询的基，然后在这些基中查找字段，如果有就加入列表，列表放在全局便于程序各部分使用
* `find_article(key: str)`
	* 接收一个查询序号字符串，返回对应文章的json字典

# TODO LIST
* 接入正式的NOSQL数据库，提供更强的文本搜索能力
* 拓展文本分析的内容，根据过往范式进行进一步研究


# -*- coding: utf-8 -*-	
import sys
import os
import xml.dom.minidom as minidom 
import codecs

stdout = sys.stdout
stdin = sys.stdin
stderr = sys.stderr
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = stdout
sys.stdin = stdin
sys.stderr = stderr

#将转入的编码转换为unicode
def covert_to_unicode(msg):
    unstr = None
    if isinstance(msg, unicode):
        unstr = msg
    elif isinstance(msg, str):
        try:
            unstr = msg.decode('utf-8')
        except Exception as inst:
            log = open("error.log", "a")
            log.write(time.strftime("%Y-%m-%d %X", time.localtime()))
            log.write("\n")
            log.write(str(type(inst)))
            log.write("\n")
    else:
        log = open("error.log", "a")
        log.write(time.strftime("%Y-%m-%d %X", time.localtime()))
        log.write("\n")
        log.write("covert_to_unicode error")
        log.write("\n")
    return unstr

##操作XML文件类
class CreateOperatorXml():
    def __init__(self,filename):
        self.__xml_path = filename            ##操作对象的文件名
        self.__dom = None
        self.__root = None                    ##根节点
        self.__childList = []                 ##根节点下的所有子节点
        self.__contentDic = {}                ##整个xml文件的内容
        self.__BeginOperatroXml()


    def __log(self, inst):
        log = open("error.log", "a")
        log.write(time.strftime("%Y-%m-%d %X", time.localtime()))
        log.write("\n")
        log.write(str(type(inst)))
        log.write("\n")
        log.write(repr(inst))
        log.write("\n")
        log.write(traceback.format_exc())
        log.write("\n")
        log.close()

    ##数据统一转化为unicode编码
    def _covert_code(self, msg):
        return covert_to_unicode(msg)

    #为xml文件添加一个结点,其中node_text默认值为空
    def __create_new_node(self, node_name, node_text = None):
        if self.__dom == None:
            return
        if None == node_text:
            return self.__dom.createElement(self._covert_code(node_name))
        else:
            newNode = self.__dom.createElement(self._covert_code(node_name))
            newText = self.__dom.createTextNode(self._covert_code(node_text))
            newNode.appendChild(newText)
            return newNode

    ##读取整个xml文件的内容,格式:: {Node1:{},Node2:{}}
    def __ReadAllXml(self):
        nodelist = self.__getChildNode()
        nodeDic = {}
        for node in nodelist:
            self.readXmlNodeOperator(node,nodeDic)
            self.__contentDic[node] = nodeDic
            nodeDic = {}
        #print 'self.__contentDic = ',self.__contentDic

    ##获得所有根节点下的子节点名称
    def __getChildNode(self):
        childList = []
        dom = minidom.parse(self.__xml_path)
        root=dom.documentElement
        for node in root.childNodes:
            childList.append(node.nodeName)
        return childList

    ##添加子节点及属性值
    def __AddContent(self):
        for tag in self.__contentDic.keys():
            top_node = self.__create_new_node(tag)
            for key in self.__contentDic[tag].keys():
                node = self.__create_new_node(key, self.__contentDic[tag][key])
                top_node.appendChild(node)
                self.__root.appendChild(top_node)
        return

    ##开始操作xml文件
    def __BeginOperatroXml(self):
        try:
            #创建文档对象，文档对象用于创建各种节点。
            impl = minidom.getDOMImplementation()
            self.__dom = impl.createDocument(None, self.__xml_path.split('.')[0], None)
            # 得到根节点
            self.__root = self.__dom.documentElement
            if os.path.exists(self.__xml_path):
                self.__ReadAllXml()
            else:
                #TODO 根据xml文件的类型设置默认值
                pass
        except Exception as inst:
            self.__log(inst)        #'创建coverage xml根结点失败'

    ##添加一整个节点，tagname：节点名称   content：节点下内容的字典
    def AddNodeContent(self,tagname,content):
        self.__contentDic[tagname] = content

    ##修改某个子节点下某个属性点的值
    def modifiValue(self,tagname,key,value):
        if self.__contentDic[tagname].has_key(key):
            self.__contentDic[tagname][key] = value

    ##取得指定子节点下的所有属性值
    def readXmlNodeOperator(self,tagname,aimDic):
        if not os.path.exists(self.__xml_path):
            return None
        dom = minidom.parse(self.__xml_path)
        root=dom.documentElement
        booknode=root.getElementsByTagName(tagname)
        for booklist in booknode:
            for nodelist in  booklist.childNodes:
                if nodelist.nodeType ==1:
                    nodelist.nodeName+':'
                for node in nodelist.childNodes:
                    aimDic[nodelist.nodeName] = node.data
                    #print nodelist.nodeName ," : ",node.data

    ##取得指定子节点下的某个key的值
    def readXmlNodeKey(self,tagname,key):
        dic = {}
        self.readXmlNodeOperator(tagname,dic)
        if dic.has_key(key):
            return dic[key]
        else:
            return None

    ##获取xml文件的全部内容 ,返回格式{Node:{},Node:{}}
    def GetXmlConent(self):
        return self.__contentDic

    ##结束xml文件操作
    def EndOperatroXml(self):
        try:
            self.__AddContent()
            f = open(self.__xml_path, 'wb+')
            writer = codecs.lookup('utf-8')[3](f)
            self.__dom.writexml(writer, encoding='utf-8')
            writer.close()
            f.close()
            return True
        except Exception as inst:
            self.__log(inst)                #'写coverage.xml文件出错'



##测试函数
if __name__ == '__main__':
    test = CreateOperatorXml('power.xml')
    #test.BeginOperatroXml()
    print test.GetXmlConent()
    print test.readXmlNodeKey("sqn","effective_line")
    '''test.AddNodeContent(
            u'sqn',{
            u'covername' : u'first',
            u'name' : u' ',
            u'total_line' : u'58455',
            u'effective_line' : u'16623',
            u'covered_line' : u'11368',
            u'cover_rate' :u'68.38717'}
        )
    test.AddNodeContent(
            u'lyf',{
            u'covername' : u'bigerset',
            u'name' : u'qian',
            u'total_line' : u'61424',
            u'cover_rate' : u'99.999'}
        )'''
    #test.modifiValue(u"sqn",u"name",u"kitty")
    #test.modifiValue(u"lyf",u"cover_rate",u"第三方")
    test.EndOperatroXml()

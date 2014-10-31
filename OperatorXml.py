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
        self.__xml_path = filename
        self.__dom = None
        self.__root = None
		
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
            
    def BeginOperatroXml(self,root):
        try:
            #创建文档对象，文档对象用于创建各种节点。
            impl = minidom.getDOMImplementation()
            self.__dom = impl.createDocument(None, root, None)
            # 得到根节点
            self.__root = self.__dom.documentElement
        except Exception as inst:
            self.__log(inst)        #'创建coverage xml根结点失败'


    def AddContent(self,tagname,conentDic):
        if self.__root == None:
            return             ##创建结点时，root结点不存在对象不存在
        top_node = self.__create_new_node(tagname)
        for key in conentDic.keys():
            node = self.__create_new_node(key, conentDic[key])
            top_node.appendChild(node)
        self.__root.appendChild(top_node)
        return

    def EndOperatroXml(self):
        try:
            f = open(self.__xml_path, 'wb')
            writer = codecs.lookup('utf-8')[3](f)
            self.__dom.writexml(writer, encoding='utf-8')  
            writer.close()
            f.close()
            return True
        except Exception as inst:
            self.__log(inst)                #'写coverage.xml文件出错'

    def readOperatorCommon(self,tagname,aimDic):
        #print self.__xml_path
        dom = minidom.parse(self.__xml_path)
        root=dom.documentElement
        booknode=root.getElementsByTagName(tagname)
        #print "booknode = ",booknode
        for booklist in booknode:
            for nodelist in  booklist.childNodes:
                if nodelist.nodeType ==1:
                    nodelist.nodeName+':'
                for node in nodelist.childNodes:
                    aimDic[nodelist.nodeName] = node.data
                    print nodelist.nodeName ," : ",node.data
                    #print node.data

##测试函数
if __name__ == '__main__':
    test = CreateOperatorXml('power.xml')
    test.BeginOperatroXml("God")
    test.AddContent(
            'sqn',{
            'covername' : 'first',
            'name' : '',
            'total_line' : '58455',
            'effective_line' : '16623',
            'covered_line' : '11368',
            'cover_rate' : '68.38717'}
        )
    test.AddContent(
            'lyf',{
            'covername' : 'bigerset',
            'name' : 'qian',
            'total_line' : '61424',
            'cover_rate' : '99.999'}
        )
    test.EndOperatroXml()
    dic = {}
    test.readOperatorCommon("sqn",dic)
    print dic
    print 'endl'

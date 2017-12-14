import codecs

class JunYuKG:
    scopename = 'junyu'
    connector = None
    def __init__(self,connector):
        self.connector = connector
        pass
    def addClass(self):
        self.connector.runCypher("MATCH (a {scope:'%s'}) DETACH DELETE a" % self.scopename)
        try:
            classfile = codecs.open('junyu\class.txt', 'r', encoding='utf-8')
            classnameline = classfile.readline()
            while classnameline:
                classnameline = classnameline.replace('\r\n','')
                classname = classnameline.split(',')
                if len(classname)>0:
                    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname[0],self.scopename))
                    print('Add class: %s' % (classname[0]))
                if len(classname)>1:
                    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'}) MERGE (m:Class{name:'%s',scope:'%s'}) MERGE (n)-[:subClassOf]->(m)" % (classname[0],self.scopename,classname[1],self.scopename))
                classnameline = classfile.readline()
            classfile.close()
        except Exception as e:
            print(e)
            pass
        #for classname in self.classnamelist:
        #    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname,self.scopename))
        pass

    def addInstance(self):
        self.connector.runCypher("MATCH (a:Instance {scope:'%s'}) DETACH DELETE a" % self.scopename)
        try:
            instancefile = codecs.open('junyu\instance.txt', 'r', encoding='utf-8')
            instancenameline = instancefile.readline()
            while instancenameline:
                instancenameline = instancenameline.replace('\r\n','')
                instancename = instancenameline.split(',')
                if len(instancename)>1:
                    self.connector.runCypher("MERGE (n:Instance {name:'%s',scope:'%s'}) MERGE (c:Class{name:'%s',scope:'%s'}) MERGE (n)-[:instanceOf]->(c)" % (instancename[1],self.scopename,instancename[0],self.scopename))
                    print('Add instance: %s(%s)' % (instancename[1],instancename[0]))
                instancenameline = instancefile.readline()
            instancefile.close()
        except Exception as e:
            print(e)
            pass
        pass



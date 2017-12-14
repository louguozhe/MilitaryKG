from neo4j.v1 import GraphDatabase, basic_auth
import codecs

class Neo4JConnector:
    driver = None
    session = None
    connected = False
    def __init__(self):
        pass
    def connect(self,host='localhost',port=7687,username='neo4j',password='neo4j'):
        try:
            self.driver = GraphDatabase.driver("bolt://%s:%s" % (host,port), auth=basic_auth(username,password))
            self.session = self.driver.session()
            self.connected = True
        except Exception as e:
            print(e)
            self.connected = False
        pass

    def disconnect(self):
        try:
            if self.connected:
                self.session.close()
        except Exception as e:
            print(e)
        self.connected = False

    def runCypher(self,cupher):
        try:
            if not self.connected:
                return
            self.session.run(cupher)
        except Exception as e:
            print('runCypher Error: %s' % e)
            pass

class KGImporter:
    scope = 'junyu'
    connector = None
    def __init__(self,connector,scope):
        self.connector = connector
        self.scope = scope
        pass
    def addClass(self):
        self.connector.runCypher("MATCH (a {scope:'%s'}) DETACH DELETE a" % self.scope)
        try:
            classfile = codecs.open('%s\class.txt' % self.scope, 'r', encoding='utf-8')
            classnameline = classfile.readline()
            while classnameline:
                classnameline = classnameline.replace('\r\n','')
                classname = classnameline.split(',')
                if len(classname)>0:
                    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname[0],self.scope))
                    print('Add class: %s(%s)' % (classname[0],self.scope))
                if len(classname)>1:
                    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'}) MERGE (m:Class{name:'%s',scope:'%s'}) MERGE (n)-[:subClassOf]->(m)" % (classname[0], self.scope, classname[1], self.scope))
                classnameline = classfile.readline()
            classfile.close()
        except Exception as e:
            print(e)
            pass
        #for classname in self.classnamelist:
        #    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname,self.scopename))
        pass

    def addInstance(self):
        self.connector.runCypher("MATCH (a:Instance {scope:'%s'}) DETACH DELETE a" % self.scope)
        try:
            instancefile = codecs.open('%s\instance.txt' % self.scope, 'r', encoding='utf-8')
            instancenameline = instancefile.readline()
            while instancenameline:
                instancenameline = instancenameline.replace('\r\n','')
                instancename = instancenameline.split(',')
                if len(instancename)>1:
                    self.connector.runCypher("MERGE (n:Instance {name:'%s',scope:'%s'}) MERGE (c:Class{name:'%s',scope:'%s'}) MERGE (n)-[:instanceOf]->(c)" % (instancename[1], self.scope, instancename[0], self.scope))
                    print('Add instance: %s(%s)(%s)' % (instancename[1],instancename[0],self.scope))
                instancenameline = instancefile.readline()
            instancefile.close()
        except Exception as e:
            print(e)
            pass
        pass

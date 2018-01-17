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

    def queryCypher(self,cupher):
        try:
            if not self.connected:
                return
            return self.session.run(cupher)
        except Exception as e:
            print('runCypher Error: %s' % e)
            pass

class KGImporter:
    scope = 'scope'
    connector = None
    def __init__(self,connector,scope):
        self.connector = connector
        self.scope = scope
        pass

    def removeAllClass(self):
        self.connector.runCypher("MATCH (a {scope:'%s'}) DETACH DELETE a" % self.scope)

    def createIndex(self,classname,propertyname):
        try:
            self.connector.runCypher("CREATE INDEX ON :%s(%s)" % (classname,propertyname))
        except Exception as E:
            print(E)

    def addClass(self):
        try:
            classfile = codecs.open('%s\class.txt' % self.scope, 'r', encoding='utf-8')
            classnameline = classfile.readline()
            while classnameline:
                classnameline = classnameline.replace('\n','')
                classname = classnameline.split(',')
                if len(classname)>0 and classname[0] != '':
                    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname[0],self.scope))
                    print('Add class: %s(%s)' % (classname[0],self.scope))
                if len(classname)>1 and classname[0] != '':
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
                instancenameline = instancenameline.replace('\n','')
                instancename = instancenameline.split(',')
                if len(instancename)>1 and instancename[0] != '':
                    self.connector.runCypher("MERGE (n:Instance {name:'%s',scope:'%s'}) MERGE (c:Class{name:'%s',scope:'%s'}) MERGE (n)-[:instanceOf]->(c)" % (instancename[1], self.scope, instancename[0], self.scope))
                    print('Add instance: %s(%s)(%s)' % (instancename[1],instancename[0],self.scope))
                instancenameline = instancefile.readline()
            instancefile.close()
        except Exception as e:
            print(e)
            pass
        pass


class KGToOtology:
    scope = 'scope'
    filename = None
    dfile = None
    fenleiuri = None
    def __init__(self,scope):
        self.scope = scope
        self.filename = '%s/%s.owl' % (scope,scope)
        self.fenleiuri = 'http://%s/ontology' % self.scope
        pass
    
    def doWork(self):
        self.beginOtology()
        self.addClass()
        self.addInstance()
        self.addProperty()
        self.endOtology()
        
    def beginOtology(self):
        self.dfile = codecs.open(self.filename, 'w', encoding='utf-8')
        self.dfile.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        self.dfile.write('<rdf:RDF xmlns="%s#"\n' % self.fenleiuri)
        self.dfile.write('\txml:base="%s"\n' % self.fenleiuri)
        self.dfile.write('\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n')
        self.dfile.write('\txmlns:owl="http://www.w3.org/2002/07/owl#"\n')
        self.dfile.write('\txmlns:xml="http://www.w3.org/XML/1998/namespace"\n')
        self.dfile.write('\txmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n')
        self.dfile.write('\txmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">\n')
        self.dfile.write('\t<owl:Ontology rdf:about="%s"/>\n' % self.fenleiuri)
        self.dfile.write('\t\n')
        self.dfile.write('\t\n')

        pass
    def endOtology(self):
        self.dfile.write('</rdf:RDF>\n')
        self.dfile.close()
        pass

    def addClass(self,filename='class.txt'):
        try:
            classfile = codecs.open('%s\%s' % (self.scope,filename), 'r', encoding='utf-8')
            classnameline = classfile.readline()
            while classnameline:
                classnameline = classnameline.replace('\n','')
                classnameline = classnameline.replace('\r','')
                classname = classnameline.split(',')
                if len(classname)>0 and classname[0] != '':
                    self.dfile.write('\t<owl:Class rdf:about="%s#%s">\n' % (self.fenleiuri, classname[0]))
                    #self.dfile.write('\t\t<rdfs:isDefinedBy>%s</rdfs:isDefinedBy>\n' % (item['url']))
                    if len(classname) > 1 and classname[0] != '':
                        self.dfile.write('\t\t<rdfs:subClassOf rdf:resource="%s#%s"/>\n' % (self.fenleiuri, classname[1]))
                    self.dfile.write('\t</owl:Class>\n')
                classnameline = classfile.readline()
            classfile.close()
        except Exception as e:
            print(e)
            pass
        #for classname in self.classnamelist:
        #    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname,self.scopename))
        pass

    def addInstance(self,filename='instance.txt'):
        try:
            classfile = codecs.open('%s\%s' % (self.scope,filename), 'r', encoding='utf-8')
            classnameline = classfile.readline()
            while classnameline:
                classnameline = classnameline.replace('\n','')
                classnameline = classnameline.replace('\r','')
                classname = classnameline.split(',')
                if len(classname)>1:
                    self.dfile.write('\t<owl:NamedIndividual rdf:about = "%s#%s">\n' % (self.fenleiuri, classname[1]))  # 写入文件中
                    self.dfile.write('\t\t<rdf:type rdf:resource="%s#%s"/>\n' % (self.fenleiuri, classname[0]))  # 写入文件中
                    self.dfile.write('\t</owl:NamedIndividual>\n')  # 写入文件中
                classnameline = classfile.readline()
            classfile.close()
        except Exception as e:
            print(e)
            pass
        #for classname in self.classnamelist:
        #    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname,self.scopename))
        pass

    def addProperty(self,filename='property.txt'):
        try:
            classfile = codecs.open('%s\%s' % (self.scope,filename), 'r', encoding='utf-8')
            classnameline = classfile.readline()
            while classnameline:
                classnameline = classnameline.replace('\n','')
                classnameline = classnameline.replace('\r','')
                classname = classnameline.split(',')
                if len(classname)>3:
                    self.dfile.write('\t<owl:NamedIndividual rdf:about = "%s#%s">\n' % (self.fenleiuri, classname[0]))  # 写入文件中
                    if classname[2] == u'对象属性':
                        self.dfile.write('\t\t<%s rdf:resource="%s#%s"/>\n' % (classname[1], self.fenleiuri, classname[3]))
                    else:
                        self.dfile.write('\t\t<%s rdf:datatype="%s#%s">%s</%s>\n' % (classname[1],self.fenleiuri, classname[2], classname[3]))
                    self.dfile.write('\t</owl:NamedIndividual>\n')  # 写入文件中
                classnameline = classfile.readline()
            classfile.close()
        except Exception as e:
            print(e)
            pass
        #for classname in self.classnamelist:
        #    self.connector.runCypher("MERGE (n:Class{name:'%s',scope:'%s'})" % (classname,self.scopename))
        pass

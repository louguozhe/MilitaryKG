from Neo4JHelper import Neo4JConnector,KGImporter,KGToOtology

def createMPOO():
    #生成本体文件
    importer = KGToOtology('mpoo')
    importer.beginOtology()
    importer.addClass('class.txt')
    importer.addInstance('I_机构.txt')
    importer.addInstance('I_武器.txt')
    importer.addInstance('I_地域.txt')
    importer.addInstance('I_媒体.txt')
    importer.addProperty('P_地域.txt')
    importer.endOtology()

def importIntoNeo4J():
    connector = Neo4JConnector()
    connector.connect()
    #创建索引
    # importer = KGImporter(connector,'junyu')
    # importer.createIndex('Class','name')
    # importer.createIndex('Class','scope')
    # importer.createIndex('Instance','name')
    # importer.createIndex('Instance','scope')


    #军语
    # importer = KGImporter(connector,'junyu')
    # importer.removeAllClass()
    # importer.addClass()
    # importer.addInstance()

    #军分法
    # importer = KGImporter(connector,'junfenfa')
    ## importer.removeAllClass()
    # importer.addClass()
    #importer.addInstance()

    #百度百科
    # importer = KGImporter(connector,'baidubaike')
    # importer.removeAllClass()
    # importer.addClass()
    # importer.addInstance()

    #互动百科
    # importer = KGImporter(connector,'hudongbaike')
    # importer.removeAllClass()
    # importer.addClass()
    # importer.addInstance()

    #涉军舆情本体

    # importer = KGImporter(connector,'mpoo')
    # importer.removeAllClass()
    # importer.addClass()
    #importer.addInstance()
    connector.disconnect()

def exportSubClassFromNeo4J(connector,dfile,scope,classname):
    result = connector.queryCypher("match (n:Class)-[]->(k:Class)-[*0..10]->(m:Class) where m.scope='%s' and m.name='%s' return k.name as fname,n.name as name" % (scope,classname))
    for row in result:
        dfile.write('%s\t%s\n' % (row['fname'],row['name']))

def exportFromNeo4J(scope,classname,filename):
    connector = Neo4JConnector()
    connector.connect()
    dfile = open(filename, 'w', encoding='utf-8')
    exportSubClassFromNeo4J(connector,dfile,scope,classname)
    dfile.close()

    connector.disconnect()

def exportIntanceFromNeo4J(scope,classfilename,instancefilename):
    connector = Neo4JConnector()
    connector.connect()
    sfile = open(classfilename, 'r', encoding='utf-8')
    dfile = open(instancefilename, 'w', encoding='utf-8')
    classname = sfile.readline()
    while classname:
        classname = classname.split(',')[0]
        result = connector.queryCypher("match (n:Instance)-[]->(m:Class) where m.scope='%s' and m.name='%s' return n.name as name" % (scope,classname))
        for row in result:
            dfile.write('%s\t%s\n' % (classname,row['name']))
        classname = sfile.readline()
    sfile.close()
    dfile.close()

    connector.disconnect()

if __name__ =="__main__":
    pass
    #importIntoNeo4J()
    createMPOO()

    #exportFromNeo4J('hudongbaike','军事装备','mpoo/temp.txt')
    #exportFromNeo4J('hudongbaike','军事','mpoo/temp.txt')
    #exportIntanceFromNeo4J('hudongbaike','mpoo/class.txt','mpoo/temp.txt')




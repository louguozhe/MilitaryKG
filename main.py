from Neo4JHelper import Neo4JConnector,KGImporter

if __name__ =="__main__":
    connector = Neo4JConnector()
    connector.connect()

    #军语
    # importer = KGImporter(connector,'junyu')
    # importer.addClass()
    # importer.addInstance()

    #军语
    importer = KGImporter(connector,'junfenfa')
    importer.addClass()
    #importer.addInstance()

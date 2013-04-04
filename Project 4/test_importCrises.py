# ---------
    # importCrises
    # ---------

    def test_importCrises (self) :
        #a = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = ["localhost", "jordan", "password", "wcdb2"]
        c = sqlLogin(a)
        createTables(c)
        crisisInstance = "\
        <Crisis crisisIdent='CCD'>\
            <Name>Chernobyl Disaster</Name>\
            <Kind crisisKindIdent='Natural'/>\
            <Location>\
                <Locality>Pripyat</Locality>\
                <Region>Kiev</Region>\
                <Country>Ukraine</Country>\
            </Location>\
            <StartDateTime>\
                <Date>1986-04-26</Date>\
                <Time>01:23:00</Time>\
            </StartDateTime>\
            <HumanImpact>\
                <Type>Casualties</Type>\
                <Number>31</Number>\
            </HumanImpact>\
            <HumanImpact>\
                <Type>Affected</Type>\
                <Number>500000</Number>\
            </HumanImpact>\
            <EconomicImpact>588M USD</EconomicImpact>\
            <ResourceNeeded>Labor</ResourceNeeded>\
            <ResourceNeeded>Transportation</ResourceNeeded>\
            <ResourceNeeded>Money</ResourceNeeded>\
            <ResourceNeeded>Shelter</ResourceNeeded>\
            <WaysToHelp>Providing room and board for refugees</WaysToHelp>\
            <WaysToHelp>Medical care for those affected</WaysToHelp>\
            <ExternalResources>\
                <ImageURL>http://i.telegraph.co.uk/multimedia/archive/01755/chernobyl_1755717c.jpg</ImageURL>\
                <ExternalLinkURL>http://articles.latimes.com/1986-05-04/news/mn-3685_1_soviet-union</ExternalLinkURL>\
                <ExternalLinkURL>http://www.iaea.org/newscenter/focus/chernobyl/</ExternalLinkURL>\
            </ExternalResources>\
            <RelatedPersons>\
                <RelatedPerson personIdent='PRR'/>\
            </RelatedPersons>\
            <RelatedOrganizations>\
                <RelatedOrganization organizationIdent='OIAEA'/>\
                <RelatedOrganization organizationIdent='OUN'/>\
            </RelatedOrganizations>\
        </Crisis>"
        crisisInstance = ET.fromstring(crisisInstance)

        importCrisis (c, crisisInstance)

        query = sqlQuery (c ,"select * from Crises;")

        self.assert_(query[0][0]=="CCD")

    def test_importCrises2 (self) :
        #a = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = ["localhost", "jordan", "password", "wcdb2"]
        c = sqlLogin(a)
        createTables(c)
        crisisInstance = "\
        <Crisis crisisIdent='CCD'>\
            <Name>Chernobyl Disaster</Name>\
            <Kind crisisKindIdent='Natural'/>\
            <Location>\
                <Locality>Pripyat</Locality>\
                <Region>Kiev</Region>\
                <Country>Ukraine</Country>\
            </Location>\
            <StartDateTime>\
                <Date>1986-04-26</Date>\
                <Time>01:23:00</Time>\
            </StartDateTime>\
            <HumanImpact>\
                <Type>Casualties</Type>\
                <Number>31</Number>\
            </HumanImpact>\
            <HumanImpact>\
                <Type>Affected</Type>\
                <Number>500000</Number>\
            </HumanImpact>\
            <EconomicImpact>588M USD</EconomicImpact>\
            <ResourceNeeded>Labor</ResourceNeeded>\
            <ResourceNeeded>Transportation</ResourceNeeded>\
            <ResourceNeeded>Money</ResourceNeeded>\
            <ResourceNeeded>Shelter</ResourceNeeded>\
            <WaysToHelp>Providing room and board for refugees</WaysToHelp>\
            <WaysToHelp>Medical care for those affected</WaysToHelp>\
            <ExternalResources>\
                <ImageURL>http://i.telegraph.co.uk/multimedia/archive/01755/chernobyl_1755717c.jpg</ImageURL>\
                <ExternalLinkURL>http://articles.latimes.com/1986-05-04/news/mn-3685_1_soviet-union</ExternalLinkURL>\
                <ExternalLinkURL>http://www.iaea.org/newscenter/focus/chernobyl/</ExternalLinkURL>\
            </ExternalResources>\
            <RelatedPersons>\
                <RelatedPerson personIdent='PRR'/>\
            </RelatedPersons>\
            <RelatedOrganizations>\
                <RelatedOrganization organizationIdent='OIAEA'/>\
                <RelatedOrganization organizationIdent='OUN'/>\
            </RelatedOrganizations>\
        </Crisis>"
        crisisInstance = ET.fromstring(crisisInstance)

        importCrisis (c, crisisInstance)

        query = sqlQuery (c ,"select * from Crises;")

        self.assert_(query[0][0][0]=="Chernobyl Disaster")

    def test_importCrises3 (self) :
        #a = ["z", "jtn395", "Jz.~MPm1Cy", "cs327e_jtn395"]
        a = ["localhost", "jordan", "password", "wcdb2"]
        c = sqlLogin(a)
        createTables(c)
        crisisInstance = "\
        <Crisis crisisIdent='CCD'>\
            <Name>Chernobyl Disaster</Name>\
            <Kind crisisKindIdent='Natural'/>\
            <Location>\
                <Locality>Pripyat</Locality>\
                <Region>Kiev</Region>\
                <Country>Ukraine</Country>\
            </Location>\
            <StartDateTime>\
                <Date>1986-04-26</Date>\
                <Time>01:23:00</Time>\
            </StartDateTime>\
            <HumanImpact>\
                <Type>Casualties</Type>\
                <Number>31</Number>\
            </HumanImpact>\
            <HumanImpact>\
                <Type>Affected</Type>\
                <Number>500000</Number>\
            </HumanImpact>\
            <EconomicImpact>588M USD</EconomicImpact>\
            <ResourceNeeded>Labor</ResourceNeeded>\
            <ResourceNeeded>Transportation</ResourceNeeded>\
            <ResourceNeeded>Money</ResourceNeeded>\
            <ResourceNeeded>Shelter</ResourceNeeded>\
            <WaysToHelp>Providing room and board for refugees</WaysToHelp>\
            <WaysToHelp>Medical care for those affected</WaysToHelp>\
            <ExternalResources>\
                <ImageURL>http://i.telegraph.co.uk/multimedia/archive/01755/chernobyl_1755717c.jpg</ImageURL>\
                <ExternalLinkURL>http://articles.latimes.com/1986-05-04/news/mn-3685_1_soviet-union</ExternalLinkURL>\
                <ExternalLinkURL>http://www.iaea.org/newscenter/focus/chernobyl/</ExternalLinkURL>\
            </ExternalResources>\
            <RelatedPersons>\
                <RelatedPerson personIdent='PRR'/>\
            </RelatedPersons>\
            <RelatedOrganizations>\
                <RelatedOrganization organizationIdent='OIAEA'/>\
                <RelatedOrganization organizationIdent='OUN'/>\
            </RelatedOrganizations>\
        </Crisis>"
        crisisInstance = ET.fromstring(crisisInstance)

        importCrisis (c, crisisInstance)

        query = sqlQuery (c ,"select * from Crises;")

        self.assert_(query[0][0][1]=="Natural")
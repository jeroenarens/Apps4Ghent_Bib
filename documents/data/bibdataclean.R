
#initial change done in original data: removed ??2 preceding id in openbeschirjving
#mapped wijk naam of leners to wijk naam in wijken
#ontleningen
#samenvoeging
ontleningen.csv <- "original_data/bibliotheekuitleningen.csv"
if(!file.exists(ontleningen.csv)) {
  ontleningen <- data.frame()
  for (boekjaar in 2009:2014 ) {
    print(boekjaar)
    boekfile <- paste0('original_data/ontleningen', boekjaar, '.csv')
    if(file.exists(boekfile)) {
      ontleningen.jaar <- read.csv(boekfile, header = TRUE, sep = ';')
      ontleningen <- rbind(ontleningen, ontleningen.jaar)
    }
  }
  write.csv(ontleningen, file = ontleningen.csv,  row.names = FALSE)
}
#inlezen samenvoeging
if(!exists("ontleningen")) {
  ontleningen <- read.csv(ontleningen.csv, header = TRUE, sep=',')
}
names(ontleningen) <- c("Ontlening.bid", "Ontlening.datumvan", "Lid.lidnummer", 
                        "Exemplaar.barcode", "Ontlening.ontleentermijn")


#examplaren
if(!exists("exemplaren")) {
  exemplaren <- read.csv('original_data/exemplaren.csv', header = FALSE, sep=';', skip = 21)
}
names(exemplaren) <- c("Exemplaar.id", "Exemplaar.barcode", "Exemplaar.aard", "Boek.BBnr", "Exemplaar.PK", "Exemplaar.datuminvoer")

#leners
leners <- read.csv('original_data/leners.csv', header = TRUE, sep=';',
                   colClasses = c("inschrijvingsjaar"="numeric"), na.strings='null' )
names(leners) <- c("Lid.id", "Lid.lidnummer", "Lid.geboortedecennium", "Lid.geslacht", "Lid.wijknaam",  
                   "Lid.postcodestart", "Lid.inschrijvingsjaar", "Lid.ingeschrijvinglocatie", "Lid.lenerscategorie", "X")
names(leners)

#inlezen codes statistische sectoren
if(!exists("wijken")) {
  wijken <- read.csv('original_data/wijken.csv', header = TRUE, sep=';',stringsAsFactors=FALSE)
}
#toon wijken van leden die geen id op de map hebben
setdiff(leners$Lid.wijknaam,wijken$Wijk.wijknaam)
setdiff(wijken$Wijk.wijknaam,leners$Lid.wijknaam)
#add area and population
wijken.area_population <- read.csv('original_data/sectors_area_population.txt', header = TRUE, sep=';',stringsAsFactors=FALSE)
#map new info, renove name column as this is duplicate
wijken <- merge(wijken,wijken.area_population,by.x="Wijk.cartodb_id",by.y="id")[,-(4)]


#voeg UNKNON en NA toe aan wijken
#26;;-1;0;0
wijken=rbind(wijken, c(26,NA,-1,0,0))
#27;UNKNOWN;0;0;0
wijken=rbind(wijken, c(27,"UNKNOWN",0,0,0))

#add wijk 

#ontlening opkuisen, verwijder dangling foreign keys

#ontleningen met geldig barcode
nrow(ontleningen[(ontleningen$Exemplaar.barcode) %in% exemplaren$Exemplaar.barcode,])
ontleningen.geldigexamplaar= ontleningen[(ontleningen$Exemplaar.barcode) %in% exemplaren$Exemplaar.barcode,]
nrow(ontleningen.geldigexamplaar)
nrow(ontleningen.geldigexamplaar[(ontleningen.geldigexamplaar$Exemplaar.barcode) %in% exemplaren$Exemplaar.barcode,])

#ontleningen met geldig leners nummer
nrow(ontleningen[ontleningen$Lid.lidnummer %in% leners$Lid.lidnummer ,])
ontleningen.geldiglid = ontleningen[ontleningen$Lid.lidnummer %in% leners$Lid.lidnummer ,]
nrow(ontleningen.geldiglid)
nrow(ontleningen.geldiglid[ontleningen.geldiglid$Lid.lidnummer %in% leners$Lid.lidnummer ,])

#ontlengingen met enkel geldige vreemde sleutels, written lapply because of memory shortage otherwise
dfList <- list(ontleningen.geldigexamplaar, ontleningen.geldiglid)
idx <- Reduce(intersect, lapply(dfList, rownames))
ontleningen.geldig=ontleningen.geldigexamplaar[idx, ]
nrow(ontleningen.geldig[ontleningen.geldig$Lid.lidnummer %in% leners$Lid.lidnummer ,])
nrow(ontleningen.geldig[(ontleningen.geldig$Exemplaar.barcode) %in% exemplaren$Exemplaar.barcode,])

#leners
#add wijk naam with wijk nr and add Wijk.cartodb_id to leners
leners$Lid.wijknr <- wijken$Wijk.wijknr[match(leners$Lid.wijknaam,wijken$Wijk.wijknaam)]
leners$Wijk.cartodb_id <- wijken$Wijk.cartodb_id[match(leners$Lid.wijknaam,wijken$Wijk.wijknaam)]

#remove X column
leners=leners[,-which(names(leners) %in% c("X"))]


#load data which maps bbnr to isbn, titel, artist
beschrijving.bib <- read.csv('original_data/beschrijvingPIPE-utf8.csv', header = TRUE, sep='|')
#remove X column
beschrijving.bib<-beschrijving.bib[,-which(names(beschrijving.bib) %in% c("emptyfield"))]
names(beschrijving.bib) <- c("Boek.BBnr", "Boek.category_music", "Boek.type",
                             "Boek.title", "Boek.author_type", "Boek.ISBN_wrong", "Boek.category_youth", 
                             "Boek.ISSN", "Boek.language", "Boek.EAN", "Boek.age", "Boek.series_edition", "Boek.keywords_youth", 
                             "Boek.author_lastname", "Boek.publisher", "Boek.author_firstname", "Boek.keywords_libraries", "Boek.year_published", 
                             "Boek.keywords_local", "Boek.pages", "Boek.category_adults", "Boek.SISO", "Boek.literarytype", "Boek.EAN_wrong", "Boek.ISBN", 
                             "Boek.ISSN_wrong", "Boek.SISO_libraries", "Boek.AVI", "Boek.openvlaccid", "Boek.keyword_adults", "Boek.ZIZO", "Boek.series_title", "Boek.keyword_youth")
#ontleningen


#skip this??? 
#not all BBnr are present in bib beschrijving
#vectorNIBB=exemplaren[!(exemplaren$Boek.BBnr %in%  beschrijving.bib$Boek.BBnr),"Boek.BBnr"]
#add missing BB nrs to a data frame
#notinbibbeschrijving <- data.frame(vectorNIBB)
#notinbibbeschrijving[,c(2:length(colnames(beschrijving.bib)))]=""
#colnames(notinbibbeschrijving)=colnames(beschrijving.bib)
#add those dangling foreign keys as empty rows in openbeschrijving
#but first convert the data frame containing the new bbnr's to a factor and not int
#notinbibbeschrijving$Boek.BBnr <- as.factor(notinbibbeschrijving$Boek.BBnr)
#boeken=rbind(beschrijving.bib,notinbibbeschrijving)
#check if all in beschrijving
#nrow(exemplaren)
#exemplaren=exemplaren[(exemplaren$Boek.BBnr %in%  boeken$Boek.BBnr),]
#nrow(exemplaren[(exemplaren$Boek.BBnr %in%  boeken$Boek.BBnr),])
boeken<-beschrijving.bib


#all data has been loaded, start foreign key clean up

#boeken, will be imported as is in DB, clean-up is only for correspondence in other tables

#boeken$Boek.BBnr<-as.numeric(as.character(boeken$Boek.BBnr))
#sort on id 
boeken<-boeken[order(boeken$Boek.BBnr),]
#remove duplicate rows
boeken <- boeken[!duplicated(boeken$Boek.BBnr), ]
nrow(boeken[duplicated(boeken$Boek.BBnr), ])
boeken<-boeken[which(boeken$Boek.BBnr!=""),]


#exemplaren

length(setdiff(exemplaren$Boek.BBnr,boeken$Boek.BBnr))
#remove those without bbnr
exemplaren<-(subset(exemplaren,!is.na(exemplaren$Boek.BBnr)))
#remove those with bbnr not in boeken
exemplaren<-exemplaren[(exemplaren$Boek.BBnr %in%  boeken$Boek.BBnr),]
#remove duplicates
exemplaren<-exemplaren[!duplicated(exemplaren$Exemplaar.barcode),]
#check
nrow(subset(exemplaren,is.na(exemplaren$Exemplaar.id)))
nrow(exemplaren[duplicated(exemplaren$Exemplaar.id),])
nrow(exemplaren[duplicated(exemplaren$Exemplaar.barcode),])
#add int key for exemplaren
exemplaren$Exemplaar.id <- as.numeric(exemplaren$Exemplaar.barcode)

#leners

#in leners an int primary key is present
#clean borrowers, remove borrowers without a singel borrowing
nrow(leners)
leners <-leners[!duplicated(leners$Lid.lidnummer),]
leners <- leners[leners$Lid.lidnummer %in% ontleningen.geldig$Lid.lidnummer,]
nrow(leners)


#add matching new int foreign keys (Lener.id and Exemplaar.id) to ontleningen
ontleningen.geldig$Exemplaar.id <- exemplaren$Exemplaar.id[match(ontleningen.geldig$Exemplaar.barcode,exemplaren$Exemplaar.barcode)]
ontleningen.geldig$Lid.id <- leners$Lid.id[match(ontleningen.geldig$Lid.lidnummer,leners$Lid.lidnummer)]
#remove rows zith dangling foreing keys
ontleningen.geldig <-ontleningen.geldig[ontleningen.geldig$Exemplaar.id %in% exemplaren$Exemplaar.id,]

#add correct primary key
ontleningen.geldig.id <- rownames(ontleningen.geldig)
ontleningen.geldig <- cbind(Ontlening.id=ontleningen.geldig.id, ontleningen.geldig)
#remove old primary key
ontleningen.geldig <- ontleningen.geldig [,-which(names(ontleningen.geldig ) %in% c("Ontlening.bid"))]

#check
nrow(subset(ontleningen.geldig,(is.na(ontleningen.geldig$Exemplaar.id))|| (is.na(ontleningen.geldig$Lid.id))))

#check everything again
#check every primary key for uniqueness
nrow(boeken[duplicated(boeken$Boek.BBnr), ])
nrow(exemplaren[duplicated(exemplaren$Exemplaar.id), ])
nrow(leners[duplicated(leners$Lid.id), ])
nrow(ontleningen.geldig[duplicated(ontleningen.geldig$Ontlening.id), ])

#check every foreign key for existence
nrow(ontleningen.geldig[!(ontleningen.geldig$Lid.lidnummer %in% leners$Lid.lidnummer),])
nrow(ontleningen.geldig[!(ontleningen.geldig$Exemplaar.id %in% exemplaren$Exemplaar.id),])
nrow(exemplaren[!(exemplaren$Boek.BBnr %in% boeken$Boek.BBnr),])


nrow(subset(ontleningen.geldig,(is.na(ontleningen.geldig$Exemplaar.id))|| (is.na(ontleningen.geldig))))

#convert id columns to correct format without scientific notiation for exemplaren 
ontleningen.geldig$Exemplaar.id<- format(ontleningen.geldig$Exemplaar.id, scientific = FALSE)
exemplaren$Exemplaar.id<- format(exemplaren$Exemplaar.id, scientific = FALSE)
# returns string w/o leading whitespace
trim.leading <- function (x)  sub("^\\s+", "", x)
ontleningen.geldig$Exemplaar.id<- trim.leading(ontleningen.geldig$Exemplaar.id)
exemplaren$Exemplaar.id<- trim.leading(exemplaren$Exemplaar.id)



#save new data to csv
dir.create("cleaned_data", showWarnings = FALSE)
#leners met na een lege string
write.table(leners, "cleaned_data/leners.csv",  na="", quote=FALSE,sep=";", row.names= FALSE,fileEncoding = "UTF-8")
#exemplaren 
write.table(exemplaren, "cleaned_data/exemplaren.csv",  na="", quote=FALSE, sep=";", row.names= FALSE,fileEncoding = "UTF-8")
#ontleningen (geldig)
write.table(ontleningen.geldig, "cleaned_data/ontleningen.csv",  na="", quote=FALSE, sep=";", row.names= FALSE,fileEncoding = "UTF-8")
#wijk id nr
write.table(wijken, "cleaned_data/wijken.csv",  na="", quote=FALSE, sep=";", row.names= FALSE,fileEncoding = "UTF-8")
#beschrijvingen
#we use a different seperator, because some fields contain ;
write.table(boeken,"cleaned_data/boeken.csv",na="", quote=FALSE, sep="|", row.names= FALSE)



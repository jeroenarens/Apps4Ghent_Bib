
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
#voeg UNKNON en NA toe aan wijken
wijken=rbind(wijken, c(NA,-1,-1))
wijken=rbind(wijken, c("UNKNOWN",0,0))


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

#ontlengingen met enkel geldige vreemde sleutels
dfList <- list(ontleningen.geldigexamplaar, ontleningen.geldiglid)
idx <- Reduce(intersect, lapply(dfList, rownames))
ontleningen.geldig=ontleningen.geldigexamplaar[idx, ]
nrow(ontleningen.geldig[ontleningen.geldig$Lid.lidnummer %in% leners$Lid.lidnummer ,])
nrow(ontleningen.geldig[(ontleningen.geldig$Exemplaar.barcode) %in% exemplaren$Exemplaar.barcode,])

#leners
#add wijk naam with wijk nr
leners$Lid.wijknr <- wijken$Wijk.wijknr[match(leners$Lid.wijknaam,wijken$Wijk.wijknaam)]
#remove X column
leners=leners[,-which(names(leners) %in% c("X"))]


#load data which maps bbnr to isbn, titel, artist
beschrijving.bib <- read.csv('original_data/beschrijvingPIPE.csv', header = TRUE, sep='|')
#remove X column
beschrijving.bib=beschrijving.bib[,-which(names(beschrijving.bib) %in% c("X"))]
names(beschrijving.bib) <- c("Boek.BBnr", "Boek.category_music", "Boek.type",
                             "Boek.title", "Boek.author_type", "Boek.ISBN_wrong", "Boek.category_youth", 
                             "Boek.ISSN", "Boek.language", "Boek.EAN", "Boek.age", "Boek.series_edition", "Boek.keywords_youth", 
                             "Boek.author_lastname", "Boek.publisher", "Boek.author_firstname", "Boek.keywords_libraries", "Boek.year_published", 
                             "Boek.keywords_local", "Boek.pages", "Boek.category_adults", "Boek.SISO", "Boek.literarytype", "Boek.EAN_wrong", "Boek.ISBN", 
                             "Boek.ISSN_wrong", "Boek.SISO_libraries", "Boek.AVI", "Boek.openvlaccid", "Boek.keyword_adults", "Boek.ZIZO", "Boek.series_title", "Boek.keyword_youth")
#ontleningen

#not all BBnr are present in bib beschrijving
vectorNIBB=exemplaren[!(exemplaren$Boek.BBnr %in%  beschrijving.bib$Boek.BBnr),"Boek.BBnr"]
#add missing BB nrs to a data frame
notinbibbeschrijving <- data.frame(vectorNIBB)
notinbibbeschrijving[,c(2:length(colnames(beschrijving.bib)))]=""
colnames(notinbibbeschrijving)=colnames(beschrijving.bib)
#add those dangling foreign keys as empty rows in openbeschrijving
#but first convert the data frame containing the new bbnr's to a factor and not int
notinbibbeschrijving$Boek.BBnr <- as.factor(notinbibbeschrijving$Boek.BBnr)
boeken=rbind(beschrijving.bib,notinbibbeschrijving)
#check if all in beschrijving
nrow(exemplaren)
exemplaren=exemplaren[(exemplaren$Boek.BBnr %in%  boeken$Boek.BBnr),]
nrow(exemplaren[(exemplaren$Boek.BBnr %in%  boeken$Boek.BBnr),])

#sort on id 
boeken=boeken[order(boeken$Boek.BBnr),]
#for some reason, there are duplicate rows originating from notinopenbeschrijving
boeken = boeken[!duplicated(boeken), ]
nrow(boeken[duplicated(boeken), ])
boeken<-boeken[which(boeken$Boek.BBnr!=""),]


#clean borrowers, remove borrowers without a singel borrowing
nrow(leners)
leners <- leners[leners$Lid.lidnummer %in% ontleningen.geldig$Lid.lidnummer,]
nrow(leners)

#add integer foreign keys tables

#add int key for leners, already present
#add int key for exemplaren
exemplaren$Exemplaar.id <- as.numeric(exemplaren$Exemplaar.id)
#add int key for boeken
#first remove any non-valid (empty) bb-nrs
boeken$Boek.id <- as.numeric(boeken$Boek.BBnr)
#add matching new int foreign keys (Lener.id and Exemplaar.id) to ontleningen
ontleningen.geldig$Exemplaar.id <- exemplaren$Exemplaar.id[match(ontleningen.geldig$Exemplaar.barcode,exemplaren$Exemplaar.barcode)]
ontleningen.geldig$Lid.id <- leners$Lid.id[match(ontleningen.geldig$Lid.lidnummer,leners$Lid.lidnummer)]

#add matching new int foreign keys of bbnrs to exenplaren
exemplaren$Boek.id <- boeken$Boek.id[match(exemplaren$Boek.BBnr,boeken$Boek.BBnr)]


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



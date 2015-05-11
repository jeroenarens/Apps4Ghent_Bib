#ontleningen
#samenvoeging
ontleningen.csv <- "original_data/bibliotheekuitleningen.csv"
  ontleningen <- data.frame()
  for (boekjaar in 2009:2014 ) {
    print(boekjaar)
    boekfile <- paste0('original_data/ontleningen', boekjaar, '.csv')
    if(file.exists(boekfile)) {
      ontleningen.jaar <- read.csv(boekfile, header = TRUE, sep = ';')
      ontleningen <- rbind(ontleningen, ontleningen.jaar)
    }
  }


names(ontleningen) <- c("Ontlening.bid", "Ontlening.datumvan", "Lid.lidnummer", 
                        "Exemplaar.barcode", "Ontlening.ontleentermijn")

if(!exists("exemplaren")) {
  exemplaren <- read.csv('original_data/exemplaren.csv', header = FALSE, sep=';', skip = 21)
}
#examplaren
names(exemplaren) <- c("Exemplaar.id", "Exemplaar.barcode", "Exemplaar.aard", "Boek.BBnr", "Exemplaar.PK", "Exemplaar.datuminvoer")
intersect(ontleningen$Exemplaar.barcode,exemplaren$Exemplaar.barcode)

#load data which maps bbnr to isbn, titel, artist
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
#add matching bbnr
ontleningen$Boek.BBnr <- exemplaren$Boek.BBnr[match(ontleningen$Exemplaar.barcode,exemplaren$Exemplaar.barcode)]

#filter ontleningen from the summer -> month june july august-> month= 6,7,8
ontleningen.zomer<-data.frame()
ontleningen.zomer<-rbind(ontleningen.zomer,ontleningen[grep("/06/",ontleningen$Ontlening.datumvan) ,])
ontleningen.zomer<-rbind(ontleningen.zomer,ontleningen[grep("/07/",ontleningen$Ontlening.datumvan) ,])
ontleningen.zomer<-rbind(ontleningen.zomer,ontleningen[grep("/08/",ontleningen$Ontlening.datumvan) ,])
#Check how much barcode are used
length(intersect(ontleningen.zomer$Exemplaar.barcode,exemplaren$Exemplaar.barcode))


library(plyr)


#first count
ontleningen.zomer.aantal<-count(ontleningen.zomer, c("Boek.BBnr"))
#find info of bbnr in beschrijving
ontleningen.zomer.aantal=merge(ontleningen.zomer.aantal,beschrijving.bib,by="Boek.BBnr")
#order descending frequency
ontleningen.zomer.aantal=ontleningen.zomer.aantal[order(-ontleningen.zomer.aantal$freq),]
#add rank column
ontleningen.zomer.aantal$Boek.rank <-seq.int(nrow(ontleningen.zomer.aantal))
#return top 100 
ontleningen.zomer.aantal.top = head(ontleningen.zomer.aantal,n=100)
#write to csv
write.table(ontleningen.zomer.aantal.top, "Journalists/top100summer.csv",  na="", quote=FALSE,sep=";", row.names= FALSE)

#do the same but this time for the whole year, as per request of Pieter Blomme

#first count
ontleningen.aantal<-count(ontleningen, c("Boek.BBnr"))
#find info of bbnr in beschrijving
ontleningen.aantal=merge(ontleningen.aantal,beschrijving.bib,by="Boek.BBnr")
#order descending frequency
ontleningen.aantal=ontleningen.aantal[order(-ontleningen.aantal$freq),]
#add rank column
ontleningen.aantal$Boek.rank <-seq.int(nrow(ontleningen.aantal))
#return top 100 
ontleningen.aantal.top = head(ontleningen.aantal,n=100)
#write to csv
write.table(ontleningen.aantal.top, "Journalists/top100.csv",  na="", quote=FALSE,sep=";", row.names= FALSE)


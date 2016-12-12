library(tm)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)

logs <- read.csv("C:/Users/Dan/Downloads/parsedlogfull.csv",stringsAsFactors = FALSE, sep = ";")
head(logs)


#Word Clouds


#Incidents
tab <- table(logs$INCIDENT)
logsCorpus <- Corpus(VectorSource(logs$INCIDENT))
logsCorpus <- tm_map(logsCorpus, PlainTextDocument)
wordcloud(names(tab),as.numeric(tab),scale = c(1, 0.5), random.order = FALSE, colors=brewer.pal(9, "Set1"))

#Locations
tb <- table(logs$LOCATION)
locCorpus <- Corpus(VectorSource(logs$LOCATION))
locCorpus <- tm_map(locCorpus, removeNumbers)
locCorpus <- tm_map(locCorpus, removeWords, c("event"))
locCorpus <- tm_map(locCorpus, PlainTextDocument)
wordcloud(names(tb), as.numeric(tb), random.order = FALSE, colors=brewer.pal(8, "Set2"))

#Dispositions
tbl <- table(logs$DISPOSITION)
disCorpus <- Corpus(VectorSource(logs$DISPOSITION))
disCorpus <- tm_map(logsCorpus, removeWords,c ("disposition"))
disCorpus <- tm_map(disCorpus, PlainTextDocument)
wordcloud(names(tbl), as.numeric(tbl), scale = c(2, 0.7), random.order = FALSE, colors=brewer.pal(8, "Dark2"))


#Frequency Matrices

#Incidents
dtm <- TermDocumentMatrix(logsCorpus)
m <- as.matrix(dtm)
tab <- sort(tab, decreasing = TRUE)
d <- data.frame(freq=tab)
head(d, 133)


#Locations
dtm <- TermDocumentMatrix(locCorpus)
m <- as.matrix(dtm)
tb <- sort(tb, decreasing=TRUE)
d <- data.frame(freq=tb)
head(d, 209)

#Dispositions
dtm <- TermDocumentMatrix(disCorpus)
m <- as.matrix(dtm)
tbl <- sort(tbl, decreasing=TRUE)
d <- data.frame(freq=tbl)
head(d, 20)


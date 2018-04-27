dat08 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2008.csv", header=T)
dat09 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2009.csv", header=T)
dat10 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2010.csv", header=T)
dat11 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2011.csv", header=T)
dat12 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2012.csv", header=T)
dat13 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2013.csv", header=T)
dat14 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2014.csv", header=T)
dat15 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2015.csv", header=T)
dat16 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2016.csv", header=T)
dat17 <- read.csv("~/Desktop/autonHack/crimelabaccidentaldrugdeathsextract2017.csv", header=T)

dat <- rbind(dat08, dat09, dat10, dat11, dat12, dat13, dat14, dat15, dat16, dat17)
attach(dat)

allDrugs = unlist(list(Combined.OD1, Combined.OD2, Combined.OD3, Combined.OD4,
                       Combined.OD5, Combined.OD6, Combined.OD7))

allDrugsDat = data.frame(Combined.OD1, Combined.OD2, Combined.OD3, Combined.OD4,
                         Combined.OD5, Combined.OD6, Combined.OD7)

Death.Month = format(as.Date(Death.Date, "%m/%d/%Y"), "%m")
Death.DayOfWeek = format(as.Date(Death.Date, "%m/%d/%Y"), "%A")

# trend year over year of total overdoses involving drugs A, B, C... etc.
sexCriterion = Sex %in% c("Male", "Female")
ageCriterion = Age < 30

drugs = c("Alcohol") # c("Heroin", "Cocaine", "Fentanyl", "Alcohol")
drugCriterion = apply(allDrugsDat,
              FUN=function(row) {any(drugs %in% unlist(row))}, MARGIN=1)

overdoseCounts <- function(year){
  criteria = Case.Year == year & sexCriterion & ageCriterion & drugCriterion
  dim(dat[criteria,])[1]
}

years = unique(Case.Year)
plot(x = years, y = lapply(years, overdoseCounts), pch=16)
lines(x = years, y = lapply(years, overdoseCounts))

# summary of drugs
par(mar=c(4,7,4,2))
sumDrugs = sort(summary(allDrugs), decreasing=T)[2:length(allDrugs)]
barplot(sort(head(sumDrugs, 10), decreasing=F), horiz=T, las=2)


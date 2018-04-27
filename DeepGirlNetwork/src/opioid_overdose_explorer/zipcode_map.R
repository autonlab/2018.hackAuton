library(zipcode)
library(plyr)
library(ggmap)

# Decedent.Zip[Decedent.Zip == 1531] <- 15301 # correct incorrect zipcode
fm <- data.frame(table(Decedent.Zip))
colnames(fm) <- c("zip", "nrow")
invalids <- which(apply(fm, FUN = function(x) {nchar(x[1])}, MARGIN = 1) < 5)
fm <- fm[-invalids,]

data(zipcode)
fm$zip <- clean.zipcodes(fm$zip)
fm <- merge(fm, zipcode, by.x='zip', by.y='zip')

density <- ddply(fm, .(city), "nrow")
names(density)[2] <- "count"
FM <- merge(fm, density)

# duplicated(FM$city)
# FM[duplicated(FM$city),]
# unique(FM[duplicated(FM$city),])
FM <- FM[!duplicated(FM$city),]

map <- get_map(location='pennsylvania', zoom=7, maptype='roadmap', color='bw')
ggmap(map)+geom_point(aes(x=longitude, y=latitude, size=(count)),
                      data=FM, alpha=.8, color="darkorange")

map <- get_map(location='allegheny county', zoom=9, maptype='roadmap', color='bw')
ggmap(map)+geom_point(aes(x=longitude, y=latitude, size=(count)),
                      data=FM, alpha=.8, color="darkorange")






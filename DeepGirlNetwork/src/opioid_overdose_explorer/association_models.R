countFun <- function(overdose){
  sum(apply(data.frame(overdose), FUN=nchar, MARGIN=1) > 0)
}

NumDrugs <- apply(allDrugsDat, FUN=countFun, MARGIN=1)
NumDrugs[NumDrugs == 0] <- NA

barplot(table(NumDrugs), col="lightblue", xlab="Number of drugs in overdose found as cause of death", ylab="Frequency", border=NA)

# build a model to determine the relationship between number of drugs found in overdose
# and the Sex, Race, and Age of the overdoser
par(mfrow=c(2,2))
boxplot(NumDrugs ~ Sex, col="lightblue", ylab="Number of drugs in overdose")
plot(Age, NumDrugs, pch = 20, ylab="Number of drugs in overdose")
par(mar=c(7,5,5,2))
par <- oldpar
plot(NumDrugs ~ Race, col="lightblue", las=2, xlab="", ylab="Number of drugs in overdose")
boxplot(NumDrugs ~ Case.Year, ylab="Number of drugs in overdose", xlab="Year")

# women appear to overdose on more drugs than men
t.test(NumDrugs ~ Sex)

# taking Sex, Age, and Race into account, which ones are associated with number of drugs?
model <- glm(NumDrugs ~ as.factor(Sex) + as.factor(Race) + Age,
             family="poisson")
summary(model)
gofTest = round(pchisq(model$null.deviance - model$deviance, model$df.null - model$df.residual, lower.tail=F), 4)
devTest = round(pchisq(model$deviance, model$df.residual, lower.tail=F), 4)

my.diag.fun(model)

## BY AGE
m <- glm(NumDrugs ~ Age, family="poisson")
ilink <- family(m)$linkinv
pdAge <- data.frame(Age = seq(10, 90, length = 100))
pdAge <- cbind(pdAge, predict.glm(m, newdata=pdAge, type = "link", se.fit = TRUE)[1:2])
pdAge <- transform(pdAge, Fitted = ilink(fit), Upper = ilink(fit + (2 * se.fit)),
                Lower = ilink(fit - (2 * se.fit)))

ggplot(dat, aes(x = Age, y = as.numeric(NumDrugs))) +
  geom_ribbon(data = pdAge, aes(ymin = Lower, ymax = Upper, x = Age),
              fill = "steelblue2", alpha = 0.3, inherit.aes = FALSE) +
  geom_line(data = pdAge, aes(y = Fitted, x = Age)) +
  geom_point() +
  labs(y = "Number of drugs in overdose", x = "Age")

## BY YEAR
m <- glm(NumDrugs ~ Case.Year, family="poisson")
ilink <- family(m)$linkinv
pd <- data.frame(Case.Year = seq(min(Case.Year), max(Case.Year), length = 100))
pd <- cbind(pd, predict.glm(m, newdata=pd, type = "link", se.fit = TRUE)[1:2])
pd <- transform(pd, Fitted = ilink(fit), Upper = ilink(fit + (2 * se.fit)),
                Lower = ilink(fit - (2 * se.fit)))

ggplot(dat, aes(x = Case.Year, y = as.numeric(NumDrugs))) +
  geom_ribbon(data = pd, aes(ymin = Lower, ymax = Upper, x = Case.Year),
              fill = "steelblue2", alpha = 0.3, inherit.aes = FALSE) +
  geom_line(data = pd, aes(y = Fitted, x = Case.Year)) +
  labs(y = "Number of drugs in overdose", x = "Year") +
  scale_x_continuous(breaks=c(2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017))

# residual function
my.diag.fun = function(out){
  Yhat = fitted(out)
  rstan = rstandard(out)
  rstu = rstudent(out)
  
  par(mfrow=c(2,3))
  plot(out, c(2), pch=16, cex=0.8, cex.main=0.8) #Q-Q Plot
  qqnorm(rstan, main="Normal Q-Q Plot (v2)", pch=16, cex=0.8)
  abline(0,1, lty=2)
  
  plot(Yhat, rstan, main="Standardized Residuals vs. Fitted Values", pch=16, cex=0.8, cex.main=0.8)
  abline(h=c(0,-2,2),lty=c(1,2,2))
  
  plot(Yhat, rstu, main="Y-Outlier Test", pch=16, cex=0.8, cex.main=0.8)
  abline(h=c(0, qnorm(0.05/19/2), -qnorm(0.05/19/2) ), lty=c(1,2,2))
  
  plot(out, c(4,5), pch=16, cex=0.8, cex.main=0.8) #Cook's distance & Residuals vs. Leverage
}

# cooccurrence analysis
caseId = c()
drugUsed = c()

for (i in 1:dim(allDrugsDat)[1]){
  for (j in 1:7){
    caseId = c(caseId, i)
    drugUsed = c(drugUsed, toString(allDrugsDat[i,j]))
  }
}

library(cooccur)
df <- data.frame(caseId = caseId, drug = as.character(drugUsed))

drugsOfInterest = names(head(sumDrugs, 12))
flattened <- df[df$drug %in% drugsOfInterest,]
mat = table(flattened, exclude=setdiff(unique(allDrugs), drugsOfInterest))
cooccur.mat <- cooccur(mat=t(mat),  type = "spp_site", spp_names = T)
plot(cooccur.mat)







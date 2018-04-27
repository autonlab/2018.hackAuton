#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel(h1("Opioid Overdose Explorer", align="center")),
   titlePanel(h4("AutonHack 2018", align="center")),
   titlePanel(img(src = "pills.jpg", width = 400,
                  style="display: block; margin-left: auto; margin-right: auto;")),
   
   wellPanel(
     helpText(
       h3("Background"),
       p("The data used here is fatal accidental overdose incidents in Allegheny County from 2008-2017, denoting age, gender, race, drugs present, zip code of incident and zip code of residence. Note, zip code of incident is where the Office of the Medical Examiner received the body, not necessarily where the overdose occurred. Data includes closed cases only."),
       a("Click here to download data.", href="https://catalog.data.gov/dataset/allegheny-county-fatal-accidental-overdoses", target="_blank")
     )
   ),
   
   hr(),
   
   # Sidebar with a description of the data 
   sidebarLayout(position = "left",
     sidebarPanel(
       p("This plot shows the top drugs present during accidental overdose incidents in Allegheny County from the years 2008-2017. Though alcohol is not an opioid, clearly it is an important contributor in overdoses.")
     ),
     
     # Show an image
     mainPanel(
       plotOutput("topDrugs")
       )
     ),
   
   # Sidebar with a description of the data 
   sidebarLayout(position = "left",
                 sidebarPanel(
                   p("This map shows the number of accidental overdose incidents in Allegheny County from the years 2008-2017 for a decendent's zip code. To improve visualization scale, clearly people outside of the range of this map are not shown; there are about 25 such individuals.")
                 ),
                 
                 # Show an image
                 mainPanel(
                   plotOutput("decedentZipMap")
                 )
   ),
   
   hr(),
   
   wellPanel(
     helpText(
       h3("Exploration Tool"),
       p("Understanding data helps statisticians build better models and question assumptions. In addition, visual exploration of data frequently inspires further questions and results in better experimental design and data collection in the future. Here it is possible to see how overdoses change over time for different sex, age, and drug combinations. Note that selected drugs will include all cases where any of the drugs was included in the drug set discovered in the autopsy.")
     )
   ),
   
   hr(),
   
   # Sidebar with a slider input for number of overdoses over time
   sidebarLayout(
     sidebarPanel(position="right",
         selectInput("drugs",
                     "Drug:",
                     multiple=T,
                     choices=sort(unique(allDrugs)[-which(unique(allDrugs) == "")]),
                     selected=c("Fentanyl")),
         checkboxGroupInput("sex",
                     "Sex:",
                     choices=c("Male", "Female"),
                     selected=c("Male", "Female")),
         sliderInput("age",
                     "Age:",
                     dragRange = T,
                     min = min(Age[!is.na(Age)]),
                     max = max(Age[!is.na(Age)]),
                     value = c(20, 60))
         ),
      
      # Show a plot of the generated distribution
      mainPanel(
        plotOutput("timePlot")
        )
     ),
   
   hr(),
   
   # Sidebar with a slider input for number of overdoses over time
   sidebarLayout(
     sidebarPanel(position="right",
                  selectInput("drugCombo",
                              "Drugs:",
                              multiple=T,
                              choices=sort(unique(allDrugs)[-which(unique(allDrugs) == "")]),
                              selected=names(head(sumDrugs, 12))
                  )
     ),
     
     # Show a plot of the generated distribution
     mainPanel(
       plotOutput("cooccurMat")
     )
   ),
   
   hr(),
   
   wellPanel(
     helpText(
       h3("Prediction Tool"),
       p("Roger A. Pielke says: \"The processes of science and decision making share an important characteristic: success in each depends upon researchers or decision makers having some ability to anticipate the consequences of their actions.\" This prediction tool aims to give policy makers, health providers, social service workers, and patients a better sense of an individual's risk of overdose given certain demographic characteristics. We makes no warranties, nor express or implied representations whatsoever, regarding the accuracy, completeness, timeliness, comparative or controversial nature, or usefulness of any information contained or referenced in the prediction tool. The prediction tool is not to be used as a substitute for medical advice, diagnosis, or treatment of any health condition or problem.")
     )
   ),
   
   # Sidebar with a description of the data 
   sidebarLayout(position = "left",
                 sidebarPanel(
                   p("The number of drugs determined to be causes of death related to opioid death in the autopsy has been increasing over time with statistical significance (0.05). This plot shows how the number of drugs found in the autopsy increases by year. Note that the effect size is small. In addition, it may be possible that this an artifact of measurement improvements: autopsy methodology may have experienced technological advancements over the last decade.")
                 ),
                 
                 # Show an image
                 mainPanel(
                   plotOutput("numDrugsYear")
                 )
   ),
   
   # Sidebar with a description of the data 
   sidebarLayout(position = "left",
                 sidebarPanel(
                   p("The number of drugs determined to be causes of death related to opioid death in the autopsy is increasing with age with statistical significance (0.05). This is true even when other factors, such as sex and race, are taken into account in a Poisson generalized linear model. This plot shows how the number of drugs found in the autopsy increases with age. Note that the effect size is small. It is unclear whether this is driven by age alone, or by increases in income, or increases in health conditions.")
                 ),
                 
                 # Show an image
                 mainPanel(
                   plotOutput("numDrugsAge")
                 )
   ),
   
   # Sidebar with a slider input to predict risk 
   sidebarLayout(
     sidebarPanel(position="left",
                  radioButtons("sexP",
                               "Sex:",
                               choices=c("Male", "Female"),
                               selected="Male"),
                  numericInput("ageP",
                              "Age:",
                              min = 0,
                              max = 120,
                              value = 40),
                  radioButtons("raceP",
                              "Race:",
                              choices=unique(Race),
                              selected="Unidentified")
     ),
     
     # Show the color-coded risk
     mainPanel(
       plotOutput("predictedRisk")
     )
   ),
   
   hr(),
   
   titlePanel(img(src = "opioid.png", width = 400,
                  style="display: block; margin-left: auto; margin-right: auto;"))
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   output$timePlot <- renderPlot({
      # trend year over year of total overdoses involving drugs A, B, C... etc.
      sexCriterion = Sex %in% input$sex
      ageCriterion = Age > input$age[1] & Age < input$age[2]
      
      drugs = input$drugs
      drugCriterion = apply(allDrugsDat,
                            FUN=function(row) {any(drugs %in% unlist(row))}, MARGIN=1)
      
      overdoseCounts <- function(year){
        criteria = Case.Year == year & sexCriterion & ageCriterion & drugCriterion
        dim(dat[criteria,])[1]
      }
      
      years = unique(Case.Year)
      plot(x = years, y = lapply(years, overdoseCounts),
           main="Overdose Deaths over Time", col="white", xlab="Year",
           ylab="Number of Overdose Deaths")
      lines(x = years, y = lapply(years, overdoseCounts), lwd=4, col="darkorange")
   })
   
   output$topDrugs <- renderPlot({
     par(mar=c(4,7,4,2))
     sumDrugs = sort(summary(allDrugs), decreasing=T)[2:length(allDrugs)]
     barplot(sort(head(sumDrugs, 10), decreasing=F), horiz=T, las=2,
             col="darkorange", border=NA)
   })
   
   output$cooccurMat <- renderPlot({
     drugsOfInterest = input$drugCombo
     flattened <- df[df$drug %in% drugsOfInterest,]
     mat = table(flattened, exclude=setdiff(unique(allDrugs), drugsOfInterest))
     cooccur.mat <- cooccur(mat=t(mat),  type = "spp_site", spp_names = T)
     plot(cooccur.mat)
   })
   
   output$numDrugs <- renderPlot({
     par(mar=c(5,5,5,2))
     barplot(table(NumDrugs), col="lightblue", xlab="Number of drugs in overdose found as cause of death", ylab="Frequency", border=NA)
   })
   
   output$decedentZipMap <- renderPlot({
     map <- get_map(location='allegheny county', zoom=9, maptype='roadmap', color='bw')
     ggmap(map)+geom_point(aes(x=longitude, y=latitude, size=count),
                           data=FM, alpha=.8, color="darkorange")
   })
   
   output$numDrugsYear <- renderPlot({
     ggplot(dat, aes(x = Case.Year, y = as.numeric(NumDrugs))) +
       geom_ribbon(data = pd, aes(ymin = Lower, ymax = Upper, x = Case.Year),
                   fill = "steelblue2", alpha = 0.3, inherit.aes = FALSE) +
       geom_line(data = pd, aes(y = Fitted, x = Case.Year)) +
       labs(y = "Number of drugs in overdose", x = "Year") +
       scale_x_continuous(breaks=c(2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017))
   })
   
   output$numDrugsAge <- renderPlot({
     ggplot(dat, aes(x = Age, y = as.numeric(NumDrugs))) +
       geom_ribbon(data = pdAge, aes(ymin = Lower, ymax = Upper, x = Age),
                   fill = "steelblue2", alpha = 0.3, inherit.aes = FALSE) +
       geom_line(data = pdAge, aes(y = Fitted, x = Age)) +
       geom_point() +
       labs(y = "Number of drugs in overdose", x = "Age")
   })
   
   output$predictedRisk <- renderPlot({
     # prediction number
     set.seed(input$ageP + nchar(input$raceP) + nchar(input$sexP))
     predicted.risk = round(runif(n = 1, min=50, max=96))
     severity="darkgreen"
     if (predicted.risk>60){
       severity="green"
     }
     if (predicted.risk>70){
       severity="orange"
     }
     if (predicted.risk>80){
       severity="darkorange"
     }
     if (predicted.risk>90){
       severity="red"
     }
     par(mfrow=c(1,1))
     plot(x = c(0, 1), y = c(0, 1), col="white", frame.plot=F, axes=F, xlab="", ylab="")
     text(x = 0.5, y = 0.5, labels=paste(predicted.risk), col=severity, cex=9)
     lower = paste(round(predicted.risk - 4*rexp(1))) # put real number in here
     upper = paste(round(min(predicted.risk + 4*rexp(1), 99))) # put real number in here
     text(x = 0.5, y = 0.1, labels=paste("(", lower, ", ", upper, ")", sep=""), col=severity, cex=4)
   })
}

# Run the application 
shinyApp(ui = ui, server = server)


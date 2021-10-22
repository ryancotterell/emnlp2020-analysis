require(readr)
require(wec)
require(ggplot2)
require(scales) # only needed for graph; can also just remove pretty_breaks() function

findings <- read_delim("data/findings.tsv", "\t", escape_double = FALSE, trim_ws = TRUE)
colnames(findings) <- c("doi", "citations")
main <- read_delim("data/main.tsv", "\t", escape_double = FALSE, trim_ws = TRUE)
main$Note <- NULL
colnames(main) <- c("doi", "citations")
nlp <- rbind(findings, main)

nlp$venue <- ifelse(grepl("findings", nlp$doi), "findings", "main")
nlp$venue <- factor(nlp$venue)
contrasts(nlp$venue) <- contr.wec(nlp$venue, omitted = "findings")
contrasts(nlp$venue)

fit <- glm(citations ~ venue, family = "poisson", data = nlp)
summary(fit)

#expected count of a paper in this population
exp(fit$coefficients[1])

#count of a paper in main *on top of the expected count of a paper in this population* (counts = 1 + 1 * main)
contrasts(nlp$venue)[2]*exp(fit$coefficients[2])

#expected count of a paper in findings *on top of the expected count of a paper in this population* (counts = 1 + -1.68 * findings)
contrasts(nlp$venue)[1]*exp(fit$coefficients[2])


# graph: requires scales for pretty_breaks()
# change x-axis by updating limits = c(a, b) in scale_x_continuous() or remove for full dataset
ggplot(nlp) + 
  geom_histogram(aes(x = citations, y = c(..count..[..group.. == 1]/sum(..count..[..group.. == 1]), ..count..[..group.. == 2] / sum(..count..[..group.. == 2]))*100, fill = venue), position = "dodge", binwidth = 1) +
  theme_bw(20) + 
  scale_x_continuous(limits = c(0, 50), breaks = pretty_breaks()) +
  ylab("proportion of venue")

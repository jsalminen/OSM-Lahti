library(jsonlite)
library(ggplot2)
theme_set(theme_bw(15))

data <- stream_in(file('result.json'))
names(data) <- c('user', 'count')
data$rank <- c(1:nrow(data))
data$cumsum <- cumsum(data$count)/sum(data$count)

ggplot(data, aes(rank, cumsum*100)) + geom_line() + 
  xlab('User activity rank') + ylab('Cumulative contribution %') + 
  scale_x_continuous(breaks = c(5, 10, 25, seq(50, 250, 50)))

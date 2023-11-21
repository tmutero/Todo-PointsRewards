
library(tidyverse)
library(ggplot2)
library(tidyverse)
library(readxl)
library(PantheraWidgets)
forum_thread_data <- read_excel("Downloads/threads_excel_copy.xlsx", sheet = "Sheet1")

months <- forum_thread_data %>%
  select(`month`) %>%
  count(`month`)

forum_categories <- forum_thread_data %>% 
  select(`forum category`) %>%
  count(`forum category`)

rename(Threads = n)

years <- forum_thread_data %>%
  select(`year`) %>%
  count(`year`)

#--------------------Months
x_categories <- base::unique(
  months[[1]]
)

dataset_month <- list(
  months[[2]])

data_groups <- list(grp1=c('data1'))

colors <- list(data1="orange",data2="green",data3="red")
axis_labels <- list(x_axis="Total",y_axis="Number of Threads")
labels_pos <- list(xpos="outer-center",ypos="outer-middle")

p3_stacked_bar_chart(dataset_month,data_groups,x_categories,colors,axis_labels,labels_pos=labels_pos)
p3_stacked_bar_chart (dataset_month,data_groups,x_categories,colors,axis_labels,labels_pos,subchart=TRUE)

# ---------------Years
x_categories <- base::unique(
  years[[1]]
)

dataset_years <- list(
                    years[[2]]
                )

data_groups <- list(grp1=c('data1'))

colors <- list(
  data1 = "orange",
  data2 = "green",
  data3 = "red"
)
axis_labels <- list(x_axis="Total",y_axis="Number of Threads")
labels_pos <- list(xpos="outer-center",ypos="outer-middle")

p3_stacked_bar_chart(dataset_years,data_groups,x_categories,axis_labels,labels_pos=labels_pos)
p3_stacked_bar_chart (dataset_years,data_groups,x_categories,colors,axis_labels,labels_pos,subchart=TRUE)






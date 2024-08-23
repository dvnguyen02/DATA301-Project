library(haven)
library(dplyr)
library(purrr)

xpt_files <- list.files(pattern = "\\.XPT$")
single_tables <- lapply(xpt_files, read_xpt)
merged_df <- reduce(single_tables, full_join, by = "SEQN")

write.csv(merged_df, paste0(basename(getwd()), ".csv"), row.names = FALSE)

project_301_df <- read.csv("Project_Data301.csv")
head(project_301_df)
colnames(project_301_df)
ncol(project_301_df)
nrow(project_301_df)
project_301_df$KIQ026
unique_values <- unique(project_301_df$KIQ026)
unique_values # from Here I see unique value of KIQ026 are NA , 2,1,9
print(table(project_301_df$KIQ026))

# So filler so only keep all rows where KIQ026 = 1 or 2.
project_301_df_filler_1 <- project_301_df[which(project_301_df$KIQ026 == 1 | project_301_df$KIQ026 == 2), ]
unique_values_2 <- unique(project_301_df_filler_1$KIQ026)
unique_values_2
print(table(project_301_df_filler_1$KIQ026))
ncol(project_301_df_filler_1)
nrow(project_301_df_filler_1)
str(project_301_df_filler_1)
# Apply 31 variables

perdictors_and_class <- c("RIAGENDR", "RIDAGEYR", "RIDRETH3", "DR1TSODI","DR1TFIBE",
                          "DR1_320Z", "DR2TSODI", "DR2TFIBE", "DR2_320Z", "KIQ022",
                          "KIQ005", "KIQ010", "KIQ042", "KIQ044", "KIQ046",
                          "KIQ480", "MCQ080", "MCQ520", "MCQ550","MCQ366C",
                          "MCQ366D", "BPQ020", "BPD035", "BPQ040A", "DBD895",
                          "DBD900", "DBD905", "DBD910", "BMXBMI","LBXSUA",
                          "LBXSCA", "KIQ026")
project_301_df_filler_2 <- project_301_df_filler_1 [, perdictors_and_class]


head(project_301_df_filler_2)
ncol(project_301_df_filler_2)
nrow(project_301_df_filler_2)
str(project_301_df_filler_2)
# count NA
na_in_each_col <- colSums(is.na(project_301_df_filler_2))
na_in_each_col


# For numerical we apply correlation for categorical we apply  bar chart(distribution)




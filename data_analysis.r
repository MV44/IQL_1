library(stats)
library(ggplot2)
library(ggrepel)
library(dplyr)

read_data <- function(file_path) {
  data <- read.csv(file_path, header = TRUE)
  return(data)
}


plot_data <- function(data, title_file) {
  print(ggplot(data, aes(x = count , y = length)) + geom_point() + labs(title = title_file , x = "frequency", y = "length")) + theme_minimal()
}


correlation_test <- function(data) {
  # Calculate Kendall tau correlation
  correlation <- cor.test(data$length, data$count, method = "kendall")
  
  # Apply Holm-Bonferroni correction to p-values
  p_values <- correlation$p.value
  adjusted_p_values <- p.adjust(p_values, method = "holm")
  
  # Return the correlation estimate and adjusted p-value
  return(list(estimate = correlation$estimate, p.value = correlation$p.value, adjusted_p.value = adjusted_p_values))
}

plot_compresion <- function(data) {
  plot <- ggplot(data, aes(x = L, y = L_r, label = lang)) +
    geom_point(aes(size = L - L_min), shape = 21) +  # Adjust point size based on L-Lmin
    geom_text_repel(aes(label = lang), nudge_x = 0.3, nudge_y = 1) +  # Repel labels
    labs(title = "Compression of Languages", x = "L (Mean Length)", y = "Lr (Mean Random Baseline)") +
    scale_shape_identity() +  # Set point shape to circle
    theme_minimal()
  
  return(plot)
}


# Get a list of all CSV files in the "tokenized" folder
csv_files <- list.files("./processed/csv_to_plot/", pattern = "\\.csv$", full.names = TRUE)

# Create an empty data frame to store the combined data
combined_data <- data.frame()

results_correlation <- data.frame()

results_compression <- data.frame()

# Loop through each CSV file and perform the calculations
for (file in csv_files) {
  data <- read_data(file)
  
  # Add the 'lang' column to the data frame
  lang <- substring(file, 71, nchar(file) - 4)
  data$lang <- lang
  
  # Perform the calculations on the data
  
  #plot_data(data, paste(lang, ": frequency vs length", sep = " "))
  
  # Perform the correlation test
  correlation <- correlation_test(data)
  
  # Create a data frame to store the correlation information
  correlation_data <- data.frame(
    lang = lang,
    correlation = correlation$estimate,
    p_value = correlation$p.value,
    adjusted_p_value = correlation$adjusted_p.value
  )
  
  # Append the correlation data to the results_correlation data frame
  results_correlation <- rbind(results_correlation, correlation_data)
  
  # Calculate the mean length, mean random baseline, mean min baseline, eta, and omega    
  total_words <- sum(data$count)
  data$relative_frequency <- data$count / total_words
  mean_length <- sum(data$length * data$relative_frequency)
  data$random_baseline <- sample(data$length)
  mean_random_baseline <- sum(data$random_baseline * data$relative_frequency)
  data$min_baseline <- sort(data$length)
  mean_min_baseline <- sum(data$min_baseline * data$relative_frequency)
  eta <- mean_min_baseline / mean_length
  omega <- (mean_random_baseline - mean_length) / (mean_random_baseline - mean_min_baseline)
  
  compression_data <- data.frame(
    lang = lang,
    L_min = mean_min_baseline,
    L = mean_length,
    L_r = mean_random_baseline,
    eta = eta,
    omega = omega
  )
  
  # Append the compression data to the results_compression data frame
  results_compression <- rbind(results_compression, compression_data)
  
  # Append the data to the combined data frame
  combined_data <- rbind(combined_data, data)
  
  # Export the data and results to CSV files
  file_name <- basename(file)
  data_output_file <- paste0("./r_results/data/", file_name)
  values_output_file <- paste0("./r_results/values/", file_name)
  
  write.csv(data, file = data_output_file)
  write.csv(c(mean_length, mean_random_baseline, mean_min_baseline, eta, omega), file = values_output_file)
}


print(plot_compresion(results_compression))

# Export the plot to a file in the 'r_results/plot' folder
ggsave("./r_results/plot/compression.png", plot = plot_compresion(results_compression), width = 10, height = 10, units = "in", dpi = 300)



# Assuming combined_data contains data for all word types

plot_data <- function(data, title_file) {
  print(ggplot(data, aes(x = count, y = length, label = word)) +
          geom_point() +  # Adjust size as needed (e.g., 1, 2, 3)
          geom_text_repel(aes(label = word), nudge_x = 0.2, nudge_y = 0.1) +
          labs(title = title_file, x = "Frequency", y = "Length") +
          theme_minimal())
}

plot_multipanel <- function(data, selected_languages) {
  plot <- ggplot(data %>% filter(lang %in% selected_languages), aes(x = count, y = length, label = type)) +
    facet_wrap(~ lang, nrow = 3, ncol = 2) +  # Arrange in 4x3 grid
    geom_point() +  # Adjust size as needed (e.g., 1, 2, 3)
    labs(title = "Word Length vs. Frequency by Language", x = "Frequency", y = "Length") +
    theme_minimal()
  
  return(plot)
}

# Define the selected languages
selected_languages_1 <- head(unique(combined_data$lang), 6)
selected_languages_2 <- tail(unique(combined_data$lang), 6)


# Plot the multipanel figure
multipanel_1 <- plot_multipanel(combined_data, selected_languages_1)
print(multipanel_1)
multipanel_2 <- plot_multipanel(combined_data, selected_languages_2)
print(multipanel_2)

# export the plots to a file in the 'r_results/plot' folder
ggsave("./r_results/plot/multipanel_1.png", plot = multipanel_1, width = 10, height = 10, units = "in", dpi = 300)
ggsave("./r_results/plot/multipanel_2.png", plot = multipanel_2, width = 10, height = 10, units = "in", dpi = 300)

# Export the data fram results_compression to a table in the 'r_results/table' folder
write.csv(results_compression, file = "./r_results/table/compression_results.csv")

# Export the data fram results_correlation to a table in the 'r_results/table' folder
write.csv(results_correlation, file = "./r_results/table/correlation_results.csv")

# Remove the useless elements from the global environment
rm(data, correlation, compression_data, correlation_data, lang, mean_length, mean_random_baseline, mean_min_baseline, eta, omega, total_words, data_output_file, values_output_file, file_name)

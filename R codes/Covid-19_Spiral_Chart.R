#Leitura e tratamento dos dados
pacman::p_load("tidyverse", "ggtext", "here", "lubridate", "ggplot2")
owid_url <- "https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true"
country <- "United States"
covid <- read_csv(owid_url)
covid_cases <- covid %>% 
  filter(location == country) %>% 
  filter(date <= date('2023-05-31')) %>%
  select(date, new_cases, new_cases_smoothed) %>% 
  arrange(date) %>% 
  add_row(date = as_date("2020-01-01"), new_cases = 0, new_cases_smoothed = 0,
          .before = 1) %>% 
  complete(date = seq(min(.$date), max(.$date), by = 1),
           fill = list(new_cases = 0, new_cases_smoothed = 0)) %>% 
  mutate(day_of_year = yday(date),
         year = year(date)
  )

#Criação do gráfico bruto
p <- covid_cases %>% 
  ggplot() +
  geom_segment(aes(x = day_of_year, xend = day_of_year + 1, 
                   y = as.POSIXct(date), yend = as.POSIXct(date))) +
  coord_polar()
p

#Retira estilos e valores
p + theme_void()

#Design e diagramação
size_factor <- 60
outline_color <- "#D97C86"
fill_color <- "#F0C0C1"
base_grey <- "grey28"

#Aplica dados ao gráfico espiral
p <- covid_cases %>% 
  ggplot() +
  geom_ribbon(aes(x = day_of_year, 
                  ymin = as.POSIXct(date) - new_cases_smoothed / 2 * size_factor,
                  ymax = as.POSIXct(date) + new_cases_smoothed / 2 * size_factor,
                  group = year),
              size = 0.3, col = outline_color, fill = fill_color, show.legend = FALSE) +
  geom_segment(aes(x = day_of_year, xend = day_of_year + 1, 
                   y = as.POSIXct(date), yend = as.POSIXct(date)),
               col = base_grey, size = 0.3) +
  coord_polar() +
  theme_void()
p

#Espaçamento de meses
month_length <- c(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

month_breaks <- cumsum(month_length) - 30

#Criação de eixos dos meses
p + scale_x_continuous(minor_breaks = month_breaks, 
                       breaks = month_breaks[c(1, 4, 7, 10)],
                       labels = c("Janeiro", "Abril", "Júlio", "Outubro")) +
  theme(
    plot.background = element_rect(color = NA, fill = "white"),
    panel.grid.major.x = element_line(color = "grey70", size = 0.2, linetype = "dotted"),
    panel.grid.minor.x = element_line(color = "grey70", size = 0.2, linetype = "dotted"),
    axis.text.x = element_text(color = base_grey, size = 5, hjust = 0.5),
  )

#Remove lacunas e melhora proporção do raio
p <- covid_cases %>% 
  filter(date != as_date("2020-02-29")) %>%
  group_by(year) %>%
  mutate(day_of_year = row_number()) %>%
  ungroup() %>%
  ggplot() +
  geom_ribbon(aes(x = day_of_year, 
                  ymin = as.POSIXct(date) - new_cases_smoothed / 2 * size_factor,
                  ymax = as.POSIXct(date) + new_cases_smoothed / 2 * size_factor,
                  group = year),
              color = outline_color, size = 0.3, fill = fill_color, show.legend = FALSE) +
  geom_segment(aes(x = day_of_year, xend = day_of_year + 1, 
                   y = as.POSIXct(date), yend = as.POSIXct(date)),
               col = base_grey, size = 0.3) +
  scale_x_continuous(minor_breaks = month_breaks, 
                     breaks = month_breaks[c(1, 4, 7, 10)],
                     labels = c("Janeiro", "Abril", "Júlio", "Outubro"),
                     limits = c(1, 365),
                     expand = c(0, 0)
  ) +
  scale_y_continuous(limits = c(as.POSIXct("2019-07-01"), NA),
                     expand = c(0, 0)) +
  coord_polar() +
  theme_void() +
  theme(
    plot.background = element_rect(color = NA, fill = "white"),
    panel.grid.major.x = element_line(color = "grey70", size = 0.2, linetype = "dotted"),
    panel.grid.minor.x = element_line(color = "grey70", size = 0.2, linetype = "dotted"),
    axis.text.x = element_text(color = base_grey, size = 5, hjust = 0.5)
  )
p

#Formatação de texto
text_color <- rgb(18, 18, 18, maxColorValue = 255)
base_family <- "Libre Franklin Medium"
subtitle_date <- max(covid_cases$date) %>% 
  format("%b. %d, %Y")
year_annotations <- list(
  year = 2020:2023,
  x = rep(4, 4),
  y = as.POSIXct(paste(2020:2023, "01", "01", sep = "-"))
)

#Aplicação legenda de texto
p <- covid_cases %>% 
  filter(date != as_date("2020-02-29")) %>%
  group_by(year) %>%
  mutate(day_of_year = row_number()) %>%
  ungroup() %>%
  ggplot() +
  geom_ribbon(aes(x = day_of_year, 
                  ymin = as.POSIXct(date) - new_cases_smoothed / 2 * size_factor,
                  ymax = as.POSIXct(date) + new_cases_smoothed / 2 * size_factor,
                  group = year),
              color = outline_color, size = 0.3, fill = fill_color, show.legend = FALSE) +
  geom_segment(aes(x = day_of_year, xend = day_of_year + 1, 
                   y = as.POSIXct(date), yend = as.POSIXct(date)),
               col = base_grey, size = 0.3) +

  annotate("richtext", 
           label = "Média de<br>7 dias",
           x = 30, y = as.POSIXct("2021-09-30"),
           family = base_family, size = 2, color = text_color,
           label.colour = NA, fill = NA) +
  annotate("segment",
           x = 20, xend = 22.5, 
           y = as.POSIXct("2021-06-01"), yend = as.POSIXct("2021-03-15"),
           color = text_color, size = 0.3) +

  annotate("text", label = paste0(year_annotations$year, "\u2192"), x = year_annotations$x, 
           y = year_annotations$y, 
           family = "Arial",
           size = 1.5, vjust = -0.6, hjust = 0.15) +   
  
  scale_x_continuous(minor_breaks = month_breaks, 
                     breaks = month_breaks[c(1, 4, 7, 10)],
                     labels = c("Janeiro.", "Abril", "Júlio", "Outubro"),
                     limits = c(1, 365),
                     expand = c(0, 0)
  ) +
  scale_y_continuous(limits = c(as.POSIXct("2019-07-01"), NA),
                     expand = c(0, 0)) +
  coord_polar() +
  labs(
    subtitle = subtitle_date
  ) +
  theme_void(base_family = base_family) +
  theme(
    plot.background = element_rect(color = NA, fill = "white"),
    panel.grid.major.x = element_line(color = "grey70", size = 0.2, linetype = "dotted"),
    panel.grid.minor.x = element_line(color = "grey70", size = 0.2, linetype = "dotted"),
    axis.text.x = element_text(color = base_grey, size = 5, hjust = 0.5),
    text = element_text(color = text_color),
    plot.subtitle = element_text(hjust = 0.5, size = 5)
  )
p


#Aplicação de legenda gráfica
library(patchwork)

p_legend <- 
  tibble(
    cases = c(0, 150000),
    ymin = c(0, -75000),
    ymax = c(0, 75000),
  ) %>% 
  ggplot(aes(cases)) +
  geom_ribbon(aes(ymin = size_factor * ymin, ymax = size_factor * ymax),
              color = outline_color, fill = fill_color, size = 0.3) +
  geom_line(aes(y = 1), color = base_grey) +
  geom_text(aes(label = ifelse(cases == 0, 0, "150k cases"), 
                y = 1, hjust = ifelse(cases == 0, 1.5, -0.1)),
            size = 2) +
  coord_cartesian(xlim = c(0, 350000), 
                  ylim = c(-as.numeric(as.POSIXct("1971-01-01")), NA), 
                  clip = "off") + 
  labs(title = "New Covid-19 cases,<br>United States") +
  theme_void() +
  theme(plot.title = element_markdown(color = text_color, 
                                      family = "Helvetica",
                                      face = "bold", size = 8, hjust = 0.5,
                                      lineheight = 1.1))

ragg::agg_png(here("plots", "nyt_spiral_with-legend.png"),
              res = 300, width = 1200, height = 1200 * 746/615)
p + inset_element(p_legend, left = 0.05, bottom = 0.725, right = 0.25, top = 0.95)

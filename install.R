# Install every package the five practicals use. Run once.
pkgs <- c("rmarkdown", "knitr",
          "sf", "terra", "ggplot2", "dplyr", "units",
          "rnaturalearth", "rnaturalearthdata",
          "spdep", "gstat", "tmap",          # tmap >= 4.0
          "spatstat", "spocc", "geodata")
install.packages(setdiff(pkgs, rownames(installed.packages())))

# ne_states() in Practical 1 needs this data package, which is not on CRAN
if (!requireNamespace("rnaturalearthhires", quietly = TRUE))
  install.packages("rnaturalearthhires", repos = "https://ropensci.r-universe.dev")

stopifnot(packageVersion("tmap") >= "4.0")

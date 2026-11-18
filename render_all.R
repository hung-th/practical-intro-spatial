# Render all five practicals to GitHub Markdown (practicalN_*.md + figures).
# Run from this folder: Rscript render_all.R
files <- sprintf("practical%d_%s.Rmd", 1:5,
                 c("my_first_map", "spatial_autocorrelation",
                   "spatial_interpolation", "species_distribution", "mini_project"))
for (f in files) {
  t0 <- Sys.time()
  rmarkdown::render(f, envir = new.env(), quiet = TRUE)
  message(sprintf("%-40s %5.0f s", f, as.numeric(Sys.time() - t0, units = "secs")))
}

# Introduction to Spatial Models: practicals

R practicals for *Introduction to Spatial Models* (DTC: Statistics, Data
Science and AI). All five run in one 2-hour session for first-year PhD
students, after a 1-hour lecture.

Each practical is an R Markdown file (`.Rmd`) with a rendered GitHub Markdown
copy (`.md`) next to it. On GitHub, open the `.md` files to see the code,
output and figures without running anything.

| # | Practical | Time | Rendered | Data |
|---|---|---|---|---|
| 1 | My first map: `sf` and `terra` | 25 min | [practical1_my_first_map.md](practical1_my_first_map.md) | `data/ww/`, `data/oaks.csv`, `data/tavg.tif` |
| 2 | Spatial autocorrelation: Moran's I | 25 min | [practical2_spatial_autocorrelation.md](practical2_spatial_autocorrelation.md) | `data/snow/` |
| 3 | Spatial interpolation and cross-validation | 30 min | [practical3_spatial_interpolation.md](practical3_spatial_interpolation.md) | `data/hp.csv`, `data/LAD_DEC_24_UK_BGC/` |
| 4 | Species distribution modelling with point processes | 25 min | [practical4_species_distribution.md](practical4_species_distribution.md) | GBIF, downloaded live |
| 5 | Mini-project: environmental covariates | 15 min, then open-ended | [practical5_mini_project.md](practical5_mini_project.md) | GBIF, WorldClim and elevation, downloaded live |

Each practical is split into stations with timings (⏱️), plus
**EXPECT TO SEE** and **MILESTONE!** notes so that students can check their
progress. Sections marked **+ optional** can be skipped.

## Running it yourself

1. Clone or download this repository and open the folder in RStudio (or set
   it as your working directory). All paths are relative to it.
2. Install the packages once:
   ```r
   source("install.R")
   ```
3. Render everything from start to finish:
   ```r
   source("render_all.R")
   ```
   Or open any `.Rmd` and click **Knit**, or run its chunks one by one.

It was last rendered with R 4.5.2, sf 1.1-0, terra 1.9-34, spdep 1.4-2,
gstat 2.1-5, tmap 4.2, spatstat 3.6-3, spocc 1.2.4 and geodata 0.6-9. tmap
**4.0 or later** is required, because the maps use the version 4 syntax.

Practicals 4 and 5 need an internet connection. Practical 5 saves the
WorldClim and elevation layers it downloads in `data/climate/` and
`data/elevation/`; these are not in the repository.

## Notes for demonstrators

- **GBIF records change.** Practicals 4 and 5 download *Dalbergia oliveri*
  records live, so counts and AIC values drift as GBIF is updated. In the
  rendered copy, 183 records were downloaded and 102 kept after cleaning.
- **Windows Smart App Control.** On Windows 11 it can block an R package's
  DLL, with the message *"An Application Control policy has blocked this
  file"*. Re-running usually works. If it does not, reinstall the package
  that is named in the error.
- **Practical 2: the choice of W matters.** The housing blocks are separated
  by streets, so `poly2nb()` finds no neighbours until boundaries within 10 m
  count as touching (`snap = 10`). With that W, global Moran's I for deaths
  is about −0.05 (p ≈ 0.56). The comparison table shows how much the
  conclusion depends on the definition of a neighbour, which is worth
  discussing with students.
- **Practical 4: AIC.** The linear trend `~ x + y` barely beats the
  homogeneous model (AIC 2214.5 against 2214.7). The quadratic trend
  (2137.1) and the covariate models in Practical 5 (2086.4 for the best one)
  make the comparison clearer.
- **Units.** Point-process intensities are per km² (the pattern is rescaled
  from metres). In Practical 5, precipitation is in metres and elevation in
  km, so that the squared terms stay well scaled.

## Data sources

- `data/ww/`, `data/oaks.csv`: Wytham Woods stand polygons and oak tree
  locations.
- `data/tavg.tif`: WorldClim 2.1 monthly mean temperature, 30 arc-seconds,
  UK extent ([worldclim.org](https://www.worldclim.org/)).
- `data/snow/`: deaths in the 1854 Soho cholera outbreak by housing block,
  after John Snow (1855). British National Grid.
- `data/hp.csv`: 1,234 Oxfordshire sales from the HM Land Registry
  [Price Paid Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads),
  downloaded September 2025. Contains HM Land Registry data © Crown copyright
  and database right 2025, licensed under the Open Government Licence v3.0.
- `data/LAD_DEC_24_UK_BGC/`: ONS Local Authority District boundaries,
  December 2024. Source: Office for National Statistics, licensed under the
  Open Government Licence v3.0. Contains OS data © Crown copyright and
  database right 2024.
- Downloaded live: occurrence records from [GBIF](https://www.gbif.org/)
  via `spocc`; WorldClim 2.1 bioclimatic variables and elevation via
  `geodata`; country boundaries from Natural Earth via `rnaturalearth`.

## Author

Tin Hang (Henry) Hung

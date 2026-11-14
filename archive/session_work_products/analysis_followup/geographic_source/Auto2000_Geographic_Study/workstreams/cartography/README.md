# Cartographic and interactive outputs

Run from the study root after routing output exists:

```bash
python workstreams/cartography/build_figures.py
python workstreams/cartography/build_interactive.py
```

Required Python packages: pandas, numpy, matplotlib, geopandas (the latter is used by other contextual map scripts). All map point coordinates are WGS84 longitude/latitude. Static local maps use a longitude/latitude graticule with aspect adjustment at the study latitude, an approximate straight-line scale bar and a north marker. They are not topographic or full-road-network maps.

The self-contained SVG explorer has no tile, CDN, font or JavaScript library dependency. It is usable without internet. Origins and candidate records are embedded in the HTML. Drag the empty/graticule part of the map to pan and scroll to zoom. Provider and origin click records expose evidence notes. Reset restores the original view. The origin-study rectangle is not an administrative boundary.

Mapped repair/service candidates do not establish independent ownership or equivalent Toyota/model/job capability. General-workshop branch documentation does not verify the selected paid job at a current appointment. OtoXpert network offers do not establish model/part eligibility at each outlet. These limitations apply to every figure.

Travel time is the OSRM driving model duration, not traffic observations or the route weight/cost. Static origin maps show discrete grid locations rather than an interpolated isochrone surface. All grid shares refer to the computational sample, not population, car owners or customers. Modelled route examples are selected for analytical contrast, not representative customer journeys.

Figures are registered in figure_registry.json with source and interpretation captions. The PDF builder can reuse them. Source tables and numeric results remain authoritative if a figure display uses a bounded colour or axis scale. Origin snapping and destination-margin effects are plotted explicitly.

import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import type { GeoJsonObject } from "geojson";
import rawAtlas from "./data/atlas-v1.json";
import { type Market, type Outlet, type Origin } from "./geography";
import { useKey } from "./ui";
type Layers = {
  dealer: boolean;
  owned: boolean;
  comparison: boolean;
  origins: boolean;
};
const atlas = rawAtlas as unknown as Record<Market, GeoJsonObject>;
export default function ServiceMap({
  market,
  origins,
  outlets,
  layers,
  network,
  selected,
  outletId,
  offline,
  onOrigin,
  onOutlet,
}: {
  market: Market;
  origins: Origin[];
  outlets: Outlet[];
  layers: Layers;
  network: boolean;
  selected: string;
  outletId: string;
  offline: boolean;
  onOrigin: (origin: Origin) => void;
  onOutlet: (outlet: Outlet) => void;
}) {
  const { t, lang } = useKey();
  const element = useRef<HTMLDivElement>(null);
  const instance = useRef<L.Map | null>(null);
  const callbacks = useRef({ onOrigin, onOutlet });
  callbacks.current = { onOrigin, onOutlet };
  const [tileState, setTileState] = useState<"loading" | "online" | "offline">(
    "loading",
  );
  useEffect(() => {
    if (!element.current) return;
    const map = L.map(element.current, {
      scrollWheelZoom: false,
      attributionControl: false,
      zoomControl: false,
      zoomAnimation: false,
      fadeAnimation: false,
      markerZoomAnimation: false,
      minZoom: 9,
      maxZoom: 17,
    });
    instance.current = map;
    const pane = map.createPane("keyAtlas");
    pane.style.zIndex = "190";
    L.control.scale({ imperial: false, position: "bottomleft" }).addTo(map);
    L.geoJSON(atlas[market], {
      pane: "keyAtlas",
      interactive: false,
      style: (feature) => {
        const category = feature?.properties.category;
        if (category === "land")
          return { stroke: false, fillColor: "#f3f0e6", fillOpacity: 1 };
        if (category === "urban")
          return {
            color: "#bcb6a5",
            weight: 1,
            fillColor: "#ded9c9",
            fillOpacity: 0.84,
          };
        if (category === "water")
          return { color: "#73a7b7", weight: 2, fill: false };
        return { color: "#a19c86", dashArray: "5 6", weight: 1, fill: false };
      },
    }).addTo(map);
    map.fitBounds(L.latLngBounds(origins.map((o) => o.position)), {
      padding: [34, 35],
    });
    const observer =
      typeof ResizeObserver !== "undefined"
        ? new ResizeObserver(() => {
            if (instance.current === map)
              map.invalidateSize({ animate: false, pan: false });
          })
        : undefined;
    observer?.observe(element.current);
    return () => {
      observer?.disconnect();
      instance.current = null;
      map.stop();
      map.remove();
    };
  }, [market, origins]);
  useEffect(() => {
    const map = instance.current;
    if (!map) return;
    if (offline) {
      setTileState("offline");
      return;
    }
    setTileState("loading");
    let loaded = false;
    let active = true;
    const tiles = L.tileLayer(
      "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
      { maxNativeZoom: 19, updateWhenIdle: true, keepBuffer: 1 },
    );
    const unavailable = () => {
      if (loaded || !active || instance.current !== map) return;
      setTileState("offline");
      // Leaflet still reads its map while reporting the final failed tile.
      queueMicrotask(() => {
        if (active && !loaded && instance.current === map) tiles.remove();
      });
    };
    const timer = window.setTimeout(unavailable, 2600);
    tiles.on("tileload", () => {
      loaded = true;
      window.clearTimeout(timer);
      setTileState("online");
    });
    tiles.on("load", unavailable);
    tiles.addTo(map);
    return () => {
      active = false;
      window.clearTimeout(timer);
      tiles.off();
      tiles.remove();
    };
  }, [market, offline]);
  useEffect(() => {
    const map = instance.current;
    if (!map) return;
    const drawn = L.layerGroup().addTo(map);
    const color = {
      dealer: "#15232e",
      owned: "#a4570a",
      comparison: "#7d559b",
    };
    if (layers.origins)
      origins.forEach((origin) => {
        const gap = (network ? origin.after : origin.before) > 5;
        L.circleMarker(origin.position, {
          radius: origin.id === selected ? 8 : gap ? 5 : 4,
          fillColor: gap ? "#cc092f" : "#128579",
          fillOpacity: 0.95,
          color: origin.id === selected ? "#17222b" : "#fff",
          weight: origin.id === selected ? 2 : 1.3,
        })
          .bindTooltip(origin.id)
          .on("click", () => callbacks.current.onOrigin(origin))
          .addTo(drawn);
      });
    outlets.forEach((outlet) => {
      const kind =
        layers[outlet.kind] && (outlet.kind !== "owned" || network)
          ? outlet.kind
          : outlet.oilComparator && layers.comparison
            ? "comparison"
            : undefined;
      if (!kind) return;
      L.circleMarker(outlet.position, {
        radius: outlet.id === outletId ? 10 : 6,
        fillColor: color[kind],
        color: "#fff",
        weight: outlet.id === outletId ? 3 : 1.5,
        fillOpacity: 1,
      })
        .bindTooltip(outlet.name)
        .on("click", () => callbacks.current.onOutlet(outlet))
        .addTo(drawn);
    });
    if (selected && layers.origins)
      drawn.eachLayer((layer) => {
        if (
          layer instanceof L.CircleMarker &&
          layer.getTooltip()?.getContent() === selected
        )
          layer.bringToFront();
      });
    return () => {
      drawn.remove();
    };
  }, [market, origins, outlets, layers, network, selected, outletId, lang]);
  const zoom = (direction: number) => {
    const map = instance.current;
    if (map) map.setZoom(map.getZoom() + direction, { animate: false });
  };
  return (
    <div className="key-map-frame">
      <div
        className="key-map"
        ref={element}
        role="region"
        aria-label={t(
          "Pan and zoom workshop access map",
          "Peta akses bengkel, dapat digeser dan diperbesar",
        )}
      />
      <div className="key-map-tools">
        <button
          type="button"
          onClick={() => zoom(1)}
          aria-label={t("Zoom in", "Perbesar")}
        >
          +
        </button>
        <button
          type="button"
          onClick={() => zoom(-1)}
          aria-label={t("Zoom out", "Perkecil")}
        >
          −
        </button>
      </div>
      <span
        className="key-map-mode"
        data-map-source={tileState}
        aria-live="polite"
      >
        {tileState === "online"
          ? t("Street map", "Peta jalan")
          : t("Local atlas", "Atlas lokal")}
      </span>
      <span className="key-attribution">
        <a
          href="https://www.naturalearthdata.com/about/terms-of-use/"
          target="_blank"
          rel="noreferrer"
        >
          Natural Earth
        </a>{" "}
        ·{" "}
        <a
          href="https://www.openstreetmap.org/copyright"
          target="_blank"
          rel="noreferrer"
        >
          © OpenStreetMap
        </a>
      </span>
    </div>
  );
}

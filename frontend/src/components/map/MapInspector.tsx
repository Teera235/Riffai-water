"use client";

import TambonDetailPanel from "@/components/map/TambonDetailPanel";

export default function MapInspector(props: {
  tambon: any | null;
  onClose: () => void;
}) {
  // Future: unify other feature inspections (stations, ONWR subbasins, tiles).
  return <TambonDetailPanel tambon={props.tambon} onClose={props.onClose} />;
}


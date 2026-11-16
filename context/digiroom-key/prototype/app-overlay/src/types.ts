export type Language = "en" | "id";
export type CarId = "zenix" | "bz4x";
export type Mode = "showroom" | "garage" | "family" | "energy";
export type Quality = "lite" | "standard" | "high";
export interface Scenario {
  car: CarId;
  mode: Mode;
  paint: string;
  garageWidth: number;
  garageDepth: number;
  offset: number;
  doorOpen: boolean;
  tailgateOpen: boolean;
  obstacle: boolean;
  passengers: number;
  luggage: number;
  folded: boolean;
  stroller: boolean;
  childSeat: boolean;
  kmWeek: number;
  fuelPrice: number;
  electricityPrice: number;
  homeCharging: boolean;
  publicChargeShare: number;
  publicChargePrice: number;
  publicCharger: string;
  backupTrip: string;
  energyStep: number;
}
export interface SceneProps {
  scenario: Scenario;
  quality: Quality;
  reducedMotion: boolean;
  resetKey: number;
  onSelectCar: (car: CarId) => void;
  onError: () => void;
  language?: Language;
  onStats?: (stats: {
    fps: number;
    drawCalls: number;
    triangles: number;
  }) => void;
}
export const DEFAULT_SCENARIO: Scenario = {
  car: "zenix",
  mode: "showroom",
  paint: "#b1b7b8",
  garageWidth: 3.1,
  garageDepth: 5.6,
  offset: 0,
  doorOpen: false,
  tailgateOpen: false,
  obstacle: false,
  passengers: 5,
  luggage: 2,
  folded: false,
  stroller: false,
  childSeat: false,
  kmWeek: 250,
  fuelPrice: 15950,
  electricityPrice: 1700,
  homeCharging: true,
  publicChargeShare: 0,
  publicChargePrice: 2500,
  publicCharger: "",
  backupTrip: "",
  energyStep: 0,
};

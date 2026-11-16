import {
  DEFAULT_SCENARIO,
  type CarId,
  type Language,
  type Mode,
  type Scenario,
} from "./types";

export interface Car {
  name: string;
  shortName: string;
  powertrain: "HEV" | "BEV";
  length: number;
  width: number;
  height: number;
  seats: number;
  modelYear: string;
  description: string;
  modelPath: string;
}

/** Source dimensions are separate from the authored geometry and scenarios. */
export const CARS: Record<CarId, Car> = {
  zenix: {
    name: "Kijang Innova Zenix",
    shortName: "Innova Zenix",
    powertrain: "HEV",
    length: 4.755,
    width: 1.85,
    height: 1.795,
    seats: 7,
    modelYear: "Hybrid EV",
    description: "Seven-position hybrid MPV reference.",
    modelPath: "/models/zenix.glb",
  },
  bz4x: {
    name: "Toyota bZ4X",
    shortName: "bZ4X",
    powertrain: "BEV",
    length: 4.69,
    width: 1.86,
    height: 1.65,
    seats: 5,
    modelYear: "Battery EV",
    description: "Five-seat battery-electric SUV reference.",
    modelPath: "/models/bz4x.glb",
  },
};

export const SCENARIO_ASSUMPTIONS = Object.freeze({
  doorExcursionM: 0.65,
  tailgateExcursionM: 0.7,
  motorcycleWidthM: 0.55,
  hybridLitresPer100Km: 5.5,
  referenceLitresPer100Km: 8,
  bevKwhPer100Km: 12.13,
  chargingOverhead: 0.1,
  usableBatteryKwh: 64,
  fuelTankLitres: 52,
  weeksPerMonth: 52 / 12,
});

function bounded(
  value: unknown,
  fallback: number,
  min: number,
  max: number,
  integer = false,
): number {
  if (typeof value !== "number" || !Number.isFinite(value)) return fallback;
  const n = Math.min(max, Math.max(min, value));
  return integer ? Math.round(n) : n;
}

/** Only known own fields survive persisted/imported inputs. Nothing is spread from untrusted data. */
export function validateScenario(input: unknown): Scenario {
  const p =
    input && typeof input === "object" && !Array.isArray(input)
      ? (input as Record<string, unknown>)
      : {};
  const bool = (key: keyof Scenario): boolean =>
    typeof p[key] === "boolean"
      ? (p[key] as boolean)
      : (DEFAULT_SCENARIO[key] as boolean);
  return {
    car: p.car === "bz4x" || p.car === "zenix" ? p.car : DEFAULT_SCENARIO.car,
    mode:
      p.mode === "showroom" ||
      p.mode === "garage" ||
      p.mode === "family" ||
      p.mode === "energy"
        ? p.mode
        : DEFAULT_SCENARIO.mode,
    paint:
      typeof p.paint === "string" && /^#[0-9a-f]{6}$/i.test(p.paint)
        ? p.paint
        : DEFAULT_SCENARIO.paint,
    garageWidth: bounded(p.garageWidth, DEFAULT_SCENARIO.garageWidth, 2.2, 5),
    garageDepth: bounded(p.garageDepth, DEFAULT_SCENARIO.garageDepth, 4, 8),
    offset: bounded(p.offset, DEFAULT_SCENARIO.offset, -0.5, 0.5),
    doorOpen: bool("doorOpen"),
    tailgateOpen: bool("tailgateOpen"),
    obstacle: bool("obstacle"),
    passengers: bounded(
      p.passengers,
      DEFAULT_SCENARIO.passengers,
      p.childSeat === true ? 2 : 1,
      7,
      true,
    ),
    luggage: bounded(p.luggage, DEFAULT_SCENARIO.luggage, 0, 6, true),
    folded: bool("folded"),
    stroller: bool("stroller"),
    childSeat: bool("childSeat"),
    kmWeek: bounded(p.kmWeek, DEFAULT_SCENARIO.kmWeek, 50, 1000),
    fuelPrice: bounded(p.fuelPrice, DEFAULT_SCENARIO.fuelPrice, 9000, 20000),
    electricityPrice: bounded(
      p.electricityPrice,
      DEFAULT_SCENARIO.electricityPrice,
      1000,
      4000,
    ),
    homeCharging: bool("homeCharging"),
    publicChargeShare: bounded(p.publicChargeShare, 0, 0, 100, true),
    publicChargePrice: bounded(p.publicChargePrice, 2500, 1000, 10000),
    publicCharger:
      typeof p.publicCharger === "string"
        ? p.publicCharger.replace(/[\r\n\u0000-\u001f]/g, " ").slice(0, 140)
        : "",
    backupTrip:
      typeof p.backupTrip === "string"
        ? p.backupTrip.replace(/[\r\n\u0000-\u001f]/g, " ").slice(0, 140)
        : "",
    energyStep: bounded(p.energyStep, DEFAULT_SCENARIO.energyStep, 0, 2, true),
  };
}

export interface GarageResult {
  sideClearance: number;
  rearClearance: number;
  doorClearance: number;
  fits: boolean;
  doorFits: boolean;
  tailgateFits: boolean;
  obstacleConflict: boolean;
}

export function garageResult(input: Scenario): GarageResult {
  const s = validateScenario(input);
  const car = CARS[s.car];
  // Front is +Z. The authored driver door and motorcycle are on -X.
  // A positive +X offset increases space on that side of the parked car.
  const leftGap = (s.garageWidth - car.width) / 2 + s.offset;
  const rightGap = (s.garageWidth - car.width) / 2 - s.offset;
  const availableDriverSpace =
    leftGap - (s.obstacle ? SCENARIO_ASSUMPTIONS.motorcycleWidthM : 0);
  const rearClearance = (s.garageDepth - car.length) / 2;
  const epsilon = 1e-9; // Prevent binary rounding from flipping an exactly touching envelope.
  const obstacleConflict =
    s.obstacle && leftGap + epsilon < SCENARIO_ASSUMPTIONS.motorcycleWidthM;
  const fits =
    leftGap >= -epsilon &&
    rightGap >= -epsilon &&
    rearClearance >= -epsilon &&
    !obstacleConflict;
  return {
    sideClearance: Math.min(leftGap, rightGap),
    rearClearance,
    doorClearance: availableDriverSpace - SCENARIO_ASSUMPTIONS.doorExcursionM,
    fits,
    doorFits:
      fits &&
      availableDriverSpace + epsilon >= SCENARIO_ASSUMPTIONS.doorExcursionM,
    tailgateFits:
      fits &&
      rearClearance + epsilon >= SCENARIO_ASSUMPTIONS.tailgateExcursionM,
    obstacleConflict,
  };
}

export interface FamilyResult {
  seatsAvailable: number;
  passengerFits: boolean;
  luggageFits: boolean;
  luggageCapacity: number;
}

export function familyResult(input: Scenario): FamilyResult {
  const s = validateScenario(input);
  const seatsAvailable = CARS[s.car].seats - (s.folded ? 2 : 0);
  // Counts are deliberately authored packing tasks, not measured boot volume.
  const luggageCapacity = s.folded ? 6 : 3;
  return {
    seatsAvailable,
    passengerFits: s.passengers <= seatsAvailable,
    luggageFits: s.luggage + (s.stroller ? 2 : 0) <= luggageCapacity,
    luggageCapacity,
  };
}

export interface EnergyResult {
  fuelLitres: number;
  energyKwh: number;
  publicShare: number;
  averageChargePrice: number;
  weeklyCost: number;
  monthlyCost: number;
  referenceWeeklyCost: number;
  savingWeekly: number;
  estimatedRangeKm: number;
}

export function energyResult(input: Scenario): EnergyResult {
  const s = validateScenario(input);
  const a = SCENARIO_ASSUMPTIONS;
  const fuelLitres =
    s.car === "zenix" ? (s.kmWeek * a.hybridLitresPer100Km) / 100 : 0;
  const energyKwh =
    s.car === "bz4x"
      ? ((s.kmWeek * a.bevKwhPer100Km) / 100) * (1 + a.chargingOverhead)
      : 0;
  const publicShare = s.publicChargeShare / 100;
  const averageChargePrice =
    (1 - publicShare) * s.electricityPrice + publicShare * s.publicChargePrice;
  const weeklyCost = fuelLitres * s.fuelPrice + energyKwh * averageChargePrice;
  const referenceWeeklyCost =
    ((s.kmWeek * a.referenceLitresPer100Km) / 100) * s.fuelPrice;
  return {
    fuelLitres,
    energyKwh,
    publicShare,
    averageChargePrice,
    weeklyCost,
    monthlyCost: weeklyCost * a.weeksPerMonth,
    referenceWeeklyCost,
    savingWeekly: referenceWeeklyCost - weeklyCost,
    estimatedRangeKm:
      s.car === "bz4x"
        ? (a.usableBatteryKwh / a.bevKwhPer100Km) * 100
        : (a.fuelTankLitres / a.hybridLitresPer100Km) * 100,
  };
}

/** Supported concern routing, not a remote model or open-ended engineering answer. */
export function suggestMode(text: string): Mode {
  const t = text.toLocaleLowerCase("en");
  if (
    /garage|garasi|parking|parkir|gate|gerbang|fit|muat|sempit|clearance|tailgate|pintu/.test(
      t,
    )
  )
    return "garage";
  if (
    /family|keluarga|parent|orang tua|luggage|koper|stroller|seat|kursi|child|anak|berenam|penumpang|people|bags?|six|enam/.test(
      t,
    )
  )
    return "family";
  if (
    /charging|charge|charger|cas|listrik|hybrid|hibrida|fuel|bensin|commut|traffic|macet|cost|biaya|hemat|week|minggu/.test(
      t,
    )
  )
    return "energy";
  return "showroom";
}

export function createBriefText(
  input: Scenario,
  language: Language,
  concerns: string[] = [],
): string {
  const s = validateScenario(input);
  const car = CARS[s.car];
  const g = garageResult(s);
  const f = familyResult(s);
  const e = energyResult(s);
  const id = language === "id";
  const money = new Intl.NumberFormat(id ? "id-ID" : "en-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  });
  const yes = (v: boolean) => (v ? (id ? "Ya" : "Yes") : id ? "Tidak" : "No");
  const safeConcerns = concerns
    .filter((c): c is string => typeof c === "string")
    .map((c) => c.replace(/[\r\n\u0000-\u001f]+/g, " ").slice(0, 400))
    .slice(0, 20);
  return [
    id
      ? "DIGIROOM LIFE TEST: RENCANA KUNJUNGAN"
      : "DIGIROOM LIFE TEST: VISIT BRIEF",
    "",
    `${id ? "Kendaraan" : "Vehicle"}: ${car.name} ${car.powertrain}`,
    `${id ? "Warna tampilan" : "Display colour"}: ${s.paint}`,
    "",
    id ? "YANG INGIN SAYA COBA" : "WHAT I WANT TO TRY",
    ...(safeConcerns.length
      ? safeConcerns.map((c) => `• ${c}`)
      : [
          id
            ? "• Jelaskan kendaraan dan pilihan demonstrasinya."
            : "• Explain the vehicle and available demonstrations.",
        ]),
    "",
    id ? "PARKIR DAN AKSES" : "PARKING AND ACCESS",
    `${id ? "Garasi" : "Garage"}: ${s.garageWidth.toFixed(2)} × ${s.garageDepth.toFixed(2)} m`,
    `${id ? "Posisi samping" : "Lateral offset"}: ${s.offset.toFixed(2)} m`,
    `${id ? "Sepeda motor di samping" : "Motorcycle at side"}: ${yes(s.obstacle)}`,
    `${id ? "Sisa ruang pintu dalam ilustrasi" : "Door envelope remainder in illustration"}: ${g.doorClearance.toFixed(2)} m`,
    `${id ? "Sisa ruang belakang" : "Rear clearance"}: ${g.rearClearance.toFixed(2)} m`,
    "",
    id ? "PENUMPANG DAN BARANG" : "PASSENGERS AND LUGGAGE",
    `${id ? "Penumpang" : "Passengers"}: ${s.passengers}; ${id ? "posisi duduk" : "seating positions"}: ${f.seatsAvailable}`,
    `${id ? "Barang pilihan" : "Selected luggage items"}: ${s.luggage}; ${id ? "kursi dilipat" : "seats folded"}: ${yes(s.folded)}`,
    `${id ? "Kereta bayi" : "Stroller"}: ${yes(s.stroller)}; ${id ? "kursi anak" : "child seat"}: ${yes(s.childSeat)}`,
    "",
    id ? "ASUMSI PERJALANAN" : "DRIVING ASSUMPTIONS",
    s.car === "bz4x"
      ? id
        ? "BEV: 12,13 kWh/100 km ditambah 10% rugi pengisian (asumsi)."
        : "BEV: 12.13 kWh/100 km plus 10% charging overhead (planning assumption)."
      : id
        ? "HEV: bensin 5,5 L/100 km (asumsi)."
        : "HEV: 5.5 L/100 km petrol (planning assumption).",
    `${id ? "Jarak mingguan" : "Weekly distance"}: ${s.kmWeek} km`,
    ...(car.powertrain === "HEV"
      ? [
          `${id ? "Pertamax RON92 per liter" : "Pertamax RON92 per litre"}: ${money.format(s.fuelPrice)}`,
        ]
      : []),
    ...(car.powertrain === "BEV"
      ? [
          `${id ? "Listrik per kWh" : "Electricity per kWh"}: ${money.format(e.averageChargePrice)} (${e.publicShare * 100}% ${id ? "pengisian publik" : "public charging"})`,
          ...(s.publicCharger
            ? [
                `${id ? "Lokasi pengisian publik" : "Public charger"}: ${s.publicCharger}`,
              ]
            : []),
          ...(s.backupTrip
            ? [
                `${id ? "Rencana perjalanan alternatif" : "Alternate trip plan"}: ${s.backupTrip}`,
              ]
            : []),
        ]
      : []),
    `${id ? "Estimasi biaya energi per minggu" : "Estimated weekly energy cost"}: ${money.format(e.weeklyCost)}`,
    "",
    id ? "UNTUK DIPASTIKAN DI CABANG" : "TO CHECK AT THE BRANCH",
    id
      ? "Ukuran dan akses nyata, konfigurasi kursi, kenyamanan penumpang, kecocokan kursi anak, serta varian dan unit demonstrasi."
      : "Actual clearances and access, seat configuration, passenger comfort, child-seat compatibility, and the exact variant and demonstrator.",
    "",
    id
      ? "Rencana tersimpan saja. Belum ada permintaan janji temu yang dikirim."
      : "Saved brief only. No appointment request has been sent.",
    id
      ? "Geometri bukaan, barang, konsumsi dan biaya merupakan asumsi perencanaan. Ini bukan pemeriksaan kecocokan, penawaran harga, atau hasil pengujian kendaraan."
      : "Opening geometry, luggage, consumption and costs are planning assumptions. This is not a fit certification, price offer or vehicle test result.",
  ].join("\n");
}

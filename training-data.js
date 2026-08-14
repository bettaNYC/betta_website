/* ============================================================
   TRAINING LOG  —  Elisabetta Rappo
   ------------------------------------------------------------
   Add a session by adding ONE line to the array below.
   Newest or oldest order doesn't matter — the page sorts by date.

   Fields:
     date        "YYYY-MM-DD"
     sport       "Run" or "Bike"
     distance_km number   (kilometres)
     time        "MM:SS" or "H:MM:SS"  (moving time)

   Pace (Run, min/km) and speed (Bike, km/h) are computed for you.
   Strava paywalled its API in 2026, so this is entered by hand.
   ============================================================ */

window.TRAINING_DATA = [
  // ── Runs (from my Strava export) ──
  { date: "2026-06-23", sport: "Run",  distance_km: 9.41,  time: "52:00" },
  { date: "2026-08-01", sport: "Run",  distance_km: 17.01, time: "1:26:00" },
  { date: "2026-08-02", sport: "Run",  distance_km: 5.00,  time: "25:32" },

  // ── Bike ── (EXAMPLE rides — replace these four with your real ones) ──
  { date: "2026-06-28", sport: "Bike", distance_km: 32.0,  time: "1:12:00" },
  { date: "2026-07-12", sport: "Bike", distance_km: 45.5,  time: "1:38:00" },
  { date: "2026-07-26", sport: "Bike", distance_km: 28.2,  time: "1:02:00" },
  { date: "2026-08-09", sport: "Bike", distance_km: 52.4,  time: "1:52:00" },
];

// === Skrypt: B2K.ks ===
// Start z GZU i separacja glowicy w apogeum

// --- POBRANIE CZASU OTWARCIA GZU ---
// PRINT "Wprowadz moment otwarcia GZU [s]:".
SET gzu_time TO 1.
PRINT "Otworzenie GZU po: " + gzu_time + " [s] od separacji boosterow".

// --- ODLICZANIE STARTOWE ---
SET countdown TO 10.
UNTIL countdown < 0 {
    PRINT "T-" + countdown.
    WAIT 1.
    SET countdown TO countdown - 1.
}.

// --- START ---
STAGE.
PRINT "Start!".

// --- CZEKAJ AZ PALIWO STALE SIE SKONCZY ---
WAIT UNTIL SHIP:SOLID < 0.1.
PRINT "Separacja boosterow".
STAGE.

// --- CZEKAJ PODANĄ ILOŚĆ SEKUND, OTWORZ GZU ---
WAIT gzu_time.
PRINT "Glowny silnik".
LOCK THROTTLE TO 1.
STAGE.

// --- CZEKAJ DO APOGEUM I SEPARUJ GLOWICE ---
WAIT UNTIL SHIP:ALTITUDE >= SHIP:ORBIT:APOAPSIS - 50. // lekka tolerancja
PRINT "Apogeum osiagniete – separacja glowicy".
STAGE.

PRINT "Sekwencja zakończona.".

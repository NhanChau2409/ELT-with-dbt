select
    f.value:number::string as flightnumber,
    to_date(f.value:movement.revisedtime.utc)::string as flightdate,

    f.value:callsign::string as callsign,
    f.value:codesharestatus::string as codesharestatus,
    f.value:iscargo::boolean as iscargo,
    -- f.value:status::STRING AS flightStatus,
    f.value:aircraft.modes::string as aircraft_modes,
    f.value:aircraft.model::string as aircraft_model,
    f.value:aircraft.reg::string as aircraft_reg,

    f.value:airline.iata::string as airline_iata,
    f.value:airline.icao::string as airline_icao,
    f.value:airline.name::string as airline_name,

    f.value:movement.airport.iata::string as from_airport_iata,
    f.value:movement.airport.icao::string as from_airport_icao,
    f.value:movement.airport.name::string as from_airport_name,
    f.value:movement.airport.timezone::string as from_airport_tz,

    f.value:movement.baggagebelt::string as baggagebelt,
    f.value:movement.gate::string as gate,
    -- f.value:movement.quality::ARRAY AS quality,
    f.value:movement.terminal::string as terminal,

    -- f.value:movement.revisedTime.local::TIMESTAMP AS revisedTime_local,
    f.value:movement.revisedtime.utc::string as revisedtime_utc,

    -- f.value:movement.scheduledTime.local::TIMESTAMP AS scheduledTime_local,
    f.value:movement.scheduledtime.utc::string as scheduledtime_utc
from
    {{ source("S3", "S3") }} s,
    lateral flatten(input => s.response, path => 'arrivals') f

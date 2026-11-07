{{ config(materialized='table') }}
select
  cast(event_timestamp as date) as energy_date,
  count(*) as measurement_count,
  round(sum(estimated_energy_wh), 2) as estimated_energy_wh,
  round(avg(Global_active_power), 4) as avg_global_active_power_kw,
  round(max(Global_active_power), 4) as peak_global_active_power_kw,
  round(avg(Voltage), 2) as avg_voltage
from read_csv_auto('{{ env_var("ENERGY_CLEAN_CSV", "../data/processed/energy_clean.csv") }}', header=true)
group by 1

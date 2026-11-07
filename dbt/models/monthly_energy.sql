{{ config(materialized='table') }}
select
  date_trunc('month', energy_date)::date as energy_month,
  sum(measurement_count) as measurement_count,
  round(sum(estimated_energy_wh), 2) as estimated_energy_wh,
  round(avg(avg_global_active_power_kw), 4) as avg_daily_active_power_kw,
  round(max(peak_global_active_power_kw), 4) as monthly_peak_active_power_kw
from {{ ref('daily_energy') }}
group by 1

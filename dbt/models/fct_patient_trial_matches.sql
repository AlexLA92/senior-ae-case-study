with matches as (

  select * from {{ ref('raw_patient_trial_matches') }}

)

, final as (

  select
    patient_id
    , trial_id
    , site_id
    , processedAt
    , reviewedAt
    , enrolledAt
  from matches

)

select * from final

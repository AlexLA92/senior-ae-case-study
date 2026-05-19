with source as (

  select * from {{ ref('raw_patient_trial_matches') }}

)

, final as (

  select
    match_id
    , patient_id
    , trial_id
    , site_id
    , processed_at
    , reviewed_at
    , enrolled_at
  from source

)

select * from final

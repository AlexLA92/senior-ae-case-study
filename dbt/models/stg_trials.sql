with source as (

  select * from {{ ref('raw_trials') }}

)

, final as (

  select
    trial_id
    , sponsor_id
    , trialName
    , indication
    , phase
    , status
    , start_date
    , end_date
  from source

)

select * from final

with trials as (

  select * from {{ ref('stg_trials') }}

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
  from trials

)

select * from final

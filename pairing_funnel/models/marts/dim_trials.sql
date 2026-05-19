with trials as (

  select * from {{ ref('stg_trials') }}

)

, final as (

  select
    trial_id
    , sponsor_id
    , trial_name
    , indication
    , phase
    , status
    , start_date
    , end_date
  from trials

)

select * from final

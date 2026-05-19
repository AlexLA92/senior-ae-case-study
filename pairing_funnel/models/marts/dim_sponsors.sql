with sponsors as (

  select * from {{ ref('stg_sponsors') }}

)

, final as (

  select
    sponsor_id
    , sponsor_name
    , created_at
  from sponsors

)

select * from final

with sponsors as (

  select * from {{ ref('stg_sponsors') }}

)

, final as (

  select
    sponsor_id
    , sponsor_name
    , createdAt
  from sponsors

)

select * from final

with source as (

  select * from {{ ref('raw_sponsors') }}

)

, final as (

  select
    sponsor_id
    , sponsor_name
    , created_at
  from source

)

select * from final

with source as (

  select * from {{ ref('raw_sites') }}

)

, final as (

  select
    site_id
    , site_name
    , country_code
    , country_name
  from source

)

select * from final

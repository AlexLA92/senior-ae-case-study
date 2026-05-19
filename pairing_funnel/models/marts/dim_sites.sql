with sites as (

  select * from {{ ref('stg_sites') }}

)

, final as (

  select
    site_id
    , site_name
    , country_code
    , country_name
  from sites

)

select * from final

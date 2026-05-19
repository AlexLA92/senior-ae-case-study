with source as (

  select * from {{ ref('raw_sites') }}

)

, final as (

  select
    site_id
    , siteName
    , countryCode
    , country_name
  from source

)

select * from final

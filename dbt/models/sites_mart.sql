with sites as (

  select * from {{ ref('staging_sites') }}

)

, final as (

  select
    site_id
    , siteName
    , countryCode
    , country_name
  from sites

)

select * from final

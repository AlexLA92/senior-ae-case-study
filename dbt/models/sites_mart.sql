with sites as (

  select * from {{ ref('stg_sites') }}

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

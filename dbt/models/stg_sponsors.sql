with source as (

  select * from read_csv_auto('seeds/raw_sponsors.csv')

)

, final as (

  select
    sponsor_id
    , sponsor_name
    , createdAt
  from source

)

select * from final

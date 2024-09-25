with source_data as (
    select * from {{ source('sources', 'helsinki') }}
)

select
    *
from
    source_data


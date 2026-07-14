
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select minute
from "wiki"."analytics"."fct_edits_per_minute"
where minute is null



  
  
      
    ) dbt_internal_test
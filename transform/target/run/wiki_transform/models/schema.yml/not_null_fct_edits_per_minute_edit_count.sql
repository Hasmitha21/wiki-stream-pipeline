
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select edit_count
from "wiki"."analytics"."fct_edits_per_minute"
where edit_count is null



  
  
      
    ) dbt_internal_test
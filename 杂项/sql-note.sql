



 SELECT a.id, d.state, a.url   
 FROM  mls_public_record_association as a   
 INNER JOIN mls_listing as b ON a.primary_listing_id=b.id   
 INNER JOIN address as d ON d.id=b.mls_address_id   
 INNER JOIN attribute as c ON b.standard_status=c.id   
 WHERE (c.name='ACTIVE' or c.name='PENDING') and d.state NOT in ('FL', 'TN', 'IL', 'MD', 'WA', 'MI') and a.url NOT LIKE '%/for-sale/' 
 limit 0,10 ;  


select ml.id from movoto_listing_change_time mt
inner join mls_listing ml on ml.id=mt.listing_id
inner join mls_public_record_association ma on ma.primary_listing_id=ml.id
where mt.curr_status not in ('active','pending')
and locate('/for-sale/', ma.url) and ml.updated_at>'2008-08-08'
union all
select ml.id
from mls_listing ml
inner join movoto_listing_change_time mt     on mt.listing_id=ml.id
inner join mls_public_record_association ma on ma.primary_listing_id=ml.id
where mt.curr_status in ('active','pending')
and (mt.prev_status not in ('active','pending') or mt.prev_status is null)
and locate('/for-sale/', ma.url)=0 and ml.updated_at>'2008-08-08'




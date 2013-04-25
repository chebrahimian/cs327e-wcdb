/*------------------------------------------------------------------------------------------------------
#1. Which people are associated with more than one crisis?
*/

drop table if exists temp1;

create temporary table temp1 as
	select *

from person as A inner join personcrisis as B

on A.id = B.id_person;


select id, first_name, last_name

from temp1

group by id

having count(*) >1;

/*------------------------------------------------------------------------------------------------------
#2. For the past 5 decades, which countries had the most world crises per decade?
*/

drop table if exists decade1;
drop table if exists decade2;
drop table if exists decade3;
drop table if exists decade4;
drop table if exists decade5;
drop table if exists crises_decades;
drop table if exists count_by_decade;

create temporary table decade1
	(select '2010-2020' as decade, c.name, l.country
		from crisis c 
			inner join location l on (l.entity_type = 'C' and c.id = l.entity_id)
		where
			start_date >= '2010-01-01' and
			start_date <= '2019-12-31');

create temporary table decade2
	(select '2000-2010' as decade, c.name, l.country
		from crisis c
			inner join location l on (l.entity_type = 'C' and c.id = l.entity_id)
		where
			start_date >= '2000-01-01' and
			start_date <= '2009-12-31');

create temporary table decade3
	(select '1990-2000' as decade, c.name, l.country
		from crisis c
			inner join location l on (l.entity_type = 'C' and c.id = l.entity_id)
		where
			start_date >= '1990-01-01' and
			start_date <= '1999-12-31');

create temporary table decade4
	(select '1980-1990' as decade, c.name, l.country
		from crisis c
			inner join location l on (l.entity_type = 'C' and c.id = l.entity_id)
		where
			start_date >= '1980-01-01' and
			start_date <= '1989-12-31');

create temporary table decade5
	(select '1970-1980' as decade, c.name, l.country
		from crisis c
			inner join location l on (l.entity_type = 'C' and c.id = l.entity_id)
		where
			start_date >= '1970-01-01' and
			start_date <= '1979-12-31');

create temporary table crises_decades
	select decade, name as crisis, country from 
		(select * from decade1) as d1
		union (select * from decade2)
		union (select * from decade3)
		union (select * from decade4)
		union (select * from decade5);

create temporary table count_by_decade
	select decade, country, count(*) as num
		from crises_decades
		group by decade, country;

select decade, country, num
	from count_by_decade S
	where num >= ALL
		(select count(*)
			from crises_decades R
			where
				S.decade = R.decade
			group by decade, country)
	order by decade desc;

	
/*------------------------------------------------------------------------------------------------------
#3. What is the average death toll of accident crises?
*/

select Round(AVG(hi.number), 2) as avg_death
	from humanimpact hi
		inner join crisis c on (c.id = hi.crisis_id)
	where hi.type = 'Death'
		and c.kind = 'ACC';

		
/*------------------------------------------------------------------------------------------------------
# 4. What is the average death toll of world crises per country?
*/

select country, avg(number)

from humanimpact inner join location

on humanimpact.crisis_id = location.entity_id

where humanimpact.type = 'Casualties'

group by location.country;

/*------------------------------------------------------------------------------------------------------
# 5. What is the most common resource(s) needed?
*/

drop table if exists t1;

create temporary table t1
	select description, count(*) as num
		from resourceneeded
		group by description;

select description
	from t1
	where num >= ALL
		(select count(*)
			from resourceneeded
			group by description);

/*------------------------------------------------------------------------------------------------------
# 6. How many persons are related to crises located in countries other than their own?
*/

select count(distinct(p.id)) as _num_people
	from 
		crisis c
		inner join location l1 on (c.id = l1.entity_id)
		inner join personcrisis pc on (c.id = pc.id_crisis)
		inner join person p on (pc.id_person = p.id)
		inner join location l2 on (p.id = l2.entity_id)
	where l1.country != l2.country;

	
/*------------------------------------------------------------------------------------------------------
# 7. How many crises occurred during the 1960s?
*/

select start_date

from crisis

where start_date between '1960/01/01' 
and '1969/12/31';

/*------------------------------------------------------------------------------------------------------
# 8. Which orgs are located outside the United States and were involved in more than 1 crisis?
*/

select o.name as organization, count(*) as num_crises
		from
			crisisorganization as co
			inner join location l on (co.id_organization = l.entity_id)
			inner join organization o on (l.entity_id = o.id)
		where
			l.country != 'United States'
		group by co.id_organization
		having count(co.id_crisis) > 1;
		
/*------------------------------------------------------------------------------------------------------
# 9. Which Orgs, Crises, and Persons have the same location?
*/

select o.locality, o.region, o.country, cl.name as crisis, o.name as organization, pl.name as person
	from organization o
		inner join (
				select c.name, l1.locality, l1.region, l1.country
				from crisis c inner join location l1 on (l1.entity_type = 'C' and l1.entity_id = c.id)) as cl
			on (o.locality = cl.locality and o.region = cl.region and o.country = cl.country)
		inner join (
				select concat(p.first_name,' ',p.last_name) as name, l2.locality, l2.region, l2.country 
				from person p inner join location l2 on (l2.entity_type = 'P' and l2.entity_id = p.id)) as pl
			on (cl.locality = pl.locality and cl.region = pl.region and cl.country = pl.country);

/*------------------------------------------------------------------------------------------------------
# 10. Which crisis has the minimum human impact?
*/

select name from 
	(select name, sum(number) as number
	from Crisis as A, HumanImpact as B
	where A.id = B.crisis_id 
	group by name) as R
where R.number <= all
	(select sum(number) as number
	from Crisis as A, HumanImpact as B
	where A.id = B.crisis_id 
	group by name);

/*------------------------------------------------------------------------------------------------------
# 11. Count the number of crises that each organization helped
*/

select id_organization, count(*) 
from crisisorganization

group by id_organization;

/*------------------------------------------------------------------------------------------------------
# 12. Name and Postal Address of all orgs in California
*/

select name, street_address, locality, region, country, postal_code 
from organization

where region = 'California';

/*------------------------------------------------------------------------------------------------------
# 13. List all crises that happened in the same state/region
*/

select crisis.id, crisis.name, location.region

from crisis inner join location

on crisis.id = location.entity_id

where location.country = 'United States'

order by country;

/*------------------------------------------------------------------------------------------------------
# 14. Find the total number of human casualties caused by crises in the 1990s
*/

select sum(number)

from crisis inner join humanimpact

on crisis.id = humanimpact.crisis_id

where start_date between '1990/01/01' and '1999/12/31'

and type = 'Death';

/*------------------------------------------------------------------------------------------------------
# 15. Find the organization(s) that has provided support on the most Crises
*/

select name from Organization where id in
(select id_organization as id from
(select id_organization, count(*) as idCount from CrisisOrganization group by id_organization) as T
where idCount >= ALL
(select idCount from
(select id_organization, count(*) as idCount from CrisisOrganization group by id_organization) as T));

/*------------------------------------------------------------------------------------------------------
# 16. How many orgs are government based?
*/

select id, name

from organization

where kind = 'GOV'

order by name asc;

/*------------------------------------------------------------------------------------------------------
# 17. What is the total number of casualties across the DB?
*/

select sum(number) 
from humanimpact

where type = 'Death';

/*------------------------------------------------------------------------------------------------------
# 18. What is the most common type/kind of crisis occuring in the DB?
*/

drop table if exists t1;

create temporary table t1 
	select kind, count(*) as num
		from crisis
		group by kind;

select ck.name
	from t1
		inner join crisiskind ck on (t1.kind = ck.id)
	where t1.num >= ALL
		(select count(*)
			from crisis c
			group by kind);

/*------------------------------------------------------------------------------------------------------
# 19. Create a list of telephone numbers, emails, and other contact info for all orgs
*/

select name, telephone, fax, email,

street_address, locality, region, postal_code, country

from organization
order by name;

/*------------------------------------------------------------------------------------------------------
# 20. What is the longest-lasting crisis? (If no end date, then ignore)
*/

select name 

from (select name, datediff(end_date, start_date) as J 	from Crisis) as A

where A.J >= all

(select datediff(end_date, start_date) as J from Crisis);

/*------------------------------------------------------------------------------------------------------
# 21. Which person(s) is involved or associated with the most organizations?
*/

drop table if exists t1;

create temporary table t1 
	select id_person, count(*) as num
		from organizationperson
		group by id_person;

select CONCAT(p.first_name,' ',p.last_name) as person
	from t1
		inner join person p on (t1.id_person = p.id)
	where t1.num >= ALL
		(select count(*)
			from organizationperson op
			group by op.id_person);


/*------------------------------------------------------------------------------------------------------
# 22. How many hurricane crises (CrisisKind=HU)?
*/

select count(*)

from crisis
where 
kind = 'HU';

/*------------------------------------------------------------------------------------------------------
# 23. Name all humanitarian orgs in the DB
*/

select name

from organization

where kind = 'HO'

order by name asc;

/*------------------------------------------------------------------------------------------------------
# 24. List the crises in the order when they occurred (earliest to latest)
*/

select name, start_date
from crisis 
order by start_date asc;

/*------------------------------------------------------------------------------------------------------
# 25. Get the name and kind of all persons in the US (United States, USA, United States of America)
*/

select location.entity_id, person.first_name, person.last_name,

locality, region, country

from person inner join location

on person.id = location.entity_id

where country = 'United States';


/*------------------------------------------------------------------------------------------------------
# 26. Who has the longest name?
*/

select first_name, middle_name, last_name 

	from (select first_name, middle_name, last_name, 
	(length(first_name) + length(middle_name) + length(last_name)) as 	J from Person) as A 

where A.J >= all 

	(select (length(first_name) + length(middle_name) + length(last_name)) from Person);

/*------------------------------------------------------------------------------------------------------
# 27. Which kinds of crisis only have one crisis example?
*/

drop table if exists t1;

create temporary table t1 
	select kind, count(*) as num
		from crisis
		group by kind;

select ck.name
	from t1
		inner join crisiskind ck on (t1.kind = ck.id)
	where
		t1.num = 1;

/*------------------------------------------------------------------------------------------------------
# 28. Which people dont have a middle name?
*/

select CONCAT(p.first_name,' ',p.last_name) as person
	from person p
	where
		p.middle_name is null or p.middle_name is "";

/*------------------------------------------------------------------------------------------------------
# 29. What are the names that start with B?
*/

select id, first_name, last_name

from person

where first_name REGEXP '^B'

order by last_name;

/*------------------------------------------------------------------------------------------------------
# 30. List all the people associated with each country.
*/

select location.country, person.first_name, person.last_name
from 
location inner join person

on location.entity_id = person.id

order by country;

/*------------------------------------------------------------------------------------------------------
# 31. What crisis affected the most countries?
*/

drop table if exists t1;

create temporary table t1
	select c.name, count(*) as num
		from location l
			inner join crisis c on (l.entity_id = c.id)
		group by c.name;

select name
	from t1
	where
		t1.num >= ALL
		(select count(*)
			from location l
				inner join crisis c on (l.entity_id = c.id)
		 group by c.name);

/*------------------------------------------------------------------------------------------------------
# 32. What is the first (earliest) crisis in the first database?
*/

select id, name, start_date

from crisis as c1

where not exists
  (select * 
    from crisis as c2

    where c1.start_date > c2.start_date);

/*------------------------------------------------------------------------------------------------------
# 33. What is the number of organizations in the US?
*/

select count(*) as number
	from organization o
	where
		o.country = 'United States';

/*------------------------------------------------------------------------------------------------------
# 34. How many people are singers?
*/

select count(*)

from personkind

where id = 'SNG';

/*------------------------------------------------------------------------------------------------------
# 35. What is the number of leaders (current and former)? (PersonKind is "LD")\\
*/

select count(*) as number
	from person p
	where
		p.kind = 'LD';

/*------------------------------------------------------------------------------------------------------
# 36. Find the start date of every hurricane that occurred in the US
*/

select name, start_date

from crisis inner join location

on crisis.id = location.entity_id

where crisis.kind = 'HU' and location.country = 'United States';

/*------------------------------------------------------------------------------------------------------
# 37. Number of natural disasters occurring from June 5th 2000 to June 5th 2012
*/

select id, name, start_date

from crisis

where start_date between '2000/6/5' and '2012/6/5';

/*------------------------------------------------------------------------------------------------------
# 38. Number of political figures grouped by country.
*/

select max(country)
from location

where entity_type = 'C';

/*------------------------------------------------------------------------------------------------------
# 39. Location with the most number of natural disasters
*/

drop table if exists natural_disasters;
drop table if exists t1;

create temporary table natural_disasters
	select * from crisiskind
	where
		id = 'DI' OR
		id = 'EQ' OR
		id = 'FL' OR
		id = 'FR' OR
		id = 'HU' OR
		id = 'TO' OR
		id = 'TS' OR
		id = 'VO';

create temporary table t1
	select l.country, count(*) as num
		from crisis c
			inner join location l on (l.entity_type = 'C' and c.id = l.entity_id)
		where
			c.kind in
				(select id from natural_disasters)
		group by l.country;

select country, num
	from t1 as S
	where num >= ALL
		(select count(*)
			from (select c.kind, l.country 
				from crisis c
				inner join location l on (l.entity_type = 'C' and c.id = l.entity_id)) as t2
		where
			t2.kind in
				(select id from natural_disasters)
		group by country);

/*------------------------------------------------------------------------------------------------------
# 40. Average number of deaths caused by hurricanes.
*/

select avg(number)

from humanimpact inner join crisis

on humanimpact.crisis_id = crisis.id

where kind = 'HU' and type = 'Death';

/*------------------------------------------------------------------------------------------------------
# 41. total number of deaths caused by terrorist attacks
*/

select sum(number) as deaths

from Crisis as A, HumanImpact as B

where A.id = B.crisis_id and A.kind = 'TA';

/*------------------------------------------------------------------------------------------------------
# 42. List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with.
*/

select count(*)

from personcrisis inner join crisis

on personcrisis.id_crisis = crisis.id

where id_person = 'WStickney' and kind = 'HU';

/*------------------------------------------------------------------------------------------------------
# 43. List of hurricanes in the US where FEMA was NOT involved.
*/

select distinct(c.name)
	from
		crisis c
		inner join crisisorganization co on (c.id = co.id_crisis)
	where 
		c.kind = 'HU' and
		co.id_organization != 'FEMA';

/*------------------------------------------------------------------------------------------------------
# 44. Number of crises that intelligence agencies were involved in.
*/

select count(*) from

organization as org inner join crisisorganization

on org.id = crisisorganization.id_organization

where kind = 'IA';

/*------------------------------------------------------------------------------------------------------
# 45. How many more orgs does America have than Britain. 
*/

select A.x - B.y as "'MURRICA!"

from
 (
(select count(country) as x from organization where country = 'United States') as A,
 
(select count(country) as y from organization where country = 'Britain') as B
)
;
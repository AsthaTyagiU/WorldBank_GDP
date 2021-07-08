--countries with income level of "Upper middle income"
select name from v_worldbank
where incomelevel='Upper middle income'

-- countries with income level of "Low income" per region
select distinct region,name from v_worldbank
where incomelevel='Low income' 
order by region

--region with the highest proportion of "High income" countries
select region, count(*) as max_High_Income_Countries from v_worldbank
where incomelevel='High income'
group by region
order by count(*) desc
limit 1;

--cumulative/running value of GDP per region ordered by income from lowest to highest and country name
select region, sum(gdp),v.name
from v_worldbank v 
join gdp g
on v.countryid=g.countryid
where year>2016
and region<>'Aggregates'
group by region, v.name
order by region, sum(gdp) asc

--percentage difference in value of GDP year-on-year per country (base year as 2017)
select v.name as country,
	(((g7.gdp/g6.gdp)-1)*100) as gdp_yoy
from gdp g7 
 join  gdp g6 
 on g7.countryid =g6.countryid
 join v_worldbank v
 on g7.countryid= v.countryid
 where g7.year=2017 and g6.year=2016 
 and v.region<>'Aggregates'
 
 
--List 3 countries with lowest GDP per region
with cte (region,name, gdp, rank) as
(select region, name, gdp, rank() over (partition by region order by gdp asc)
from gdp g
join v_worldbank v
on g.countryid=v.countryid
where v.region<>'Aggregates' and year=2017
)
select region, name as country, gdp
from cte
where rank<4


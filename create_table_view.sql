-- To create tables and view
Create table country(
countryID char(3) primary key,
	iso2code CHAR(2),
	name VARCHAR (80)
);

Create table region(
	regionID char(3) primary key,
	regioniso CHAR(2),
	region VARCHAR (80)
);

Create table income(
	incomeID char(3) primary key,
	incomeISO CHAR(2),
	incomelevel VARCHAR (80)
);


CREATE TABLE worldBank(
	countryID char(3) PRIMARY KEY,
	regionID char(3),
	incomeID char(3),
	CONSTRAINT fk_countryID
      FOREIGN KEY(countryID) 
	  REFERENCES country(countryID),
	CONSTRAINT fk_regionID
      FOREIGN KEY(regionID) 
	  REFERENCES region(regionID),
	CONSTRAINT fk_incomeID
      FOREIGN KEY(incomeID) 
	  REFERENCES income(incomeID)  
);


CREATE TABLE GDP(
	countryID char(3),
	year integer,
	GDP float,
	CONSTRAINT fk_gdpcountryID
      FOREIGN KEY(countryID) 
	  REFERENCES country(countryID)
);

create view v_worldbank AS
(select c.countryid, c.name, wb.regionid,r.region, wb.incomeid,  i.incomelevel 
 from worldbank wb 
 join country c
on c.countryid=wb.countryid
 join region r
on r.regionID=wb.regionID
 join income i
 on i.incomeID=wb.incomeID
);
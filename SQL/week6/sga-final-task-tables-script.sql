CREATE TABLE plan_status (
	quarterid varchar(6) NOT NULL,
	status varchar(10) NOT NULL,
	modifieddatetime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	author varchar(20) NOT NULL DEFAULT CURRENT_USER,
	country varchar(5) NOT NULL,
	CONSTRAINT plan_status_pk PRIMARY KEY (quarterid, country)
);
CREATE TABLE plan_data (
	versionid varchar(1) NOT NULL,
	country varchar(5) NOT NULL,
	quarterid varchar(6) NOT NULL,
	pcid int4 NOT NULL,
	salesamt numeric(18,2) NULL,
	CONSTRAINT planapp_data_pkey PRIMARY KEY (quarterid, country, pcid, versionid)
);
CREATE TABLE country_managers (
	username varchar(30) NOT NULL,
	country varchar(5) NOT NULL,
	CONSTRAINT country_managers_pk PRIMARY KEY (username, country)
);

CREATE TABLE company (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	cname varchar(200) NOT NULL,
	countrycode varchar(10) NULL,
	city varchar(30) NULL,
	CONSTRAINT d_company_pk PRIMARY KEY (id)
);
CREATE TABLE company_sales (
	cid int4 NOT NULL,
	salesamt numeric(18,2) NULL,
	year int4 NULL,
	quarter_yr int4 NULL,
	qr varchar(6) NOT NULL,
	categoryid int4 NOT NULL,
	ccls varchar(1) NULL,
	CONSTRAINT company_sales_pk PRIMARY KEY (qr, cid, categoryid)
);
CREATE TABLE company_abc (
	cid int4 NOT NULL,
	salestotal numeric NULL,
	cls varchar(1) NULL,
	year int4 NOT NULL,
	CONSTRAINT company_abc_pk PRIMARY KEY (cid, year)
);



create view v_plan_edit as
select pd.country, pd.quarterid, pd.pcid, pd.salesamt, pd.versionid
	from plan_data pd
	where
		pd.versionid = 'P'
		and
			pd.country in (select country
				from country_managers cm
					where cm.username = current_user)
		and
			pd.quarterid in (select ps.quarterid
				from plan_status ps
					where ps.author = current_user and ps.status = 'L');



create view v_plan as
select pd.country,
    pd.pcid,
    pd.quarterid,
    pd.salesamt
   FROM plan_data pd
  WHERE pd.versionid = 'A'
  	AND (pd.country IN (SELECT cm.country FROM country_managers cm
          WHERE cm.username = CURRENT_USER)
          or
          pg_has_role(current_user, 'planadmin', 'member'))
    AND (pd.quarterid IN ( SELECT ps.quarterid
           FROM plan_status ps
          WHERE ps.status = 'A'));

create role planadmin;
create role planmanager;

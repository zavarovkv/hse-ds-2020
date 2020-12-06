import psycopg2


db_name = '2020_plans_Zavarov'
db_host = 'localhost'
db_port = 5433


def start_planning(year, quarter, user, pwd):
    #  Delete plan data from the plan_data table related to the target year and quarter.
    #  In the plan_status table delete records related to the target quarter.
    sql_delete_plan_data = 'delete from plan_data where quarterid = %(quarterid)s;'
    sql_delete_plan_status = 'delete from plan_status where quarterid = %(quarterid)s;'

    # Create planning status records (plan_status table) for the selected quarter.
    # The number of records added equals the number of countries in which customer-companies
    # (shops) are situated.
    sql_create_plan_status = '''
        insert into plan_status (quarterid, status, modifieddatetime, author, country)
            select
                %(quarterid)s 		as quarterid, 
                'R'::text 			as status,
                now()				as modifieddatetime,
                user 				as author,
                countryregioncode 	as country
            from country2;'''

    # Generate version N of planning data in the plan_data table. Use the calculation algorithm
    # is described in section 1.4. on the page.
    sql_create_plan_data = '''
        insert into plan_data (versionid, country, quarterid, pcid, salesamt)
            select 
                'N'::text 					as versionid,
                country						as country,
                year || '.' || quarter_yr 	as quarterid,
                pcid						as pcid,
                case 
                    when (salesamt_year_early + salesamt_year_later) is not null
                    then (salesamt_year_early + salesamt_year_later) / 2 else 0
                    end as salesamt
            from (
                select 
                    df.country 								 as country,
                    df.year 								 as year,
                    df.quarter_yr 							 as quarter_yr,
                    df.pcid 								 as pcid,
                    avg_sales_year_early.salesamt_year_early as salesamt_year_early,
                    avg_sales_year_later.salesamt_year_later as salesamt_year_later
                from (
                    select 
                        countryregioncode 		as country,
                        %(year)s::dec	 		as year,
                        %(quarter_yr)s::dec 	as quarter_yr,
                        pc.productcategoryid 	as pcid
                    from country2
                    cross join productcategory pc) as df
                left join (
                    select
                        avg(cs.salesamt) 	as salesamt_year_early,
                        cs.year + 2			as year,
                        cs.quarter_yr 		as quarter_yr,
                        cs.categoryid		as pcid,
                        cmp.countrycode 	as country
                    from company_sales cs
                    join company cmp on cs.cid = cmp.id
                    where cs.ccls != 'C'
                    group by year, quarter_yr, pcid, country
                ) as avg_sales_year_early
                on (
                    avg_sales_year_early.country 	= df.country and 
                    avg_sales_year_early.year	 	= df.year and
                    avg_sales_year_early.quarter_yr = df.quarter_yr and
                    avg_sales_year_early.pcid 		= df.pcid)
                left join (
                    select
                        avg(cs.salesamt) 	as salesamt_year_later,
                        cs.year + 1			as year,
                        cs.quarter_yr 		as quarter_yr,
                        cs.categoryid		as pcid,
                        cmp.countrycode 	as country
                    from company_sales cs
                    join company cmp on cs.cid = cmp.id
                    where cs.ccls != 'C'
                    group by year, quarter_yr, pcid, country
                ) as avg_sales_year_later
                on (
                    avg_sales_year_later.country = df.country and 
                    avg_sales_year_later.year = df.year and
                    avg_sales_year_later.quarter_yr = df.quarter_yr and
                    avg_sales_year_later.pcid = df.pcid)
            ) as dt;'''

    # Copy data from version N into version P in the plan_data table.
    sql_copy_plan_data = '''
        insert into plan_data (versionid, country, quarterid, pcid, salesamt)
            select 
                'P'::text 	as versionid,
                country,
                quarterid,
                pcid,
                salesamt
            from plan_data pd
            where pd.quarterid = %(quarterid)s and versionid = 'N' and salesamt > 0;'''

    quarterid = str(year) + '.' + str(quarter)

    with psycopg2.connect(dbname=db_name, user=user, password=pwd, host=db_host, port=db_port) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_delete_plan_data,    {'quarterid': quarterid})
                cursor.execute(sql_delete_plan_status,  {'quarterid': quarterid})
                cursor.execute(sql_create_plan_status,  {'quarterid': quarterid})
                cursor.execute(sql_create_plan_data,    {'quarter_yr': quarter, 'year': year})
                cursor.execute(sql_copy_plan_data,      {'quarterid': quarterid})
            except Exception as err:
                print(f'Error: {err}')

                # rollback the previous transaction before starting another
                conn.rollback()

                return False

            else:
                conn.commit()

    return True


def main():
    result = start_planning(2014, 1, 'ivan', 'ivan_pwd')
    if result:
        print('Operation completed.')
    else:
        print('Something went wrong.')


if __name__ == '__main__':
    main()

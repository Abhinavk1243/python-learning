create table web_data.temporary_table
Select sso_id,email,client_id,first_name,optin_genral from web_data.dummy_table;

/*step 2 */

UPDATE  web_data.scaleback_redemption_codes_target_test_1 as target 
INNER JOIN 
(select  redemption_code,sso_id, client_id from 
	(select ROW_NUMBER() OVER (ORDER BY sso_id) as row_num,sso_id,client_id
	from web_data.temporary_table) as A inner join 
	(select ROW_NUMBER() OVER (ORDER BY redemption_code) as row_num ,redemption_code from web_data.scaleback_redemption_codes_target_test
	where sent_to_fitbit is true and assigned is false and code_type = 'scale') as B on A.row_num=B.row_num) as source ON 
(target.redemption_code = source.redemption_code )
SET target.sso_id = source.sso_id,
target.customer = source.client_id,
target.assigned = True ,
target.assigned_date = now();


/* step 3*/
drop table IF EXISTS web_data.final_table;

/*step 4 */
 create table web_data.final_table
 select A.email,A.first_name, A.optin_genral,B.redemption_code,A.sso_id from 
 web_data.scaleback_redemption_codes_target_test as B inner join web_data.temporary_table as A on A.sso_id = B.sso_id;

/*step 5 */
drop table IF EXISTS web_data.temporary_table;

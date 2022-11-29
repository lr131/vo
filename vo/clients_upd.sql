--UPDATE
--	clients_client
--SET
--	birthday = '1900-01-01'
--WHERE
--	birthday ISNULL ;

--UPDATE
--	clients_client
--SET
--	birthday = '1900-01-01'
--WHERE
--	birthday like '189%' ;

--SELECT * from clients_client where birthday like '189%' ;

--UPDATE
--	clients_client
--SET
--	cuser_id = 1
--WHERE
--	city LIKE "Якутск";

--UPDATE
--	clients_client
--SET
--	muser_id = 1
--WHERE
--	city LIKE "Якутск";

--UPDATE
--	clients_client
--SET
--	muser_id = 1
--WHERE
--	note LIKE "%Уточнить%";

--у них есть дети, обновляем
--UPDATE
--	clients_client
--SET
--	have_kids  = TRUE
--WHERE
--	comment  LIKE "%ын%" or note like "%ын%"
--	or comment  LIKE "%доч%" or note like "%доч%"
--	or comment  LIKE "% дет%" or note like "% дет%";

--UPDATE
--	clients_client
--SET
--	have_kids  = TRUE
--WHERE
--	comment  LIKE "%ын%" or note like "%ын%"
--	or comment  LIKE "%доч%" or note like "%доч%"
--	or comment  LIKE "% дет%" or note like "% дет%";


-- узнать, у кого есть дети
--SELECT  * from clients_client cc
--where
--comment  LIKE "%ын%" or note like "%ын%"
--or comment  LIKE "%доч%" or note like "%доч%"
--or comment  LIKE "% дет%" or note like "% дет%";


-- этих поправить руками, тут 12 человек. Что они не курсовые и у кого есть дети (или кто чей ребёнок)
SELECT  * from clients_client cc WHERE  comment like "%урс%нет%";

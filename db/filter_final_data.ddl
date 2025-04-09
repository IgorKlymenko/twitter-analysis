DROP FUNCTION filter_final_data(boolean,boolean);
CREATE OR REPLACE FUNCTION filter_final_data(canadian_param boolean, founder_param boolean)
RETURNS SETOF final
LANGUAGE sql
AS $$
    SELECT * FROM final
    WHERE 
        (canadian_param = false OR canadian = true)
        AND
        (founder_param = false OR founder = true)
    ORDER BY score DESC;
$$;
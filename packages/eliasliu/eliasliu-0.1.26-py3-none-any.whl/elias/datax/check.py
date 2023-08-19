# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 16:23:37 2023

@author: Administrator
"""


from elias import usual as u
from loguru import logger

def null_rows_check(table_name,hosts,output='null_rate'):
    '''
    完备性检查

    Parameters
    ----------
    table_name : TYPE
        DESCRIPTION.
    hosts : TYPE
        DESCRIPTION.

    Returns
    -------
    null_rows : TYPE
        DESCRIPTION.

    '''
    from elias.datax import auto_create_table as ac
    df = ac.schema_transfer(ac.schema_read(table_name,hosts))
    
    target_db_type = hosts['dbtype']
    
    if target_db_type == 'mysql':
        col_sql_list = []
        for i in range(len(df)):
            if df['col_type_name'][i] in ['int','float']:
                col_sql = f"`{df['col_name'][i]}` is null"
            elif df['col_type_name'][i] in ['string','text']:
                col_sql = f"`{df['col_name'][i]}`= '' or `{df['col_name'][i]}` is null"
            else:
                col_sql = f"`{df['col_name'][i]}`= '' or `{df['col_name'][i]}` is null"
            
            # col_sql = f"{col_sql1} or `{df['col_name'][i]}` is null"
            col_sql_list.append(col_sql)
        
        final_col_sql = '\n or '.join(col_sql_list)
        
        sql = f'''
        SELECT
        sum(if({final_col_sql},1,0)) as `null_rows`,
        count(*) as rows,
        sum(if({final_col_sql},1,0))/count(*) as `null_rate`
        FROM
        	`{hosts['db']}`.`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')
        
        df_null = u.mysql_select(sql, hosts)
    
    
    elif target_db_type == 'clickhouse':
        col_sql_list = []
        for i in range(len(df)):
            if df['col_type_name'][i] in ['int','float']:
                col_sql = f"`{df['col_name'][i]}` is null"
            elif df['col_type_name'][i] in ['string','text']:
                col_sql = f"`{df['col_name'][i]}`= '' or `{df['col_name'][i]}` is null"
            else:
                col_sql = f"`{df['col_name'][i]}`= '' or `{df['col_name'][i]}` is null"
            
            # col_sql = f"{col_sql1} or `{df['col_name'][i]}` is null"
            col_sql_list.append(col_sql)
        
        final_col_sql = '\n or '.join(col_sql_list)
        
        sql = f'''
        SELECT
        sum(if({final_col_sql},1,0)) as `null_rows`,
        count(*) as rows,
        sum(if({final_col_sql},1,0))/count(*) as `null_rate`
        FROM
        	`{hosts['db']}`.`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')
        
        df_null = u.clickhouse_select(sql, hosts)
    
    
    elif target_db_type == 'maxcompute':
        col_sql_list = []
        for i in range(len(df)):
            if df['col_type_name'][i] in ['int','float']:
                col_sql = f"`{df['col_name'][i]}` is null"
            elif df['col_type_name'][i] in ['string','text']:
                if df['col_type'][i] == 'datetime':
                    col_sql = f"`{df['col_name'][i]}` is null"
                else:
                    col_sql = f"`{df['col_name'][i]}`= '' or `{df['col_name'][i]}` is null"
            else:
                col_sql = f"`{df['col_name'][i]}`= '' or `{df['col_name'][i]}` is null"
            
            # col_sql = f"{col_sql1} or `{df['col_name'][i]}` is null"
            col_sql_list.append(col_sql)
        
        final_col_sql = '\n or '.join(col_sql_list)
        
        sql = f'''
        SELECT
        sum(if({final_col_sql},1,0)) as `null_rows`,
        count(*) as rows,
        sum(if({final_col_sql},1,0))/count(*) as `null_rate`
        FROM
        	`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')
        
        df_null = u.mc_select(sql, hosts)
    
    else:
        raise ValueError("Unsupported target database type.")
    
    logger.info(f"\n\nsql select finished\n\n rows:{ df_null['rows'][0]}\n null_rows:{ df_null['null_rows'][0]}\n null_rate:{ df_null['null_rate'][0]}\n")
    try:
        result = df_null[output][0]
    except Exception as e:
        raise ValueError(f"{e}\nUnsupported output type. Only ('rows' or 'null_rows' or 'null_rate'")
        
    return result



def key_check(table_name,hosts,key,output='key_rate'):
    
    target_db_type = hosts['dbtype']
    
    if target_db_type == 'mysql':
        sql = f'''
        select 
        count(*) as `rows`,
        count(distinct `{key}`) as `key_rows`,
        count(distinct `{key}`)/count(*) as `key_rate`
        FROM
        	`{hosts['db']}`.`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')

        df_key = u.mysql_select(sql, hosts)
        
    elif target_db_type == 'clickhouse':
        sql = f'''
        select 
        count(*) as `rows`,
        count(distinct `{key}`) as `key_rows`,
        count(distinct `{key}`)/count(*) as `key_rate`
        FROM
        	`{hosts['db']}`.`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')

        df_key = u.clickhouse_select(sql, hosts)
        
    elif target_db_type == 'maxcompute':
        sql = f'''
        select 
        count(*) as `rows`,
        count(distinct `{key}`) as `key_rows`,
        count(distinct `{key}`)/count(*) as `key_rate`
        FROM
        	`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')

        df_key = u.mc_select(sql, hosts)
    
    else:
        raise ValueError("Unsupported target database type.")
    
    logger.info(f"\n\nsql select finished\n\n rows:{ df_key['rows'][0]}\n null_rows:{ df_key['key_rows'][0]}\n null_rate:{ df_key['key_rate'][0]}\n")
    try:
        result = df_key[output][0]
    except Exception as e:
        raise ValueError(f"{e}\nUnsupported output type. Only ('rows' or 'key_rows' or 'key_rate'")
        
    return result




def is_valid_time(time_str, time_format):
    from datetime import datetime
    try:
        datetime.strptime(time_str, time_format)
        return True
    except Exception as e:
        raise ValueError(f"{e}\nUnsupported time_str. Only %H:%M:%S")
        return False


def time_check(table_name,hosts,col_name,time_rule = '09:00:00',output='time_score'):
    
    
    time_rule_check = is_valid_time(time_rule, "%H:%M:%S")
    logger.info(f"time_rule is valid ( {time_rule} ：{time_rule_check} )")
    
    time_limit = u.today()+' '+time_rule
    
    target_db_type = hosts['dbtype']
    
    if target_db_type == 'mysql':
        sql = f'''
        select 
            max({col_name}) as `update_time`,
            TIMESTAMPDIFF(SECOND, max({col_name}),'{time_limit}') as time_gap,
            if(TIMESTAMPDIFF(SECOND, max({col_name}),'{time_limit}')>=0,1,0) as time_score
        FROM
        	`{hosts['db']}`.`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')

        df_time = u.mysql_select(sql, hosts)
        
    elif target_db_type == 'clickhouse':
        sql = f'''
        select 
            max({col_name}) as `update_time`,
            toUnixTimestamp('{time_limit}') - toUnixTimestamp(max({col_name})) as time_gap,
            if(toUnixTimestamp('{time_limit}') - toUnixTimestamp(max({col_name}))>=0,1,0) as time_score
        FROM
        	`{hosts['db']}`.`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')

        df_time = u.clickhouse_select(sql, hosts)
        
    elif target_db_type == 'maxcompute':
        sql = f'''
        select 
            max({col_name}) as `update_time`,
            UNIX_TIMESTAMP('{time_limit}') - UNIX_TIMESTAMP(max({col_name}))  as time_gap,
            if(UNIX_TIMESTAMP('{time_limit}') - UNIX_TIMESTAMP(max({col_name}))>=0,1,0) as time_score
        FROM
        	`{table_name}` x
        '''
        logger.info(f'sql generating …… \n\n {sql} \n\n')
        logger.info('sql selecting')

        df_time = u.mc_select(sql, hosts)
    
    else:
        raise ValueError("Unsupported target database type.")
    
    logger.info(f"\n\nsql select finished\n\n update_time:{ df_time['update_time'][0]}\n time_gap:{ df_time['time_gap'][0]}\n time_score:{ df_time['time_score'][0]}\n")
    try:
        result = df_time[output][0]
    except Exception as e:
        raise ValueError(f"{e}\nUnsupported output type. Only ('update_time' or 'time_gap' or 'time_score'")
        
    return result



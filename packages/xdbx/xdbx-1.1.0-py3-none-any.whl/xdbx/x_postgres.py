# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2023/8/16 13:44
# @Author : BruceLong
# @FileName: x_postgres.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import copy
import datetime
import json
from typing import Dict, List

import psycopg2

from .config import *
from .x_single import SingletonType
import logging as log
from pyxbox import tools


def auto_retry(func):
    def wapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.error(
                    """
                    error:%s
                    sql:  %s
                    """
                    % (e, kwargs.get("sql") or args[1])
                )

    return wapper


class PostgrePipeline(metaclass=SingletonType):
    '''
    SqlServer存储管道
    '''

    def __init__(self):
        '''
        初始化操作
        '''
        self.host = POSTGRES_HOST
        self.username = POSTGRES_USERNAME
        self.port = POSTGRES_PORT
        self.password = POSTGRES_PASSWORD
        self.db = POSTGRES_DB

    def __get_connect(self):
        '''
        创建连接信息
        :return:
        '''
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.connect = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.db,
            options="-c search_path=dbo,public"
        )
        cursor = self.connect.cursor()
        if not cursor:
            raise (NameError, "连接数据库失败")
        else:
            return self.connect, cursor

    def get_connect_test(self):
        return self.__get_connect()

    def __create_table(self, cur, con, ite: dict, table: str, primary_key=None):
        '''
        合建表相关的信息
        :param item: 数据
        :param table: 表名
        :return:
        '''
        # cur = self.__get_connect()
        # 判断是否存在该表
        item = copy.deepcopy(ite)
        sql = f'''SELECT tablename FROM pg_tables WHERE schemaname = 'public' and tablename ='{table}';'''
        cur.execute(sql)
        max_len = 767
        if not cur.fetchone():
            # 生成创建字段信息
            # 生成创建字段信息
            primary_key_dict = {}
            if isinstance(primary_key, str):
                primary_key_dict = {primary_key: max_len // 4}
            if isinstance(primary_key, dict):
                primary_key_dict = primary_key
            if isinstance(primary_key, list):
                primary_key_dict = {key: max_len // 4 // len(primary_key) for key in primary_key}
            if primary_key_dict:
                [item.pop(i) for i in primary_key_dict if i in list(item.keys())]
            field_info = ',\n'.join(
                [
                    f'{field} TEXT'
                    for field, values in item.items()
                ]
            )

            # end_field = list(item.keys())[-1]
            cur.execute('select version()')
            postgres_version = cur.fetchone()[0]
            pk_field = ','.join([f'`{i}`' for i in primary_key_dict.keys()])
            sql_table = f'''CREATE TABLE {table}(
                                x_id BIGSERIAL,
                                x_inserttime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                x_updatetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                {field_info},
                                PRIMARY KEY ("x_id")
                            );
                        '''
            if primary_key:
                pk_info = ',\n'.join(
                    [
                        f'{field} varchar(255)'
                        for field, values in primary_key_dict.items()
                    ]
                )
                field_info = ',\n'.join([field_info, pk_info]) if pk_info else field_info
                sql_table = f'''CREATE TABLE {table}(
                                x_id BIGSERIAL,
                                x_inserttime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                x_updatetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                {field_info},
                                PRIMARY KEY ("{pk_field}")
                                );'''
            try:
                # print(sql_table)
                cur.execute(sql_table)
                con.commit()
                # print(f'Postgres Version is :{postgres_version}', '*' * 15, 'Create Table Successful')
                log.info(''.join([f'Postgres Version is :{postgres_version}', '*' * 15, 'Create Table Successful']))
            except Exception as e:
                # print(f'Postgres Version is :{postgres_version}', '*' * 15, 'Create Table Failed', e)
                log.error(
                    ''.join([f'Postgres Version is :{postgres_version}', '*' * 15, 'Create Table Failed', str(e)]))
        else:
            # 查询表字段
            select_fields_sql = f'''SELECT 
                                        column_name, 
                                        data_type, 
                                        character_maximum_length,
                                        column_default,
                                        is_nullable
                                    FROM 
                                        information_schema.columns
                                    WHERE 
                                        table_name = '{table}'
                                    ORDER BY 
                                        ordinal_position;
                                    '''
            cur.execute(select_fields_sql)
            # 获取已经存在的表字段
            allready_exists_fields = {i[0].lower() for i in cur.fetchall()}
            # 目前新的字段名
            new_fields = {i.lower() for i in item.keys()}
            # 差集算出需要添加的字段名
            not_exists_fields = new_fields - allready_exists_fields
            if list(not_exists_fields):
                # 构造字段信息
                not_exists_fields_info = ','.join(
                    [
                        f'{field} text'
                        for field, values in item.items() if field.lower() in not_exists_fields
                    ]
                )
                add_fields_sql = f'''alter table {table} add {not_exists_fields_info}'''
                try:
                    # print(add_fields_sql)
                    cur.execute(add_fields_sql)
                    con.commit()
                    # print('Create Field Successful')
                    log.info('Create Field Successful')
                except Exception as e:
                    # print('Create Field Failed', e)
                    log.error('Create Field Failed' + str(e))
                    # raise e

    @auto_retry
    def find(self, sql, limit=0, to_json=True):
        """
        @summary:
        无数据： 返回()
        有数据： 若limit == 1 则返回 (data1, data2)
                否则返回 ((data1, data2),)
        ---------
        @param sql:
        @param limit:
        @param to_json 是否将查询结果转为json
        ---------
        @result:
        """
        conn, cursor = self.__get_connect()

        cursor.execute(sql)

        if limit == 1:
            result = cursor.fetchone()  # 全部查出来，截取 不推荐使用
        elif limit > 1:
            result = cursor.fetchmany(limit)  # 全部查出来，截取 不推荐使用
        else:
            result = cursor.fetchall()

        if to_json:
            columns = [i[0] for i in cursor.description]

            # 处理数据
            def convert(col):
                if isinstance(col, (datetime.date, datetime.time)):
                    return str(col)
                elif isinstance(col, str) and (
                        col.startswith("{") or col.startswith("[")
                ):
                    try:
                        # col = self.unescape_string(col)
                        return json.loads(col)
                    except:
                        return col
                else:
                    # col = self.unescape_string(col)
                    return col

            if limit == 1:
                result = [convert(col) for col in result]
                result = dict(zip(columns, result))
            else:
                result = [[convert(col) for col in row] for row in result]
                result = (dict(zip(columns, r)) for r in result)

        self.close_connection(conn, cursor)

        return result

    def add(self, sql, item, table, primary_key, exception_callfunc=None):
        """

        Args:
            sql:
            exception_callfunc: 异常回调

        Returns: 添加行数

        """
        try:
            conn, cursor = self.__get_connect()
            self.__create_table(cur=cursor, con=conn, ite=item, table=table, primary_key=primary_key)
            affect_count = cursor.execute(sql)
            conn.commit()

        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
            """
                % (e, sql)
            )
            if exception_callfunc:
                exception_callfunc(e)
            raise e
        finally:
            self.close_connection(conn, cursor)

        return affect_count

    def upsert(self, item: Dict, table: str, primary_key, **kwargs):
        """
        添加数据, 直接传递json格式的数据，不用拼sql
        Args:
            table: 表名
            item: 字典 {"xxx":"xxx"}
            **kwargs:
            @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
            @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
            @param insert_ignore: 数据存在忽略
        Returns: 添加行数
        """

        sql = tools.x_sql.make_insert_sql(table, item, **kwargs)
        return self.add(sql, item, table, primary_key)

    def insert_one(self, item: dict, table: str, primary_key=None, auto_table: bool = True):
        '''
        插入一条数据
        :param item:
        :param table:
        :return:
        '''
        conn, cursor = self.__get_connect()
        if auto_table:
            self.__create_table(cur=cursor, con=conn, ite=item, table=table, primary_key=primary_key)
        # 获取到一个以键且为逗号分隔的字符串，返回一个字符串
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        print(sql)
        try:
            # 这里的第二个参数传入的要是一个元组
            # data = [v if isinstance(v, int) else str(v) for v in item.values()]
            data = [str(v) for v in item.values()]
            # print(data)
            cursor.execute(sql, tuple(data))
            # print('Insert One Successful')
            log.info('Insert One Successful')
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
        pass

    def insert_many(self, items: List[Dict], table, primary_key=None, auto_table: bool = True, **kwargs):
        """
        @summary: 批量添加数据
        ---------
        @ param sql: insert ignore into (xxx,xxx) values (%s, %s, %s)
        # param items: 列表 [{}, {}, {}]
        ---------
        @result: 添加行数
        """
        try:
            conn, cursor = self.__get_connect()
            if auto_table:
                self.__create_table(cur=cursor, con=conn, ite=items[0], table=table, primary_key=primary_key)
            sql, values = tools.x_sql.make_batch_sql(table, items, **kwargs)
            affect_count = cursor.executemany(sql, values)
            conn.commit()
            # print('Insert Many Successful')
            log.info('Insert Many Successful')

        except Exception as e:
            # print('Insert Many Failed:', e)
            log.error('Insert Many Failed:' + str(e))
            raise e
        finally:
            self.close_connection(conn, cursor)

        return affect_count

    def update(self, table, item: Dict, where):
        """
        更新, 不用拼sql
        Args:
            table: 表名
            item: 数据 {"xxx":"xxx"}
            where: 更新条件 where后面的条件，如 where='status=1'

        Returns: True / False

        """
        sql = tools.x_sql.make_update_sql(table, item, where)
        return self.execute(sql)

    def execute(self, sql):
        try:
            conn, cursor = self.__get_connect()
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
            """
                % (e, sql)
            )
            raise e
        else:
            return True
        finally:
            self.close_connection(conn, cursor)

    def close_connection(self, conn, cursor):
        cursor.close()
        conn.close()


x_pgsql = PostgrePipeline()

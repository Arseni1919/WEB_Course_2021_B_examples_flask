# Example Project of the WEB Course 2021-B at BGU

## MySQL information

First, you will need to install MySQL on a computer.
- [Installation of MySQL](https://medium.com/365datascience/installing-mysql-and-getting-acquainted-with-the-interface-cf0f98e599f2)

Then, install mysql.connector.
- [`mysql` - get started](https://www.w3schools.com/python/python_mysql_getstarted.asp)

You need to create schema and then a certain table inside this schema.
Here is the cheatsheet to help you with the basic commands.
- [MySQL cheatsheet](https://gist.github.com/hofmannsven/9164408)

Example of creating a table:

```mysql
CREATE TABLE table_try1 (
  id int auto_increment primary key,
  name varchar(255),
  email text,
  create_date timestamp default CURRENT_TIMESTAMP,
  password varchar(120)
);
```

Check syntax of MySQL. For example here:
- [MySQL Syntax Check](https://www.piliapp.com/mysql-syntax-check/)

You can explore all the possibilities of MySQL here.
- [MySQL docs](https://dev.mysql.com/doc/connector-python/en/)





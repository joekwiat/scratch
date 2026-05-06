import argparse
import configparser
import csv
import pathlib
import sys
import tomllib
import redshift_connector

CONFIG_PATH  = pathlib.Path(__file__).parent / ".config.ini"
QUERIES_PATH = pathlib.Path(__file__).parent / "queries.toml"


def load_config(path: pathlib.Path = CONFIG_PATH) -> dict:
    cfg = configparser.RawConfigParser()
    if not cfg.read(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    section = cfg["redshift"]
    return {
        "host":     section["host"],
        "port":     section.getint("port", 5439),
        "database": section["database"],
        "user":     section["user"],
        "password": section["password"],
    }


def get_connection(params: dict | None = None) -> redshift_connector.Connection:
    params = params or load_config()
    return redshift_connector.connect(**params)


def run_query(conn: redshift_connector.Connection, key: str, path: pathlib.Path = QUERIES_PATH) -> None:
    with open(path, "rb") as f:
        queries = tomllib.load(f)
    if key not in queries:
        available = ", ".join(queries)
        raise KeyError(f"Query {key!r} not found. Available: {available}")
    sql = queries[key]["sql"]
    with conn.cursor() as cur:
        cur.execute(sql)
        if cur.description:
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            writer = csv.writer(sys.stdout)
            writer.writerow(cols)
            for row in rows:
                writer.writerow("" if v is None else v for v in row)


def select_from_table(conn: redshift_connector.Connection, schema_table: str) -> None:
    if "." not in schema_table:
        raise ValueError(f"Expected schema.table, got: {schema_table!r}")
    schema, table = schema_table.split(".", 1)
    with conn.cursor() as cur:
        cur.execute(f'SELECT * FROM "{schema}"."{table}" LIMIT 100')
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    writer = csv.writer(sys.stdout)
    writer.writerow(cols)
    for row in rows:
        writer.writerow("" if v is None else v for v in row)


def show_table(conn: redshift_connector.Connection, schema_table: str) -> None:
    if "." not in schema_table:
        raise ValueError(f"Expected schema.table, got: {schema_table!r}")
    schema, table = schema_table.split(".", 1)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
            """,
            (schema, table),
        )
        rows = cur.fetchall()
    if not rows:
        print(f"No columns found for {schema_table!r} — check the name and permissions.")
        return
    print(f"{'column':<40} {'type':<30} {'nullable'}")
    print("-" * 80)
    for col, dtype, max_len, nullable in rows:
        display_type = f"{dtype}({max_len})" if max_len else dtype
        print(f"{col:<40} {display_type:<30} {nullable}")


def show_tables(conn: redshift_connector.Connection, schema: str | None) -> None:
    if schema:
        where = "AND table_schema = %s"
        bind = (schema,)

    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
              {where}
            ORDER BY table_schema, table_name
            """,
            bind,
        )
        rows = cur.fetchall()

    for db_schema, table in rows:
        print(f"{db_schema}.{table}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redshift utility")
    parser.add_argument(
        "--show-schema",
        nargs="?",
        const=None,
        default=argparse.SUPPRESS,
        metavar="SCHEMA",
        help="Show tables. Optionally filter to a specific schema.",
    )
    parser.add_argument(
        "--show-table",
        metavar="SCHEMA.TABLE",
        help="Show column schema for the given table.",
    )
    parser.add_argument(
        "--select-from-table",
        metavar="SCHEMA.TABLE",
        help="Show up to 100 rows from the given table.",
    )
    parser.add_argument(
        "--run-query",
        metavar="KEY",
        help="Run a named query from queries.toml.",
    )
    args = parser.parse_args()

    conn = get_connection()

    if args.run_query:
        run_query(conn, args.run_query)
    elif args.show_table:
        show_table(conn, args.show_table)
    elif args.select_from_table:
        select_from_table(conn, args.select_from_table)
    elif hasattr(args, "show_schema"):
        show_tables(conn, args.show_schema)
    else:
        cfg = load_config()
        print(f"Connected to {cfg['database']} on {cfg['host']} as {cfg['user']}")

    conn.close()

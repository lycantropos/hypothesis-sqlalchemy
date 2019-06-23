from typing import (Any,
                    Callable,
                    List)

from hypothesis import strategies
from sqlalchemy.schema import (Column,
                               MetaData,
                               Table)

from hypothesis_sqlalchemy import columns
from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import sql_identifiers


def factory(*,
            tables_names: Strategy[str] = sql_identifiers,
            metadatas: Strategy[MetaData],
            columns_lists: Strategy[List[Column]] =
            columns.non_all_unique_lists_factory(),
            extend_existing: Strategy[bool] = strategies.just(True)
            ) -> Strategy:
    def table_factory(draw: Callable[[Strategy], Any]) -> Table:
        table_name = draw(tables_names)
        metadata = draw(metadatas)
        columns_list = draw(columns_lists)
        return Table(table_name,
                     metadata,
                     *columns_list,
                     extend_existing=draw(extend_existing))

    return strategies.composite(table_factory)()

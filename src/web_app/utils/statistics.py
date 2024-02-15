from pandas import DataFrame, Series
from pandas.core.indexes.accessors import DatetimeProperties


def order_processing_rate_per_hour(warehouse_orders: DataFrame) -> tuple[Series, Series, Series]:
    """
    Given a warehouse orders DataFrame, the function processes datas and returns a series
    of Series objects in the following order:
    <ol>
        <li><b>Orders started every hour</b>: a Series with a number of rows with datetime and their relative count
                                              (number of orders started ONLY)</li>
        <li><b>Orders finished every hour</b>: as orders started but only with the number of orders completed.</li>
        <li><b>Orders completed every hour</b>: a Series with Start datetime, Finish datetime and their relative count.
                                                In this case, it's possible to find rows without a Start datetime.
                                                The reason is simple: if an order is started at (e.g.) 10:58 and
                                                finished at 11:05, it will not be counted in the 10-hour counter.</li>
    </ol>

    @param warehouse_orders: the DataFrame containing the warehouse orders.
    @return: a tuple in the form (orders_started_every_hour, orders_finished_every_hour, orders_completed_every_hour).
    """
    # take every order and convert time into hours
    hour_start_orders: DatetimeProperties = warehouse_orders["Start"].dt.to_period("H")
    hour_end_orders: DatetimeProperties = warehouse_orders["Finish"].dt.to_period("H")
    # count how many orders have started each hour (does not sort, so it keeps the real time order)
    orders_started_every_hour: Series = hour_start_orders.value_counts(sort=False)
    # count how many orders has finished each hour
    orders_finished_every_hour: Series = hour_end_orders.value_counts(sort=False)
    # create a unique matrix and count how many values are the same at each hour
    orders_completed_every_hour: Series = DataFrame({'Start': hour_start_orders, 'Finish': hour_end_orders}).value_counts(sort=False)
    return orders_started_every_hour, orders_finished_every_hour, orders_completed_every_hour

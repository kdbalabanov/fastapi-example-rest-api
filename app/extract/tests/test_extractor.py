from datetime import date

import pandas

from app.extract import extractor


def test_transform_response_data():
    input_columns = ['date', 'low', 'high', 'open', 'close', 'volume']
    input_data = [
        [1641340800, 10000.00, 10000.00, 10000.00, 10000.00, 25067.674768],
        [1641427200, 20000.00, 20000.00, 20000.00, 20000.00, 20780.047850],
        [1641513600, 30000.00, 30000.00, 30000.00, 30000.00, 26122.199907],
        [1641600000, 60000.00, 60000.00, 60000.00, 60000.00, 15454.113151],
        [1641686400, 30000.00, 30000.00, 30000.00, 30000.00, 11074.224982]
    ]

    expected_columns = input_columns
    expected_data = [
        [date(2022, 1, 5).isoformat(), 10000.00, 10000.00, 10000.00, 10000.00, 25067.674768],
        [date(2022, 1, 6).isoformat(), 20000.00, 20000.00, 20000.00, 20000.00, 20780.047850],
        [date(2022, 1, 7).isoformat(), 30000.00, 30000.00, 30000.00, 30000.00, 26122.199907],
        [date(2022, 1, 8).isoformat(), 60000.00, 60000.00, 60000.00, 60000.00, 15454.113151],
        [date(2022, 1, 9).isoformat(), 30000.00, 30000.00, 30000.00, 30000.00, 11074.224982]
    ]

    result_df = pandas.DataFrame(input_data, columns=input_columns)
    expected_df = pandas.DataFrame(expected_data, columns=expected_columns)
    extractor.transform_coinbase_data(result_df)
    pandas.testing.assert_frame_equal(expected_df, result_df)

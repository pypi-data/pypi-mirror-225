def filter_df_on_operating_units(df, operating_units):
    return df[df["Operating Unit"].isin(operating_units)]


def ensure_tuple(value):
    if isinstance(value, tuple):
        return value
    elif isinstance(value, list):
        return tuple(value)
    else:
        return (value,)

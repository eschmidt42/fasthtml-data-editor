import pandas as pd
from fasthtml.common import (
    H1,
    Button,
    Container,
    Div,
    Form,
    Input,
    Table,
    Tbody,
    Td,
    Th,
    Thead,
    Title,
    Tr,
    fast_app,
    picolink,
    serve,
)

app, rt = fast_app(hdrs=(picolink,))

# Example data
df = pd.DataFrame(
    data={
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "Los Angeles", "Chicago"],
    }
)


def dataframe_to_form(df: pd.DataFrame):
    table_head = Thead(Tr(Th(v, scope="col") for v in df.columns))
    table_body = Tbody(
        Tr(
            Td(Input(default=v, id=f"{i_row}-{k}", placeholder=v))
            for k, v in row.items()
        )
        for i_row, row in df.iterrows()
    )

    table = Table(table_head, table_body)
    button = Button(
        "save",
    )

    form = Form(table, button, action="/", method="post", target_id="dataframe")
    return form


@rt("/", methods=["get"])
def home_get():
    global df
    form = dataframe_to_form(df)
    container = Container(H1("DataFrame editor"), Div(form, id="dataframe-container"))
    return Title("DataFrame editor"), container


@rt("/", methods=["post"])
def home_post(d: dict):
    global df
    new_data = df.to_dict(orient="list")
    for key, value in d.items():
        row_idx = int(key.split("-")[0])
        column = key.split("-")[1]

        if value:
            new_data[column][row_idx] = value

    df = pd.DataFrame(new_data)
    return home_get()


if __name__ == "__main__":
    serve(port=5001)

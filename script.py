import modal

app = modal.App("My-App")

@app.function()
def sum(x: int, y: int) -> None:
    print( x + y )

@app.function()
def square(x: int) -> None:
    print( x ** 2 )


@app.local_entrypoint()
def main(x: int) -> None:
    square.remote(x)
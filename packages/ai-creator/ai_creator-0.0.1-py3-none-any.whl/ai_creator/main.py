from enum import Enum
from typing import Annotated
import typer

app = typer.Typer()


class ImageColor(str, Enum):
    grayscale = "grayscale"
    rgb = "rgb"


    def __str__(self):
        return self.value


@app.command()
def make(
        img_size: Annotated[tuple[int, int], typer.Argument(help="Training images size (WIDTH HEIGH)")],
        img_color: ImageColor,
        author: str = "<anonymous>",
        epochs: Annotated[int, typer.Option(help="Number of epochs/generations to train")] = 8,
        batch_size: Annotated[int, typer.Option(help="batch-size")] = 64,
        val_split: Annotated[float, typer.Option(help="validation-split")] = 0.2,
        dropout: Annotated[float, typer.Option(help="dropout")] = 0.4,
):
    """
    Create a new ai-model
    """
    print("DEBUG: Command valid")


@app.command()
def force_changes():
    """
    Force changes on internal data from a .aim model [DANGEROUS]
    """
    print("DEBUG: Command valid")


# if __name__ == "__main__":
#     app()

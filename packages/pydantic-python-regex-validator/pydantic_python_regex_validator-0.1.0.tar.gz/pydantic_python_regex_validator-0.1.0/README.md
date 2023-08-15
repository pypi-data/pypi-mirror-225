# A regex parser for Pydantic, using pythons regex validator.

Since pydantic V2, pydantics regex validator has some limitations. It cannot do look arounds.
There is some documenation on how to get around this. This package simplifies things for developers

We provide the class, Regex, which can be used.

## Usage in Pydantic

To use simply do:

 
```python
from pydantic_python_regex_validator import Regex
from pydantic import BaseModel
from typing import Annotated

class MyModel(BaseModel):
    my_field: Annotated[str, Regex(r'^foo')]
```

This will then have field, `my_field`, which will have the regex constraint `^foo`

## Usage in FastAPI

This can also be used with fastapi.
```python
from pydantic_python_regex_validator import Regex
from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/test")
async def endpoint(my_param: Annotated[str, Query(), Regex(r"^foo")]):
    return my_param
```

This then has an endpoint at `/test` which takes a param, `my_param`, which has the regex constraint `^foo`
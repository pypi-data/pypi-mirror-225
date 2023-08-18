# Railtown AI Logging Python Package

## Setup

1. Sign up for [Railtown AI](https://railtown.ai)
1. Create a project, navigate to the Project Configuration page, and copy your API key
1. In your app...
   1. install the Railtown AI SDK: `pip install railtownai`
   1. Set `RAILTOWN_API_KEY` in your environment variables or manually set it in your app: `railtownai.init('YOUR_RAILTOWN_API_KEY')`
   1. Log errors with the following example

```python

import railtownai

railtownai.init('YOUR_RAILTOWN_API_KEY')

try:
   some_code_that_throws_an_error()

except Exception as e:
   railtownai.log(e)
```

## Contributing

See the [contributing guide](./CONTRIBUTING.md) for more information.

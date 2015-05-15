# slack-overflow

A programmer's best friend, now in Slack. Search StackOverflow right from Slack without coming off as dumb.

![](http://i.imgur.com/c9HuKw8.gif)

## Usage

From any Slack channel, just type `/overflow [search terms]`. The questions will be shown on the same channel visible just to you.

## Installation

1. Go to your channel
2. Click on **Configure Integrations**.
3. Scroll all the way down to **DIY Integrations & Customizations section**.
4. Click on **Add** next to **Slash Commands**.
  - Command: `/overflow`
  - URL: `http://so.goel.io/overflow`
  - Method: `POST`
  - All other settings can be set on your own discretion.

## Developing

Add a `config.py` file based on `config.py.example` file. Grab your StackExchange key from http://stackapps.com/

```python
# Install python dependencies
$ pip install -r requirements.txt

# Start the server
$ python app.py
```

## Contributing

- Please use the [issue tracker](https://github.com/karan/slack-overflow/issues) to report any bugs or file feature requests.

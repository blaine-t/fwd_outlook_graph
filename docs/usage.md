# Usage

Here I have compiled a different example configs for different common use cases I see FOG being used in. These will only show the variations from the example config and not the whole config

**ALWAYS REMEMBER TO CHANGE SETTINGS LIKE CLIENT_STATE, CLIENT_ID, AND SUBSCRIPTION_URL NO MATTER WHAT CONFIG YOU USE**

## Traditional Forwarding

```python
TRANSPARENT_FORWARD = False
TO_RECIPIENTS = ["email@example.com"]
CATCH_ALL = ""
```

## Transparent Forwarding to one account without catch-all

```python
TO_RECIPIENTS = ["email@example.com"]
CATCH_ALL = ""
```

## Forwarding emails to multiple accounts (E.G. School and Work email)

```python
CATCH_ALL = ""
```

## Transparent Forwarding with catch-all

You don't have to deviate from the default config for transparent forwarding with catch-all!

## Behind just Cloudflare (NOT RECOMMENDED AS DEFAULT SOLUTIONS DONT HAVE SSL)

```python
PROXY = {
'FOR': 1,
'PROTO': 1,
'HOST': 0,
'PREFIX': 0
}
```

Not fully tested. Please report any bugs if you have this configuration to [issues](https://github.com/blaine-t/fwd_outlook_graph/issues)

## Behind just an NGINX proxy

```python
PROXY = {
'FOR': 1,
'PROTO': 1,
'HOST': 1,
'PREFIX': 1
}
```

Not fully tested. Please report any bugs if you have this configuration to [issues](https://github.com/blaine-t/fwd_outlook_graph/issues)

## Behind NGINX proxy and Cloudflare

```python
PROXY = {
    'FOR': 2,
    'PROTO': 2,
    'HOST': 1,
    'PREFIX': 1
}
```

Fully tested and what I used for development and production.

If you have any other configurations you want to recommend please refer to [Contributing](../README.md#contributing)
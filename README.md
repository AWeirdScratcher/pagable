<div align="center">

# pagable (WIP)

A Python web framework for direct client-side interactions without having to learn Javascript.

**[We're looking for contributors](https://discord.gg/pRWgjYJa3v)**

<div>

![Get Started](https://img.shields.io/badge/▲%20Get%20Started%20→-20B2AA?style=for-the-badge)
![GitHub issues](https://img.shields.io/badge/⬤%20Contribute%20→-2f768e?style=for-the-badge)

</div>

</div>

<div>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AWeirdScratcher/pagable/assets/90096971/8cc29a0e-5e3c-4104-89b5-86a13e53c73d" width="450" align="right">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/AWeirdScratcher/pagable/assets/90096971/b49503a1-3d93-43f1-9196-44a82bca9c65" width="450" align="right">
    <img alt="Simple Pagable app in Python" src="https://github.com/AWeirdScratcher/pagable/assets/90096971/0445707b-d122-4142-9e64-3676199bcb70" width="450" align="right">
  </picture>
</div>

## ◆ Python x Frontend

Pagable is designed for developers who love Python, but aren't a fan of Javascript. Pagable solved it all.

Want to show a message box to the user on the client-side from Python? Just use the `alert()` API out of the box. No extra configeration needed. It just works.

![Try Pagable](https://img.shields.io/badge/◆%20Try%20Pagable%20→-20B2AA?style=for-the-badge)

***

<div>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AWeirdScratcher/pagable/assets/90096971/0445707b-d122-4142-9e64-3676199bcb70" width="450" align="left">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/AWeirdScratcher/pagable/assets/90096971/3a4079b0-1209-4d1b-bee7-acac16337110" width="450" align="left">
    <img alt="Simple Pagable page but in Markdown" src="https://github.com/AWeirdScratcher/pagable/assets/90096971/0445707b-d122-4142-9e64-3676199bcb70" width="450" align="left">
  </picture>
</div>

## ◆ Markdown Pages

Want to host static pages instead? We've got your back. Just write some Markdown, and you've got yourself a page with CSS styling!

Additionally, Pagable also supports frontmatters, so you can add extra configerations such as `title`, `theme`, and more with ease!

We're planning to add "scripts" so that say, a button is being triggered, you can handle it using Python.

![Try Pagable for MD](https://img.shields.io/badge/◆%20Try%20Pagable%20For%20MD%20→-2f768e?style=for-the-badge)

<br />

***

## ▲ Getting Started

Enough of the features! I want the CONTENT!

To install and run:

```shell
$ git clone https://github.com/AWeirdScratcher/pagable
$ cd pagable
$ python -m pagable create .
created app ('.')
$ python3 main.py
```

Simple Python page example:

```python
from pagable import html


async def handle():
    return [
        html.h1("Welcome!"),
        html.p([
            "This page is amazing, isn't it? ",
            html.a("Click me!", href="https://google.com")
        ]),
    ]
```

> Note: This project is still a WIP. If you wish to contribute and help me build this project, please [Contact Me](https://discord.gg/pRWgjYJa3v)

***

This project was made for fun, so it might not be the best idea to put this in production.

Additional security reviews are pending (and welcomed).

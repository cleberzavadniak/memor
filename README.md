# memor-client

**Memor** is an application that allows you to easily
store and retrieve small portions of data, like
URLs, names or document numbers, while allowing you
to share your collection with others or sync between
computers.


## How it works

Memor works with **collections**, that is, collections
of **items**. Each item being composed of an *ID*,
a *term* and its *tags*. Like these:

    1 | http://example.com | web example tests
    2 | memor | applications notes open-source python

You can create a **private or public** collection
(but there's nothing on the server preventing you from
sharing your private collection ID (a *slug*) with
someone you **trust**).

The only real difference between a public and a private
collection is that usually public ones receive
**pretty names**, something human-readable, easy to
remember, while private ones will focus on security
and try to be a long string of really random characters.


### Memor server security model

The security model of Memor server is
**100% transparent**: it's up to the client to come up
with a safe ID for its collection.

This `memor-client` generates 64-long random strings as
IDs for "private" collections. If you think about it,
it's harder to guess than most passwords used out there
(the chance of guessing right is one in a number with
91 digits).


## Requirements

* A POSIX-compliant operating system
* Python >= 3.8
* pip (Python's package manager)


## Installation

    pip install git+https://github.com/cleberzavadniak/memor


## Setup

Before using the program, you must set it up in your machine:

    memor setup


## Usage

Add an item:

    memor + "some thing you want to save" tag1 tag2 tag3 [...]

List all items:

    memor /

Search by tags (AND):

    memor / tag-1 tag-2 tag-3

Search by tags (OR):

    memor / tag-1 / tag-2 / tag-3

Search by tags (AND + OR):

    memor / tag-1 tag-2 / tag-alfa tag-beta

Search by tags, only in your collection:

    memor ./ tag-1 tag-2

Search by tags with JSON output:

    memor // tag-1

Search by tags, only in your collection, with JSON output:

    memor .// tag-1


## Sharing your collection with other people

Simply send them your collection ID and they can
**subscribe** to it using the `memor sub` command
(and `memor sync` afterwards).


## Keeping more than one collection

Set a `MEMOR_DATA_DIR` environment variable pointing
to a new directory where memor should save its data.

You could use an alias in your shell, for instance,
like this:

    alias memor-public='MEMOR_DATA_DIR=$HOME/.config/memor/public memor'

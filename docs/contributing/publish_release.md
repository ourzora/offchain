# Publishing a Release

This guide is specific to contributors and serves to document how we publish releases of the offchain library.
It might be an interesting read, but you'll likely never use anything out of it on a day-to-day basis.

---

## Prerequisites

There is a bit of polish that needs to be done before pushing your code.

### Knowing your Version

Before merging your pull request, you'll want to make sure that the application version defined in `pyproject.toml`
has been incremented, following semantic versioning. This will be used later when tagging the release and in the changelog.

If we're currently on version `0.0.1`, and this pull request is a patch release, we'll update our version
to `0.0.2`.

???+ example
    ```toml
    [tool.poetry]
    name = "offchain"
    version = "0.0.2"
    ```

### Create a Changelog Entry

You'll want to ensure you've written a version entry to the [changelog](https://github.com/ourzora/offchain/blob/main/docs/changelog.md).
This will not only be published in the docs, but it will be extracted and written as the description for the release.

Entries are formatted like:

```md
# Changelog

## v0.0.2

- element
- another element
- the best element

## v0.0.1

- worst element
- another solid element
- the sad element
```

!!! tip
    Make sure the changelog file has a new line at the end.

You can add as many elements as you'd like, but make sure the versions are separated by new lines in descending order and are appended with a `v` like shown in the above example.

### Update the Index Version
You'll also want to update the version that's notated on the [index](https://ourzora.github.io/offchain/) page.
Similarly to how the changelog version is formatted, make sure the version is appended with a `v`.

???+ example
    ```md
    Documentation for version: **v0.0.2**
    ```

---

Once you've confirmed the version is correct, your changelog entry has been committed, and you have approval on
your pull request, merge it into `main` to begin the next steps.

## Tag a Release

Now that your changes are merged into `main`, we can now tag this release and configure it on GitHub.
When running the command below, this will create a tag for `v0.0.2` and sign it using your GPG key.
Make sure your versions are appended with `v`. This will be the version published to PyPi later.

!!! warning Sign Your Releases
    All releases must be made with a GPG signed tag. Don't create a tag without signing it.

```bash
git tag -a v0.0.2 -sm "v0.0.2"
git push origin v0.0.2
```

When pushing the tag, the CI pipeline will validate that your tag matches the version defined in `pyproject.toml`.
If it doesn't, the version will automatically update to match the tag version. This is only for safety and should never happen.

If the versions match and are good to go, a release branch will be created, including the commits from the tag.

## Publish the Release on GitHub

Once you've created and pushed the tag, you should notice a draft release on GitHub. The title should be `v0.0.2`,
and the content should be from the changelog for that release.

!!! success
    Validate that everything is correct and publish the release! This will automatically publish the release to PyPi.

And you're done, congratulations! You've successfully published a new version of the offchain library!

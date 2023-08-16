=====
Usage
=====

To use Django test queries in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'test_queries.apps.TestQueriesConfig',
        ...
    )

Add Django test queries's URL patterns:

.. code-block:: python

    from test_queries import urls as test_queries_urls


    urlpatterns = [
        ...
        url(r'^', include(test_queries_urls)),
        ...
    ]

from factory import DjangoModelFactory, fuzzy, SubFactory

from test_app.models import A, B


class AFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText()

    class Meta:
        model = A


class BFactory(DjangoModelFactory):
    a = SubFactory(AFactory)
    name = fuzzy.FuzzyText()
    limit = fuzzy.FuzzyText()

    class Meta:
        model = B

import markdown
import pytest

from neoteroi.mkdocs.spantable import SpanTableExtension, make_extension


@pytest.mark.parametrize(
    "example,expected_result",
    [
        [
            """
            ::spantable:: caption="Offices by country" class="offices-by-country"

            | Country      | Address                                                  |
            | ------------ | -------------------------------------------------------- |
            | France @span | 8 Rue St Ferréol - 92190 City: Meudon (Île-de-France)    |
            |              | 50 boulevard Amiral Courbet - 94310 Orly (Île-de-France) |
            |              | ...                                                      |
            | Italy @span  | Str. S. Maurizio, 12, 10072 Caselle torinese TO          |
            |              | S.S. Torino-Asti - 10026 Santena (TO)                    |
            |              | ...                                                      |
            | Poland @span | al. Jana Pawła II 22, 00-133 Warszawa                    |
            |              | plac Trzech Krzyży 4/6, 00-535 Warszawa                  |
            |              | ...                                                      |
            |              | ...                                                      |

            ::end-spantable::
            """,
            """
<div class="span-table-wrapper">
<table class="span-table offices-by-country"><caption>Offices by country</caption><tr>
<td>Country</td>
<td>Address</td>
</tr>
<tr>
<td rowspan="3">France</td>
<td>8 Rue St Ferréol - 92190 City: Meudon (Île-de-France)</td>
</tr>
<tr>
<td>50 boulevard Amiral Courbet - 94310 Orly (Île-de-France)</td>
</tr>
<tr>
<td>...</td>
</tr>
<tr>
<td rowspan="3">Italy</td>
<td>Str. S. Maurizio, 12, 10072 Caselle torinese TO</td>
</tr>
<tr>
<td>S.S. Torino-Asti - 10026 Santena (TO)</td>
</tr>
<tr>
<td>...</td>
</tr>
<tr>
<td rowspan="4">Poland</td>
<td>al. Jana Pawła II 22, 00-133 Warszawa</td>
</tr>
<tr>
<td>plac Trzech Krzyży 4/6, 00-535 Warszawa</td>
</tr>
<tr>
<td>...</td>
</tr>
<tr>
<td>...</td>
</tr>
</table>
</div>
    """,
        ],
        [
            """
::spantable:: caption="Offices by country" class="offices-by-country"

| Country      | Address                                                  |
| ------------ | -------------------------------------------------------- |
| France @span | 8 Rue St Ferréol - 92190 City: Meudon (Île-de-France)    |
|              | 50 boulevard Amiral Courbet - 94310 Orly (Île-de-France) |
|              | ...                                                      |
| Italy @span  | Str. S. Maurizio, 12, 10072 Caselle torinese TO          |
|              | S.S. Torino-Asti - 10026 Santena (TO)                    |
|              | ...                                                      |
| Poland @span | al. Jana Pawła II 22, 00-133 Warszawa                    |
|              | plac Trzech Krzyży 4/6, 00-535 Warszawa                  |
|              | ...                                                      |
|              | ...                                                      |

            ::end-spantable::
            """,
            """
<div class="span-table-wrapper">
<table class="span-table offices-by-country"><caption>Offices by country</caption><tr>
<td>Country</td>
<td>Address</td>
</tr>
<tr>
<td rowspan="3">France</td>
<td>8 Rue St Ferréol - 92190 City: Meudon (Île-de-France)</td>
</tr>
<tr>
<td>50 boulevard Amiral Courbet - 94310 Orly (Île-de-France)</td>
</tr>
<tr>
<td>...</td>
</tr>
<tr>
<td rowspan="3">Italy</td>
<td>Str. S. Maurizio, 12, 10072 Caselle torinese TO</td>
</tr>
<tr>
<td>S.S. Torino-Asti - 10026 Santena (TO)</td>
</tr>
<tr>
<td>...</td>
</tr>
<tr>
<td rowspan="4">Poland</td>
<td>al. Jana Pawła II 22, 00-133 Warszawa</td>
</tr>
<tr>
<td>plac Trzech Krzyży 4/6, 00-535 Warszawa</td>
</tr>
<tr>
<td>...</td>
</tr>
<tr>
<td>...</td>
</tr>
</table>
</div>
    """,
        ],
        [
            """
            ::spantable:: caption="Life Expectancy By Current Age" class="foo"

            | Italy @span   |       | 40 @span      |       | 20 @span      |       |
            | ------------- | ----- | ------------- | ----- | ------------- | ----- |
            |               |       | Men           | Women | Men           | Women |
            |               |       | 78            | 82    | 77            | 81    |
            | Poland @span  |       | 40 @span      |       | 20 @span      |       |
            | ------------- | ----- | ------------- | ----- | ------------- | ----- |
            |               |       | Men           | Women | Men           | Women |
            |               |       | 78            | 82    | 77            | 81    |

            ::end-spantable::
            """,
            """
<div class="span-table-wrapper">
<table class="span-table foo"><caption>Life Expectancy By Current Age</caption><tr>
<td colspan="2" rowspan="3">Italy</td>
<td colspan="2">40</td>
<td colspan="2">20</td>
</tr>
<tr>
<td>Men</td>
<td>Women</td>
<td>Men</td>
<td>Women</td>
</tr>
<tr>
<td>78</td>
<td>82</td>
<td>77</td>
<td>81</td>
</tr>
<tr>
<td colspan="2" rowspan="3">Poland</td>
<td colspan="2">40</td>
<td colspan="2">20</td>
</tr>
<tr>
<td>Men</td>
<td>Women</td>
<td>Men</td>
<td>Women</td>
</tr>
<tr>
<td>78</td>
<td>82</td>
<td>77</td>
<td>81</td>
</tr>
</table>
</div>
            """,
        ],
        [
            """
            ::spantable::

            | Format| Source                         | Example                                                     |
            | :--| :----------------------------- | :---------------------------------------------------------- |
            | YAML @span | File                      | `[OAD(./docs/swagger.yaml)]`                                |
            | | URL                      | `[OAD(https://example-domain.net/swagger/v1/swagger.yaml)]`                                |
            | JSON @span | File | `[OAD(./docs/swagger.json)]` |
            | | URL | `[OAD(https://example-domain.net/swagger/v1/swagger.json)]` |

            ::end-spantable::
            """,
            """
<div class="span-table-wrapper">
<table class="span-table">
<tr>
<td>Format</td>
<td>Source</td>
<td>Example</td>
</tr>
<tr>
<td rowspan="2">YAML</td>
<td>File</td>
<td><code>[OAD(./docs/swagger.yaml)]</code></td>
</tr>
<tr>
<td>URL</td>
<td><code>[OAD(https://example-domain.net/swagger/v1/swagger.yaml)]</code></td>
</tr>
<tr>
<td rowspan="2">JSON</td>
<td>File</td>
<td><code>[OAD(./docs/swagger.json)]</code></td>
</tr>
<tr>
<td>URL</td>
<td><code>[OAD(https://example-domain.net/swagger/v1/swagger.json)]</code></td>
</tr>
</table>
</div>
            """,
        ],
        [
            """
            ::spantable:: caption="Dungeons & Dragons 4th edition"

            | Class   | Power Source      |
            | ------- | ----------------- |
            | Cleric  | Divine @span=0:2  |
            | Paladin |                   |
            | Fighter | Martial @span=0:5 |
            | Ranger  |                   |
            | Rogue   |                   |
            | Warlord | Arcane  @span=0:2 |
            | Warlock |                   |

            ::end-spantable::
            """,
            """
<div class="span-table-wrapper">
<table class="span-table"><caption>Dungeons &amp; Dragons 4th edition</caption><tr>
<td>Class</td>
<td>Power Source</td>
</tr>
<tr>
<td>Cleric</td>
<td rowspan="2">Divine</td>
</tr>
<tr>
<td>Paladin</td>
</tr>
<tr>
<td>Fighter</td>
<td rowspan="5">Martial</td>
</tr>
<tr>
<td>Ranger</td>
</tr>
<tr>
<td>Rogue</td>
</tr>
<tr>
<td>Warlord</td>
</tr>
<tr>
<td>Warlock</td>
</tr>
</table>
</div>
            """,
        ],
        [
            """
            ::spantable:: caption="Dungeons & Dragons 4th edition"

            | Class   | Power Source      |
            | ------- | ----------------- |
            | Cleric @class="divine" | Divine @span=0:2 @class="divine"  |
            | Paladin @class="divine" |                   |
            | Fighter | Martial @span=0:5 |
            | Ranger  |                   |
            | Rogue   |                   |
            | Warlord | Arcane  @span=0:2 |
            | Warlock |                   |

            ::end-spantable::
            """,
            """
<div class="span-table-wrapper">
<table class="span-table"><caption>Dungeons &amp; Dragons 4th edition</caption><tr>
<td>Class</td>
<td>Power Source</td>
</tr>
<tr>
<td class="divine">Cleric</td>
<td class="divine" rowspan="2">Divine</td>
</tr>
<tr>
<td class="divine">Paladin</td>
</tr>
<tr>
<td>Fighter</td>
<td rowspan="5">Martial</td>
</tr>
<tr>
<td>Ranger</td>
</tr>
<tr>
<td>Rogue</td>
</tr>
<tr>
<td>Warlord</td>
</tr>
<tr>
<td>Warlock</td>
</tr>
</table>
</div>
            """,
        ],
    ],
)
def test_spantable_extension(example, expected_result):
    html = markdown.markdown(example, extensions=[SpanTableExtension()])
    assert html == expected_result.strip()


def test_spantable_extension_handles_unclosed_tag():
    example = """
::spantable:: caption="Offices by country" class="offices-by-country"

| Country      | Address                                                  |
| ------------ | -------------------------------------------------------- |
| Italy @span  | Str. S. Maurizio, 12, 10072 Caselle torinese TO          |
|              | S.S. Torino-Asti - 10026 Santena (TO)                    |
|              | ...                                                      |
    """
    html = markdown.markdown(example, extensions=[SpanTableExtension()])
    assert (
        '::spantable:: caption="Offices by country" class="offices-by-country"' in html
    )


def test_make_extension():
    assert isinstance(make_extension(), SpanTableExtension)

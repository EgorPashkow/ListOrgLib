# ListOrgLib
Library for convenient parsing of data from the site list-org.com

## Requirements
- lxml

## Examples
Get organization by link
```python
ListOrgParser = Parser()
org = ListOrgParser.parse("https://www.list-org.com/company/1")
res = vars(org)
for i in res:
    print(i, " : ", res[i])
```

Get the organization's reporting
```python
ListOrgParser = Parser()
org = ListOrgParser.parse_report("https://www.list-org.com/company/1")
print(org.years)
print(org.get_by_key_and_year("Итого по разделу I - Внеоборотные активы","2018"))
```

Find an organization by INN
```python
ListOrgParser = Parser()
orgs = ListOrgParser.search("4631002737", search_type="inn", limit=10)
print(orgs[0].organization_name)
```

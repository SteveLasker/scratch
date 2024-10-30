# CDDL and EDN examples

The goal:
```json
{
  "meta-map": [
    { "key": "42" },
    { "key1": "42" },
    { "key2": "42" }
  ]
}
```

Examples:
```cddl
meta-map = { key => value}

key = tstr
value = tstr
```

```cddl
people = [* person ]
person = {
 first: tstr
 last: tstr
 age: int
}
```

```json
{
  "people": [
    {
      "first": "steve",
      "last": "lasker",
      "age": 42
    }
  ]
}

```

## Meta-Map

Works With https://atacama.informatik.uni-bremen.de/

**CDDL**

```cddl
my-object = {
    "metamap": meta-map
}

meta-map = {
    * key => value
}

key = tstr
value = tstr
```

**JSON**

```json
{    
    "metamap": {
          "key": "exampleKey",
          "value": "exampleValue"
      }
}
```


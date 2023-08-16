<h1 align="center"><code>rpsl-parser</code></h1>

<div align="center">
  <a href="https://github.com/srv6d/rpsl-parser/actions">
    <img src="https://github.com/srv6d/rpsl-parser/workflows/CI/badge.svg" alt="CI status">
  </a>
</div>
<br>

An [RFC 2622] conformant Routing Policy Specification Language (RPSL) parser with a focus on speed and correctness. It is written in Rust and extensively leverages zero-copy, [outperforming other parsers](doc/benchmark) by a factor of 33-60x. To ensure robust parsing of any valid RPSL input, an exhaustive suite of [property based tests](tests/property_based/) is used.

> [!WARNING]
> This project is still in early stages of development and its API is not yet stable.

## Examples

```rust
let role_acme = "
role:        ACME Company
address:     Packet Street 6
address:     128 Series of Tubes
address:     Internet
email:       rpsl-parser@github.com
nic-hdl:     RPSL1-RIPE
source:      RIPE
";
let parsed = rpsl_parser::parse_rpsl_object(role_acme).unwrap();
println!("{:#?}", parsed);
```

Outputs the following object:

```sh
Object(
  [
    Attribute {
      name: "role",
      values: [Some("ACME Company",),],
    },
    Attribute {
      name: "address",
      values: [Some("Packet Street 6",),],
    },
    Attribute {
      name: "address",
      values: [Some("128 Series of Tubes",),],
    },
    Attribute {
      name: "address",
      values: [Some("Internet",),],
    },
    Attribute {
      name: "email",
      values: [Some("irrdb@github.com",),],
    },
    Attribute {
      name: "nic-hdl",
      values: [Some("IRRD2-RIPE",),],
    },
    Attribute {
      name: "source",
      values: [Some("RIPE",),],
    },
  ],
)
```

[RFC 2622]: https://datatracker.ietf.org/doc/html/rfc2622

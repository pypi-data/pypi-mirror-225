use qdx_common::*;

#[derive(Typedef)]
struct Foo {
    _x: bool,
    _y: Vec<f64>,
    _z: ((f64, f64, f64), Vec<Conformer>),
}

#[derive(Typedef)]
struct Bar(bool, Vec<f64>, Foo);

#[derive(Typedef)]
struct Baz(String, Vec<Conformer>);

#[test]
fn test_named_struct() {
    init_built_in_types();

    let t = <Foo as Typedef>::describe();
    assert_eq!(
        r#"{"k":"record","t":{"_x":"bool","_y":{"k":"array","t":"f64"},"_z":{"k":"tuple","t":[{"k":"tuple","t":["f64","f64","f64"]},{"k":"array","t":"Conformer"}]}}}"#,
        serde_json::to_string(&t).unwrap()
    );
}

#[test]
fn test_unnamed_struct() {
    init_built_in_types();

    let t = <Baz as Typedef>::describe();
    assert_eq!(
        r#"{"k":"tuple","t":["string",{"k":"array","t":"Conformer"}]}"#,
        serde_json::to_string(&t).unwrap()
    );
}
